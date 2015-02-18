## Creating your tweetbot in a jiffy

You can create your twitter account with a disposable email address.
This one seems to work: http://www.throwawaymail.com/
This one is good too: http://temp-mail.org/

#### Interacting with Twitter

Twitter provides an API, which is a way of accessing the functionalities of a web application programmatically. In order to use the API you need an API key, which is a way of telling the Twitter API that your bot is a third-party that wants access to a particular twitter account without having to give that third party the username and password of the twitter account:

You can create a new key here:
https://apps.twitter.com/

When generating the key make sure your app has the right permissions "Read, Write access individual posts".

Example tuitorial:
  - http://emerging.commons.gc.cuny.edu/2013/10/making-twitter-bot-python-tutorial/
  - http://inventwithpython.com/blog/2012/03/25/how-to-code-a-twitter-bot-in-python-on-dreamhost/

#### The code
To write our tweetbot we will be using the python programming language. This is already installed in your macbook. We need a python library called tweetpy that will be our programming interface to twitter. You can get the library (https://github.com/tweepy/tweepy)[here] and the (http://tweepy.readthedocs.org/en/v3.2.0/)[documentation is here].
