# Mapping Relevant Fire Tweets in Southern California

#### Authors
Sophia Alice: [Linkedin](https://www.linkedin.com/in/sophia-alice/)           
Dae Han: [Linkedin](https://www.linkedin.com/in/daehuihan/)             
Sonam Thakkar: [Linkedin](https://www.linkedin.com/in/sonamthakkar5/)


## Problem Statement

We used tweets scraped from Twitter in order to create a classification model that filters out tweets in an area that are related to a fire. This model can then be applied to tweets containing geographic information so that a user could visit a website, type in their location, and see if anyone in their area is reporting a fire and, if so, can read tweets that contain vital information about the location of the fire, evacuation routes, and any news updates.

## Scraping from Twitter

In order to obtain tweets from Twitter, we tried three different Python API wrappers for the Twitter API: Tweepy, GetOldTweets3, and Python-Twitter. We first created a developer account with Twitter to receive an API key so we could access the data. The Twitter API restricts access to only tweets from the previous 7 days and sets a rate limit so that you can only access so many tweets per hour.

#### Tweepy

We first built a Twitter scraper in Python using Tweepy using different keywords related to the then current fires in California and set the radius to capture every tweet within different radii of the city. But we quickly ran into issues with Tweepy because of the way the streaming method is structured. It created a continuous connection with Twitter and even after applying the relevant alterations, our scraper would hit the rate limit and time out before completing a scrape almost every time. In addition, out of the handufl of tweets the scrape did return none of them contained any geographic information: no latitude or longitude values, no user location information, no city names. Since Tweepy was not providing any tweets with geographic information, we abandoned this as a source of data and switched to using a different scraper.

#### GetOldTweets3

After Tweepy, we then used GetOldTweets3 to build a dataset of tweets. GetOldTweets3 does not interface with the Twitter API because it instead interfaces with a databse of tweets that have previously been scraped from Twitter. Because it is not connected to the Twitter API, there were no issues with hitting the rate limit like we had using Tweepy and we also could access tweets that were more than 7 days old. Using GetOldTweets3, we were able to create a dataset of about 21,000 tweets, but these tweets, like the ones we received from the Tweepy scrape, lacked geographic data. These tweets unfortunately could also not be mapped.

#### Python-Twitter

After the two previous wrappers we then tried the Python-Twitter wrapper. This wrapper allowed us to filter tweets by keyword and also a geographic area as small as a circle with a radius of 1 km. It unfortunately also interfaced with the Twitter API so we again faced issues with rate limiting, but we were able to complete our scrapes and return data with geographic data using this wrapper. We looked at the Getty and Maria fires and created a grid of 225 points (15 km x 15 km) centered around each fire where each point was 1 km apart to grab any tweets from around the area of the fire with geographic information. Using this wrapper we were finally able to scrape tweets with geographic information! Unfortunately, there weren't too many of them. According to Twitter, [only 1-2% of tweets contain geographic information](https://developer.twitter.com/en/docs/tutorials/tweet-geo-metadata) and our final dataset of tweets containing geographic information only had 91 tweets.

#### Data from a Past Project

In order to add more tweets with geographic information to our dataset, we looked at past projects to see if any previous groups were succesful in obtaining tweets with geographic information. Out of all the past projects, only the [project from Chris Sinatra's group](https://github.com/csinatra/Twitter-Disaster-Repo) contained any data with geographic information. We augmented our dataset of tweets containing geographic information with their data.

## Data Dictionary

| Feature       | Data type | Description                                              |  
|---------------|-----------|----------------------------------------------------------|  
| text          | string    | Texts from all the posts                                 |  
| hashtags      | string    | Hashtags from the posts                                  |  
| user_name     | string    | User name of the person who tweeted                      |  
| date          | date-time | Date and time of the tweets                              |  
| user_location | string    | Location of the user who sent the tweet                  |  
| label         | bool      | label is based on related to fire or not related to fire |  
| lat           | integer   | Latitude of the tweets                                   |  
| long          | integer   | Longitude of the tweets                                  |  
| location      | string    | Location from where the user has tweeted                 |  


## Exploratory Data Analysis and Modeling

#### Target Class Balance:

**Values in the label column:**
0 represents irrelevant tweets
1 represents relevant tweets
2 represents may be relevant or may not be relevant (ambiguous tweets)

Class 1 and 2 are about 3 to 7 ratio and the two classes are a total of 2644 rows. The size of the data is  big enough to build model. As there will be more tweets that are not related to disasters than the ones that are related to disasters, the class ratio of 3 to 7 is a good starting point.

<img src = "https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/Value_counts_label_column.png" width="500"/>

#### Metrics:

In order to classify tweets as relevant, we aimed to minimize false negatives (type II error) and worked to maximize our sensitivity score. False negative values occur when a tweet that is about a disaster is classified as being irrelevant and we did not want to miss any tweets that might matter.

#### Models

**1. Logistic Regression ( TF-IDF Vectorizer )**                             
Winds, canyon and acres are among the most important words in classifying disaster related tweets using Logistic Regression model. The disaster type of the scraped data is restrained to 'wild fire'. Considering winds are important indicator in understanding where the fire is spreading towards and how fast the fire is spreading

<img src = "https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/Logistic_regression_word_count.png" width="500"/>

With a sign of slight overfit, the accuracy score for logistic regression model was in the range of 0.83-0.88. However, sensitivity score for this model was 0.62. This shows high rate of type II error. For our aim was to minimize this error type, this model was not the best for this project.             

To improve this model, 
    - try different reguralization using L1, L2, elastic net penalty options and C value
    - additional NLP
    - try adding words that have low coefficients to stopword list

![alt text](https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/Logistic_regression_roc_auc_curve.png "logistic regression roc curve")

**2. Random Forest ( TF-IDF Vectorizer )**                             
Acres, canyon and winds are among the most important words in classifying disaster related tweets using Random Forest. The disaster type of the scraped data is restrained to 'wild fire'. Considering how wide the fire is expanding is an important indicator in this model.

<img src = "https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/random-forest-important-words.png" width="500"/>

The accuracy score for Random Forest model remained in the range of 0.76 - 0.77. Furthermore, the sensitivity score for this model was 0.22, which indicates high rate of type II errors. 

To improve this model,
    - try emsemble, bagging and boosting model
    - try changing target class ratio
    - try doing more thorough hyperparameter tuning.

![alt text](https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/Random_forest_roc_auc_curve.png "random forest roc curve")

**3. Multinomial Naive Bayes ( Count Vectorizer )**                             
Naive Bayes model had 0.94 accuracy score for train set. As the accuracy score for test set and validation set remained at 0.84 and 0.82, respectively, the model is overfitting. However, this model scores the higest on sensitivity score, which makes it an ideal model for this project.

To improve this model,
    - try checking out the percentage of unseen words in the test dataset.
    - try different lemmatization and stemming to reduce the percentage of unseen word.

![alt text](https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/Multinomial_nb_roc_auc%20curve.png "naive bayes roc curve")

#### Evaluating the Models

|                  |Logistic Regression/TF-IDF  | Random Forest/TF-IDF  | Multinomial Naive Bayes/CVEC  |
|------------------|---------------------|---------------|-------------------------|
| Training score   | 0.88              | 0.77        | 0.94                  |
| Testing score    | 0.86              | 0.76        | 0.84                |
| CV score         | 0.83              | 0.76        | 0.82                  |
| Sensitivity      | 0.62              | 0.22        | 0.90                  |
| Specificity      | 0.95              | 0.98        | 0.82                  |
| ROC AUC score    | 0.96               | 0.87         | 0.98                  |

We chose the Naive Bayes model with a CountVectorizer since it had the highest sensitivity score compared to the other two models and also had high (although overfit) training and testing accuracy scores. 

## Flask Application

We applied the relevant tweet classification model to the geographic tweets and then built an app using Flask that lets a user search by city and then plots the relevant tweets as points on a Google Maps basemap where you can then click on a point and see the tweet.

![alt text](https://github.com/dae-han/disaster_tweet_map/blob/master/graphs/flask-map-image.png "flask map image")


## Recommendations and Suggestions for Further Improvements

#### Data Collection

The lack of geographic coordinates in the vast majority of tweets makes it difficult to accurately map the locations of users and, combined with the rate limiting, presents a challenge for integrating the modeling and scraping into a flask application. In addiiton, the fact that Twitter limits access  to tweets that are 7 days old or less means that if we wished to collect any historical Twitter data we would have to save them separately from the scraped tweets.
To get around the issue with date restricted tweets, we recommend running the scrape daily and saving the tweets remotely and then pulling them down and augmenting that day's scrape with the past tweets.

#### Modeling

Our training set for our relevant tweet classifier was limited to only tweets related to "fire" keywords in the LA area and thus cannot be used with any accuracy on data about other disasters in other parts of the country or the world. Adding more data from scrapes using keywords related to other disasters and centered around other locations would allow us to create a more robust training set and a classifier that can be generalized to other disasters and locations. In order to accomplish this we recommend pulling out a subset of every scrape to manually classify as relevant or irrelevant and to then add the newly labeled tweets to the training set, and then rerunning and retuning the classification model.


#### Mapping

The latitudes and longitudes of some of our tweets are clearly wrong because, when mapped, they are in the Pacific Ocean. In order to remove these tweets we recommend filtering the tweets by graphing them and seeing if they fall inside or outside of a boundary line created from a shapefile of the coastline.
