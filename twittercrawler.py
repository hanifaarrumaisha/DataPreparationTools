import pandas as pd
import tweepy
import csv
from db_connect import Database

## Connect to db
db = Database().connect()
cur = db.cursor()

## API Token
consumer_key = 'oPFVEYNuioxpnBhj5oISbZMBT'
consumer_secret = 'gj5rdjAHZ2Rv97F3WOKwTUr0Ihi3gGUwlQR7y7O07mrlGNERHJ'
access_token = '72770652-9uCzg4BnJ1X2ZIMls2GgQiGhB3iLed85wpPz74qN2'
access_token_secret = 'jPIegQ7csXIQXRk1BAc4RmMunMfXFo61jmEAUBnqQD9eL'

## auth API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# # Open/Create a file to append data
# csvFile = open('baru.txt', 'a')

# #Use csv Writer
# csvWriter = csv.writer(csvFile)
# csvWriter.writerow(['tweet_id','created_at', 'screen_name', 'name', 'followers_count', 'friends_count', 'retweet_count', 'favorite_count', 'conversation'])
# csvFile.flush()

## example execute DB
# cur.execute("SELECT * FROM db_preparation_tools.KEYWORDS;")
# print(cur.fetchall())
count=0
for tweet in tweepy.Cursor(api.search, q= '\"netizen\" OR \"kygo\"', since='2018-04-01').items():
	cur.execute("USE db_preparation_tools;")

	print([tweet.id_str, tweet.author.screen_name.encode('utf-8'), tweet.author.name.encode('utf-8'), tweet.user.id_str, tweet.created_at, tweet.text.encode('utf-8'), tweet.author.followers_count, tweet.author.friends_count, tweet._json['retweet_count'], tweet._json['favorite_count']])

	query = ("SELECT * FROM ACCOUNTS WHERE acc_id=%s")
	cur.execute(query % (tweet.user.id_str,))
	if not(cur.fetchall()):
		query = ("INSERT INTO ACCOUNTS (screen_name, acc_id, followers_count, following_count, name) VALUES (%s, %s, %s, %s, %s)")
		param = (tweet.author.screen_name.encode('utf-8'), tweet.user.id_str, tweet.author.followers_count, tweet.author.friends_count, tweet.author.name.encode('utf-8'))
		cur.execute(query, param)
		db.commit()
	else:	
		print("Account sudah ada")

	query = ("SELECT * FROM TWEETS WHERE tweet_id=%s")
	cur.execute(query % (tweet.id_str,) )
	print(tweet.id_str)
	data = cur.fetchone()
	print("data: ", data)
	if not(data):
		query = ("INSERT INTO TWEETS (created_at, conversation, retweet_count, favorite_count, tweet_id, acc_id) VALUES (%s, %s, %s, %s, %s, %s)")
		print(tweet.id)
		param = (tweet.created_at, tweet.text.encode('utf-8'), tweet._json['retweet_count'], tweet._json['favorite_count'], tweet.id, tweet.user.id_str)
		cur.execute(query, param)
		db.commit()
		query = ("SELECT * FROM TWEETS WHERE tweet_id=%s")
		cur.execute(query % (tweet.id,))
		print (cur.fetchall())
	else:
		print("Tweet sudah ada")
#     print (tweet.text.encode('utf-8'))
	count+=1