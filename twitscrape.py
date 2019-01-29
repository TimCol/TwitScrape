import json
import requests
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def init_driver():
     driver = webdriver.Chrome()
     driver.wait = WebDriverWait(driver, 5)
     return driver

def search_twitter(driver, user):
	url = "https://twitter.com/" + user
	driver.get(url)
	wait = WebDriverWait(driver, 3)
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		time.sleep(2)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
		    break
		last_height = new_height
		page_source = driver.page_source
	return driver.page_source

def get_page_tweets(soup):
	tweets = soup.find_all("li", {"data-item-type" : "tweet"})
	tweetnumber = 0
	for tweet in tweets:
		get_tweet_text(tweet, tweetnumber)
		tweetnumber += 1

def get_tweet_text(tweet, tweetnumber):
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    print "tweet number " + str(tweetnumber) + "\n\n" + tweet_text + "\n\n"


if __name__ == "__main__":
	minnie = init_driver()
	soup = BeautifulSoup(search_twitter(minnie, "hackthebox_eu"))
	get_page_tweets(soup)
	minnie.close()


