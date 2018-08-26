import yaml
from finnpostagger import FinnPosTagger

fpt = FinnPosTagger()
print(yaml.dump(fpt.tag("tämä on testi")))
#fpt.end()
