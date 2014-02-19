import codecs
import re,string
import random
import sys
import time
import nltk
from nltk.stem.snowball import GermanStemmer, EnglishStemmer
#es = nltk.corpus.wordnet.morphy
en = EnglishStemmer()
de = GermanStemmer()

class Preprocessing():
    def split_sentences(self,x):
        return x.split('|||')
    def eng_tokenize(self,y):
        z=y.strip()
        newstring = z.lower()
        newstring = z
        p=newstring.split(' ')
        for i in range(len(p)):
            alpha=p[i]
            if alpha.isdigit():
                p[i]='NUM'
            else:
                p[i]=en.stem(alpha)
        return p
    def ger_tokenize(self,y):
        z=y.strip()
        newstring = z.lower()
        newstring = z
        p=newstring.split(' ')
        for i in range(len(p)):
            alpha=p[i]
            if alpha.isdigit():
                p[i]='NUM'
            else:
                p[i]=de.stem(alpha)
        return p
            



def initialize_translation11(source,target):
    translation={}
    for k in range(len(source)):
        source_sentence = source[k]
        target_sentence= target[k]
        for sword in source_sentence:
            if sword not in translation:
                translation[sword]={}
            for tword in target_sentence:
                if tword not in translation[sword]:
                    translation[sword][tword]=0.0
                translation[sword][tword]+=1.0
    for sword in translation:
        denom=sum([float(translation[sword][tword]) for tword in translation[sword]])
        for tword in translation[sword]:
            translation[sword][tword]=translation[sword][tword]/float(denom)
    return translation

def model1(source, target ,translation ):
	count = {}
	total =  {}
	for i in range(len(source)):
		source_sentence = source[i]
		target_sentence = target[i]
		for sword in source_sentence:
			denom = float ( sum ( [float ( translation[sword][tword] ) for tword in target_sentence ] ) ) 
			for tword in target_sentence:
				delta = float ( translation[sword][tword] ) / float ( denom ) 
				count[(sword,tword)] = count.get((sword,tword) , 0.0) + delta
				#total[sword] = total.get(sword , 0.0) + delta 
				#total[tword] = total.get(sword , 0.0) + delta 
				total[tword] = total.get(tword , 0.0) + delta 

		if i % 1000 == 0:
			print str(i/1000) + "% complete"
	for (sword, tword) in  count:
		#translation[sword][tword] = float(count[(sword, tword)]) / total[sword]
		translation[sword][tword] = float(count[(sword, tword)]) / total[tword]

	return translation


def alignment_model12(source, target, translation):
	l=len(source)
	f=open('new3.a2i11iter5.stem.all.lower.output.txt','w')
	for k in range(l):
		source_sentence = source[k]
		target_sentence = target[k]
		print_string=''
		for i in range(1,len(source_sentence)):
			sword=source_sentence[i]
			(prob,tword,ind)=max( [ ( translation [ sword][target_sentence[j]],target_sentence[j],j) for j in range(len(target_sentence)) ]) 
			if i > 0:
				#print tword,sword,prob
				print_string+=str(i-1)+"-"+str(ind)+' '
		f.write(print_string+'\n')
	f.close()



if __name__ == "__main__":
    source=[]
    target=[]
    p=Preprocessing()
    with codecs.open('data/dev-test-train.de-en','r','utf-8') as g:
    	i = 0
        for myline in g.readlines():
            source_sent=p.split_sentences(myline.strip())[0]
            target_sent=p.split_sentences(myline.strip())[1]
            es=p.ger_tokenize(source_sent)
            es.insert(0,'NULL')
            source.append(es)
            target.append(p.eng_tokenize(target_sent))
    g.close()
    it=1
    t = initialize_translation11(source,target)
    while it < 5:
        print 'iteration num',it
        t=model1(source,target,t)
        it+=1
        sys.stdout.flush()
    alignment_model12(source,target,t)
    
