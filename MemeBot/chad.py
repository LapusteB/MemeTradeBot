import tweepy
import os
import codecs
from collections import Counter
from dotenv import load_dotenv
import sys

# Set UTF-8 encoding for standard output
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

load_dotenv()

# # Twitter API credentials
TWITTER_API_KEY = os.getenv("API_KEY")
TWITTER_API_SECRET = os.getenv("API_KEY_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


# Twitter List ID
TWITTER_LIST_ID = "1654276583606177793"

# Initialize Twitter client
client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def get_twitter_data(list_id):
    """Fetch tweets from a Twitter List."""
    print("Fetching tweets...")
    response = client.get_list_tweets(
        id=list_id, max_results=100, tweet_fields=["public_metrics", "created_at"]
    )
    tweet_count = 0
    if not response.data:
        return []
    if response.data:
        tweet_count += len(response.data)
    print("Tweet count: ", tweet_count)

    return [
        {
            "text": tweet.text,
            "retweets": tweet.public_metrics["retweet_count"],
            "likes": tweet.public_metrics["like_count"],
            "date": tweet.created_at,
        }
        for tweet in response.data
    ]

def analyze_meme_trends(tweets):
    """Analyze trends from tweets: popular tweets and common words."""
    print("Analyzing trends...")
    # Get top 10 most engaging tweets
    popular_tweets = sorted(
        tweets, key=lambda x: x["retweets"] + x["likes"], reverse=True
    )[:10]
    # Extract most common words
    all_words = " ".join([tweet["text"] for tweet in tweets]).split()
    common_words = Counter(all_words).most_common(10)
    return popular_tweets, common_words

def display_results(popular_tweets, common_words):
    """Display the analysis results."""
    print("\nTop 10 Popular Tweets:")
    for tweet in popular_tweets:
        print(
            f"- {tweet['text'].encode('utf-8', errors='ignore').decode('utf-8')} "
            f"(Retweets: {tweet['retweets']}, Likes: {tweet['likes']})"
        )

    print("\nTop 10 Common Words in Tweets:")
    for word, count in common_words:
        print(f"- {word}: {count} times")

    

def main():
    # Step 1: Fetch Twitter data
    tweets = get_twitter_data(TWITTER_LIST_ID)
    if not tweets:
        print("No tweets found.")
        return

    # Step 2: Analyze trends
    popular_tweets, common_words = analyze_meme_trends(tweets)

    # Step 3: Display results
    display_results(popular_tweets, common_words)

if __name__ == "__main__":
    main()
