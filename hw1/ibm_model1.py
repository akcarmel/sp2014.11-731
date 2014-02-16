import random
class Preprocessing():
    def split_sentences(self,x):
        y=x.split('|||')
        return y
    def eng_tokenize(self,x):
        return x.split(' ')
    def fren_tokenize(self,x):
        return x.split(' ')

    
def initialize(source,target):
    corpus_length=len(source)
    source_words=set()
    target_words=set()
    t={}
    count={}
    total={}
    for k in range(corpus_length):
        for i in range(len(source[k])):
            source_words.add(source[k][i])
        for j in range(len(target[k])):
            target_words.add(target[k][j])
    length=len(target_words)
    for sword in source_words:
        t[sword]={}
        count[sword]={}
        total[sword]=0.0
        for tword in target_words:
            t[sword][tword]=float(1.0/length)
            count[sword][tword]=0.0
    return t,source_words,target_words,count,total
            
def model1(source,target):
    t,source_words,target_words,count,total=initialize(source,target)
    sent_total={}
    corpus_length=len(source)
    for k in range(corpus_length):
        sent_total={}
        for tword in target[k]:
            sent_total[tword]=0.0
            for sword in source[k]:
                sent_total[tword]+=t[sword][tword]
        for tword in target[k]:
            for sword in source[k]:
                count[sword][tword]+=float(t[sword][tword]/sent_total[tword])
                total[sword]+=float(t[sword][tword]/sent_total[tword])
    for sword in source_words:
        for tword in target_words:
            t[sword][tword]=float(count[sword][tword]/total[sword])
    return t  
         
def alignment_model1(source,target,t):
    corpus_length=len(source)
    for k in range(corpus_length):
        for sword in source[k]:
            (prob,tword)=max((t[sword][tword],tword) for tword in target[k])
            print tword,sword

                    


        
        
if __name__=="__main__":
    source={}
    target={}
    p=Preprocessing()
    with open('test.data','r+') as g:
         for myline in g.readlines():
             source_sent=p.split_sentences(myline.strip())[0]
             target_sent=p.split_sentences(myline.strip())[1]
             es=p.eng_tokenize(source_sent)
             es.insert(0,'NULL')
             source.append(es)
             target.append(p.fren_tokenize(fren_sent))
    g.close()
    it=1
    while it < 5:
        print 'iteration num',it
        t=model1(source,target)
        it+=1
    alignment_model1(source,target,t)

