import sys
import configparser
import twitter

class TwitterMigrator():
    """
    Class containing the methods needed to migrate
    Twitter friends from one account to another
    """
    
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, dry_run=True, verbose=False):
        # Create an Api instance.
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)

        self.dry_run = dry_run
        self.verbose = verbose

    def get_current_user(self):
        """
        Returns the name of the authenticated user
        """
        current_user = self.api.VerifyCredentials()
        return current_user.screen_name

    def get_users(self, screen_name=None):
        """ 
        Returns a list of user names that the account follows (friends) 
        """
        try:
            friends_objs = self.api.GetFriends(screen_name=screen_name)
        except twitter.error.TwitterError as ex:
            for error_message in ex.message:
                if error_message['code'] == 88:
                    print("We've hit the get_users rate limit for now. Please try again later.")
                    sys.exit(1)
                else:
                    raise
        friends_names = []

        for user in friends_objs:  
            friends_names.append(user.screen_name)

        return friends_names

    def get_new_friends(self, source_account):
        """ 
        Returns a list of user names that the source account 
        follows, but the destination account doesn't 
        """

        src_users = self.get_users(source_account)
        dst_users = self.get_users()

        new_friends = list(set(src_users) - set(dst_users))

        return new_friends

    def follow_users(self, users_to_follow=None):
        """
        Takes a list of user names and follows them
        """

        current_user = self.get_current_user()
        if self.verbose:
            print("List of new users to follow:")
            for friend in users_to_follow:
                print(friend)


        print("You are about to follow {} users, do you want to continue?".format(len(users_to_follow)))
        answer = input("Enter yes or no: ")
        if answer == "yes":
            if self.dry_run:
                print("Dry run is selected. Will not add any friends.")
            else:
                if len(users_to_follow) > 400:
                    print("The number of users to follow: {}, is greater than what the Twitter API will allow in a 24-hour period (400). You will have to run this multiple times to complete the migration".format(len(users_to_follow)))
                for user in users_to_follow:
                    if user != current_user:
                        if self.verbose:
                            print("Attempting to follow {}".format(user))
                        try:
                            res = self.api.CreateFriendship(screen_name=user, follow=False, retweets=False) 
                            if self.verbose:
                                print("Sucessfully followed: {}".format(res.screen_name))
                        except twitter.error.TwitterError as ex:
                            for error_message in ex.message:
                                if error_message['code'] == 160:
                                    print("We've already requested to follow {}, skipping.".format(user))
                                elif error_message['code'] == 161:
                                    print("We've hit the follow rate limit for now. Try again later. Exiting.")
                                    sys.exit(1)
                                else:
                                    raise
        else:
            print("Not following users.")
def main():
    """
    Main function
    """

    config = configparser.ConfigParser()
    config.read("./twitter-friend-migrator.conf")

    verbose = config.getboolean('default', 'verbose')
    dry_run = config.getboolean('default', 'dry_run')
    consumer_key = config.get('default', 'consumer_key')
    consumer_secret = config.get('default', 'consumer_secret')
    access_token = config.get('default', 'access_token')
    access_token_secret = config.get('default', 'access_token_secret')
    source_account = config.get('default', 'source_account')

    migrator = TwitterMigrator(
        consumer_key=consumer_key, 
        consumer_secret=consumer_secret, 
        access_token_key=access_token, 
        access_token_secret=access_token_secret,
        dry_run=dry_run,
        verbose=verbose)

    new_friends = migrator.get_new_friends(source_account=source_account)
    if new_friends:
        print("The account {} is following {} Twitter accounts that you are not.".format(source_account, len(new_friends)))
        migrator.follow_users(new_friends)
    else:
        print("The account {} is not following anyone that you're not already following. Nothing to do.".format(source_account))

if __name__ == "__main__":
    main()
