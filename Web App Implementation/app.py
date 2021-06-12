from flask import Flask, render_template,request,send_from_directory,send_file,redirect,url_for
from flask_socketio import SocketIO, emit
import pandas as pd
import sys
import os
import pickle
from zipfile import ZipFile
import pymongo

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener

'''           NER           '''
java_path='C:/Program Files/Java/jdk1.8.0_172/bin/java.exe'
os.environ['JAVAHOME']=java_path


st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'stanford-ner/stanford-ner.jar',
					   encoding='utf-8')

'''           NER           '''

'''           ML MODEL          '''
pickle_tf=open('NewTfidfModel.pickle','rb')
tf_idf_vect=pickle.load(pickle_tf)
pickle_in=open('NewModel.pickle','rb')
linear_svc_model=pickle.load(pickle_in)
'''           ML MODEL          '''


'''       DB       CONNECTIONS      '''
try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print("MongoDB Connection error")
    myclient = None
    raise

db = myclient['key_needs']
if 'tweets' not in db.list_collection_names():
    print(' TWEETS TABLE NOT THERE ')
    db.create_collection('tweets')
tweets_table = db['tweets']
'''       DB       CONNECTIONS      '''

ckey="BiccnngDumXdSdV2zshOqcDMO"
csecretkey="hrOlkVf0u6fYyqKF7EvkFS4FzB5cGmlVRmcWJbmyGoJowhbMta"
atoken="609971942-u6RIVxVgHPBdUUXet81rNgkOcmEtasQePRFQhun3"
atokensecret = "Bkg9Ozu57S2vx9YBvxKjr8frIu0MiKav5mZIGsuc2eBgI"


app = Flask(__name__)
socketio = SocketIO(app)

hashtag=""

auth = OAuthHandler(consumer_key=ckey,consumer_secret=csecretkey)
auth.set_access_token(key=atoken,secret=atokensecret)
api = API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


labels = ['affected_people', 'caution_and_advice', 'deaths_reports','disease_signs_or_symptoms', 'disease_transmission',
'displaced_people_and_evacuations','donation_needs_or_offers_or_volunteering_services','infrastructure_and_utilities_damage',
'injured_or_dead_people','missing_trapped_or_found_people','not_related_or_irrelevant','other_useful_information',
'prevention','sympathy_and_emotional_support','treatment']
'''labelsShort
{1:'missing_trapped_or_found_people',
       2:'affected_injured_dead_death',
       3:'donation_needs_or_offers_or_volunteering_services',
       4:'sympathy_and_emotional_support', 
       5:'not_related_or_irrelevant',
       6:'prevention_caution_and_advice',
       7:'infrastructure_and_utilities_damage',
       8:'disease_transmission_signs_or_symptoms',
       9:'treatment'}
'''
labelsShort={"1":'missing_trapped_or_found_people',
       "2":'affected_injured_dead_death',
       "3":'donation_needs_or_offers_or_volunteering_services',
       "4":'sympathy_and_emotional_support',
       "5":'not_related_or_irrelevant',
       "6":'prevention_caution_and_advice',
       "7":'infrastructure_and_utilities_damage',
       "8":'disease_transmission_signs_or_symptoms',
       "9":'treatment'}

missing_trapped_or_found_people=[]
affected_injured_dead_death=[]
donation_needs_or_offers_or_volunteering_services=[]
sympathy_and_emotional_support=[]
not_related_or_irrelevant=[]
prevention_caution_and_advice=[]
infrastructure_and_utilities_damage=[]
disease_transmission_signs_or_symptoms=[]
treatment=[]

def add_to_list(status,y,locations):
    global missing_trapped_or_found_people,affected_injured_dead_death,donation_needs_or_offers_or_volunteering_services,\
    sympathy_and_emotional_support,not_related_or_irrelevant,prevention_caution_and_advice,infrastructure_and_utilities_damage,\
    disease_transmission_signs_or_symptoms,treatment


    if (y == "1"):
        missing_trapped_or_found_people.append({"Tweet": status.text,"Locations":locations})
    elif (y == "2"):
        affected_injured_dead_death.append({"Tweet": status.text,"Locations":locations})
    elif (y == "3"):
        donation_needs_or_offers_or_volunteering_services.append({"Tweet": status.text,"Locations":locations})
    elif (y == "4"):
        sympathy_and_emotional_support.append({"Tweet": status.text,"Locations":locations})
    elif (y == "5"):
        not_related_or_irrelevant.append({"Tweet": status.text,"Locations":locations})
    elif (y == "6"):
        prevention_caution_and_advice.append({"Tweet": status.text,"Locations":locations})
    elif (y == "7"):
        infrastructure_and_utilities_damage.append({"Tweet": status.text,"Locations":locations})
    elif (y == "8"):
        disease_transmission_signs_or_symptoms.append({"Tweet": status.text,"Locations":locations})
    else:
        treatment.append({"Tweet": status.text,"Locations":locations})


