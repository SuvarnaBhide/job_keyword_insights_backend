from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from datetime import datetime, timezone
import csv
import os
import db

app = Flask(__name__)
CORS(app)

# Load keyword counts from keyword_counts.csv
def load_keyword_counts(keyword_count_csv):
    keyword_counts = []
    with open(keyword_count_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keyword_counts.append(row)
    return keyword_counts

# Load keyword-specific data from corresponding CSV
def load_keyword_data(keyword, keyword_output_dir):
    file_path = os.path.join(keyword_output_dir, f'{keyword}.csv')
    if not os.path.isfile(file_path):
        abort(404, description=f"No data found for keyword: {keyword}")

    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Define file paths
keyword_count_csv = "keyword_counts.csv"
keyword_output_dir = "keyword_csvs"

# Load keyword counts once at startup
keyword_counts = load_keyword_counts(keyword_count_csv)

@app.route('/')
def flask_mongodb_atlas():
    return "This is a Python Flask application!"

@app.route("/test")
def test():
    db.db.test.insert_one({"name": "suzie"})
    return "Connected to the data base!"

@app.route('/api/add_data', methods=['POST'])
def add_data():
    data = request.json
    data['created_at'] = datetime.now(timezone.utc)
    result = db.db.collection.insert_one(data)
    return jsonify({'inserted_id': str(result.inserted_id)}), 201

@app.route('/api/read_all_data', methods=['GET'])
def read_all_data():
    # Sort by 'created_at' field in descending order
    names = db.db.collection.find({}, {'_id': 0, 'name': 1}).sort('created_at', -1)
    names_list = [item['name'] for item in names]
    return jsonify(names_list)

@app.route('/api/keyword_counts', methods=['GET'])
def get_keyword_counts():
    return jsonify(keyword_counts)

@app.route('/api/keyword/<keyword>', methods=['GET'])
def get_keyword_data(keyword):
    keyword_data = load_keyword_data(keyword, keyword_output_dir)
    return jsonify(keyword_data)

if __name__ == '__main__':
    app.run(debug=True)
