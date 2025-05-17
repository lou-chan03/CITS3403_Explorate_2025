## Explorate: A Flask based web application to find an itinerary around Australia, based on the user's choices

## Created by
| UWA ID | Name | Github Username |
| --- | --- | --- |
| 23694618 | Ishita Sharma | grumblingremlin |
| 23362432 | Louise Chan | lou-chan03 |
| 24111049 | Luvish Ramchurn | It-is-what-it-is1 |
| 23585984 | Tasveer Mann | TasveerMann |

## Features:
- User authentication with sign up and login functionality
- Produces an itinerary table created based on user input
- Sharing itinerary results with other users
- Analysis of various statistics across all previously made itineraries
- Rating system for itineraries

## Prerequisites
- Python 3.12 or earlier
- pip
- Chrome, Firefox, or Microsoft Edge for selenium tests
- Other items in requirements.txt

# Installation
1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```
2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate # in windows venv/Scripts/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

# Running
1. Start flask server
```bash
export FLASK_APP=app.py # in windows set FLASK_APP=app.py
flask run
```
2. Open browser and navigate
```bash
http://127.0.0.1:5000
```

# Run Tests
1. Run the unit tests
```
python -m unittest testing.unitTests
```
2. Run the selenium tests
```
python -m unittest testing.systemTests
```
# Project structure
```
Explorate/                       # Root project folder
|
├── .vscode/                    # VSCode settings and configs
│   └── settings.json
│
├── assets/                     # Static assets like logos
│   └── explorer-logo.png
│
├── instance/                   # Database files (instance folder for Flask)
│   ├── adventures.db
│   ├── explorate.db
│   └── test.db
│
├── migrations/                 # Alembic migrations for database schema versioning
│   └── versions/
│       ├── a5629f15c52d\_ratings\_db.py
│       ├── ac7b4a60d0c6\_add\_recommendation\_id\_to\_ratings\_model.py
│       └── fbfa263f0bd7\_updating\_w\_overall\_rating\_column.py
│
├── static/                     # Static files served to clients (CSS, JS, images)
│   ├── css/
│   │   ├── mytrips.css
│   │   ├── recommendation.css
│   │   ├── style.css
│   │   ├── styles-share.css
│   │   ├── styles.css
│   │   └── teststyle.css
│   ├── images/
│   │   ├── Capture.PNG
│   │   ├── IMG\_9604.png
│   │   ├── IMG\_9605.png
│   │   ├── IMG\_9606.png
│   │   ├── Insights.png
│   │   ├── Itineray.png
│   │   ├── auMap.png
│   │   ├── explorer.png
│   │   ├── green-bg.png
│   │   ├── pencil-96.png
│   │   ├── profile.png
│   │   ├── trips.png
│   │   └── x-22.png
│   └── js/
│       ├── MyTrip.js
│       ├── ideal.js
│       ├── name.js
│       ├── script.js
│       ├── scriptQ.js
│       ├── script\_DataEnt.js
│       ├── shareView\.js
│       └── share\_script.js
│
├── templates/                 # HTML templates (Jinja2)
│   ├── Adv\_name.html
│   ├── Data\_Ent\_Q1.html
│   ├── Data\_Entry.html
│   ├── MyTrips.html
│   ├── auth.html
│   ├── base.html
│   ├── homepage.html
│   ├── index.html
│   ├── name.html
│   ├── other-trips.html
│   ├── rate-page.html
│   ├── share-blog.html
│   ├── share-page.html
│   ├── shareView\.html
│   └── testtravel.html
│
├── testing/                   # Test modules
│   ├── **init**.py
│   ├── systemTests.py
│   └── unitTests.py
│
├── .DS\_Store                  # macOS metadata file (can be ignored)
├── .gitignore                 # Git ignore file
├── README.md                  # Project readme and instructions
├── README                     # Possibly an older readme
├── alembic.ini                # Alembic config for migrations
├── app.py                     # Flask app entry point
├── auth.py                    # Authentication related routes and logic
├── blueprints.py              # Registering blueprints for modular Flask app
├── config.py                  # Configuration variables (DB URI, secret key, etc.)
├── create\_db.py               # Script to create the initial database
├── models.py                  # SQLAlchemy ORM models
├── routes.py                  # Flask routes (views)
├── script.py.mako             # Alembic template for migrations
├── script.js                  # (Looks like a duplicate in root? Possibly clean this up)
├── backup.bundle              # Possibly a backup of something (check if needed)
├── requirements.txt           # Python dependencies list

```
