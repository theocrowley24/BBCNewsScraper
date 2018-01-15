"""
Scrapes multiple news websites inserting the data into a database
"""
from urllib.request import urlopen
import time
import MySQLdb
from bs4 import BeautifulSoup

"""
Database function, this connects to the database, instances a cursor and executes queries
"""
def Database(storyTitle, link, website):

    try:
        db = MySQLdb.connect("localhost", "username", "password", "dbname", use_unicode=True, charset="utf8")
        cursor = db.cursor()
        unix = int(time.time())
        cursor.execute("INSERT INTO news(news_id, news_title, news_url, news_unix, news_source) VALUES (%s,%s,%s,%s, %s) """,
        (0, storyTitle, link, unix, website))
        db.commit()
    except:
        print("Cannot connect to databse!")

"""
BBCNews function, scrapes latest-stories from the BBC News website
"""
def BBCNews():
    #URL for the page to download
    bbcNews = 'http://www.bbc.co.uk/news'

    #Opens page
    try:
        page = urlopen(bbcNews)

        soup = BeautifulSoup(page, 'lxml')

        #Finds all stories by searching with the class
        latestStories = soup.find_all('a', 
        class_="gs-c-promo-heading nw-o-link-split__anchor gs-o-faux-block-link__overlay-link gel-pica-bold")

        website = "BBC News"

        #Iterates through all the stories taking out the url and the story title
        for story in latestStories:
            link = 'http://bbc.co.uk'  + story['href']
            storyTitle = story.h3.get_text()
            print(storyTitle + " - " + link)
            Database(storyTitle, link, website)
        pass
    except:
        print("Cannot connect to website!")

    
"""
SkyNews function, scrapes latest-stories from the Sky News website
"""
def SkyNews():
    #URL for the page to download
    skyNews = 'http://news.sky.com'

    #Opens page
    try:
        page = urlopen(skyNews)
        soup = BeautifulSoup(page, 'xml')

        latestStories = soup.find_all('a', class_="sdc-news-story-grid__link")

        website = "Sky News"

        for story in latestStories:
            link = 'http://news.sky.com' + story['href']
            storyTitle = story.get_text()
            if (not storyTitle.isspace() and 'Video' not in storyTitle and not link.isspace() 
            and len(storyTitle.replace(" ", "")) > 25 and 'Sky News Analysis  Comment' not in storyTitle):
                print(storyTitle + " - " + link)
                Database(storyTitle, link, website)
        pass
    except:
        print("Cannot connect to website")

SkyNews()
BBCNews()


