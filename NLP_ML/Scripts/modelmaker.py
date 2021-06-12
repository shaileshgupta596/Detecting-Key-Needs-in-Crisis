# -*- coding: utf-8 -*-

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
#import pickle
import os

java_path='C:/Program Files (x86)/Java/jdk1.8.0_144/bin/java.exe'
os.environ['JAVAHOME']=java_path


st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'stanford-ner/stanford-ner.jar',
					   encoding='utf-8')

text = ['video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth',
'video report kathmandu overwhelmed rubble earth']
tokenized_text = [word_tokenize(sent) for sent in text]
tokenized_tweet=[]
for sent in tokenized_text:
	tweet=[]
	for words in sent:
		tweet.append(words.capitalize())
	tokenized_tweet.append(tweet)



classified_text = [st.tag(sent) for sent in tokenized_tweet]


print(classified_text)

