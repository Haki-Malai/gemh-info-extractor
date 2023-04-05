# gemh-info-extractor

![python](https://img.shields.io/badge/python-3.10-blue)

This project implements an algorithm in Python to parse given txt files and extract information about a company. Specifically, the algorithm extracts the company's official name, GEMH number, website (if mentioned in the file), and the date of the website's registration.

The code first turns the txt file to a list of wards and defines a class called **DataExtractor** that extracts data from the list. It has methods to extract website values, GEMH values, date values, and name values from the list of words. The class also has various attributes that define patterns and words used to extract the data.

The extracted data is then stored in a MySQL database, and can be accessed via a RESTful API endpoint that takes as input the company's GEMH number and returns all available information about the company.

The RESTful API provides a live documentation site on /docs url.

## How to Run
To run this project, you'll need to have Docker and Docker Compose installed on your system. Once you have those installed, follow these steps:
### Using Docker Compose
To run the app using Docker Compose, follow these steps:
  1. Clone this repository to your machine.
  2. Navigate to the project directory in your terminal.
  3. Run the following command:
  ```sh
  docker-compose up --build
  ```
  This will build the Docker image and start the app on http://0.0.0.0:8000.

### Using Flask Run
To run the app using Flask Run, follow these steps:
  1. Clone this repository to your machine.
  2. Navigate to the project directory in your terminal.
  3. Create a virtual environment:
  ```sh
  python3 -m venv venv
  ```
  4. Activate the virtual environment:
  ```sh
  source venv/bin/activate
  ```
  5. Install the required packages:
  ```sh
  pip install -r requirements.txt
  ```
  6. Run the mysql and redis containers or use your own and edit the .env file:
  ```sh
  docker-compose up -d db redis
  ```
  7. Extract the data from the txts to the mysql server:
  ```sh
  flask extract
  ```
  8. Run the app:
  ```sh
  flask run
  ```
 
### Options
```bash
flask --help
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  An application to load must be given with the '--app' option, 'FLASK_APP'
  environment variable, or with a 'wsgi.py' or 'app.py' file in the current
  directory.

Options:
  -e, --env-file FILE   Load environment variables from this file. python-
                        dotenv must be installed.
  -A, --app IMPORT      The Flask application or factory function to load, in
                        the form 'module:name'. Module can be a dotted import
                        or file path. Name is not required if it is 'app',
                        'application', 'create_app', or 'make_app', and can be
                        'name(args)' to pass arguments.
  --debug / --no-debug  Set debug mode.
  --version             Show the Flask version.
  --help                Show this message and exit.

Commands:
  db       Perform database migrations.
  extract  Extract data from text files in the ./txt folder.
  routes   Show the routes for the app.
  run      Run a development server.
  shell    Run a shell in the app context.
  test     Run tests.
```

## Live API Documentation
The API documentation is available on http://localhost:5000/docs, using the Element UI interface. You can use this interface to explore the available endpoints and their parameters, as well as to try out requests and see the responses. Connection to https://www.unpkg.com/ is required for the page to render correctly.

## License
This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.