'''
saves tweets to file

plans:
- save to db: http://pythondata.com/collecting-storing-tweets-python-mysql/
- save to file: http://stackoverflow.com/questions/14158880/python-suggestion-how-to-improve-to-write-in-streaming-text-file-in-python

run:
nohup python streamer2file.py > tweets.txt &
'''
from geopy.geocoders import Nominatim
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import json
# import schedule
import time

ckey = 'uyQXm9AMlcWy4d5n8o5l2XlEN'
consumer_secret = 'bF5RuNCQ9IYS8857Dm9w7RQXV7ppKdUtqq4OJsqQUsIArh5w5i'
access_token_key = '4824205753-iEAp9mwDnSuUmexdZndnvQGzl532Zb3mlO3QSDb'
access_token_secret = 'XbLBtOec179sE4j2c2Ia7dzZdyv5k7kZgAlz91xOOLGRv'
 
 #https://gist.github.com/IAmKio/10363065/af9d6f0c18aceac6e58a106cc7d6885a4ba1220a
countries = {'Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Ashmore and Cartier Islands',
'Australian Antarctic Territory','Christmas Island','Cocos (Keeling) Islands','Coral Sea Islands Territory','Heard Island and McDonald Islands','Norfolk Island',
'Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia','Bosnia and Herzegovina',
'Federation of Bosnia and Herzegovina','Republika Srpska','Botswana','Brazil','Brunei','Bulgaria','Burkina Faso','Burma','Burundi','Cambodia','Cameroon',
'Canada','Cape Verde','Central African Republic','Chad','Chile','China','Hong Kong','Macau','Colombia','Comoros','Congo','Costa Rica','Croatia','Cuba',
'Cyprus','Czech Republic','Denmark','Faroe Islands','Greenland','Djibouti','Dominica','Dominican Republic','East Timor','Ecuador','Egypt','El Salvador',
'Equatorial Guinea','Eritrea','Estonia','Ethiopia','Fiji','Finland','Aland','France','Clipperton Island','French Polynesia','New Caledonia','Saint Barthelemy',
'Saint Martin','Saint Pierre and Miquelon','Wallis and Futuna','French Southern and Antarctic Lands','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada',
'Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel','Italy','Ivory Coast',
'Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kiribati','Korea',' North','Korea',' South','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya',
'Cyrenaica','Liechtenstein','Lithuania','Luxembourg','Macedonia','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Mauritania','Mauritius',
'Mexico','Federated States of Micronesia','Moldova','Monaco','Mongolia','Montenegro','Morocco','Mozambique','Namibia','Nauru','Nepal','Netherlands','Netherlands',
'Aruba','Curacao','Sint Maarten','New Zealand','Ross Dependency','Tokelau','Cook Islands','Niue','Nicaragua','Niger','Nigeria','Norway','Oman','Pakistan','Azad Kashmir',
'Gilgit-Baltistan','Palau','Palestine','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russia','Rwanda',
'Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Seychelles',
'Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Swaziland','Sweden',
'Switzerland','Syria','Tajikistan','Tanzania','Thailand','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Tuvalu','Uganda','Ukraine',
'United Arab Emirates','United Kingdom','Akrotiri and Dhekelia','Anguilla','Bermuda','British Indian Ocean Territory','British Virgin Islands','Cayman Islands','Falkland Islands',
'Gibraltar','Montserrat','Pitcairn Islands','Saint Helena',' Ascension and Tristan da Cunha','South Georgia and the South Sandwich Islands','Turks and Caicos Islands',
'British Antarctic Territory','Guernsey','Alderney','Herm','Sark','Isle of Man','Jersey','United States of America','American Samoa','Guam','Northern Mariana Islands','Puerto Rico',
'U.S. Virgin Islands','Marshall Islands','Micronesia','Palau','Uruguay','Uzbekistan','Vanuatu','Vatican City','Venezuela','Vietnam','Yemen','Zambia','Zimbabwe','Abkhazia',
'Cook Islands','Kosovo','Nagorno-Karabakh','Niue','Northern Cyprus','Sahrawi Arab Democratic Republic','Somaliland','South Ossetia','Taiwan','Transnistria'}
geolocator = Nominatim()

#Listener Class Override
class Streamlistener(StreamListener):
    def on_data(self, data):
        try:
            tweet = json.loads(data)

            data = {}
            #if tweet["geo"]: need to gather more tweets for the phrases collocation but will only plot those with geo
            data = {}
            data["text"] = tweet["text"]
            data["date"] = tweet["created_at"]
            if tweet["geo"]:
                data["latitude"] = tweet["geo"]["coordinates"][0]
                data["longitude"] = tweet["geo"]["coordinates"][1]
                
                pos = str(data["latitude"]) + ', ' + str(data["longitude"])
                location = geolocator.reverse(pos, language='en')
                raw = location.raw
                country = raw['address']['country']
                # print(country)
                if country in countries:
                    data["country"] = country
                #     print("\n")
                #     print pos
                #     print country
                #     print data
                #     print("\n")
            print(data)
            # save(data)
            # print("\n")
        except BaseException, e:
            # print 'failed ondata,', str(e)
            pass
        except ConnectionError, c:
            print 'Connection error.', str(e)
            pass
        except Exception, ex:
            print 'Generic exception happened.', str(e)
            pass
 
    def on_error(self, status):
        print status

# def save(data):
    # print(data)
    # with open("tweets.txt", 'a', buffering=0.01*(1024**2)) as myfile:
    #     for line in data:
    #         myfile.write(line + '\n')

def start_stream():
    while True:
        try:
            listener = Streamlistener()
            twitterStream = Stream(auth, listener) #initialize Stream object with a time out limit
            # twitterStream.filter(track=keyword_list)  #call the filter method to run the Stream Object

            #https://dev.twitter.com/streaming/reference/get/statuses/sample
            twitterStream.sample()


            #https://github.com/azurro/country-bounding-boxes/blob/master/dataset/ph.json
            #twitterStream.filter(locations=[112.16672,4.3833541,127.0737203,21.5296298])  #call the filter method to run the Stream Object
            #twitterStream.filter(locations=[12.865353, -168.344469, 67.929266, -42.133528])  #call the filter method to run the Stream Object
            #twitterStream.filter(locations=[-56.286063, -29.301501,74.250793, 174.253191,-63.874556, -170.629625,70.718096, -29.828842 ])  #call the filter method to run the Stream Object
            #twitterStream.filter(locations=[-69.624350, -23.9022753, -57.353627, -7.164010 ])  #call the filter method to run the Stream Object
        except Exception, e:
            # Oh well, reconnect and keep trucking
            print 'Generic exception happened. Continuing..', str(e)
            pass
        except KeyboardInterrupt:
            # Or however you want to exit this loop
            twitterStream.disconnect()
            break



if __name__ == '__main__':
    auth = OAuthHandler(ckey, consumer_secret) #OAuth object
    auth.set_access_token(access_token_key, access_token_secret)
    start_stream()



