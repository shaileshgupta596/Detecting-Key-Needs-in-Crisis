# -*- coding: utf-8 -*-

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
java_path='C:/Program Files/Java/jdk1.8.0_172/bin/java.exe'
os.environ['JAVAHOME']=java_path


st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'stanford-ner/stanford-ner.jar',
					   encoding='utf-8')

text = 'video report kathmandu overwhelmed rubble earth'
text2='Team of PS Mohan Garden, Dwarka District, reunited 5 yrs old boy with his family in just 3 hrs. He was found wandering at Som Bazaar  market, Mohan Garden, 4 km away from his home.'
tokenized_text = word_tokenize(text)
tokenized_text=[word.capitalize() for word in tokenized_text]
classified_text = st.tag(tokenized_text)

print(classified_text)
print(type(classified_text))