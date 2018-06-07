from twython import Twython, TwythonError
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
import random, time, string, os, pronouncing

def setup():
    with open('keys.txt', 'r') as keys:
        API_KEY = keys.readline().strip()
        API_SECRET = keys.readline().strip()
        ACCESS_TOKEN = keys.readline().strip()
        ACCESS_TOKEN_SECRET = keys.readline().strip()

    twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return twitter

def countSyllables(word):
    phones = pronouncing.phones_for_word(word)
    return pronouncing.syllable_count(phones[0])

def isStopWord(word):
    sw = set(stopwords.words('english'))
    if word in sw: return True
    else: return False

def getRandomSong():
    songs = os.listdir('songs')
    rand = random.randint(0, len(songs)-1)
    return songs[rand]

def getRandomLyric():
    with open('songs/' + getRandomSong(), 'r') as songfile:
        lyrics = songfile.readlines()

    rand = random.randint(0, len(lyrics)-1)
    return lyrics[rand].lower()

def remix(lyric):
    t = TweetTokenizer()
    d = TreebankWordDetokenizer()

    words = t.tokenize(lyric)
    r1 = random.randint(0, len(words)-1)
    # filter out punctuation, stop words, and words with no rhymes
    while words[r1] in string.punctuation or isStopWord(words[r1]) or len(pronouncing.rhymes(words[r1])) == 0:
        if len(words) == 1: return lyric
        r1 = random.randint(0, len(words)-1)

    # this is the word to be replaced
    word = words[r1]
    syl = countSyllables(word)

    # find rhymes with same number of syllables
    rhymes = pronouncing.rhymes(word)
    r2 = random.randint(0, len(rhymes)-1)
    count = 1
    while (count <= len(rhymes) and syl != countSyllables(rhymes[r2])) or isStopWord(rhymes[r2]):
        r2 = random.randint(0, len(rhymes)-1)
        count += 1
    words[r1] = rhymes[r2]

    return d.detokenize(words)

def tweet(twitter):
    lyric = getRandomLyric()
    twitter.update_status(status = remix(lyric))

while True:
    rand = random.randint(3600, 21600) # wait between 1 hour and 6 hours
    time.sleep(rand)
    twitter = setup()
    tweet(twitter)
