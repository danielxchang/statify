import os

from uuid import uuid4
from flask import Flask, jsonify, request, Response

from constants import *
from play_by_play import PlayByPlay

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/play-by-play/<sport>', methods=['POST'])
def post_data(sport):
    uploaded_files = request.files
    if len(uploaded_files) == 2 \
        and ROSTER_FILE_KEY in uploaded_files  \
        and PBP_FILE_KEY in uploaded_files:
        roster_file = uploaded_files['roster']
        pbp_file = uploaded_files['pbp']

        roster_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"roster-${uuid4()}.csv")
        pbp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"pbp-${uuid4()}.csv")
        print(roster_file_path)
        print(pbp_file_path)
        roster_file.save(roster_file_path)
        pbp_file.save(pbp_file_path)
    else:
        return Response(status=400)

    json_data = {
        "box_score": {
            "data" : None
        },
        "play_by_play": {
            "data" : None
        }
        }
    pbp = PlayByPlay(sport)
    return jsonify(data = json_data)

@app.route('/template/<sport>')
def get_template_link(sport):
    if sport == 'basketball':
        url = BASKETBALL_TEMPLATE_URL
    return jsonify(template = url)

if __name__ == "__main__":
    app.run(debug=True)