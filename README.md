# piot2-car-share

### Installation (Fix requirements file later when have time)
`python3 -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

`pip install email-validator`

`pip install coverage`

`pip install Flask-Script`

`pip install Flask-Bcrypt`

`pip install Flask-Cors`

`pip install jwt`

`pip install Flask-User`

`pip install Flask-Testing`

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