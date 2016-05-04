# coding=utf-8
#!/bin/bash
#Classifier based on Unigrams for sentiment analysis in Twitter

import sys
import random
import numpy as np

fp = open("train_clean",'r')
fp2 = open("train_labels",'r')
fpt = open("test_clean",'r')
fpt2 = open("test_labels",'r')

stopwords = ["a","d","e","f","g","h","j","k","l","m","n","o","p","s","t","w","y","z","about","above","after","again","against","all","am","an","and","any","are","as","at","be","because","been","before","being","below","between","both","but","by","could","did","do","does","doing","down","during","each","few","for","from","further","had","has","have","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","it","it's","its","itself","let's","me","more","most","my","myself","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","she","she'd","she'll","she's","should","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","we","we'd","we'll","we're","we've","were","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
dict_final_tokens = []

num_class = 4
classlist = ['Action','Belief','Thought','Others']
confusion_mat = [[0]*num_class for i in range(num_class)]
num_of_folds = 0
total_accu = 0

L = fp.readlines()
L2 = fp2.readlines()
tL = fpt.readlines()
tL2 = fpt2.readlines()
fp.close()
fp2.close()

total_size = len(L)
start=0

token_train_list = []
label_train_list = []
token_test_list = []
label_test_list = []

for i in range(len(tL)):
	token_test_list.append(tL[i].strip('\n'))
	label_test_list.append(tL2[i].strip('\n'))

for i in range(len(L)):
		token_train_list.append(L[i].strip('\n'))
		label_train_list.append(L2[i].strip('\n'))

len_training = len(token_train_list)

for sentence in token_train_list:
	tokenlist_sentence = sentence.split(' ')
	for token in tokenlist_sentence:
		if token not in stopwords:
			if token.isalpha() and token not in dict_final_tokens:
				dict_final_tokens.append(token)

print len(dict_final_tokens)

dict_final_tokens.sort()

#print dict_final_tokens

unigram_matrix = [[0]*len(dict_final_tokens) for i in range(len_training)]
Prob_A = [0]*len(dict_final_tokens)
Prob_B = [0]*len(dict_final_tokens)
Prob_T = [0]*len(dict_final_tokens)
Prob_O = [0]*len(dict_final_tokens)

A_count = 0
B_count = 0
T_count = 0
O_count = 0

for label in label_train_list:
	if label.strip('\n').strip('\r')=='1':
		A_count += 1
	elif label.strip('\n').strip('\r')=='2':
		B_count += 1
	elif label.strip('\n').strip('\r')=='3':
		T_count += 1
	else:
		O_count += 1

print A_count,B_count,T_count,O_count

Prior_A = A_count/float(len_training)
Prior_B = B_count/float(len_training)
Prior_T = T_count/float(len_training)
Prior_O = O_count/float(len_training)

#	print Prior_A,Prior_B,Prior_T,Prior_O

s_count = 0
for sentence in token_train_list:
	tokenlist_sentence = sentence.split(' ')
	for token in tokenlist_sentence:
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			unigram_matrix[s_count][indx] += 1
			if label_train_list[s_count].strip('\n') == '1':
				Prob_A[indx] +=1
			elif label_train_list[s_count].strip('\n') == '2':
				Prob_B[indx] +=1
			elif label_train_list[s_count].strip('\n') == '3':
				Prob_T[indx] +=1
			else:
				Prob_O[indx] +=1
	s_count +=1


#print "The final matrix is:\t", unigram_matrix

classified_test_set = []

for i in range(len(Prob_A)):
		Prob_A[i] = Prob_A[i]/float(A_count)

for i in range(len(Prob_B)):
		Prob_B[i] = Prob_B[i]/float(B_count)

for i in range(len(Prob_T)):
		Prob_T[i] = Prob_T[i]/float(T_count)

for i in range(len(Prob_O)):
		Prob_O[i] = Prob_O[i]/float(O_count)

for sentence in token_test_list:
	tokenlist_sentence = sentence.split(' ')
	Prob_A_test = 1
	Prob_B_test = 1
	Prob_T_test = 1
	Prob_O_test = 1
	for token in tokenlist_sentence:
		token = token.lower()
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			if not Prob_A[indx]:
				Prob_A_test *= Prob_A[indx]
			if not Prob_B[indx]:
				Prob_B_test *= Prob_B[indx]
			if not Prob_T[indx]:
				Prob_T_test *= Prob_T[indx]
			if not Prob_O[indx]:
				Prob_O_test *= Prob_O[indx]
#			else:
#				print "not in dictionary: "+token

	Prob_A_test *= Prior_A
	Prob_B_test *= Prior_B
	Prob_T_test *= Prior_T
	Prob_O_test *= Prior_O

#		print Prob_A_test,Prob_B_test,Prob_T_test,Prob_O_test

	dict = {}
	dict['1'] = Prob_A_test
	dict['2'] = Prob_B_test
	dict['3'] = Prob_T_test
	dict['4'] = Prob_O_test

	cur_class='1'
	max = dict['1']
	for key in dict:
		if dict[key] > max:
			max = dict[key]
			cur_class = key
	
	classified_test_set.append(cur_class)

#	print classified_test_set

accu_count = 0

for i in range(len(classified_test_set)):
	'''ind1 = classlist.index(classified_test_set[i])
	ind2 = classlist.index(label_test_list[i].strip('\n').strip('\r'))
	confusion_mat[ind1][ind2] = confusion_mat[ind1][ind2] + 1'''
	if classified_test_set[i] == label_test_list[i].strip('\n').strip('\r'):
		accu_count += 1

accu = accu_count/float(len(label_test_list))
print "accuracy:"
print accu

from sklearn.metrics import precision_recall_fscore_support
print precision_recall_fscore_support(np.asarray(label_test_list), np.asarray(classified_test_set))

'''print "confusion-matrix:"
for i in range(0,num_class):
	print classlist[i] +'\t'+ str(confusion_mat[i])'''

