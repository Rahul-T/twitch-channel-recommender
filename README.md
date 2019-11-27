# Twitch Channel Recommender
Recommends Twitch channel to a user based on user set preferences and real-time chat data

For an in-depth explanation of the project, please view this [report](./FinalReport.pdf)

[Video demo of functionality](https://www.youtube.com/watch?v=R-YS_NFtGGw)

*Note: To run code locally you may need to install the following Chrome extension related to Cross-Origin Resource Sharing: [Moesif CORS](https://chrome.google.com/webstore/detail/moesif-orign-cors-changer/digfbfaphojjndkpccljibejjbppifbc?hl=en-US)*

## Backend

#### Important Files

* `api.py` - Provides endpoints for frontend of application to access most viewed games and channel recommendation
* `cleantext.py` - Cleans message text (e.g. removing stopwords, puncuation, etc.)
* `emotedict.py` - Maps emotes to IDs (this is necessary due to the format of the dataset that is used for training)
* `manualoverrides.py` - Contains manual overrides to improve accuracy
* `messageanalysis.py` - Extracts most common emote and word from message, passes pair into model, then returns resulting emotion
* `mlmodels.py` - Formats dataset and trains SVM model (emote-word pairs to emotions), Word2Vec model (emotes, words to vectors), and TFIDF model (emotes, words to frequencies) 
* `realtimestream.py` - Retrieves most viewed channels and real-time chat messages from Twitch API endpoints
* `trainingdata.py` - Builds emote-word pair to emotion mappings

#### Installing Backend Dependencies
To install all backend dependencies , execute the following commands:

```
cd backend
pip install -r requirements.txt
```

Uncomment the following lines in `backend/cleantext.py`
```
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

#### Backend Setup
* Run `cd backend`
* Setup environment variables 
    * Get auth token from [Twitch Apps](https://twitchapps.com/tmi/)
    * Get client ID by registering a new application at [Twitch Developers](https://dev.twitch.tv/console)
    * Create file `env.sh` with the following contents:
    ```
    export TWITCH_USERNAME=YourTwitchUserName
    export OAUTH=oauth:YourOauthToken
    export CLIENT_ID=YourClientID
    ```
    * Run `source env.sh`
* Build dictionaries mapping emotes to their emote ID's 
    * Retrieve emotes.json from [Twitch Emotes](https://twitchemotes.com/apidocs)
    * Run `buildEmoteDicts()` in `emotedict.py`
* Get [Twitter Sentiment Analyzer](https://github.com/nikicc/twitter-emotion-recognition) code
* Collect and format training data
    * Retrieve Twitch messages from [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VE0IVQ)
    * Run `emoteCluster()` in `trainingdata.py`
* Follow instructions at [What does Kappa mean?](https://github.com/evanslt/BlogCode/tree/master/NLP) to train custom Twitch Word2Vec model
* Train ML models (Word2Vec, my custom model, Tfidf)
    * Run `trainModel()` in `mlmodels.py`
    * Run `tfidf()` and `createWeightsDict()` in `mlmodels.py`
* Run `python manualoverrides.py` (hand-written manual overrides to increase accuracy)

#### Running Backend Server
To run the backend server, execute the following commands:

```
cd backend
source env.sh
python api.py
```

## Frontend

#### Important Files

* `src/components/Home.js` - Main page where user inputs preferences and views returned recommendation  

#### Installing Frontend Dependencies
To install all frontend dependencies, execute the following commands:
```
cd frontend
npm install
```

#### Running Frontend

To run the frontend, execute the following commands:

```
cd frontend
npm run start
```

## Credits

This application uses the following open source code:

Stream Twitch Chat: https://learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/

Text Cleaning: https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html

Sentiment Analyzer: https://github.com/nikicc/twitter-emotion-recognition

Twitch Word2Vec: https://github.com/evanslt/BlogCode/tree/master/NLP
