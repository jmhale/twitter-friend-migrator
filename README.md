# Twitter Friend Migrator

## Purpose
This will grab a list of accounts that an account is following ("friends", in Twitter vernacular), compare with who you are currently following, and offer to follow anyone that you currently aren't.

This can be useful if you're trying to consolidate Twitter accounts, and want to bulk-follow everyone from the account that you're deprecating.

## Getting Started
Before running this, you will need to sign up for a Twitter Developer account, and create an app. This will give you two API keypairs (consumer and app), both of which are required for this project to run.

https://developer.twitter.com/

### Sample config
```
[default]
verbose = True
dry_run = False

consumer_key = aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
consumer_secret = bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
access_token = cccccc-dddddddddddddddddddddddddddddddddddddddd
access_token_secret = eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

source_account = account_to_copy_from
```

### Usage
```
pip install -r requirements.txt
python twitter-friend-migrator.py
```

## Rate limits
Twitter has very strict rate limits to prevent abuse. If you have a large number of friends that you're trying to migrate over, you'll likely need to run this several times to get everyone.

https://help.twitter.com/en/using-twitter/twitter-follow-limit