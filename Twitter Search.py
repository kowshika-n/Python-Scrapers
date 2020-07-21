#!python3
# -*- coding: utf-8 -*-
import re
import sys
import time
import html
import subprocess
from twython import Twython
from twython import TwythonError

_version = '0.2'
_author = 'Kowshika https://kowshika-n.github.io'

# Get from twitter dev.
APP_KEY = 'APP_KEY'
APP_KEY_SECRET = 'APP_KEY_SECRET' 
ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

# compat for 140 char tweets, extended for 280 chars
TWEET_MODE = 'extended'
RESULT_TYPE = 'popular'
# can also be recent or mixed
MAX_TWEET_COUNT_PER_SEARCH = 10
# limiting for testing - rate limitied to 450 requests/15 mins


def catch(error):
    '''Method to catch errors and display error line'''
    exc_type, exc_obj, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno)
    print('%s : %s at Line %s.' % (type(error), error, lineNo))


def getHashTags(tweet):
    hashtags = list()
    try:
        hashtagCount = len(tweet['entities']['hashtags'])
        if hashtagCount > 0:
            for i in range(hashtagCount):
                tag = tweet['entities']['hashtags'][i]['text']
                tag = cleanString(tag)
                if tag and len(tag) > 1:
                    hashtags.append(tag)

    except Exception as e:
        catch(e)
    # make unique list of hashtags
    Set = set(hashtags)
    return [ x for x in iter(Set)]


def getURLs(tweet):
    urlList = list()
    try:
        urlCount = len(tweet['entities']['urls'])
        if urlCount > 0:
            for i in range(urlCount):
                url = tweet['entities']['urls'][i]['url']
                if url and len(url) > 1:
                    urlList.append(url)

    except Exception as e:
        catch(e)
    return urlList


def getTag(tweet, mapKey):
    '''get any element from top level of tweet json'''
    value = None
    try:
        value = tweet[mapKey]
    except Exception as e:
        catch(e)
    return value


def getTweets(tweet, TWEET_MODE):
    '''get tweet string based on tweet extraction mode'''
    tweetString = ''
    try:
        # get tweet text from json 
        if TWEET_MODE == 'compact':
            tweetString = (tweet['text'].encode('utf-8').decode("utf-8"))
        else:
            tweetString = (tweet['full_text'].encode('utf-8').decode("utf-8"))
    except Exception as e:
        catch(e)

    if tweetString and len(tweetString) > 1:
        tweetString = cleanString(tweetString)
    return tweetString


def cleanString(text):
    '''clean a string of bytecodes and non english chars and unnecessary spaces'''
    copyTxt = text
    try:
        # convert and decode bytes string and remove non english text
        copyTxt = copyTxt.encode('ascii', errors='ignore').decode('utf-8')
        if copyTxt and len(copyTxt) > 1:
            # remove HTML entities and convert to normal string
            copyTxt = html.unescape(copyTxt)
            # remove twitter URLs from tweet
            copyTxt = re.sub(r"http(?:s)?:\/\/(?:www\.)?(twitter\.com)?(t\.co)?\/([a-zA-Z0-9_]+)", " ", copyTxt)
            # remove newlines and tabs
            copyTxt = re.sub(r"[\n\t]", " ", copyTxt)
            copyTxt = re.sub(r"\s\s+", " ", copyTxt)
            #  remove whitespaces from front and end
            copyTxt = copyTxt.strip()
    except Exception as e:
        catch(e)
        copyTxt = text
    return copyTxt


def SearchTwitter(searchTerms):
    try:
        # Initiate a twitter connection
        twitter = Twython(app_key=APP_KEY, 
                    app_secret=APP_KEY_SECRET, 
                    oauth_token=ACCESS_TOKEN, 
                    oauth_token_secret=ACCESS_TOKEN_SECRET,
                    client_args = { "headers": { "accept-charset": "utf-8" } } )

        if not twitter:
            print(f'ERROR: No Twitter Connection found.')
        else:
            for query in searchTerms:
                search_results = twitter.search(q=query,
                                                count=MAX_TWEET_COUNT_PER_SEARCH,
                                                tweet_mode=TWEET_MODE, result_type=RESULT_TYPE)
                if not search_results:
                    print(f'No search results found for : {query}')
                else:
                    print("\n")
                    # print(search_results)
                    results = search_results['statuses']
                    if len(results) <= 0:
                        print(f'No search results found for : {query}')
                    else:
                        print(f"TWEETS ABOUT {query} :  {len(results)}")
                        for tweet in results:
                            #print(tweet)
                            tweetString = getTweets(tweet, TWEET_MODE)
                            hashtags = getHashTags(tweet)
                            favorite_count = getTag(tweet, 'favorite_count')
                            retweet_count = getTag(tweet, 'retweet_count')
                            created_at = getTag(tweet, 'created_at')
                            tweet_id = getTag(tweet, 'id_str')
                            urls_in_tweet = getURLs(tweet)
                            user_ID = getTag(tweet['user'], 'screen_name')
                            user_Name = cleanString(getTag(tweet['user'], 'name'))
                            print(f'{tweetString}\ntweet_id = {tweet_id}, favorite_count = {favorite_count}, retweet_count = {retweet_count}, '
                                  f'created = {created_at}, By = @{user_ID}/{user_Name}, hashtags = {hashtags}, URLs = {urls_in_tweet}\n')
                
    except Exception as e:
        catch(e)


def main():
    if len(sys.argv) <= 1:
        print('No search terms found. Usage with cmd/powershell : Python TwitterSearch.py "search #Term"')
    else:
        print("Search Terms Found : %s " % sys.argv[1:])
        SearchTwitter(sys.argv[1:])
    time.sleep(2)


def test():
    sys.argv.append('testing')
    main()


if __name__ == "__main__":
    main()
