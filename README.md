# Wedding
This is the code base for my wedding website, built on Django and SQLite.

The site is hosted [here](https://danandchristin.com/).


## Development Setup
```bash
# install frontend dependencies and build assets
nvm install v6.9.4
npm rebuild node-sass
npm install
npm run build

# set up a virtualenv and install dependencies
virtualenv env
sourece env/bin/activate
pip install -r requirements.txt

# configure your installation
cp wedding/wedding/settings_secret.py.template wedding/wedding/settings_secret.py
# ..and edit values therein

# run migrations
python manage.py migrate

# run django server
python manage.py runserver

```
