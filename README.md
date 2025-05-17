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
Explorate/
├── static/
│   ├── css/
│   │   ├── mytrips.css
│   │   ├── recommendation.css
│   │   ├── shareview.css
│   │   ├── style.css
│   │   ├── styles-share.css
│   │   ├── styles.css
│   │   ├── teststyle.css
│   ├── images/
│   │   ├── Capture.PNG
│   │   ├── IMG_9604.png
│   │   ├── IMG_9605.png
│   │   ├── IMG_9606.png
│   │   ├── Insights.png
│   │   ├── Itineray.png
│   │   ├── auMap.png
│   │   ├── explorer.png
│   │   ├── green-bg.png
│   │   ├── pencil-96.png
│   │   ├── profile.png
│   │   ├── trips.png
│   │   ├── x-22.png
│   ├── js/
│       ├── MyTrip.js
│       ├── ideal.js
│       ├── name.js
│       ├── script.js
│       ├── scriptQ.js
│       ├── script_DataEnt.js
│       ├── shareView.js
│       ├── share_script.js
├── templates/
├── __init__.py
├── auth.py
├── blueprints.py
├── config.py
├── csrf.py
├── models.py
├── routes.py
├── instance/
│   ├── adventures.db
│   ├── explorate.db
│   ├── test.db
├── migrations/
│   ├── versions/
│       ├── a5629f15c52d_ratings_db.py
│       ├── ac7b4a60d0c6_add_recommendation_id_to_ratings_model.py
│       ├── fbfa263f0bd7_updating_w_overall_rating_column.py
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
├── testing/
│   ├── __init__.py
│   ├── systemTests.py
│   ├── unitTests.py
├── .DS_Store
├── .gitignore
├── README.md
├── app.py
├── backup.bundle
├── create_db.py
├── requirements.txt


```
