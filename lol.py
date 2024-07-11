import csv
import mysql.connector
import os

# Define the TSV file path
tsv_file_path = ''

# Extract quiz name from the TSV file name
quiz_name = os.path.splitext(os.path.basename(tsv_file_path))[0]

# Define database connection parameters
db_config = {
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'your_db_host',
    'database': 'your_db_name',
}

# Function to get the next available ID for a table
def get_next_id(cursor, table_name):
    cursor.execute(f"SELECT IFNULL(MAX(id), 0) + 1 FROM {table_name}")
    return cursor.fetchone()[0]

# Function to generate the SQL for inserting questions and options
def generate_sql_insert_queries(tsv_file_path, quiz_id, next_question_id, next_option_id):
    # Read the TSV file
    with open(tsv_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        
        question_insert_statements = []
        option_insert_statements = []
        
        question_id = next_question_id
        option_id = next_option_id
        option_labels = ['A', 'B', 'C', 'D']
        
        for row in reader:
            question_content = row['Question']
            correct_answer = row['CorrectAnswer']
            
            # Insert statement for the question
            question_insert = f"INSERT INTO Question (quiz_id, content) VALUES ({quiz_id}, '{question_content.replace("'", "''")}');"
            question_insert_statements.append(question_insert)
            
            # Insert statements for the options
            for i, option_label in enumerate(option_labels):
                option_content = row[f'Option{i+1}']
                is_correct = 'TRUE' if option_content == correct_answer else 'FALSE'
                option_insert = (
                    f"INSERT INTO MCQ_Option (question_id, option_label, is_correct, content, explanation) "
                    f"VALUES ({question_id}, '{option_label}', {is_correct}, '{option_content.replace("'", "''")}', NULL);"
                )
                option_insert_statements.append(option_insert)
                option_id += 1
            
            question_id += 1
        
        return question_insert_statements, option_insert_statements

# Establish a database connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Insert the new quiz
quiz_insert = f"INSERT INTO Quiz (name, description) VALUES ('{quiz_name}', 'A quiz generated from the {quiz_name} TSV file.');"
cursor.execute(quiz_insert)
connection.commit()

# Get the ID of the newly inserted quiz
quiz_id = cursor.lastrowid

# Get the next available IDs for Question and MCQ_Option tables
next_question_id = get_next_id(cursor, 'Question')
next_option_id = get_next_id(cursor, 'MCQ_Option')

# Generate SQL insert queries
question_inserts, option_inserts = generate_sql_insert_queries(tsv_file_path, quiz_id, next_question_id, next_option_id)

# Close the database connection
cursor.close()
connection.close()

# Print the SQL insert queries
print(f"-- Inserted Quiz ID: {quiz_id}")
print(f"-- Quiz Insert Statement: {quiz_insert}\n")

for query in question_inserts + option_inserts:
    print(query)
