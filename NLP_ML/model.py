import numpy as np 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  ## TFIDF Model
from sklearn.model_selection import train_test_split
from time import ctime,time
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBClassifier
import pickle
from sklearn import metrics

pickle_in=open('final_dataset.pickle','rb')
final_dataset=pickle.load(pickle_in)

label1={'other_useful_information':0, 'missing_trapped_or_found_people':1,
       'affectedPeople_or_injured_or_dead_people_or_DeathReports':2,
       'donation_needs_or_offers_or_volunteering_services':3,
       'sympathy_and_emotional_support':4, 'not_related_or_irrelevant':5,
       'prevention_or_caution_and_advice':6,
       'infrastructure_and_utilities_damage':7,
       'disease_transmission_or_disease_signs_or_symptoms':8, 'treatment':9}
def label(x):
    return label1[x];


final_dataset["numeric_label"]=final_dataset["label"].map(label)

X = final_dataset['preprocessed'].values# text data will be converted into operational format
y=final_dataset['numeric_label'].values #same as it is
print(X[0:5])
print('Corresponding result >>>>>>>>>>>>>>>>>>>>')
print(y[0:5])

tf_idf_vect = TfidfVectorizer()# initializing the vector by creating object
X= tf_idf_vect.fit_transform(X) # tranforming text data into vector format
X.shape


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 123)

from sklearn.svm import LinearSVC
linear_svc_model = LinearSVC(multi_class="ovr") # note perform changes in attribute to get bettter accuracy
linear_svc_model.fit(X_train,y_train)#passing data into model for training
y_pred=linear_svc_model.predict(X_test)#after training we pass rest 20%of data for testing purpose
acc=metrics.accuracy_score(y_test,y_pred) 
#here we are passing actual result and predicted result to find out accuracy
print('acuuracy>>>>',acc*100)
z=tf_idf_vect.transform(['Team of PS Mohan Garden, Dwarka District, reunited 5 yrs old boy with his family in just 3 hrs. He was found wandering at Som Bazaar  market, Mohan Garden, 4 km away from his home.'])
print(linear_svc_model.predict(z))


start_time = time()
print(ctime())

tuned_params = {'max_depth': [4,5,6,7,8], 'learning_rate': [0.01, 0.05, 0.1,0.25,0.5,0.8], 'n_estimators': [ 300, 400, 500,600,700], 'reg_lambda': [0.001, 0.1, 1.0, 10.0, 100.0]}
model = RandomizedSearchCV(XGBClassifier(), tuned_params, n_iter=15, scoring = 'accuracy', n_jobs=-1)
model.fit(X_train,y_train) # actual data and actual prediction


model.fit(X_train,y_train)
y_pred=model.predict(X_test)
acc=metrics.accuracy_score(y_test,y_pred) 
#here we are passing actual result and predicted result to find out accuracy
print('acuuracy>>>>',acc*100)
print(model.best_estimator_)
print("--- %s seconds ---" % (time() - start_time))





