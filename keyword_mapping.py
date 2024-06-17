import spacy
import os
import csv
from collections import Counter
from string import punctuation

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to convert CSV to list
def csv_to_list(file_path):
    result_list = []

    with open(file_path, mode = 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column header)
        for row in reader:
            if row: # To avoid adding empty rows
                result_list.append(row[0])
    
    return result_list

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
    return set(matched_keywords) # Return unique matched_keywords

# Function to process a single file
def process_file(file_path, predefined_keywords):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Extract the keywords from Job Descriptions
    extracted_keywords = extract_keywords(text)
    #print('Extracted keywords\n\n\n: ', extracted_keywords)

    # Map extracted keywords to predefined keywords
    mapped_keywords = map_keywords(extracted_keywords, predefined_keywords)

    return mapped_keywords

# Function to store all files in CSV
def store_all_files_in_csv(base_path, predefined_keywords, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Filename', 'Keywords']) # Write the column headers

        for filename in os.listdir(base_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(base_path, filename)
                if os.path.isfile(file_path):
                    # Store the mapped keywords in the output CSV
                    mapped_keywords = process_file(file_path, predefined_keywords)
                    if mapped_keywords is not None:
                        writer.writerow([filename, ', '.join(mapped_keywords)])
                        #print(f'\n\nMAPPED KEYWORDS for {filename}:\t\t', mapped_keywords)
                else:
                    print(f"File {file_path} does not exist.")

# Main function
if __name__ == '__main__':

    # Define file paths
    keywords_filepath = "keywords\\full_stack_developer_keywords.csv"
    base_path = "job_descriptions\\full_stack_developer_job_descriptions"
    output_csv = "mapped_keywords_csvs\\full_stack_developer_mapped_keywords.csv"

    predefined_keywords = csv_to_list(keywords_filepath)
    store_all_files_in_csv(base_path, predefined_keywords, output_csv)