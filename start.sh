# For development use (simple logging, etc):
VIRTUALENV=.data/venv
if [ ! -d $VIRTUALENV ]; then
  python3 -m venv $VIRTUALENV
fi

python3 -m pip install flask-sqlalchemy
python3 -m pip install flask
python3 -m pip install SQLAlchemy-serializer
python3 -m pip install flask_restful
python3 -m pip install flask_wtf
python3 -m pip install flask_login

python3 server.py
# For production use:
# gunicorn server:app -w 1 --log-file -