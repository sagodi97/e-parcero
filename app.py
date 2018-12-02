from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json

app = Flask(__name__)


@app.route('/get_movie_detail', methods=['POST'])
def get_movie_detail():
    data = request.get_json()
    movie = data['queryResult']['parameters']['movies']
    api_key = os.getenv('OMDB_API_KEY')
    movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
    movie_detail = json.loads(movie_detail)
    response = F"""Sure thing, check it out:\n\n
**Title** : {movie_detail['Title']}\n
**Released** : {movie_detail['Released']}\n
**Cast** : { movie_detail['Actors']}\n
**Plot**: {movie_detail['Plot']}"""
    reply = {
        'fulfillmentText': response
    }
    return jsonify(reply)   


if __name__ == '__main__':
    app.run()
