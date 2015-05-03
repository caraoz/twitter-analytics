# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import codecs
import chardet

f = open(".txt","w",encoding='utf-8')
DATA_FILE = ".json"
# Build a JSON array
data = "[{0}]".format(",".join([l for l in open(DATA_FILE,encoding='utf-8').readlines()]))

### Create a pandas DataFrame (think: 2-dimensional table) to get a 
### spreadsheet-like interface into the data
df = pd.read_json(data, orient='records')
print("Successfully imported " + str(len(df)) + " tweets")

#print(df)



#####check if rate limited
#####
def limitCheck():
        limit_notices = df[pd.notnull(df.limit)]
        ##Remove the limit notice column from the DataFrame entirely
        df = df[pd.notnull(df['id'])]
        print("Number of total tweets that were rate-limited", sum([ln['track'] for ln in limit_notices.limit]) )
        print("Total number of limit notices", str(len(limit_notices)) )


#####


# Create a time-based index on the tweets for time series analysis
# on the created_at field of the existing DataFrame.
def firstLast():
        df.set_index('created_at', drop=False, inplace=True)
        print("Created date/time index on tweets")

        print("First tweet timestamp (UTC)	" + str(df['created_at'][0]))
        print("Last tweet timestamp (UTC)	" + str(df['created_at'][-1]))


#####
## Let's group the tweets by hour and look at the overall volumes with a simple
## histogram
def hourHistogram():
        grouped = df.groupby(lambda x: x.hour)
        print("Number of relevant tweets by the hour (UTC)")
        print(" ")
        for hour, group in grouped:
                star = '*'*int((len(group)/1000))
                print(str(hour)+"       "+str(len(group))+"     "+str(star) )



# Let's group the tweets by (hour, minute) and look at the overall volumes with a simple
# text-based histogram

def group_by_15_min_intervals(x):
        if   0 <= x.minute <= 15: return (x.hour, "0-15")
        elif 15 < x.minute <= 30: return (x.hour, "16-30")
        elif 30 < x.minute <= 45: return (x.hour, "31-45")
        else: return (x.hour, "46-00")
def minuteHistogram():
        grouped = df.groupby(lambda x: group_by_15_min_intervals(x))
        print("Number of relevant tweets by intervals (UTC)")
        for interval, group in grouped:
                star = '*'*int((len(group) / 20))
                print(str(interval)+"\t"+str(len(group))+"\t"+str(star))
        plt.plot([len(group) for hour, group in grouped][1:-1])
        plt.ylabel("Tweet Volume")
        plt.xlabel("Time (in minutes within an hour)")
        nomme = DATA_FILE.split(".")[0] + "-MinuteHistogram.png"
        plt.savefig(nomme)

def twitterLeader():
# The "user" field is a record (dictionary), and we can pop it off
# and then use the Series constructor to make it easy to use with pandas.
# ORIGINAL http://nbviewer.ipython.org/github/chdoig/Mining-the-Social-Web-2nd-Edition/blob/master/ipynb/__Understanding%20the%20Reaction%20to%20Amazon%20Prime%20Air.ipynb

        #user_col = df.pop('user').apply(pd.Series) ######original
        #user_col = df.pop('screen_name').apply(pd.Series) #####new
        # Get the screen name column
        authors = screen_name
        # And count things
        authors_counter = Counter(authors.values)
        # And tally the totals
        print("Most frequent (top 25) authors of tweets")
        print('\n'.join(["{0}\t{1}".format(a, f) for a, f in authors_counter.most_common(25)]))
        num_unique_authors = len(set(authors.values))
        # Get only the unique authors
        print("There are {0} unique authors out of {1} tweets".format(num_unique_authors, len(df)))

def tWhoresTest():
        user_col = df.pop('screen_name')
        authors = user_col
        authors = user_col.values
        authors_counter = Counter(authors)
        print("Most frequent (top 25) authors of tweets")
        print('\n'.join(["{0}\t\t{1}".format(a, f) for a, f in authors_counter.most_common(25)]))
        num_unique_authors = len(set(authors))
        print("There are {0} unique authors out of {1} tweets".format(num_unique_authors, len(df)))




def languages():
        print(df.lang.value_counts())
        

def natlang(word):
        tokens = []
        from collections import Counter
        en_text = df[df['lang'] == 'en'].pop('text')
        for txt in en_text.values:
                tokens.extend([t.lower().strip(":,.") for t in txt.split()])
                
        # Use a Counter to construct frequency tuples
        tokens_counter = Counter(tokens)
        # Display some of the most commonly occurring tokens
        #print(tokens_counter.most_common(50))
        import nltk
        # Remove stopwords to decrease noise
        ignore_terms = []
        ignore_terms.extend(nltk.corpus.stopwords.words('english'))
        [tokens_counter.pop(t, None) for t in ignore_terms]
        # Redisplay the data (and then some)
        #print(tokens_counter.most_common(200))

        ##cool text stuff
        nltk_text = nltk.Text(tokens)
        nltk_text.collocations()
        #f.write(nltk_text.collocations())
        print(nltk_text.concordance(word))
        #f.write(nltk_text.concordance("muslim"))



firstLast()
hourHistogram()
minuteHistogram()
#twitterLeader()
tWhoresTest()
languages()
natlang("nbc")
#filterednatlang()











