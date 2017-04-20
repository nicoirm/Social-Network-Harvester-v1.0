import threading
import queue
from datetime import datetime, timedelta
from django.utils.timezone import utc
from Twitter.models import TWUser, follower, favorite_tweet, Tweet, get_from_any_or_create
import psutil
import time
from SocialNetworkHarvester_v1p0.settings import facebookLogger
#from memory_profiler import profile

from SocialNetworkHarvester_v1p0.settings import facebookLogger, DEBUG, LOG_DIRECTORY
def log(*args, **kwargs):
    facebookLogger.log(*args, **kwargs)
pretty = lambda s : facebookLogger.pretty(s)
logerror = lambda s: facebookLogger.exception(s)

process = psutil.Process()

QUEUEMAXSIZE = 10000

threadsExitFlag = [False]

updateQueue = queue.Queue(maxsize=QUEUEMAXSIZE)    #stores twUsers
updateQueue._name = 'updateQueue'
friendsUpdateQueue = queue.Queue(maxsize=QUEUEMAXSIZE)          #stores twUsers
friendsUpdateQueue._name = 'friendsUpdateQueue'
followersUpdateQueue = queue.Queue(maxsize=QUEUEMAXSIZE)        #stores twUsers
followersUpdateQueue._name = 'followersUpdateQueue'
favoriteTweetUpdateQueue = queue.Queue(maxsize=QUEUEMAXSIZE)    #stores twUsers
favoriteTweetUpdateQueue._name = 'favoriteTweetUpdateQueue'
userHarvestQueue = queue.Queue(maxsize=QUEUEMAXSIZE)            #stores twUsers
userHarvestQueue._name = 'userHarvestQueue'

hashtagHarvestQueue = queue.Queue(maxsize=QUEUEMAXSIZE)         #stores twHashtagHarvesters
hashtagHarvestQueue._name = 'hashtagHarvestQueue'

tweetUpdateQueue = queue.Queue(maxsize=QUEUEMAXSIZE)            #stores twTweets
tweetUpdateQueue._name = 'tweetUpdateQueue'
twRetweetUpdateQueue = queue.Queue(maxsize=QUEUEMAXSIZE)        #stores twTweets
twRetweetUpdateQueue._name = 'twRetweetUpdateQueue'

clientQueue = queue.Queue()                 #stores client objects
exceptionQueue = queue.Queue()              #stores exceptions

allQueues = [updateQueue,friendsUpdateQueue,followersUpdateQueue,
             favoriteTweetUpdateQueue,userHarvestQueue,hashtagHarvestQueue,
             tweetUpdateQueue,twRetweetUpdateQueue]

def today():
    return datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0,tzinfo=utc)

def xDaysAgo(x=0):
    return today() - timedelta(days=x)


startTime = time.time()

def elapsedSeconds():
    return int(time.time() - startTime)