import codecs
import pickle
import heapq
def read_alignment_file(align_file):
    f=codecs.open(align_file,'r','utf-8')
    tt={}
    tt2={}
    for myline in f:
        mylist=myline.strip().split('|||')
        src_sent=mylist[0]
        tgt_sent=mylist[1]
        alignments=mylist[2]
        src_list=src_sent.split(' ')
        tgt_list=tgt_sent.split(' ')
        alignment_list=alignments.split(' ')
        alignment={}
        for align in alignment_list:
            if align=='':
               continue
            myl=align.strip().split('-')
            fword=src_list[int(myl[0])]
            eword=tgt_list[int(myl[1])]
            '''
            if fword not in tt:
               tt[fword]={}
            if eword not in tt[fword]:
               tt[fword][eword]=0.0
            tt[fword][eword]+=1.0
            '''
            if eword not in tt2:
               tt2[eword]={}
            if fword not in tt2[eword]:
               tt2[eword][fword]=0.0
            tt2[eword][fword]+=1.0
    f.close()
    #return tt,tt2
    return tt2

def normalize_tt(tt):
    lew_tt={}
    for fword in tt:
        ftotal=0.0
        lew_tt[fword]={}
        for eword,ewtotal in tt[fword].iteritems():
            ftotal+=ewtotal
            lew_tt[fword][eword]=ewtotal
        for eword,ewtotal in tt[fword].iteritems():
            lew_tt[fword][eword]=lew_tt[fword][eword]/ftotal
    return lew_tt

def shorten_tt(tt):
    short_tt={}
    for fword in tt:
        word_list=tt[fword].iteritems()
        short_tt[fword]=[]
        short_tt[fword]=[ words[0] for words in heapq.nlargest(20,word_list,key=lambda t:t[1])]
    return short_tt
            
            
if __name__ == "__main__":
    tt2=read_alignment_file("train.ru-en.align")
    #new_tt=normalize_tt(tt)
    new_tt2=normalize_tt(tt2)
    short=shorten_tt(new_tt2)
    '''
    output = open('lextm1.pkl', 'wb')
    pickle.dump(new_tt, output)
    output.close()
    output = open('lextm2.pkl', 'wb')
    pickle.dump(new_tt2, output)
    output.close()
    '''
    output = open('lextm2_short.pkl', 'wb')
    pickle.dump(short, output)
    output.close()


            
               
            
            

