from flask import Flask, jsonify, request, Response

from helpers.constants import UPLOAD_FOLDER, BASKETBALL_TEMPLATE_URL
from dataworkers.data_processor import DataProcessor
from dataworkers.file_handler import FileHandler

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

file_handler = FileHandler(app.config['UPLOAD_FOLDER'])

@app.route('/play-by-play/<sport>/<extension>', methods=['POST'])
def post_data(sport, extension):
    uploaded_paths = file_handler.validate_input_files(request.files, sport, extension)
    if not uploaded_paths:
        return Response(status = 400)
    
    data_processor = DataProcessor(sport, 'csv')
    data = data_processor.retrieve_data(uploaded_paths)
    file_handler.finished_reading_files(uploaded_paths.values())
    print(data)
    return jsonify(message = 'Success!')

@app.route('/game/<game_id>')
def get_game(game_id):
    # Retrieve data from MySQL database
    return jsonify(game_id = game_id)

@app.route('/template/<sport>')
def get_template_link(sport):
    if sport == 'basketball':
        url = BASKETBALL_TEMPLATE_URL
    return jsonify(template = url)

if __name__ == "__main__":
    app.run(debug=True)