import sys, os, nltk

models_dir = 'models'
def openlines(filename):
    filename = os.path.join(models_dir, filename)
    with open(filename, 'r') as f:
        return [line for line in f.read().splitlines() if line.strip()]

def openwords(filename):
    words = []
    for line in openlines(filename):
        words += [word for word in line.split(' ') if word]
    return words

unimodel = {}
for tag in ('NN', 'CD', 'DT', 'IN', 'RP'):
    for word in openwords(tag):
        unimodel[word] = tag
        
class NamaKomoditiTagger:
    @staticmethod
    def choose_tag(tokens, index, history):
        print tokens, index, history
NamaKomoditiTagger._taggers = [NamaKomoditiTagger]
    
tagger = nltk.RegexpTagger([(r'^[0-9.]+$', 'CD')],
backoff = nltk.tag.UnigramTagger(model=unimodel))

if __name__ == "__main__":
    print tagger.tag(sys.argv[1:])
