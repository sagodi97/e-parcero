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
    if movie_detail['Response'] == 'True' and movie_detail['Type'] == 'series':
        response = F"""Check it out:\n\n{movie_detail['Title']} ({movie_detail['Released']})\n\n{movie_detail['Plot']}\n
Cast : { movie_detail['Actors']}\n\nIMDB Rating: {movie_detail['Ratings'][0]['Value']}\nNumber of Seasons: {movie_detail['totalSeasons']}"""
    elif movie_detail['Response'] == 'True' and movie_detail['Type'] == 'movie':
        response = F"""Check it out:\n\n                                        
        {movie_detail['Title']} ({movie_detail['Released']})\n                  
        {movie_detail['Plot']}\n\nCast : { movie_detail['Actors']}\n            
                                                                                
        Rotten Tomatoes Tomatometer: 🍅 {movie_detail['Ratings'][1]['Value']}    
        IMDB Rating: {movie_detail['Ratings'][0]['Value']}\n                    
        Metacritic Score: {movie_detail['Ratings'][2]['Value']}"""
    elif movie_detail['Response'] == 'False':
        response = f"Sorry, I looked for {movie} in my brain but nothing came up..."

    reply = {
        'fulfillmentText': response
    }
    return jsonify(reply)   


if __name__ == '__main__':
    app.run()
