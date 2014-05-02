import math
import sklearn
from sklearn import svm
from sklearn import linear_model
import numpy
def predict_scores(training_features,labels,test_features):
    print "Fitting the features and labels and creating the model"
    #clf=linear_model.SGDRegressor(alpha='1.0')
    clf=linear_model.SGDRegressor()
    clf.fit(training_features,labels)
    return clf.predict(test_features)

def predict_scores_log(training_features,labels,test_features):
    clf=linear_model.LogisticRegression(fit_intercept=False, penalty="l2")
    new_labels=[]
    for lab in labels:
        if lab > 0.0:
            new_labels.append(+1.0)
        else:
            new_labels.append(-1.0)
    clf.fit(training_features,new_labels)
    return clf.decision_function(test_features)

def clean_array(training_array):
    (rows,cols)=training_array.shape
    print "Intial shape",rows,cols
    var_cols=[]
    col_indices=[]
    for j in range(cols):
        var=math.sqrt(numpy.dot(training_array[:,j],training_array[:,j])/float(rows))
        if abs(var) > 0.005:
            col_indices.append(j)
            var_cols.append(var)
        else:
            continue
    return training_array[:,tuple(col_indices)],col_indices,var_cols

def clean_and_normalize_array_train(training_array):
    new_training_array,col_indices,var_cols=clean_array(training_array)
    return normalizer(new_training_array,col_indices,var_cols)

def normalizer(new_training_array,col_indices,var_cols):
    (rows,cols)=new_training_array.shape
    normal_training_array=numpy.zeros((rows,cols))
    assert cols==len(col_indices)
    for j in range(cols):
        var_j=var_cols[j]
        normal_training_array[:,j]=(new_training_array[:,j])/(float(var_j))
    return normal_training_array,col_indices,var_cols

def clean_and_normalize_array_test(test_array,col_indices,var_cols):
    new_test_array=test_array[:,tuple(col_indices)]
    return normalizer(new_test_array,col_indices,var_cols)


        
