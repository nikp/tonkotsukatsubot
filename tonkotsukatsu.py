import praw
import threading
import time
import unicodedata
from threading import Thread

USER_AGENT='TonkotsuKatsuBot v0.1'
REDDIT_CLIENT_ID='<YOUR-CLIENT-ID>'
REDDIT_CLIENT_SECRET='<YOUR-CLIENT-SECRET>'
REDDIT_USERNAME='<YOUR-USER-NAME>',
REDDIT_PASSWORD='<YOUR-PASSWORD>'

OTHER_KATSU_FIGHTERS = set(['Kvaezde'], ['tonkotsukatsubot'], ['tonkotsutonkatsubot']) #other tonkotsu/katsu /r/ramen fighters

def main():
	bot = praw.Reddit(user_agent=USER_AGENT,
					client_id=REDDIT_CLIENT_ID,
					client_secret=REDDIT_CLIENT_SECRET,
					username=REDDIT_USERNAME,
					password=REDDIT_PASSWORD)
	
	ramen = bot.subreddit('ramen')
	
	if __name__ == '__main__':
	    Thread(target = monitorSubmissions, args=([ramen])).start()
	    Thread(target = monitorComments, args=([ramen])).start()

def monitorSubmissions(subreddit):
	submissions = subreddit.stream.submissions()
	for submission in submissions:
		title = submission.title.lower()
		selftext = submission.selftext.lower()
		author = submission.author.name

		if (isMe(submission) or author in OTHER_KATSU_FIGHTERS): 
			continue
		
		if ('tonkatsu' in title) or ('tonkatsu' in selftext):
		
			if (any(x for x in submission.comments if isMe(x))):
				continue
				
			print("SUBMISSION:\n")
			print(title.encode('ascii', 'ignore'))
			print("\n")
			print(selftext.encode('ascii', 'ignore'))
			print("\n")
			print(author.encode('ascii', 'ignore'))	
			
			reply(submission, author)
	
def monitorComments(subreddit):
	comments = subreddit.stream.comments()
	for comment in comments:
		text = comment.body
		author = comment.author.name
		
		if (isMe(comment) or comment.submission.author.name in OTHER_KATSU_FIGHTERS):
			continue
		
		if 'tonkatsu' in text.lower():
		
			if (any(x for x in comment.replies if isMe(x))):
				continue
		
			print("COMMENT:\n")
			print(text.encode('ascii', 'ignore'))
			print("\n")
			print(author.encode('ascii', 'ignore'))	
		
			reply(comment, author)
			
def reply(entity, author):
	message = build_message(author)
	
	retries = 0
	sleep_time = 60
	
	while retries < 5:
		try:
			entity.reply(message)
			print("___________________REPLIED!")
			break
		except praw.exceptions.PRAWException as e:
			sleep_time = e.sleep_time
			print("PRAWException: {0}, sleep_time={1}".format(e, sleep_time))	
		except praw.exceptions.APIException as e:
			print("APIException: {0}".format(e))
		except praw.exceptions.ClientException as e:
			print("ClientException: {0}".format(e))
		
		time.sleep(sleep_time)
		retries = retries + 1
		
		
def build_message(author):
	return "You should know you probably didn't have tonk**A**tsu ramen, /u/{0}. Tonkatsu is pork cutlet, a delicious japanese schnitzel, but one with no place in ramen. If you're talking about ramen, you mean tonk**O**tsu, or pork bone, which is how this creamy delicious elixir from the gods gets its depth of flavour. \n\n No hard feelings though, keep it in mind for next time! \n\n Sincerely, a friendly ramen-loving bot.".format(author)
	
def isMe(entity):
	return entity.author.name == REDDIT_USERNAME
	
if __name__ == '__main__':
    main()
