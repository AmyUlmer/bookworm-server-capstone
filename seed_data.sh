rm db.sqlite3
rm -rf ./bookwormapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations bookwormapi
python3 manage.py migrate bokowormapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata readers
python3 manage.py loaddata book_genres
python3 manage.py loaddata books
python3 manage.py loaddata events
python3 manage.py loaddata event_readers