#!/usr/bin/env python
# encoding: utf-8
""" 
twitter.py

Get recent public tweets, parse them to add links, save to file for SSI import
"""
import twitter
import re
from datetime import datetime
from urllib2 import URLError
import logging

pattern = re.compile(r'''\b((?:(?:http)://|www\.)[-a-zA-Z0-9+&@#/%=~_|$?!:,.]*[a-zA-Z0-9+&@#/%=~_|$])''')
replacement = '<a href="\\1">\\1</a>'
httpreplacement = '<a href="http://\\1">\\1</a>'
twitter_user = re.compile(r'@([A-Za-z0-9_]+)')
user_replace = '<a href="http://twitter.com/\\1">@\\1</a>'
tw_hash = re.compile(r'#([0-9]*[A-Za-z_]+[0-9]*)')
hash_replace = '<a href="http://twitter.com/search?q=%23\\1">#\\1</a>'

def get_tweets(user):
    api = twitter.Api()
    try:
        tweets = api.GetUserTimeline(user)
        return tweets
    except URLError, e:
        log.exception("URLError rasised while getting user timeline: %s " % e )

def format_tweets(tweets):
    for t in tweets:
        t.date = datetime.strptime( t.created_at, "%a %b %d %H:%M:%S +0000 %Y" )
        t.date = t.date.strftime("%b %d")
        if re.search(pattern, t.text) and re.search(pattern, t.text).expand('\\1').startswith('www'):
            t.text = re.sub(pattern, httpreplacement, t.text)
        else:
            t.text = re.sub(pattern, replacement, t.text)

        if re.search(twitter_user, t.text):
            t.text = re.sub(twitter_user, user_replace, t.text)

        if re.search(tw_hash, t.text):
            t.text = re.sub(tw_hash, hash_replace, t.text)
    return tweets

def print_tweets(tweets):
    with open('tweets.html', 'w') as f:
        for t in edited_tweets:
            f.write( "<p>%s</p><p class='small tweetdate'>%s</p>" % (t.text, t.date) )


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.WARNING, filename="get_tweets.log")
    log = logging.getLogger('twitter')

    tweets = get_tweets('theopenbastion')
    edited_tweets = format_tweets(tweets[:3])
    print_tweets(edited_tweets)
