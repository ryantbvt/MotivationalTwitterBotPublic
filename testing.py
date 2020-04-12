import tweepy
import time

print("Booting")

CONSUMER_KEY = 'yXM2wbNnSzYjDWmyjgSJx72I2'
CONSUMER_SECRET = 'vIU6koLTE1vUe4X4PycNYHONg4kViO02IgF3DU5P3cDvMrLW76'
ACCESS_KEY = '1247728862340972544-XXBsavSHzZPItSOTyNOUEmyhmy8ZSN'
ACCESS_SECRET = 'ZaURSeuvtT3t10K2F0pM8K8WNjHVwuuuAMomcBM80OZll'

#API commands
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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
        api.send_direct_message(retrieve_last_follower(), 'Thank you for following the Motivational Bot, here are a list of commands:'
                                + '\n#motivation : for a motivational quote'
                                + '\n#addquote : to add a quote to the community'
                                + '\n#communityquote : for a quote from the community'
                                + '\n#hello : for a simple hello!')

dmInfo()

while True:
    print('looking for new followers')
    time.sleep(60)