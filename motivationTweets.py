import tweepy
import time
import random

print("Booting")

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

#API commands
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    # DEV NOTE: use 1247996016105861120 for testing
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        #the commands
        if '#hello' in mention.full_text.lower():
            print('found #hello')
            print('responding back')
            api.update_status('Hello! ' + '@' + mention.user.screen_name, mention.id)

        if '#motivation' in mention.full_text.lower():
            print('found #motivation')
            print('responding back')
            api.update_status('@' + mention.user.screen_name + ' ' + randomQuotesGenerator(), mention.id)

        if '#communityquote' in mention.full_text.lower():
            print('found #communityquote')
            print('responding back')
            api.update_status('@' + mention.user.screen_name + ' ' + randomCQuotesGenerator(), mention.id)

        if '#addquote' in mention.full_text.lower():
            print('found #addquote')
            print('responding back')
            api.update_status('@' + mention.user.screen_name + ' Thanks for the quote!', mention.id)

            currentTweet = mention.full_text
            newQuote = currentTweet[24:]
            addCommunityQuote(newQuote)


#generates random quotes
def randomQuotesGenerator():
    q = open('quotes.txt', 'r')

    q_contents = q.readlines()
    #print(q_contents)
    
    arr = []
    for i in range(0, len(q_contents) - 1):
        x = q_contents[i]
        z = len(x)
        a = x[:z - 1]
        arr.append(a)

    arr.append(q_contents[i+1])
    o = random.choice(arr)
    print(o)

    q.close
    return o
    

#add quotes to list
def addQuote():
    with open('quotes.txt', 'a') as q:
        b = True
        while b == True:
            inp = input('add a quote, if not type "no"\n')
            if inp != 'no':
                q.write(inp + '\n')
            else:
                b = False

def randomCQuotesGenerator():
    q = open('communityQuotes.txt', 'r')

    q_contents = q.readlines()
    #print(q_contents)
    
    arr = []
    for i in range(0, len(q_contents) - 1):
        x = q_contents[i]
        z = len(x)
        a = x[:z - 1]
        arr.append(a)

    arr.append(q_contents[i+1])
    o = random.choice(arr)
    print(o)

    q.close
    return o

#community add quote
def addCommunityQuote(newQuote):
    with open('communityQuotes.txt', 'a') as q:
        q.write(newQuote)

def newFollowers():
    followers = tweepy.Cursor(api.followers).items(1)

    #grabs the last user
    for follower in followers:
        #print(follower.screen_name)
        lastUser = follower.id

        if lastUser != retrieve_last_follower():
            store_last_follower(lastUser)
            return True

    return False

def retrieve_last_follower():
    f = open('follower_id.txt', 'r')
    last_follower = int(f.read().strip())
    f.close()
    return last_follower

def store_last_follower(newFollower):
    f = open('follower_id.txt', 'w')
    f.write(str(newFollower))
    f.close()
    return

def dmInfo():
    if newFollowers() == True:
        print('New Follower!')
        api.send_direct_message(retrieve_last_follower(), 'Thank you for following the Motivational Bot, here are a list of commands:'
                                + '\n#motivation : for a motivational quote'
                                + '\n#addquote : to add a quote to the community'
                                + '\n#communityquote : for a quote from the community'
                                + '\n#hello : for a simple hello!')

#runs all the code ------------------------------------
addQuote()

while True:
    print('Looking for tweets')
    reply_to_tweets()
    print('Looking for new followers')
    dmInfo()

    time.sleep(60)