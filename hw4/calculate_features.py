# -*- coding: utf-8 -*-
import bleu
import codecs
import string
from nltk.tokenize import regexp_tokenize, wordpunct_tokenize
import subprocess
import argparse
russian_list=list(u"абвгдеёзийклмнопрстуфхъыьэАБВГДЕЁЗИЙКЛМНОПРСТУФХЪЫЬЭ")
import cPickle as pickle
parser = argparse.ArgumentParser(description='collecting all features')
parser.add_argument('-b100',dest='b100',help='file containing best 100 list')
parser.add_argument('-s',dest='srcf',help='source file') 
parser.add_argument('-o',dest='outf',help='output file') 
opts = parser.parse_args()
english_to_russian=pickle.load( open( "lextm2_short.pkl", "rb" ) )
#russian_to_english=pickle.load( open( "lextm.pkl", "rb" ) )



def get_bleu_score(tgt,src):
    stats=[ 0 for i in range(10)]
    stats = [sum(scores) for scores in zip(stats, bleu.bleu_stats(tgt,src))]
    return bleu.bleu(stats)

def calculate_sentence_length(sent):
    mylist=sent.strip().split(' ')
    return len(mylist),mylist

def get_given_features(myline):
    given_features=myline.split('|||')[2]
    features_list=given_features.strip().split(" ")
    all_features=[]
    for ind_feat in features_list:
        if ind_feat=='':
            continue
        feature_name=ind_feat.split("=")[0]
        feature_value=ind_feat.split("=")[1]
        feature_tuple=tuple([feature_name,float(feature_value)])
        all_features.append(feature_tuple)
    return all_features


def get_punctuation_counts(tokenized_list):
    countOf={}
    for punct in string.punctuation:
        key='punct'+str(punct)
        countOf[key]=tokenized_list.count(punct)
    return countOf

def write_features_to_file(features,feature_file_name):
    nonbare=feature_file_name+".nonbare"
    h=codecs.open(feature_file_name,'w','utf-8')
    f=codecs.open(nonbare,'w','utf-8')
    key_order=features[0].keys()
    for sent in features:
        sent_features=features[sent]
        feature_string=''
        feature_string2=''
        for feat in key_order:
            feature_string=feature_string+str(feat)+':'+str(sent_features[feat])+' '
            feature_string2+=str(sent_features[feat])+' '
        f.write(feature_string+'\n')
        h.write(feature_string2+'\n')
    f.close()
    h.close()
            
def length_and_punctuation_features(best100file,source_file,write_out_features_file):
    features={}
    src_num=0
    source_list=[]
    target_list=[]
    tgt_100=codecs.open(best100file,'r','utf-8')
    src=codecs.open(source_file,'r','utf-8')
    for src_line in src:
        sentence=src_line.split('|||')[1]
        source_list.append(sentence)
    features={}
    tgt_num=-1
    for myline in tgt_100:
        tgt_num+=1
        sentence=myline.split('|||')[1]
        target_list.append(myline)
        features[tgt_num]={}
        feature_list=get_given_features(myline)
        for tup in feature_list:
            features[tgt_num][tup[0]]=tup[1]
    tgt_100.close()
    src.close()
    num_sents=len(source_list)
    for i in xrange(0,num_sents):
        src_sentence=source_list[i]
        slength,slist=calculate_sentence_length(src_sentence)
        spunct_count=get_punctuation_counts(slist)
        for j in xrange(i*100,i*100+100):
            tgt_sentence=target_list[j]
            tlength,tlist=calculate_sentence_length(tgt_sentence)
            tpunct_count=get_punctuation_counts(tlist)
            russian_words=0.0
            for punct,value in tpunct_count.iteritems():
                key1=str(punct)+'diff'
                key2=str(punct)+'ratio'
                features[j][key1]=float(value)-float(spunct_count[punct])
                features[j][key2]=(float(value)+0.0)/(float(spunct_count[punct])+0.1)
            for word in tlist:
                for w in word:
                    if w in russian_list:
                       russian_words+=1.0
                       break
            oov=0.0
            top_lex_score=0.0
            '''
            for word in tlist:
                if not  word in english_to_russian:
                    oov+=1.0
                    continue
                for sword in slist:  
                    if sword in english_to_russian[word]:
                       top_lex_score+=1.0
                       break
            ''' 
            key3='lenratio'
            key4='lendiff'
            key5='russian words'
            key6='justlength'
            key7='num russian words'
            key8='top 20 lexical trans'
            key9='oov wrt aligned corpus'
            key10='bleu score'
            #features[j][key10]=get_bleu_score(tlist,slist)
            features[j][key3]=float(slength)-float(tlength)
            features[j][key4]=(float(slength)+0.0)/(float(tlength)+0.1)
            #features[j][key5]=(float(russian_words)+0.0)/(float(slength)+0.1)
            #features[j][key5]=(float(russian_words)+0.0)
            #features[j][key6]=float(tlength)
            #features[j][key7]=float(oov)/(float(slength)+0.1)
            #features[j][key8]=float(top_lex_score)/(float(tlength)+0.1)
    return features
if __name__ == "__main__":
    '''
    tgt_100=codecs.open("/home/alokkoth/11731/sp2014.11-731/hw4/experimental_data/dev.100best",'r','utf-8')
    src=codecs.open("/home/alokkoth/11731/sp2014.11-731/hw4/experimental_data/dev.src",'r','utf-8')
    '''
    best100file=opts.b100
    source_file=opts.srcf
    write_out_features_file=opts.outf
    features=length_and_punctuation_features(best100file,source_file,write_out_features_file)
    write_features_to_file(features,write_out_features_file)

