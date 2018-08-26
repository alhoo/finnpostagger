import subprocess
from . import finnpos_ratna_feats
from nltk import word_tokenize

from threading import Thread
from queue import Queue, Empty

import logging

logger = logging.getLogger(__name__)

class UnexpectedEndOfStream(Exception): pass

class NonBlockingStreamReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

class FinnPosTagger:
    def __init__(self, bin="finnpos-label", model="/home/lasse/data/ftb/model.bin"):
        self.bin = bin
        self.model = model
        self.proc = subprocess.Popen("finnpos-label /home/lasse/data/ftb/model.bin".split(),
           stdin=subprocess.PIPE, universal_newlines=True, bufsize=1,
           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.nbsr = NonBlockingStreamReader(self.proc.stdout)
        self.proc.stdin.write("\n\n")
        
    def __del__(self):
        try:
            self.end()
        except Exception as ex:
            if logger:
                logger.warning("Exception while destroying tagger: %s", ex)
        
    def end(self):
        self.proc.stdin.close()
        self.proc.kill()
    
    def tag(self, text):
        finnpos_input = self.format_input(text)
        finnpos_input_text = ("".join(finnpos_input[0]))+"\n"
        #print(finnpos_input_text)
        self.proc.stdin.write(finnpos_input_text)
        self.proc.stdin.flush()
        response = []
        #time.sleep(1)
        output = ''
        while output != "\n":
            output = self.nbsr.readline(10)
            # 0.1 secs to let the shell output the result
            #print("Got '%s'" % output)
            #if not output:
            #    print('[No more data]')
            #    break
            response.append(output)
        return self.format_result_lines(response)
        
    def format_input(self, text):
        return list(finnpos_ratna_feats.convert(iter(word_tokenize(text)), "/home/lasse/data/ftb/freq_words"))
    
    def format_result_lines(self, lines):
        def format_finnpos_line(line):
            parts = line.split("\t")
            names = ['word', 'blank', 'lemma', 'tags']
            #print(parts[3])
            # TODO: FIXME: tagger.tag("Menikö se nyt rikki?")
            # Nyt should have two alternatives for POS
            parts[3] = dict(list(map(lambda x: x[1:-1].split("="), filter(len, parts[3].split("|")))))
            return dict(list(zip(names, parts)))
        return list(map(format_finnpos_line, filter(lambda x:x, [it.rstrip() for it in lines])))

if __name__ == '__main__':
    fpt = FinnPosTagger()
    print(json.dumps(fpt.tag("tämä on testi"), indent=2))
    fpt.end()
