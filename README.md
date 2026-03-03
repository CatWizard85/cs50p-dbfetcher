# DBFetcher

#### Video Demo: <https://youtu.be/azyJQr6NIjg>

## Description
This web application serves as a modern interface for an old management system that still relies on DBF files. DBF (dBase) files are an older type of database format commonly used in legacy management systems. The application was built to meet the specific needs of the company where it is used. For context, this company is a wholesaler of paper and cardboard.
The purpose is to make the consultation of the warehouse database easier, faster, and more flexible for any user, even those with no technical background.
The application has two main functions:
1. It converts the legacy DBF databases into a modern SQLite structure, cleaning and normalizing the data in the process.
2. It allows users to perform searches and filtering through a simple web interface, with the option to download the results as Microsoft Excel files.

**Note:** Since this application was built for actual use in a company based in Italy, many of its contents (such as labels, field names, and messages) are in Italian.

## Features and design choices

#### DBF → SQLite Conversion
The conversion scripts use Python's **dbfread** library to read the DBF files and extract the relevant data.
The data are then parsed, filtered, cleaned, and normalized before being inserted into a new SQLite database.
Since the legacy management system is still in use, this process is automated locally and executed daily on the updated DBF files at Windows startup.

#### Minimal Frontend Interface
The HTML interface uses simple forms, tables to display results, and buttons for actions.
Forms are designed to retain the most recently entered data in their corresponding fields, allowing faster subsequent searches when users need to fill in multiple fields.

#### Flask Backend
The backend is implemented in Python using Flask.
It takes the user-provided data from the forms to dynamically build database queries and generate the corresponding results pages.
Some searches operate on single database tables, while others require joining multiple tables, such as when retrieving the prices column in the articles search.
In this specific case, using a SQL window function to handle non-aggregated columns in an aggregate query helped make the query more readable.

#### Flexible Search Engine
Users can perform exact or range-based queries across multiple tables (articles, lots, movements, clients, and suppliers).
The various fields in the search forms are treated either as exact matches or as partial matches, depending on the type of data.
For fields that are treated as exact matches but are cumbersome to enter manually, a sub-search option is provided: it opens in a popup window, and the selected result is automatically filled into the corresponding input field.

#### Excel Download
The application allows users to download search results as Excel files for further analysis.
The articles search page also provides an elaborated, partially formatted Excel file that includes an additional column with the calculated number of paper/cardboard sheets for each article — a format used by the company as a list of available articles with non-standard measurements.
All these operations are handled using Python's **pandas** and **openpyxl** libraries.

## Project structure

```
root/
│
├── app.py                  # Main Flask app
├── config.py               # Global paths configuration
├── templates/              # HTML templates for the web interface
├── static/                 # CSS and JS files
├── data/                   # Contains the generated SQLite DB, its schema and the module that creates it
├── helpers/                # Contains support modules for app.py
│
├── dbf_conversion/         # Contains the DBF files and the modules for DBF → SQLite conversion
│
└── requirements.txt        # Dependencies
```

## Requirements

- Python 3.10+
- Flask
- sqlite3
- pandas
- openpyxl
- dbfread

Install dependencies:
```
pip install -r requirements.txt
```

## How to use

1. Place the original .DBF files in the `dbf_conversion` folder.

2. Run the database creation script:
```
python -m data.create_db
```

3. Run the conversion script to insert data from the DBF files into the magazzino.db SQLite database:
```
python -m dbf_conversion.dbf_parser
```

4. Start the Flask web app:
```
python app.py
```

5. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

6. Use the navigation bar to access search pages (articles, lots, movements, clients, suppliers).

7. Perform your searches and optionally export results to Excel.

## What I learned

Through this project, I deepened my understanding of backend development and data handling in Python, improved my ability to build dynamic SQL queries, and gained hands-on experience designing a frontend interface with HTML and Jinja templates.
I learned how to:

-   Parse and normalize legacy DBF files using **dbfread**, handling edge cases and cleaning data efficiently.
-   Design and populate a modern **SQLite** database, thinking about structure, constraints, and performance.
-   Build a **Flask web application**, connecting forms to functions generating dynamic SQL queries, and managing multiple database tables with joins and window functions.
-   Implement a flexible and user-friendly **search engine** capable of exact, partial, and range queries, improving the user experience with remembered form data and popups for sub-searches.
-   Generate downloadable **Excel reports** with **pandas** and **openpyxl**, including custom-calculated columns for practical use in a real company.
-   Combine old and new technologies, creating a bridge between a legacy system and a modern, user-friendly interface.
-   Build a tool specifically around **real, practical needs**, tailoring features and workflows to make daily operations faster and easier for actual users.
-   Use **regular expressions** during the early data analysis phase to perform an initial screening of issues in the legacy database, even though they are not used in the final version of the app.

This project also strengthened my problem-solving skills, my attention to detail in both data and user interface design, and my ability to make technical tools usable for non-technical users.
