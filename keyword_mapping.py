import spacy
import os
import csv
from collections import Counter
from string import punctuation
from keywords import full_stack_developer_keywords

nlp = spacy.load("en_core_web_sm")

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

def process_file(file_path, predefined_keywords):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    extracted_keywords = extract_keywords(text)
    #print('Extracted keywords\n\n\n: ', extracted_keywords)
    mapped_keywords = map_keywords(extracted_keywords, predefined_keywords)
    return mapped_keywords

def store_all_files_in_csv(base_path, predefined_keywords, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Filename', 'Keywords'])

        for filename in os.listdir(base_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(base_path, filename)
                if os.path.isfile(file_path):
                    mapped_keywords = process_file(file_path, predefined_keywords)
                    if mapped_keywords is not None:
                        writer.writerow([filename, ', '.join(mapped_keywords)])
                        print(f'\n\nMAPPED KEYWORDS for {filename}:\t\t', mapped_keywords)
                else:
                    print(f"File {file_path} does not exist.")

# Main function
if __name__ == '__main__':
    base_path = "full_stack_developer_keywords"
    output_csv = "full_stack_developer_keywords.csv"
    predefined_keywords = full_stack_developer_keywords
    store_all_files_in_csv(base_path, predefined_keywords, output_csv)