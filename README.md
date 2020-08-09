# LostAndFoundBot

## Development Setup

Setup and start virtual environment

```
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```

To start app locally:

```
python app.py
```

To initialize database:

```
export FLASK_APP=app
flask init-db
```
