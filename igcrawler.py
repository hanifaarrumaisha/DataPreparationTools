""" 
Created by Hanifa Arrumaisha
Eeference: http://edmundmartin.com/scraping-instagram-with-python/
Copyright: 2018
"""

from random import choice, randint
import time
import json
import datetime
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv
from db_connect import Database

## Connect to db
db = Database()
cur = db.cursor()

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def explore_tags(self, keywords):
        with open('igcrawl.csv','a') as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(['keyword','username', 'owner_ID', 'following_count', 'follower_count', 'caption', 'post_ID', 'shortcode', 'comment', 'timestamp', 'likes', 'preview_likes', 'is_video', 'video_view', 'display_url'])
            file.close()

        for keyword in keywords:
            self.explore_tag(keyword)

    ##call request for explore_tags   
    def request_explore_tag(self, keyword, end_cursor):
        response = self.__request_url('https://www.instagram.com/explore/tags/'+keyword+'?__a=1&max_id='+end_cursor)
        json_data = json.loads(response)
        requests.session().close()
        with open('explore_tag_'+keyword+'.txt','w') as file:
            file.write(json.dumps(json_data))
            
        root = json_data['graphql']['hashtag']
        return root

    def explore_tag(self, keyword): 
        try:
            page=1
            root=self.request_explore_tag(keyword, str(page))

            ##loop until hasn't next page
            while (root['edge_hashtag_to_media']['page_info']['has_next_page']):
                count=1

                ## open every post in result search
                for edge in root['edge_hashtag_to_media']['edges']:
                    shortcode=edge['node']['shortcode']
                    thumbnail_resources = edge['node']['thumbnail_resources']
                    end_cursor=root['edge_hashtag_to_media']['page_info']['end_cursor']
                    
                    print("page: "+str(page)+" count: "+str(count))
                    
                    self.open_post(shortcode, keyword)
                    
                    count+=1
                
                page=page+1

                ## open next page of search tags
                root=self.request_explore_tag(keyword, end_cursor)
            print("---------"+keyword.upper()+" FINISH-----------")

        except Exception as e:
            raise e

    def timestamp_to_date(self, timestamp):
        ts = datetime.datetime.fromtimestamp(timestamp)
        return ts.strftime("%d/%m/%Y %I:%M %p")
    
    def open_post(self, shortcode, keyword):
        try:
            response = self.__request_url('https://www.instagram.com/p/'+shortcode+'/')
            json_data= self.extract_json_data(response)

            root = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
            username = root['owner']['username'].encode('utf8')
            user = self.profile_page_metrics(username.decode('utf8'))
            following_count = user['edge_follow']['count']
            follower_count = user['edge_followed_by']['count']
            caption = root['edge_media_to_caption']['edges'][0]['node']['text'].encode('utf8')
            post_ID = root['id']
            shortcode = root['shortcode']
            comment = root['edge_media_to_comment']['count']
            timestamp = self.timestamp_to_date(root['taken_at_timestamp'])
            likes = root['edge_media_preview_like']['count']
            preview_likes = root['edge_media_preview_like']['count']
            owner_ID = root['owner']['id']
            is_video = root['is_video']
            if (is_video):
                video_view = root['video_view_count']
            else:
                video_view = 0
            display_url = root['display_url']

            # pprint(caption)
            # pprint(post_ID)
            # pprint(shortcode)
            # pprint(comment)
            # pprint(timestamp)
            # pprint(likes)
            # pprint(preview_likes)
            # pprint(owner_ID)
            # pprint(is_video)
            # pprint(video_view)
            # pprint(display_url)

            ## save data in igcrawl.csv
            with open('igcrawl.csv','a') as file:
                csvWriter = csv.writer(file)
                csvWriter.writerow([keyword, username, owner_ID, following_count, follower_count, caption, post_ID, shortcode, comment, timestamp, likes, preview_likes, is_video, video_view, display_url])
        
        except Exception as e:
            raise e

    def profile_page_metrics(self, username):
        results = {}
        try:
            # tm = [1,2,4,8,16,32]
            # time.sleep(choice(tm))
            response = self.__request_url("https://www.instagram.com/"+username+'/')
            json_data = self.extract_json_data(response)
            root = json_data['entry_data']['ProfilePage'][0]['graphql']['user']

            with open('profile_page.txt','w') as file:
                file.write(json.dumps(json_data))
            return root
        except Exception as e:
            raise e

# Example execute explore_tags with keyword netizen
k = InstagramScraper()
results = k.explore_tags(['netizen','internship','magang'])
