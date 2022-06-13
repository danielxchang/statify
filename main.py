from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

from helpers.constants import TEMPLATES
from dataworkers.data_processor import DataProcessor
from fileworkers.file_handler import FileHandler

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")

file_handler = FileHandler(app.config['UPLOAD_FOLDER'])

def jsonify_data(data, is_recap = False):
    if data:
        if not is_recap:
            return jsonify(
                message = 'Success!',
                box_score = data['box_score'],
                team_stats = data['team_stats'],
                pbp = data['pbp'],
                teams = data['teams'],
            )
        else:
            return jsonify(
                message = 'Success!',
                games = data
            )
    else:
        return Response(status = 400)

@app.route('/api/<sport>/play-by-play/<extension>', methods=['POST'])
@cross_origin()
def post_data(sport, extension):
    print(request.files)
    uploaded_paths = file_handler.validate_input_files(request.files, sport, extension)
    if not uploaded_paths:
        return Response(status = 400)
    
    data_processor = DataProcessor(sport, 'csv')
    data_processor.read_data(uploaded_paths)
    file_handler.finished_reading_files(uploaded_paths.values())
    if not data_processor.translate_data():
        return Response(status = 400)
    else:
        return jsonify(message='POSTED!')

@app.route('/api/<sport>/game/<game_id>')
@cross_origin()
def get_game(sport, game_id):
    data_processor = DataProcessor(sport)
    processed_data = data_processor.retrieve_data(game_id)
    return jsonify_data(processed_data)

@app.route('/api/<sport>/game/all')
@cross_origin()
def get_all_games(sport):
    data_processor = DataProcessor(sport)
    game_recaps = data_processor.get_all_games()
    return jsonify_data(game_recaps, True)

@app.route('/api/<sport>/template')
@cross_origin()
def get_template_link(sport):
    return jsonify(template = TEMPLATES[sport])

if __name__ == "__main__":
    app.run(debug=True)