import sys
import re
import numpy as np

# conmat = [[0]*3 for i in range(3)]

from subprocess import call
path="/home/abhi/Dropbox/IIITCoursework/Sem4/Project/SentenceClassification/"
#path="/home/abhi/IIITCourseWork_TooLargeForDropbox/DWDM/Project/Final/data/"
fp=open(path+"test_data","r");
L = fp.readlines();

expected_class = []

for s in L:
	expected_class.append(s[0]);	

call(["./svm-train","-t","0",path + "training_data"])
call(["./svm-predict",path + "test_data","training_data.model","output"])

predicted_class = []

#calculating f-score
outf = open("output",'r')
tempL = outf.readlines()
for val in tempL:
	predicted_class.append(val.strip('\n'))
outf.close ()

# for i in range(len(predicted_class)):
#     conmat[int(expected_class[i])][int(predicted_class[i])] += 1

#print len(expected_class),len(predicted_class)

from sklearn.metrics import precision_recall_fscore_support
print precision_recall_fscore_support(np.asarray(expected_class), np.asarray(predicted_class))

# print "Confusion matrix:"
# print conmat