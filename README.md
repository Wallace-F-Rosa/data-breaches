# Data breaches API
This is a small learning project to study back-end development.

## Overview
An API that provides information about data breaches public reported(news, articles, press reports, etc). Inpired by [Wikipidia's List of Data Breaches](https://en.wikipedia.org/wiki/List_of_data_breaches). Built using [Python](https://www.python.org/) as programming language, [Django](https://www.djangoproject.com/) as the web framework and [Django REST framework](https://www.django-rest-framework.org/) as a toolkit to build Web APIs.

## Live Demo
    TODO

## Data breach
Information about a data breaches can be listed in `/databreaches`. The data listed has the following fields:

| field | description | type |
|---|---|---|
| id | unique identifier of the data breach | integer |
| entity | entity where the data breach happened | string |
| year | year when the data breach ocurred | integer |


### Details
The full detail about a data breach can be acquired in '/databreaches/<id>' using the id of the data breach. The data listed contains:

| field | description | type |
|---|---|---|
| id | unique identifier of the data breach | integer |
| entity | entity where the data breach happened | string |
| year | year when the data breach ocurred | integer |
| records | amount of records leaked | integer |
| organization_type | list of fields of the organition work | list |
| method | which method was used in the breaching process | string |
| sources | list of sources mentioning the breach | list |


## Documentation
The API is self describing as it is built using the [Django REST framework](https://www.django-rest-framework.org/topics/documenting-your-api/#self-describing-apis). Running the project and accessing the urls in the browser will provide the full documentation for each endpoint.

## Install and run locally
* Installing dependencies:

    `pip install -r requirements.txt`

* Apply migrations:
    `python manage.py migrate`

* To run the project localy do:

    `python manage.py runserver`
