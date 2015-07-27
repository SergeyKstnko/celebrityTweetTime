import tweepy
from tweepy import OAuthHandler
import datetime
import pandas as pd
import matplotlib.pyplot as plt


#connect to Twitter API
celebrity = '@elonmusk'

#You will need to register your application on Twitter and get your consumer_key,
#consumer_secret, access_token and access_secret there. For more details read
#the paragraph in the link below
# http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#This function returns days of the week based on the number returned by datetime.weekday()
# Param: 	integer for the day of the week
def weekdayf(weekday): 
    return{
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }[weekday]

#!!!!!!!# Creating an empty dataframe
data = {'Day of the week': [],
        'Hour': [],
        'Full Date': []
       }    
df = pd.DataFrame(data)

#for every tweet on the timeline
for status in tweepy.Cursor(api.user_timeline, id = celebrity).items(8000):
    #if the tweet is a response
    if status.in_reply_to_status_id != None:
    	#collect and append hour, weekday and full time when it was created
        data = {'Hour': [status.created_at.time().hour],
        'Day of the week': [weekdayf(status.created_at.weekday())],
        'Full date': [status._json['created_at']]
        }
        df1 = pd.DataFrame(data)
        df = df.append(df1, ignore_index = True)


listDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#plot the histogram based on the data collected
print "Data for %s" % celebrity
print "All times is in GMT/UTC"

for day in listDays:
    df3 = df[df['Day of the week'] == day]
    #uncoment the next line if you run code in iPython Notebooks
    #%matplotlib inline
    try:
        plt.hist(df3['Hour'].values, label = day, bins = 10)
    except ValueError:
        print "No data is available for %s" % day
        continue

    plt.title(day)
    plt.xlabel("Hour")
    plt.ylabel("Frequency of responses")
    plt.axis([-1, 24, 0, 20])
    plt.show()
