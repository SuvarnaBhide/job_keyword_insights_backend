# `job_keywords_insights_backend/`:  <br>Repository containing backend codebase built with Python, Flask and SQLAlchemy

### You can check out the deployed application [here](https://job-keyword-insights-backend.onrender.com/).

## Codebase description

<details>
<summary><code>archive</code></summary>

Contains code files no longer in use.

</details>

<details>
<summary><code>job_descriptions/full_stack_developer_job_descriptions</code></summary>

Contains 100 Sample Job Descriptions in `.txt` files for the role of `Full Stack Developer`

</details>

<details>
<summary><code>keyword_csvs</code></summary>

Contains `.csv` files for every keyword that have job descriptions mapped to the specific keyword. Each row represents a job description, and the columns are `Company`, `Job Title`, and `Filename`.

</details>

<details>
<summary><code>keywords</code></summary>

Contains a list of keywords associated with a specific job role. For eg: `full_stack_developer_keywords.csv` contains keywords associated with the role of `Full Stack Developer`.

</details>

<details>
<summary><code>keywords_count_csvs</code></summary>

Contains the keywords and their occurrences for every job role.
  
- <details>
    <summary><code>full_stack_developer_keywords_count.csv</code></summary>

    Keywords and their respective counts for the role of `Full Stack Developer`.
  </details>

</details>

<details>
<summary><code>mapped_keywords_csvs</code></summary>

Contains keywords mapped to a specific Job Role

- <details>
    <summary><code>full_stack_developer_mapped_keywords</code></summary>
    
    Contains a list of keywords associated with every JD for the role of `Full Stack Developer`
  </details>


</details>

<details>
<summary><code>quiz_csvs</code></summary>

Contains `.csv` files for every quiz, which contains `Question`, `Correct Option` and other options.

</details>

<details>
<summary><code>.gitignore</code></summary>

Specifies files and directories Git should ignore in version control.

</details>

<details>
<summary><code>app.py</code></summary>

This code file contains a Flask application that provides RESTful API for managing quiz and keyword-related data. It uses SQLAlchemy for the database operations and Flask-CORS for handling cross-origin resource sharing

</details>

<details>
<summary><code>config.py</code></summary>

This code file sets up the configuration for a Python application, including the MYSQL URI from environment variables

</details>

<details>
<summary><code>csv_to_sql.py</code></summary>

This contains the python script to insert the data from the `.csv` files present in `quiz_csvs/` to MySQL Database via SQL queries

</details>

<details>
<summary><code>keyword_mapping.py</code></summary>

This contains the python script that maps the keywords associated with every Job Description using a pre-defined keywords list that is present in the `keywords/` directory.

</details>

<details>
<summary><code>models.py</code></summary>

Contains the definitions of data models for the quiz application. These models represent different entities such as quizzes, users, questions, options, attempts, and responses. They define the structure and relationships between these entities in the database.

</details>

<details>
<summary><code>README.md</code></summary>

Contains the codebase description for this repo.

</details>

<details>
<summary><code>requirements.txt</code></summary>

This file contains the list of Python packages and their versions required for the backend codebase to run.

</details>

<details>
<summary><code>start.sh</code></summary>

- This is a shell script that is used to start the backend application. 
- It contains the command `python keyword_mapping.py` which executes the `keyword_mapping.py` script.
- `gunicorn -b 0.0.0.0:4000 app:app`, this command starts the Flask applicatoin using Gunicorn. 
- Gunicorn is used to run the Flask application on a specific host and port.

</details>

## Steps to use this repo on local
1. Clone this repo.
2. Install the Python packages by running this command `pip install -r requirements.txt`
3. Create a `.env` file and add your `MYSQL_URI` variable.
    > Your DB connection URL has to be named as `MYSQL_URI` for the flask app to run.
4. Then run the `start.sh` script by running command `sh start.sh`
5. Your flask app should be running on `localhost:5000`
    > Check out [app.py](https://github.com/SuvarnaBhide/job_keyword_insights_backend/blob/main/app.py) file to see the list of routes available.

