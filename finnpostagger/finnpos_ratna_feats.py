#! /usr/bin/env python3

"""@package ratna_feats

 file    finnpos-ratna-feats.py                                                     
 Author  Miikka Silfverberg                                                 
 Modifications  Lasse Hyyrynen
 brief   Extract Ratnaparkhi 1996 features from an input-file.              

         (Adwait Ratnaparkhi: A Maximum Entropy Model for Part-of-Speech    
          Tagging, EMNLP 1996)                                              
          
         Additionally use word pairs as features (previous word and
         current word as well as current word and next word). Also use
         the lower-cased word form as feature.
"""

"""                                                                            
  (C) Copyright 2014, University of Helsinki                                 
  Licensed under the Apache License, Version 2.0 (the "License");            
  you may not use this file except in compliance with the License.           
  You may obtain a copy of the License at                                    
  http://www.apache.org/licenses/LICENSE-2.0                                 
  Unless required by applicable law or agreed to in writing, software        
  distributed under the License is distributed on an "AS IS" BASIS,          
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   
  See the License for the specific language governing permissions and        
  limitations under the License.
"""

from re  import match
from os  import linesep

EXIT_FAIL    = 1
EXIT_SUCCESS = 0

# Boundary word.
BOUNDARY = "_#_"

# Maximum length of extracted suffix and prefix features.
MAX_SUF_LEN = 10
MAX_PRE_LEN = 10

def convert(ingen, freq_words):
    """ Read input from ifile and write extracted features to ofile. 
        This function doesn't check its argument streams. """

    i = 0

    while True:
        sentence = []
#        while True:
#            word = ingen.__next__()
        for word in ingen:
            word = word.rstrip()
            if word == '':
                break
            sentence.append([word])

        if not sentence:
            break

        reti = []
        # Extract features for each sentence and write output to ofile.
        for i, line in enumerate(sentence):
            wf    = '_'
            feats = '_'
            lemma = '_'
            label = '_'
            ann   = '_'
            
            if len(line) == 1:
                wf = line[0]
                lemma, label, ann = '_', '_', '_'
            elif len(line) == 3:
                wf, lemma, label = line
                ann = "_"
            else:
                wf, feats, lemma, label, ann = line

            features = []                

            if feats != '_':
                features = feats.split(' ')
        
            if not ann in ['_', '']:
                lemma_list = ann
                if ' ' in ann:
                    lemma_list = ann[:ann.find(' ')]
                
                label_feats = [ "FEAT:" + label for label in 
                                map(lambda x: x[0], eval(lemma_list)) ]

                if len(label_feats) != 0:
                    features += label_feats
                else:
                    features.append("NO_LABELS")

            features.append('PPWORD=' + get_wf(i - 2, sentence))
            features.append('PWORD='  + get_wf(i - 1, sentence))
            features.append('WORD='   + wf)
            features.append('WORD_LEN='   + str(len(wf)))
            features.append('NWORD='  + get_wf(i + 1, sentence))
            features.append('NNWORD=' + get_wf(i + 2, sentence))
            
            features.append('PWORDPAIR='  + get_wf(i - 1, sentence) + "_" + wf)
            features.append('NWORDPAIR='  + wf + "_" + get_wf(i + 1, sentence))
            
            features.append("LC_WORD=" + wf.lower())
            
            if not wf in freq_words:
                features += get_suffixes(wf)
                features += get_prefixes(wf)
            
                features.append(has_uc(wf))
                features.append(has_digit(wf))
                features.append(has_dash(wf))
            
            feat_str = " ".join(filter(None, features))
        
        
            reti.append(("%s\t%s\t%s\t%s\t%s" + linesep) 
                        % 
                        (wf, feat_str, lemma, label, ann))
        yield reti
        
    return EXIT_SUCCESS

def get_wf(i, sentence):
    return BOUNDARY if i < 0 or i + 1 > len(sentence) else sentence[i][0]

def get_suffixes(wf):
    return [ "%u-SUFFIX=%s" % (i, wf[-i:]) 
             for i in range(1, min(MAX_SUF_LEN + 1, len(wf) + 1)) ]

def get_prefixes(wf):
    return [ "%u-PREFIX=%s" % (i, wf[:i]) 
             for i in range(1, min(MAX_PRE_LEN + 1, len(wf) + 1)) ]

def has_uc(wf):
    return "HAS_UC" if match(".*([A-Z]|Å|Ä|Ö).*", wf) else None

def has_digit(wf):
    return "HAS_DIGIT" if match(".*[0-9].*", wf) else None

def has_dash(wf):
    return "HAS_DASH" if match(".*-.*", wf) else None
