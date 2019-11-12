# Twitch Channel Recommender
Recommends Twitch channel to a user based on user set preferences and real-time chat data

*Note: To run code locally you may need to install the following Chrome extension related to Cross-Origin Resource Sharing: [Moesif CORS](https://chrome.google.com/webstore/detail/moesif-orign-cors-changer/digfbfaphojjndkpccljibejjbppifbc?hl=en-US)*

## Backend

#### Installing Backend Dependencies
To install all backend dependencies , execute the following commands:

```
cd backend
pip install -r requirements.txt
```

Uncomment the following lines in `cleantext.py`
```
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

#### Running Backend Server
To run the backend server, execute the following commands:

```
cd backend
python api.py
```

## Frontend

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