class Listener(StreamListener):
    client = ""
    def __init__(self, output_file=sys.stdout):
        super(Listener,self).__init__()
        self.output_file = output_file
    def on_status(self, status):
        #print("Tweet : {0}".format(status.text))
        if not hasattr(status, "retweeted_status"):# If not  a retweet : http://docs.tweepy.org/en/latest/extended_tweets.html#introduction
            y = str(linear_svc_model.predict(tf_idf_vect.transform([status.text]))[0])
            #print("TypeOF : {} ".format(type(y)))
            tokenized_text = word_tokenize(status.text)
            tokenized_text = [word.capitalize() for word in tokenized_text]
            classified_text = st.tag(tokenized_text)
            locations = ""
            for i in classified_text:
                if i[1]=="LOCATION":
                    locations +="{},".format(i[0])
            if len(locations) > 0 and locations[-1]==",":
                locations=locations[0:len(locations)-1]
            add_to_list(status,y,locations)
            tweets_table.insert_one({'tweet_id':status.id,'tweet':status.text,'locations':locations,'class':y,'class_text':labelsShort[y]})
            socketio.emit("send_tweets",{"tweet":status.text},room=Listener.client)
            socketio.emit("send_prediction",{"class":y})
    def on_error(self, status_code):
        print("ERROR OCCURRED : ",status_code)
        return False

output = open('stream_output.txt', 'w')
listener = Listener(output_file=output)

stream = Stream(auth=auth, listener=listener)

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')

@app.route('/detect_live', methods=['GET'])
def detect_live():
    global hashtag
    hashtag = request.args.get('hashtag')
    
    if stream:
        try:
            stream.disconnect()
        except:
            pass
    
    return render_template('detect_live.html',value=hashtag)

@socketio.on('connect')
def conn():
    Listener.client = request.sid
    print("client :{}".format(Listener.client))

    return emit("CONNECTION",{"response":"ON"})

@socketio.on('hashtag_recieved?')
def hashtag():
    return emit("hashtag_recieved?", {"response": "OKAY", "hashtag": hashtag})

@socketio.on('send_tweets')
def send_tweets():
    #emit("send_tweets",{"tweet":"SENDING"})
    print("STreaming  started !", file=sys.stdout)
    stream.filter(track=["#{0}".format(hashtag.replace("#",""))],languages=["en"])
    #stream.disconnect()

@socketio.on('prediction')
def send_prediction():
    emit("send_prediction",{"prediction":"SENDING"})

@socketio.on('stop_tweets')
def stop_tweets():
    print("Streaming  STOPPING!", file=sys.stdout)
    stream.disconnect()
    print("Streaming  STOPPED!", file=sys.stdout)
    emit("stop_tweets",{"tweet":"STOPPED"})

