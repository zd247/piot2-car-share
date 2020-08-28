# piot2-car-share

### Installation
`pip install -r requirements.txt`

`pip install email-validator`

In PostgreSQL or database of choice, create 2 tables for test and development

`create database piot2;`

`create database piot2-test;`


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