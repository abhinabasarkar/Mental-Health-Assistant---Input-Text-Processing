# coding=utf-8
#!/bin/bash
#Classifier based on Unigrams for sentiment analysis in Twitter

import sys
import random
import operator

fp = open("full_clean",'r')
fp2 = open("full_labels",'r')
#fpt = open("../tokenizer/test_1000",'r')
#fpt2 = open("../tokenizer/polarity_1000",'r')

stopwords = ["a","d","e","f","g","h","j","k","l","m","n","o","p","s","t","w","y","z","about","above","after","again","against","all","am","an","and","any","are","as","at","be","because","been","before","being","below","between","both","but","by","could","did","do","does","doing","down","during","each","few","for","from","further","had","has","have","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","it","it's","its","itself","let's","me","more","most","my","myself","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","she","she'd","she'll","she's","should","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","we","we'd","we'll","we're","we've","were","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]

num_class = 4
classlist = ['Action','Belief','Thought','Others']
confusion_mat = [[0]*num_class for i in range(num_class)]
num_of_folds = 0
total_accu = 0

L = fp.readlines()
L2 = fp2.readlines()
fp.close()
fp2.close()

total_size = len(L)
start=0
dict_final_tokens = []
token_train_list = []
label_train_list = []

for i in range(total_size):
			token_train_list.append(L[i].strip('\n'))
			label_train_list.append(L2[i].strip('\n'))

for sentence in token_train_list:
		tokenlist_sentence = sentence.split(' ')
		for token in tokenlist_sentence:
			if token not in stopwords:
				if token.isalpha() and token not in dict_final_tokens:
					dict_final_tokens.append(token)

print len(dict_final_tokens)
dict_final_tokens.sort()

dict_A = {}
dict_B = {}
dict_T = {}
dict_O = {}

s_count = 0
for sentence in token_train_list:
	tokenlist_sentence = sentence.split(' ')
	for token in tokenlist_sentence:
		if token in dict_final_tokens:
			if label_train_list[s_count].strip('\n') == '1':
				if dict_A.has_key(token):
					dict_A[token]+=1
				else:
					dict_A[token]=1
			elif label_train_list[s_count].strip('\n') == '2':
				if dict_B.has_key(token):
					dict_B[token]+=1
				else:
					dict_B[token]=1
			elif label_train_list[s_count].strip('\n') == '3':
				if dict_T.has_key(token):
					dict_T[token]+=1
				else:
					dict_T[token]=1
			else:
				if dict_O.has_key(token):
					dict_O[token]+=1
				else:
					dict_O[token]=1
	s_count +=1

sorted_A = sorted(dict_A.items(), key=operator.itemgetter(1))
sorted_A.reverse()
sorted_B = sorted(dict_B.items(), key=operator.itemgetter(1))
sorted_B.reverse()
sorted_T = sorted(dict_T.items(), key=operator.itemgetter(1))
sorted_T.reverse()
sorted_O = sorted(dict_O.items(), key=operator.itemgetter(1))
sorted_O.reverse()

print"top 10 words for Action:"
for i in range(10):
	print sorted_A[i]

print"top 10 words for Belief:"
for i in range(10):
	print sorted_B[i]

print"top 10 words for Thought:"
for i in range(10):
	print sorted_T[i]

print"top 10 words for Others:"
for i in range(10):
	print sorted_O[i]