import spacy
import os
import csv
import re
from collections import Counter
from string import punctuation
from flask import abort

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to convert CSV to list
def csv_to_list(file_path):
    result_list = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column header)
        for row in reader:
            if row:  # To avoid adding empty rows
                result_list.append(row[0])
    
    return result_list

def extract_job_details(job_description):
    job_details = {}

    # Extracting job title
    match = re.search(r'Job Title:\s*(.*?)\n', job_description)
    if match:
        job_details['Job Title'] = match.group(1)

    # Extracting company name
    match = re.search(r'Company:\s*(.*?)\n', job_description)
    if match:
        job_details['Company'] = match.group(1)
    
    #print(f'Job Details: {job_details}')

    return job_details

# Function to extract keywords using TF-IDF
def extract_keywords(text):
    extracted_keywords = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = nlp(text.lower()) 

    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            extracted_keywords.append(token.text)

    return extracted_keywords

# Function to map extracted keywords to predefined keywords
def map_keywords(extracted_keywords, predefined_keywords):
    matched_keywords = []
    for keyword in extracted_keywords:
        for predefined in predefined_keywords:
            if predefined in keyword:
                matched_keywords.append(predefined)
    return set(matched_keywords)  # Return unique matched_keywords

# Function to process a single file
def process_file(file_path, predefined_keywords):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Extract the job details from Job Descriptions
    job_details = extract_job_details(text) 
    
    # Extract the keywords from Job Descriptions
    extracted_keywords = extract_keywords(text)
    #print('Extracted keywords\n\n\n: ', extracted_keywords)

    # Map extracted keywords to predefined keywords
    mapped_keywords = map_keywords(extracted_keywords, predefined_keywords)

    return {'job_details': job_details, 'mapped_keywords': mapped_keywords}

# Function to store all files in CSV
def store_all_files_in_csv(base_path, predefined_keywords, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Company', 'Job Title', 'Keywords', 'Filename'])  # Write the column headers

        for filename in os.listdir(base_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(base_path, filename)
                if os.path.isfile(file_path):
                    # Store the details in the output CSV
                    job_details = process_file(file_path, predefined_keywords)['job_details']
                    mapped_keywords = process_file(file_path, predefined_keywords)['mapped_keywords']
                    if job_details and mapped_keywords:
                        writer.writerow([job_details.get('Company', ''), job_details.get('Job Title', ''), ', '.join(mapped_keywords), filename])
                else:
                    print(f"File {file_path} does not exist.")

# Function to read full_stack_developer_mapped_keywords.csv and create separate CSVs for each keyword
def create_keyword_csvs(mapped_keywords_csv, output_dir):
    keyword_files = {}
    with open(mapped_keywords_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keywords = row['Keywords'].split(', ')
            for keyword in keywords:
                if keyword not in keyword_files:
                    keyword_files[keyword] = []
                keyword_files[keyword].append([row['Company'], row['Job Title'], row['Filename']])
    
    for keyword, rows in keyword_files.items():
        with open(os.path.join(output_dir, f'{keyword}.csv'), 'w', newline='', encoding='utf-8') as keyword_file:
            writer = csv.writer(keyword_file)
            writer.writerow(['Company', 'Job Title', 'Filename'])
            writer.writerows(rows)

# Function to extract keywords and count occurrences, and write to a CSV
def create_keyword_count_csv(mapped_keywords_csv, keyword_count_csv):
    keyword_counter = Counter()
    with open(mapped_keywords_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keywords = row['Keywords'].split(', ')
            keyword_counter.update(keywords)

    # Write the keyword counts to a separate CSV file
    with open(keyword_count_csv, 'w', newline='', encoding='utf-8') as count_file:
        count_writer = csv.writer(count_file)
        count_writer.writerow(['Keyword', 'Count'])  # Write the column headers
        
        # Sort the keyword counts in descending order and write them
        for keyword, count in keyword_counter.most_common():
            count_writer.writerow([keyword, count])

# Function to process and create all required CSVs
def process_and_create_csvs(output_csv, keyword_output_dir, keyword_count_csv):
    # Create separate CSVs for each keyword
    if not os.path.exists(keyword_output_dir):
        os.makedirs(keyword_output_dir)
    
    create_keyword_csvs(output_csv, keyword_output_dir)
    create_keyword_count_csv(output_csv, keyword_count_csv)

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

#Define file paths
keyword_count_csv = "keyword_counts.csv"
keyword_output_dir = "keyword_csvs"

# Load keyword counts once at startup
keyword_counts = load_keyword_counts(keyword_count_csv)

# Main function
if __name__ == '__main__':

    # Define file paths
    keywords_filepath = "keywords/full_stack_developer_keywords.csv"
    base_path = "job_descriptions/full_stack_developer_job_descriptions"
    output_csv = "mapped_keywords_csvs/full_stack_developer_mapped_keywords.csv"
    keyword_count_csv = "keyword_counts.csv"
    keyword_output_dir = "keyword_csvs"

    predefined_keywords = csv_to_list(keywords_filepath)
    store_all_files_in_csv(base_path, predefined_keywords, output_csv)
    
    # Process and create all required CSVs
    process_and_create_csvs(output_csv, keyword_output_dir, keyword_count_csv)
