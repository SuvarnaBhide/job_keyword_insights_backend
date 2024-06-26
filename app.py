from flask import Flask, jsonify, abort
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
from flask_cors import CORS

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

@app.route('/api/keyword_counts', methods=['GET'])
def get_keyword_counts():
    return jsonify(keyword_counts)

@app.route('/api/keyword/<keyword>', methods=['GET'])
def get_keyword_data(keyword):
    keyword_data = load_keyword_data(keyword, keyword_output_dir)
    return jsonify(keyword_data)

if __name__ == '__main__':
    app.run(debug=True)
