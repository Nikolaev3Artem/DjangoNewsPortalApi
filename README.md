Installing project

git clone git@github.com:Nikolaev3Artem/DjangoNewsPortalApi.git

cd DjangoNewsPortalApi

source env\Scripts\Activate

pip install -r requirements.txt

create .env file (env.txt is example for it):

python manage.py migrate

python manage.py runserver

API DOCS http://127.0.0.1:8000/api/schema/docs