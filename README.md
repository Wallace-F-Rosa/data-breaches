# Data breaches API
This is a small learning project to study back-end development.

## Overview
An API that provides information about data breaches public reported(news, articles, press reports, etc). Inpired by [Wikipidia's List of Data Breaches](https://en.wikipedia.org/wiki/List_of_data_breaches). Built using [Python](https://www.python.org/) as programming language, [Django](https://www.djangoproject.com/) as the web framework and [Django REST framework](https://www.django-rest-framework.org/) as a toolkit to build Web APIs.

# Requirements
* Python 3
* Django
* Rest Framework
* sphinx (documentation)

## Live Demo
    TODO

## Install requirements
`pip install -r requirements`

## How to Run the project

After installing the requirements, go to the 'api' directory:

`cd api`

Run the django migrations:

`python manage.py migration`

### Get the data from the scraper
Initialize and update the 'scrape-data-breaches' submodule:

```
git submodule update --init
cd scrape-data-breaches`
pip install -r requirements.txt
python get_data.py
```

The data will be stored on the `data.json` file.

### Populate the database
Go back to the `api` directory:

`cd ../api`

Run the custom command `populate_db` providing the path to the json file
containing the data breaches data:

`python manage.py populate_db ../scrape-data-breaches/data.json`

### Run the project
`python manage.py runserver`
Django will output the localhost link to access the project.

## Data breach
Information about a data breaches can be listed in `/databreaches`. The data listed has the following fields:


| field | description | type |
|---|---|---|
| id | unique identifier of the data breach | integer |
| entity | data about the entity where the data breach happened. contains the name of the organization (string) and a list of strings describing the line of work of the organization | dict |
| year | year when the data breach ocurred | integer |
| records | amount of records leaked | integer |
| method | which method was used in the breaching process | string |
| sources | list of sources (url strings) mentioning the breach | list |

### Details
The data about a specific data breach can be acquired in '/databreaches/<id>' using the id of the data breach.

## Documentation
### Endpoints
The API is self describing as it is built using the [Django REST framework](https://www.django-rest-framework.org/topics/documenting-your-api/#self-describing-apis). Running the project and accessing the urls in the browser will provide the full documentation for each endpoint.

### Complete documentation
Offline documentation is built using `sphinx`:
```
cd api/docs
make html
```

This will provide html documentation on api/docs/_build/index.html.

## Install and run locally
* Installing dependencies:

    `pip install -r requirements.txt`

* Apply migrations:
    `python manage.py migrate`

* To run the project localy do:

    `python manage.py runserver`
