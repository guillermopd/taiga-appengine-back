# Taiga Google App Engine Backend Deployment

This is a forked version of the great Taiga project management tool developed by Kaleidos, kudos to them!
https://github.com/taigaio/taiga-back

This repo contains small changes to allow the deployment of Taiga in Google App Engine

## Why

Google App Engine allows us to deploy Taiga in an elastic serverless way so we don't worry about scaling the application.
As an added benefit, when the application is not in use it will be scaled down to 0 without instance cost.

## Deployment

### Pre-requisites

- First follow instructions to deploy the frontend:
https://github.com/guillermopd/taiga-appengine-front-dist


### Deploy the backend service

Clone this repository

```shell script
git clone git clone git@github.com:guillermopd/taiga-appengine-back.git
```

Enter into the newly created directory and create a new virtualenv, activate it and install the python dependencies:

```shell script
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Now we use cloud_sql_proxy (included in the gcloud toolbox) to connect to our Cloud SQL instance and create the
database tables:

```shell script
cloud_sql_proxy -instances=$GOOGLE_CLOUD_PROJECT:$DB_REGION:$SQL_NAME=tcp:5432
```

This command will not exit, leave it running until the next step is finished.
Execute the Django management commands:

```shell script
python manage.py migrate --noinput
python manage.py loaddata initial_user
python manage.py loaddata initial_project_templates
python manage.py compilemessages
python manage.py collectstatic --noinput
```

Edit app.yaml file and set the variables to match your environemnt configuration

Finally, we're ready to deploy the backend service:

```shell script
gcloud app deploy --project $GOOGLE_CLOUD_PROJECT -v 5-0-12
```

