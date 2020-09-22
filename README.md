# piot2-car-share

### Trello link

https://trello.com/b/C8pm96Nv/cosc2790-piot2

### Project structure

-The project follows the Django-admin for app set up using coverage to perform unit testing in a separate environment, Django-admin provides better solution in managing administrative tasks with command-line utility

-The main server application is stored in /app folder

-The code for Raspberry Pi is stored in the folder Pi

* manage.py: running this file with options to perform administrative tasks

1./app : server application

- models: contains all the initialization of the SQAlchemy database models

- apis: contains all blueprint methods

- __init__.py: contain all the initial set up and configurations. Also to store application's routes to display html contents

- config.py: contain the app configuration

- decorator: contain custom jwt role checker

- templates: contain all html resourecs

- static: contain css and javascripts files

2. /tests

- controllers: contains all testing for blueprint apis

- models: contains all testing for SQLAlchemy model


### Username and password of 4 types of users

Admin: admin1@gmail.com

Engineer: engineer1@gmail.com

Manager: manager1@gmail.com

Customer: customer1@gmail.com

password for all: "password"

### Reports

![git commits](https://github.com/zd247/piot2-car-share/blob/master/2.png)


![trello board](https://github.com/zd247/piot2-car-share/blob/master/3.png)






### Installation (Fix requirements file later when have time)
`python3 -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

In PostgreSQL or database of choice, create 2 tables for test and development

`create database piot2;`

`create database piot2_test;`

### Database Migration

`python3 manage.py create_db`

`python3 manage.py db init`

`python3 manage.py db migrate`

If the above return an ERROR status, follow these steps to fix:

`python3 manage.py db stamp head`

`python3 manage.py db migrate` * Perform this when update new model * 

`python3 manage.py db upgrade`



Export APP_SETTING to load from app/server/config.py


### Testing

In the root directory, run:

`python3 manage.py test`

### To run the server

#### Development

`python3 manage.py runserver`

#### Production

`ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`

`pbcopy < ~/.ssh/id_rsa.pub`