@socketio.on('download_tweets')
def download_tweets():
    #print("DOWNLOAD DOWNLOAD DOWNLOAD DOWNLOAD DOWNLOAD")

    writer = pd.ExcelWriter('KeyNeeds.xlsx', engine='xlsxwriter')

    global missing_trapped_or_found_people, affected_injured_dead_death, donation_needs_or_offers_or_volunteering_services, \
        sympathy_and_emotional_support, not_related_or_irrelevant, prevention_caution_and_advice, infrastructure_and_utilities_damage, \
        disease_transmission_signs_or_symptoms, treatment

    copies= {}

    copies["missing_trapped_or_found_people"]=missing_trapped_or_found_people[:];missing_trapped_or_found_people = []
    copies["affected_injured_dead_death"]=affected_injured_dead_death[:];affected_injured_dead_death = []
    copies["donation_needs_or_offers_or_volunteering_services"]=donation_needs_or_offers_or_volunteering_services[:];donation_needs_or_offers_or_volunteering_services = []
    copies["sympathy_and_emotional_support"]=sympathy_and_emotional_support[:];sympathy_and_emotional_support = []
    copies["not_related_or_irrelevant"]=not_related_or_irrelevant[:];not_related_or_irrelevant = []
    copies["prevention_caution_and_advice"]=prevention_caution_and_advice[:];prevention_caution_and_advice = []
    copies["infrastructure_and_utilities_damage"]=infrastructure_and_utilities_damage[:];infrastructure_and_utilities_damage = []
    copies["disease_transmission_signs_or_symptoms"]=disease_transmission_signs_or_symptoms[:];disease_transmission_signs_or_symptoms = []
    copies["treatment"]=treatment[:];treatment = []


    df1 = pd.DataFrame(copies["{0}".format("missing_trapped_or_found_people")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("missing_trapped_or_found_people",len(copies["missing_trapped_or_found_people"]),len(missing_trapped_or_found_people)))
    #print(len(df1))
    df1.to_excel(writer, sheet_name="missing_trapped_or_found_people")
    df1.to_csv("data/missing_trapped_or_found_people.csv")

    df2 = pd.DataFrame(copies["{0}".format("affected_injured_dead_death")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("affected_injured_dead_death", len(copies["affected_injured_dead_death"]), len(affected_injured_dead_death)))
    #print(len(df2))
    df2.to_excel(writer, sheet_name="affected_injured_dead_death")
    df2.to_csv("data/affected_injured_dead_death.csv")

    df3 = pd.DataFrame(copies["{0}".format("donation_needs_or_offers_or_volunteering_services")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("donation_needs_or_offers_or_volunteering_services", len(copies["donation_needs_or_offers_or_volunteering_services"]),len(donation_needs_or_offers_or_volunteering_services)))
    #print(len(df3))
    df3.to_excel(writer, sheet_name="donation_offers_volunt")
    df3.to_csv("data/donation_needs_or_offers_or_volunteering_services.csv")

    df4 = pd.DataFrame(copies["{0}".format("sympathy_and_emotional_support")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("sympathy_and_emotional_support", len(copies["sympathy_and_emotional_support"]),len(sympathy_and_emotional_support)))
    #print(len(df4))
    df4.to_excel(writer, sheet_name="sympathy_and_emotional_support")
    df4.to_csv("data/sympathy_and_emotional_support.csv")

    df5 = pd.DataFrame(copies["{0}".format("not_related_or_irrelevant")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("not_related_or_irrelevant", len(copies["not_related_or_irrelevant"]),len(not_related_or_irrelevant)))
    #print(len(df5))
    df5.to_excel(writer, sheet_name="not_related_or_irrelevant")
    df5.to_csv("data/not_related_or_irrelevant.csv")

    df6 = pd.DataFrame(copies["{0}".format("prevention_caution_and_advice")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("prevention_caution_and_advice", len(copies["prevention_caution_and_advice"]),len(prevention_caution_and_advice)))
    #print(len(df6))
    df6.to_excel(writer, sheet_name="prevent_caut_advice")
    df6.to_csv("data/prevention_caution_and_advice.csv")

    df7 = pd.DataFrame(copies["{0}".format("infrastructure_and_utilities_damage")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("infrastructure_and_utilities_damage", len(copies["infrastructure_and_utilities_damage"]),len(infrastructure_and_utilities_damage)))
    #print(len(df7))
    df7.to_excel(writer, sheet_name="infras_utility_damage")
    df7.to_csv("data/infrastructure_and_utilities_damage.csv")

    df8 = pd.DataFrame(copies["{0}".format("disease_transmission_signs_or_symptoms")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("disease_transmission_signs_or_symptoms", len(copies["disease_transmission_signs_or_symptoms"]),len(disease_transmission_signs_or_symptoms)))
    #print(len(df8))
    df8.to_excel(writer, sheet_name="disease_trans_signs_symptom")
    df8.to_csv("data/disease_transmission_signs_or_symptoms.csv")

    df9 = pd.DataFrame(copies["{0}".format("treatment")], columns=['Tweet','Locations'])
    #print("{} --->> Copy : {} -- OG : {}".format("treatment",len(copies["treatment"]),len(treatment)))
    #print(len(df9))
    df9.to_excel(writer, sheet_name="treatment")
    df9.to_csv("data/treatment.csv")
    writer.save()
    #writer.close()
    # create a ZipFile object
    with ZipFile('data/zip/KeyNeeds.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk("data"):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)
            break
    emit("download_tweets", {"tweet": "GENERATED"})

@app.route("/download",methods=["GET","POST"])
def download():
    print("DOWNLOAD REQUESTED!!!")
    return send_from_directory(directory="data/zip/", filename="KeyNeeds.zip", as_attachment=True,cache_timeout=0)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)