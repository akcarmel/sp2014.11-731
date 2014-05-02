import numpy
import random
import heapq
import argparse
import get_best_test_from_indice
from train_and_predict import predict_scores
from train_and_predict import predict_scores_log
from train_and_predict import clean_array
from train_and_predict import clean_and_normalize_array_train
from train_and_predict import clean_and_normalize_array_test
from get_best_test_from_indice import get_best_sent
parser = argparse.ArgumentParser(description='collecting all features')
parser.add_argument('-tra',dest='train',help='train file bare')
parser.add_argument('-tst',dest='test',help='test file bare')
parser.add_argument('-mf',dest='mf',help='meteor scores file')
parser.add_argument('-samples',dest='numsamples',type=int,default=1000,help='number of samples from n-best for each sentence that are sampled')
parser.add_argument('-tops',dest='topsamples',type=int,default=50,help='number of top scoring samples from n-best for each sentence to be put in training file')
parser.add_argument('-tstsrc',dest='testsrcf',default='experimental_data/test.100best',help='test 100 best souce file')
opts = parser.parse_args()

def collect_meteor_scores(meteor_final):
    f=open(meteor_final,"r")
    count=-1
    meteors={}
    for myline in f:
        count+=1
        s=myline.strip().split('\t')[1]
        meteors[count]=float(s)
    f.close()
    return meteors

def collect_all_features(features_bare):
    features={}
    f=open(features_bare,"r")
    count=-1
    for myline in f:
        count+=1
        mylist=myline.strip().split(" ")
        newlist=[float(feat) for feat in mylist]
        features[count]=newlist
    f.close()
    return features
    


def take_top_samplings(scores_samplings,num):
    print "Now taking the top samplings"
    training_set=[]
    train_labels=[]
    for i in range(len(scores_samplings)):
        for h in heapq.nlargest(num,scores_samplings[i],key=lambda t:t[0]):
            new_feature=h[3]
            new_feature1=[float(feat) for feat in new_feature]
            new_feature2=[float(-1.0*float(feat)) for feat in new_feature]
            training_set.append(new_feature1)
            training_set.append(new_feature2)
            train_labels.append(+1.0*h[0])
            train_labels.append(-1.0*h[0])

    return training_set,train_labels

def get_training_samplings(meteors,features):
    num_sentences=len(features)/100
    scores_samplings={}
    print "Now going through the sentences"
    for i in range(num_sentences):
        done_samplings=0
        scores_samplings[i]=[]
        while done_samplings < opts.numsamples:
            j1=random.randrange(0, 100)
            j2=random.randrange(0, 100)
            j1_ind=100*i+j1
            j2_ind=100*i+j2
            assert len(features[j1_ind])==len(features[j2_ind])
            invert=False
            if abs(float(meteors[j1_ind]) - float(meteors[j2_ind])) > 0.005:
                done_samplings+=1
                label=float(meteors[j1_ind]) - float(meteors[j2_ind])
                if label < 0:
                   invert=True
                   label=-1.0*label
            else:
                continue
            new_feature=[]
            for k in range(len(features[j1_ind])):
                if invert:
                   new_feature.append(str(float(features[j2_ind][k])-float(features[j1_ind][k])))
                else:
                   new_feature.append(str(float(features[j1_ind][k])-float(features[j2_ind][k])))
            scores_samplings[i].append((label,j1_ind,j2_ind,new_feature))
    return scores_samplings

    

def dict_to_array(d):
    a=[]
    for k,v in d.iteritems():
        v1=[float(feat) for feat in v]
        a.append(v1)
    return a

def write_feature_files(training_set,file_name):
    f=open(file_name,'w')
    for i in range(len(training_set)):
        feat=training_set[i]
        f1=''
        for j in range(len(feat)):
            f1+=str(feat[j])+' '
        f.write(f1+'\n')
    f.close()
def write_label_files(labels,file_name):
    f=open(file_name,'w')
    for i in range(len(labels)):
        f1=labels[i]
        f.write(str(f1)+'\n')
    f.close()
def print_best_indice(test_scores):
    num_sents=len(test_scores)/100
    
    print "Number of test scores",len(test_scores)
    a=open('best.indices','w')
    best_index=[]
    for i in range(num_sents):
        scores=test_scores[i*100:i*100+100]
        maxindex=max( (v, i) for i, v in enumerate(scores) )[1]
        a.write(str(maxindex)+'\n')
        best_index.append(maxindex)
    a.close()
    return best_index
if __name__=="__main__":
    meteors=collect_meteor_scores(opts.mf)
    print "Collecting train and test features"
    all_train_features=collect_all_features(opts.train)
    all_test_features_dict=collect_all_features(opts.test)
    all_test_features=dict_to_array(all_test_features_dict)
    print "Getting Top samples and creating train set"
    scores_samplings=get_training_samplings(meteors,all_train_features)
    training_set,train_labels=take_top_samplings(scores_samplings,opts.topsamples)
    print "Predicting with SVM"
    '''
    print "Training set",training_set[1:10]
    print "labels set",train_labels[1:10]
    print "Length of training set",len(training_set)
    print "Length of label set",len(train_labels)
    write_feature_files(training_set,'train.matlab')
    write_label_files(train_labels,'labels.matlab')
    write_feature_files(all_test_features,'test.matlab')
    '''
    test_scores=predict_scores(training_set,train_labels,all_test_features)
    test_scores2=predict_scores_log(training_set,train_labels,all_test_features)
    print "Regression Done. Now printing best indice"
    best_index=print_best_indice(test_scores)
    get_best_sent(best_index,opts.testsrcf,True,False)
    best_index2=print_best_indice(test_scores2)
    get_best_sent(best_index2,opts.testsrcf,False,False)
    ###CLEANING UP THE DATA###
    training_array=numpy.array(training_set)
    test_array=numpy.array(all_test_features)
    new_train_labels=numpy.array(train_labels)
    new_training_array,indices,var=clean_array(training_array)
    print "NUMBER OF FEATURES THAT SURVIVED",len(indices)
    new_test_array=test_array[:,tuple(indices)]
    new_test_scores=predict_scores(new_training_array,train_labels,new_test_array)
    new_test_scores2=predict_scores_log(new_training_array,train_labels,new_test_array)
    best_index=print_best_indice(new_test_scores)
    get_best_sent(best_index,opts.testsrcf,True,True)
    best_index2=print_best_indice(new_test_scores2)
    get_best_sent(best_index2,opts.testsrcf,False,True)
    '''
    ###CLEANING AND NORMALIZING UP THE DATA###
    training_array=numpy.array(training_set)
    test_array=numpy.array(all_test_features)
    new_train_labels=numpy.array(train_labels)
    new_training_array,indices,var=clean_and_normalize_array_train(training_array)
    new_test_array,indices,var=clean_and_normalize_array_test(test_array,indices,var)
    print "NUMBER OF FEATURES THAT SURVIVED",len(indices)
    new_test_array=test_array[:,tuple(indices)]
    new_test_scores=predict_scores(new_training_array,train_labels,new_test_array)
    new_test_scores2=predict_scores_log(new_training_array,train_labels,new_test_array)
    best_index=print_best_indice(new_test_scores)
    get_best_sent(best_index,opts.testsrcf,True,True)
    best_index2=print_best_indice(new_test_scores2)
    get_best_sent(best_index2,opts.testsrcf,False,True)
    '''





