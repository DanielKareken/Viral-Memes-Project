import json
import sqlite3

# temp table variables for storage
timestamp = ""
hashtags = set()
user_id = ""
urls = set()

# read file
text = open("tweets-nov-2012.txt", "r", encoding='UTF8')
words = []
words = text.read().split()
text.close()

# create empty table for later storage
tweetData = 'tweets-nov-2012.sqlite'
con = sqlite3.connect(tweetData)

cur = con.cursor()
cur.executescript('DROP TABLE IF EXISTS memes')

cur.executescript("""CREATE TABLE memes
                    (meme_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    timestamp INTEGER,
                    hashtags TEXT,
                    urls TEXT);""")

# clean data by removing non alphanumeric characters and
# sort data and insert into table
cleanwords = []
category = ""
count = 0

for word in words:
    word = ''.join(e for e in word if e.isalnum())
    cleanwords.append(word)

    if word == "timestamp":
        # only occurs after first line is read, assumes previous line and inputs data, reseting temp variables
        if count > 0:
            stringtags = ""
            stringurls = ""

            i = 0
            for tag in hashtags:
                if i == 0:
                    stringtags += tag
                    i += 1
                else:
                    stringtags += ", " + tag
                    i += 1

            i = 0
            for url in stringurls:
                if i == 0:
                    stringurl += url
                    i += 1
                else:
                    stringurl += ", " + url
                    i += 1

            cur.execute('INSERT INTO memes(user_id, timestamp, hashtags, urls) VALUES (?, ?, ?, ?)',
                        (user_id, timestamp, stringtags, stringurls))
            con.commit()
            count += 1
            timestamp = ""
            hastags = set()
            user_id = ""
            urls = set()

        category = word
    elif word == "hashtags":
        category = word
    elif word == "userid":
        category = word
    elif word == "urls":
        category = word
    else:
        if category == "timestamp":
            timestamp = word
        elif category == "hashtags":
            hashtags.add(word)
        elif category == "userid":
            user_id = word
        else:
            urls.add(word)

print("done")