The goal of this project was to add the ability to identify key words in Scalica posts and make it possible for a user to subscribe to a particlar hashtag, which will enable them to view these posts.

Please register a new Scalica account and follow a couple users to see their posts, as well as making a few posts of your own, in order to properly test this service.

When loading up Scalica, you will see a Topic Feed, a Search Bar, and a Trending Hashtags area in addition to what is normally there.

When a user goes to the homepage, we run a MapReduce job and update the currently trending hashtags, which are the 5 most popular hashtags.

When a post is made, a keyword is generated from it and inserted into our database. We used the RAKE algorithm instead of IBM Watson, as Watson's installable packages are not compatible with Python 2.7.

If you enter in a keyword in the search bar, if such a keyword exists, it will display it in the results page after you press Enter. If such a keyword does not exist, it will inform you of this.
Try searching any of the trending hashtags to test this feature!
To see posts related to a particular keyword appear in your Topic Feed, you must first subscribe to one. In order to subscribe, head to /micro/subscribe.
Here you will be greeted with a text field. Enter in the exact, full name of a topic that interests you and click the subscribe button.
If you head back to the homepage, you should see posts related to that topic in your Topic Feed, as well as the name of the user who posted them. 

If you encounter a URL error, please go back to /micro and repeat your action again.
