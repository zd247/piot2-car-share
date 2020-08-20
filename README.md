# piot2-car-share

### Installation
`pip install -r requirements.txt`

In PostgreSQL or database of choice, create 2 tables for test and development

`create database flask_jwt_auth;`

`create database flask_jwt_auth_test;`


`python3 manage.py create_db`

`python3 manage.py db init`

`python3 manage.py db migrate`

Export APP_SETTING to load from app/server/config.py
