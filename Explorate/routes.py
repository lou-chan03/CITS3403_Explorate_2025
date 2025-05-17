from flask import Blueprint, render_template, request, jsonify, url_for, session
from collections import Counter
from sqlalchemy.sql import tuple_

#from app import db
from Explorate.models import db,Adventure, UserSelection, User, Recommendations, Ratings, UserFriend
import random
from flask_login import current_user, login_required, logout_user
import uuid

# Define the Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Render a Jinja template
    if current_user.is_authenticated:
        return render_template('Data_Entry.html') 
    return render_template('base.html', show_nav=True)

@main.route('/auth')
def auth():
    return render_template('auth.html')

# Define routes using the Blueprint
@main.route('/FindAdv')
@login_required
def FindAdv():
    return render_template('Data_Entry.html')  # Replace 'index.html' with your main HTML file name


@main.route('/adventure')
@login_required
def adventure():
    return render_template('Adv_name.html')  # Assumes the file is in the `templates/` directory


@main.route('/index')
@login_required
def index():
    return render_template('index.html')  # Assumes the file is in the `templates/` directory




@main.route('/questions', methods=['POST', 'GET'])
@login_required
def questions():
    csrf_token = request.headers.get('X-CSRF-Token')
    try:
        validate_csrf(csrf_token)
    except Exception as e:
        return jsonify({'error': 'CSRF validation failed'}), 400
    if request.method == 'POST':
        # Parse JSON data from the request
        data = request.get_json()
        adventure_name = data.get('adventure_name', 'Adventure1')
        adults = data.get('adults', 0)
        children = data.get('children', 0)
        pets = data.get('pets', 0)
        choice = data.get('choice', 'No')

        # Use the currently logged-in user's ID
        user_id = current_user.id
        Username= current_user.Username
        print(f"Current user ID: {user_id}")
        session['user_id'] = user_id
        session['Username'] = Username

        # Save data to the Adventure table
        new_trip = Adventure(
            adventure_name=adventure_name,
            adults=adults,
            children=children,
            pets=pets,
            choice=choice,
            user_id=user_id,
        )
        db.session.add(new_trip)
        db.session.commit()

        # Get the generated adventure_id from the newly added adventure
        adventure_id = new_trip.id
        user_id = new_trip.user_id

        # Log the operation
        print(f"Adventure saved with ID: {adventure_id}")
        print(f"Adventure saved with ID: {user_id}")

        # Render the next page dynamically
        return render_template(
            'Data_Ent_Q1.html',
            adventure_name=adventure_name,
            adults=adults,
            children=children,
            pets=pets,
            choice=choice,
            adventure_id=adventure_id,  # Pass the adventure_id to the template for later use
            user_id=user_id 
        )
    
    # Handle GET request
    return render_template('Data_Ent_Q1.html', adventure_name="Adventure1")




# Share page routes
@main.route('/share_page')
@login_required
def share_page():
    return render_template('share-page.html')

@main.route('/share_blog')
@login_required
def share_blog():
    return render_template('share-blog.html')

@main.route('/rate_page')
@login_required
def rate_page():
    return render_template('rate-page.html')

# new route to handle submission of ratings
@main.route('/submit_rating', methods=['POST'])
@login_required
def submit_rating():
    data = request.get_json()
    print("Received payload:", data)
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400

    #user_id = data['user_id']
    #adventure_id = data['adventure_id']
    recommendation_id = session.get('recommendation_id')
    if not recommendation_id:
        return jsonify({'error': 'Recommendation ID is required.'}), 400

    location_rating = data.get('location_rating', 0)
    food_rating = data.get('food_rating', 0)
    attractions_rating = data.get('attractions_rating', 0)
    accommodation_rating = data.get('accommodation_rating', 0)
    overall_rating = data.get('overall_rating', 0)
    
    # add logic to store data in database
    rating = Ratings(
        #user_id=user_id,
        #adventure_id=adventure_id,
        recommendation_id = recommendation_id,
        location_rating=location_rating,
        food_rating=food_rating,
        attractions_rating=attractions_rating,
        accommodation_rating=accommodation_rating,
        overall_rating=overall_rating
    )
    print("Rating object created:", rating)
    db.session.add(rating)
    db.session.commit()
    
    return jsonify({'message': 'Rating submitted successfully'}),200

@main.route('/other_trips')
@login_required
def other_trips():
    return render_template('other-trips.html')


# Processing logic for recommendations


@main.route('/save_selections', methods=['POST'])
@login_required
def save_selections():
    try:
        data = request.json
        print("Received payload:", data)

        selections = data.get('selections', [])
        adventure_id = data.get('adventure_id')
        user_id = data.get('user_id')
        print(f"Userrrrr ID: {user_id}")
        

        if not selections or len(selections) < 5:
            return jsonify({"error": "At least 5 inputs are required."}), 400

        if not adventure_id:
            return jsonify({"error": "Adventure ID is required."}), 400

        # Validate adventure existence
        adventure = Adventure.query.get(adventure_id)
        if not adventure:
            return jsonify({'message': 'Adventure not found'}), 404

        # Save user selections
        session_id = str(uuid.uuid4())
        selection = UserSelection(
            session_id=session_id,
            answer_1=selections[0],
            answer_2=selections[1],
            answer_3=selections[2],
            answer_4=selections[3],
            answer_5=selections[4],
            adventure_id=adventure_id
        )
        session['user_id'] = user_id
        print(f"User ID: {user_id}")
        db.session.add(selection)
        db.session.commit()  # Save user selections first
        print("User selection saved successfully.")

        # Recommendation processing
        state_mappings = {
        "Hot": ["South Australia", "Western Australia", "Northern Territory"],
        "Cold": ["Tasmania", "Victoria"],
        "Tropical": ["Queensland", "New South Wales", "Northern Territory"],
        "Beaches": ["New South Wales", "Queensland", "Western Australia", "South Australia"],
        "Nature": ["New South Wales", "Queensland", "Tasmania", "Western Australia", "Victoria", "Northern Territory"],
        "Outback": ["South Australia", "Western Australia", "Northern Territory"],
        "Adventure": ["New South Wales", "Queensland", "Western Australia", "Tasmania", "Northern Territory"],
        "Sport": ["Victoria", "New South Wales", "Tasmania"],
        "Family-friendly": ["Queensland", "New South Wales", "Northern Territory"],
        "Cultural/Arts": ["New South Wales", "Victoria", "South Australia", "Tasmania", "Northern Territory"],
        "Heritage/History": ["Tasmania", "Victoria", "South Australia", "Northern Territory"],
        "Landmarks": ["Queensland", "New South Wales", "Northern Territory", "Western Australia"],
        "Coastal / Scenic Drives": ["Queensland", "Victoria", "Tasmania", "South Australia", "Northern Territory"],
        "Mountain": ["New South Wales", "Victoria", "Tasmania", "Northern Territory"],
        "Wildlife": ["Queensland", "South Australia", "Tasmania", "Western Australia", "Northern Territory"],
        "Food and Wine": ["New South Wales", "Victoria", "South Australia", "Western Australia"]
        }
    
        location_data = {
        "Tasmania": {
            "Family-Friendly": ["Bonorong Wildlife Sanctuary", "Tasmanian Museum and Art Gallery", "Launceston City Park", "ZooDoo Wildlife Park"],
            "Sport": ["Blundstone Arena", "Silverdome Launceston"],
            "Adventure": ["Cradle Mountain-Lake St Clair", "Three Capes Track", "Gordon River Cruises", "Hastings Caves"],
            "Cultural/Arts": ["MONA", "Salamanca Arts Centre", "Theatre Royal", "TMAG"],
            "Beaches": ["Wineglass Bay", "Bay of Fires", "Seven Mile Beach", "Boat Harbour Beach", "Adventure Bay"],
            "Nature": ["Mount Field National Park", "Tarkine Wilderness", "The Nut", "Southwest National Park", "Derwent Valley"],
            "Food and Wine": ["Tamar Valley", "Bruny Island Cheese", "Hobart Salamanca Market", "Huon Valley"],
            "Coastal/Scenic Drives": ["Great Eastern Drive", "Huon Trail", "West Coast Wilderness Drive"],
            "Mountain": ["Cradle Mountain", "Mount Wellington", "Frenchmans Cap", "Hartz Mountains"],
            "Wildlife": ["Maria Island", "Bonorong Sanctuary", "Narawntapu National Park", "Devils @ Cradle"],
            "Outback": ["Queenstown", "Central Highlands"],
            "Winter Sport": ["Ben Lomond", "Mount Mawson", "Cradle Mountain (snow hiking, limited skiing)"],
            "Landmarks": ["Port Arthur", "Richmond Bridge", "Shot Tower", "Battery Point"],
            "Heritage/History": ["Cascades Female Factory", "Ross Village", "Coal Mines Historic Site", "Sarah Island"]
        },
        "South Australia": {
            "Family-Friendly": ["Adelaide Zoo", "Glenelg Foreshore Playground", "Carrick Hill Adventure Playground"],
            "Sport": ["Adelaide Oval", "Coopers Stadium", "The Bend Motorsport Park"],
            "Adventure": ["Kangaroo Island", "Flinders Ranges", "Naracoorte Caves", "River Murray Adventures", "Mount Gambier’s Sinkholes"],
            "Cultural/Arts": ["Adelaide Festival Centre", "Tandanya Institute", "South Australian Museum", "Art Gallery of South Australia"],
            "Beaches": ["Glenelg Beach", "Vivonne Bay", "Second Valley", "Rapid Bay", "Henley Beach"],
            "Nature": ["Ikara-Flinders Ranges", "Coorong National Park", "Deep Creek", "Naracoorte Caves", "Onkaparinga River National Park"],
            "Food and Wine": ["Barossa Valley", "McLaren Vale", "Clare Valley", "Hahndorf", "Central Market Adelaide"],
            "Coastal/Scenic Drives": ["Fleurieu Peninsula", "Eyre Peninsula", "Yorke Peninsula"],
            "Mountain": ["Mount Lofty", "Wilpena Pound", "Mount Remarkable", "Arkaroola Wilderness"],
            "Wildlife": ["Kangaroo Island", "Seal Bay", "Monarto Safari Park", "Cleland Wildlife Park"],
            "Outback": ["Coober Pedy", "Lake Eyre", "Painted Desert", "Oodnadatta Track"],
            "Winter Sport": ["Mount Remarkable", "Lake Alexandrina"],
            "Landmarks": ["Adelaide Oval", "Remarkable Rocks", "Victor Harbor", "Big Lobster"],
            "Heritage/History": ["Old Adelaide Gaol", "Maritime Museum", "Ayers House Museum", "Burra Heritage Town"]
        },
        "Northern Territory": {
            "Family-Friendly": ["Palmerston Water Park", "Crocodylus Park", "Aquascene", "Darwin Waterfront"],
            "Sport": ["Marrara Sporting Complex", "Hidden Valley Raceway", "TIO Stadium (AFL)"],
            "Adventure": ["Larapinta Trail", "Jatbula Trail", "Tabletop Track"],
            "Cultural/Arts": ["Museum and Art Gallery of the Northern Territory", "Red Centre", "Field of Light"],
            "Beaches": [],
            "Nature": ["George Brown Botanic Gardens", "Litchfield National Park", "Howard Springs Nature Park", "Judbarra National Park"],
            "Food and Wine": [],
            "Coastal/Scenic Drives": ["Gove Peninsula", "Djukbinj National Park", "Darwin to Litchfield National Park"],
            "Mountain": ["Macdonnell Ranges", "Kata Tjuta", "Mount Sonder", "Kings Canyon"],
            "Wildlife": ["Territory Wildlife Park", "Nitmiluk Gorge", "The Kangaroo Sanctuary"],
            "Outback": ["Litchfield National", "Simpsons Gap"],
            "Winter Sport": [],
            "Landmarks": ["Uluru-Kata Tjuta National Park", "Kakadu National Park"],
            "Heritage/History": ["Alice Springs Telegraph Station", "Patakijiyali Culture Museum"]
        },
        "Queensland": {
            "Family-Friendly": ["Australia Zoo", "Sea World", "Currumbin Wildlife Sanctuary"],
            "Sport": ["Suncorp Stadium", "The Gabba", "Metricon Stadium"],
            "Adventure": ["Scuba diving Great Barrier Reef", "Skydiving Mission Beach", "White-water rafting on the Tully River"],
            "Cultural/Arts": ["Queensland Performing Arts Centre", "Gallery of Modern Art (GOMA)", "Queensland Art Gallery"],
            "Beaches": ["Whitehaven Beach", "Surfers Paradise", "Noosa Main Beach"],
            "Nature": ["Daintree Rainforest", "Lamington National Park", "Springbrook National Park"],
            "Food and Wine": ["Granite Belt Wine Region", "Tamborine Mountain Distillery", "Eat Street Northshore"],
            "Coastal/Scenic Drives": ["Captain Cook Highway", "Great Tropical Drive", "Pacific Coast Way"],
            "Mountain": ["Glass House Mountains", "Mount Tamborine", "Mount Barney National Park"],
            "Wildlife": ["Australia Zoo (Sunshine Coast)", "Currumbin Wildlife Sanctuary", "Daintree Rainforest wildlife cruises"],
            "Outback": ["Charleville", "Longreach", "Winton"],
            "Winter Sport": [],
            "Landmarks": ["Great Barrier Reef", "Daintree Rainforest", "Story Bridge (Brisbane)"],
            "Heritage/History": ["Stockman's Hall of Fame (Longreach)", "Parliament House (Brisbane)", "Cooktown Historical Centre"]
        },
        "Western Australia": {
            "Family-Friendly": ["Scitech Perth", "Perth Zoo", "Adventure World (amusement park)"],
            "Sport": ["Optus Stadium", "WACA Ground", "HBF Park"],
            "Adventure": ["Snorkeling at Ningaloo Reef", "Rock climbing in Kalbarri", "Sandboarding at Lancelin"],
            "Cultural/Arts": ["Art Gallery of WA", "WA Museum Boola Bardip", "Perth Cultural Centre"],
            "Beaches": ["Cottesloe Beach", "Cable Beach", "Turquoise Bay"],
            "Nature": ["Karijini National Park", "Nambung National Park (Pinnacles Desert)", "Purnululu National Park"],
            "Food and Wine": ["Margaret River", "Swan Valley", "Great Southern Wine Region"],
            "Coastal/Scenic Drives": ["Indian Ocean Drive", "South West Edge Drive", "Great Ocean Drive (Esperance)"],
            "Mountain": ["Bluff Knoll", "Stirling Range National Park", "Mount Trio"],
            "Wildlife": ["Penguin Island (penguins, sea lions)", "Yanchep National Park (koalas, kangaroos)", "Rottnest Island (quokkas)"],
            "Outback": ["Gibb River Road", "Nullarbor Plain", "Karijini National Park"],
            "Winter Sport": [],
            "Landmarks": ["Wave Rock", "Pinnacles Desert (Nambung NP)", "Bungle Bungle Range (Purnululu NP)"],
            "Heritage/History": ["Fremantle Prison", "Old Gaol Albany", "Broome Historical Museum"]
        },

        "New South Wales": {
            "Family-Friendly": ["Taronga Zoo", "Luna Park Sydney", "Featherdale Wildlife Park"],
            "Sport": ["Accor Stadium", "Sydney Cricket Ground", "Allianz Stadium"],
            "Adventure": ["Skydiving in Wollongong", "Canyoning in the Blue Mountains", "Surfing at Newcastle"],
            "Cultural/Arts": ["Sydney Opera House", "Art Gallery of NSW", "Museum of Contemporary Art Australia"],
            "Beaches": ["Bondi Beach", "Byron Bay", "Hyams Beach"],
            "Nature": ["Blue Mountains", "Royal National Park", "Lord Howe Island"],
            "Food and Wine": ["Hunter Valley", "Orange wine region", "Mudgee"],
            "Coastal/Scenic Drives": [],
            "Mountain": ["Mount Kosciuszko", "Blue Mountains", "Mount Warning (Wollumbin)"],
            "Wildlife": ["Australian Reptile Park", "Koala Park Sanctuary", "Symbio Wildlife Park"],
            "Outback": ["Broken Hill", "Lightning Ridge", "Mutawintji National Park"],
            "Winter Sport": ["Thredbo", "Perisher", "Charlotte Pass"],
            "Landmarks": ["Sydney Opera House", "Sydney Harbour Bridge", "Three Sisters (Blue Mountains)"],
            "Heritage/History": []
        }
    }

        possible_states = []
        for answer in selections:
            possible_states.extend(state_mappings.get(answer, []))

        if not possible_states:
            return jsonify({"error": "No suitable states found."}), 400

        state_counts = Counter(possible_states)
        max_count = max(state_counts.values())
        top_states = [state for state, count in state_counts.items() if count == max_count]
        selected_state = random.choice(top_states)

        print("Selected state:", selected_state)

        recommendations = {}
        for key in selections[1:]:
            if key in location_data[selected_state] :
                recommendations[key] = random.choice(location_data[selected_state][key])
            else:
                recommendations[key] = f"No recommendations found for {key} in {selected_state}."

        # Validate recommendations
        print("Generated recommendations:", recommendations)
        if not recommendations:
            return jsonify({"error": "Failed to generate recommendations."}), 400

        # Save recommendations
        recommendation_entry = Recommendations(
            session_id=session_id,
            selected_state=selected_state,
            recommendation_1=recommendations.get(selections[1], None),
            recommendation_2=recommendations.get(selections[2], None),
            recommendation_3=recommendations.get(selections[3], None),
            recommendation_4=recommendations.get(selections[4], None),
        )
        db.session.add(recommendation_entry)
        db.session.commit()  # Save recommendations
        session['recommendation_id'] = recommendation_entry.id
        print("Recommendations saved successfully.")
        print(print(session.get('user_id')))

        print("Final recommendation payload:", {
        "selected_state": selected_state,
        "recommendations": recommendations,
        "recommendation_id": recommendation_entry.id
    })


        return jsonify({
            "message": "Data saved successfully",
            "selected_state": selected_state,
            "recommendations": recommendations
        })

    except Exception as e:
        db.session.rollback()
        print("Error during processing:", str(e))
        return jsonify({"error": "An error occurred during processing."}), 500



state_mappings = {
    "Hot": ["South Australia", "Western Australia", "Northern Territory"],
    "Cold": ["Tasmania", "Victoria"],
    "Tropical": ["Queensland", "New South Wales", "Northern Territory"],
    "Beaches": ["New South Wales", "Queensland", "Western Australia", "South Australia"],
    "Nature": ["New South Wales", "Queensland", "Tasmania", "Western Australia", "Victoria", "Northern Territory"],
    "Outback": ["South Australia", "Western Australia", "Northern Territory"],
    "Adventure": ["New South Wales", "Queensland", "Western Australia", "Tasmania", "Northern Territory"],
    "Sport": ["Victoria", "New South Wales", "Tasmania"],
    "Family-friendly": ["Queensland", "New South Wales", "Northern Territory"],
    "Cultural/Arts": ["New South Wales", "Victoria", "South Australia", "Tasmania", "Northern Territory"],
    "Heritage/History": ["Tasmania", "Victoria", "South Australia", "Northern Territory"],
    "Landmarks": ["Queensland", "New South Wales", "Northern Territory", "Western Australia"],
    "Coastal / Scenic Drives": ["Queensland", "Victoria", "Tasmania", "South Australia", "Northern Territory"],
    "Mountain": ["New South Wales", "Victoria", "Tasmania", "Northern Territory"],
    "Wildlife": ["Queensland", "South Australia", "Tasmania", "Western Australia", "Northern Territory"],
    "Food and Wine": ["New South Wales", "Victoria", "South Australia", "Western Australia"]
}

location_data = {
    "Tasmania": {
        "Family-Friendly": ["Bonorong Wildlife Sanctuary", "Tasmanian Museum and Art Gallery", "Launceston City Park", "ZooDoo Wildlife Park"],
        "Sport": ["Blundstone Arena", "Silverdome Launceston"],
        "Adventure": ["Cradle Mountain-Lake St Clair", "Three Capes Track", "Gordon River Cruises", "Hastings Caves"],
        "Cultural/Arts": ["MONA", "Salamanca Arts Centre", "Theatre Royal", "TMAG"],
        "Beaches": ["Wineglass Bay", "Bay of Fires", "Seven Mile Beach", "Boat Harbour Beach", "Adventure Bay"],
        "Nature": ["Mount Field National Park", "Tarkine Wilderness", "The Nut", "Southwest National Park", "Derwent Valley"],
        "Food and Wine": ["Tamar Valley", "Bruny Island Cheese", "Hobart Salamanca Market", "Huon Valley"],
        "Coastal/Scenic Drives": ["Great Eastern Drive", "Huon Trail", "West Coast Wilderness Drive"],
        "Mountain": ["Cradle Mountain", "Mount Wellington", "Frenchmans Cap", "Hartz Mountains"],
        "Wildlife": ["Maria Island", "Bonorong Sanctuary", "Narawntapu National Park", "Devils @ Cradle"],
        "Outback": ["Queenstown", "Central Highlands"],
        "Winter Sport": ["Ben Lomond", "Mount Mawson", "Cradle Mountain (snow hiking, limited skiing)"],
        "Landmarks": ["Port Arthur", "Richmond Bridge", "Shot Tower", "Battery Point"],
        "Heritage/History": ["Cascades Female Factory", "Ross Village", "Coal Mines Historic Site", "Sarah Island"]
    },
    "South Australia": {
        "Family-Friendly": ["Adelaide Zoo", "Glenelg Foreshore Playground", "Carrick Hill Adventure Playground"],
        "Sport": ["Adelaide Oval", "Coopers Stadium", "The Bend Motorsport Park"],
        "Adventure": ["Kangaroo Island", "Flinders Ranges", "Naracoorte Caves", "River Murray Adventures", "Mount Gambier’s Sinkholes"],
        "Cultural/Arts": ["Adelaide Festival Centre", "Tandanya Institute", "South Australian Museum", "Art Gallery of South Australia"],
        "Beaches": ["Glenelg Beach", "Vivonne Bay", "Second Valley", "Rapid Bay", "Henley Beach"],
        "Nature": ["Ikara-Flinders Ranges", "Coorong National Park", "Deep Creek", "Naracoorte Caves", "Onkaparinga River National Park"],
        "Food and Wine": ["Barossa Valley", "McLaren Vale", "Clare Valley", "Hahndorf", "Central Market Adelaide"],
        "Coastal/Scenic Drives": ["Fleurieu Peninsula", "Eyre Peninsula", "Yorke Peninsula"],
        "Mountain": ["Mount Lofty", "Wilpena Pound", "Mount Remarkable", "Arkaroola Wilderness"],
        "Wildlife": ["Kangaroo Island", "Seal Bay", "Monarto Safari Park", "Cleland Wildlife Park"],
        "Outback": ["Coober Pedy", "Lake Eyre", "Painted Desert", "Oodnadatta Track"],
        "Winter Sport": ["Mount Remarkable", "Lake Alexandrina"],
        "Landmarks": ["Adelaide Oval", "Remarkable Rocks", "Victor Harbor", "Big Lobster"],
        "Heritage/History": ["Old Adelaide Gaol", "Maritime Museum", "Ayers House Museum", "Burra Heritage Town"]
    },
    "Northern Territory": {
        "Family-Friendly": ["Palmerston Water Park", "Crocodylus Park", "Aquascene", "Darwin Waterfront"],
        "Sport": ["Marrara Sporting Complex", "Hidden Valley Raceway", "TIO Stadium (AFL)"],
        "Adventure": ["Larapinta Trail", "Jatbula Trail", "Tabletop Track"],
        "Cultural/Arts": ["Museum and Art Gallery of the Northern Territory", "Red Centre", "Field of Light"],
        "Beaches": [],
        "Nature": ["George Brown Botanic Gardens", "Litchfield National Park", "Howard Springs Nature Park", "Judbarra National Park"],
        "Food and Wine": [],
        "Coastal/Scenic Drives": ["Gove Peninsula", "Djukbinj National Park", "Darwin to Litchfield National Park"],
        "Mountain": ["Macdonnell Ranges", "Kata Tjuta", "Mount Sonder", "Kings Canyon"],
        "Wildlife": ["Territory Wildlife Park", "Nitmiluk Gorge", "The Kangaroo Sanctuary"],
        "Outback": ["Litchfield National", "Simpsons Gap"],
        "Winter Sport": [],
        "Landmarks": ["Uluru-Kata Tjuta National Park", "Kakadu National Park"],
        "Heritage/History": ["Alice Springs Telegraph Station", "Patakijiyali Culture Museum"]
    },
    "Queensland": {
        "Family-Friendly": ["Australia Zoo", "Sea World", "Currumbin Wildlife Sanctuary"],
        "Sport": ["Suncorp Stadium", "The Gabba", "Metricon Stadium"],
        "Adventure": ["Scuba diving Great Barrier Reef", "Skydiving Mission Beach", "White-water rafting on the Tully River"],
        "Cultural/Arts": ["Queensland Performing Arts Centre", "Gallery of Modern Art (GOMA)", "Queensland Art Gallery"],
        "Beaches": ["Whitehaven Beach", "Surfers Paradise", "Noosa Main Beach"],
        "Nature": ["Daintree Rainforest", "Lamington National Park", "Springbrook National Park"],
        "Food and Wine": ["Granite Belt Wine Region", "Tamborine Mountain Distillery", "Eat Street Northshore"],
        "Coastal/Scenic Drives": ["Captain Cook Highway", "Great Tropical Drive", "Pacific Coast Way"],
        "Mountain": ["Glass House Mountains", "Mount Tamborine", "Mount Barney National Park"],
        "Wildlife": ["Australia Zoo (Sunshine Coast)", "Currumbin Wildlife Sanctuary", "Daintree Rainforest wildlife cruises"],
        "Outback": ["Charleville", "Longreach", "Winton"],
        "Winter Sport": [],
        "Landmarks": ["Great Barrier Reef", "Daintree Rainforest", "Story Bridge (Brisbane)"],
        "Heritage/History": ["Stockman's Hall of Fame (Longreach)", "Parliament House (Brisbane)", "Cooktown Historical Centre"]
    },
    "Western Australia": {
        "Family-Friendly": ["Scitech Perth", "Perth Zoo", "Adventure World (amusement park)"],
        "Sport": ["Optus Stadium", "WACA Ground", "HBF Park"],
        "Adventure": ["Snorkeling at Ningaloo Reef", "Rock climbing in Kalbarri", "Sandboarding at Lancelin"],
        "Cultural/Arts": ["Art Gallery of WA", "WA Museum Boola Bardip", "Perth Cultural Centre"],
        "Beaches": ["Cottesloe Beach", "Cable Beach", "Turquoise Bay"],
        "Nature": ["Karijini National Park", "Nambung National Park (Pinnacles Desert)", "Purnululu National Park"],
        "Food and Wine": ["Margaret River", "Swan Valley", "Great Southern Wine Region"],
        "Coastal/Scenic Drives": ["Indian Ocean Drive", "South West Edge Drive", "Great Ocean Drive (Esperance)"],
        "Mountain": ["Bluff Knoll", "Stirling Range National Park", "Mount Trio"],
        "Wildlife": ["Penguin Island (penguins, sea lions)", "Yanchep National Park (koalas, kangaroos)", "Rottnest Island (quokkas)"],
        "Outback": ["Gibb River Road", "Nullarbor Plain", "Karijini National Park"],
        "Winter Sport": [],
        "Landmarks": ["Wave Rock", "Pinnacles Desert (Nambung NP)", "Bungle Bungle Range (Purnululu NP)"],
        "Heritage/History": ["Fremantle Prison", "Old Gaol Albany", "Broome Historical Museum"]
    },
    "New South Wales": {
        "Family-Friendly": ["Taronga Zoo", "Luna Park Sydney", "Featherdale Wildlife Park"],
        "Sport": ["Accor Stadium", "Sydney Cricket Ground", "Allianz Stadium"],
        "Adventure": ["Skydiving in Wollongong", "Canyoning in the Blue Mountains", "Surfing at Newcastle"],
        "Cultural/Arts": ["Sydney Opera House", "Art Gallery of NSW", "Museum of Contemporary Art Australia"],
        "Beaches": ["Bondi Beach", "Byron Bay", "Hyams Beach"],
        "Nature": ["Blue Mountains", "Royal National Park", "Lord Howe Island"],
        "Food and Wine": ["Hunter Valley", "Orange wine region", "Mudgee"],
        "Coastal/Scenic Drives": [],
        "Mountain": ["Mount Kosciuszko", "Blue Mountains", "Mount Warning (Wollumbin)"],
        "Wildlife": ["Australian Reptile Park", "Koala Park Sanctuary", "Symbio Wildlife Park"],
        "Outback": ["Broken Hill", "Lightning Ridge", "Mutawintji National Park"],
        "Winter Sport": ["Thredbo", "Perisher", "Charlotte Pass"],
        "Landmarks": ["Sydney Opera House", "Sydney Harbour Bridge", "Three Sisters (Blue Mountains)"],
        "Heritage/History": []
    }
}  



@main.route('/recommend', methods=['POST'])
@login_required
def recommend():
    # Get session_id from the request
    session_id = request.json.get("session_id")

    if not session_id:
        return jsonify({"error": "Session ID is required."}), 400

    # Fetch the user's selection data
    user_selection = UserSelection.query.filter_by(session_id=session_id).first()

    if not user_selection:
        return jsonify({"error": "No data found for this session."}), 404

    # Gather user answers
    answers = [
        user_selection.answer_1,
        user_selection.answer_2,
        user_selection.answer_3,
        user_selection.answer_4,
        user_selection.answer_5,
    ]

    # Determine possible states based on answers
    possible_states = []
    for answer in answers:
        if answer in state_mappings:
            possible_states.extend(state_mappings[answer])

    if not possible_states:
        return jsonify({"error": "No suitable states found."}), 400

    # Select the most likely state
    selected_state = random.choice(possible_states)

    # Select one adventure and one beach location
    recommendations = {}
    for category in answers[1:]:
        if selected_state in location_data and category in location_data[selected_state]:
            recommendations[category] = random.choice(location_data[selected_state][category])

    # Respond with the recommendations
    return jsonify({
        "state": selected_state,
        "recommendations": recommendations,
        "session_id": session_id,
        # "recommendation_id": recommendation_entry.id
    })




@main.route('/api/adventures', methods=['POST'])
@login_required
def get_adventures():
    user_id = session.get('user_id')
    print(f"User ID from session: {user_id}")
    if not user_id:
        return jsonify({'error': 'UserID is required'}), 400

    # Your existing SQLAlchemy query here, unchanged
    results = db.session.query(
        Adventure.adventure_name,
        Recommendations.recommendation_1,
        Recommendations.recommendation_2,
        Recommendations.recommendation_3,
        Recommendations.recommendation_4
    ).join(UserSelection, Adventure.id == UserSelection.adventure_id) \
     .join(Recommendations, UserSelection.session_id == Recommendations.session_id) \
     .filter(Adventure.user_id == user_id).all()

    response = [
        {
            'adventure_name': row.adventure_name,
            'recommendation_1': row.recommendation_1,
            'recommendation_2': row.recommendation_2,
            'recommendation_3': row.recommendation_3,
            'recommendation_4': row.recommendation_4
        } for row in results
    ]
    return jsonify(response)


@main.route('/MyTrips')
@login_required
def MyTrips():
    return render_template('MyTrips.html')

@main.route('/friendView')
@login_required
def friendView():
    return render_template('shareView.html')

@main.route('/friend')
@login_required
def friend():
    return render_template('name.html')


@main.route('/add_friend_adventure', methods=['POST'])
@login_required
def add_friend_adventure():
    data = request.get_json()
    frd_username = data.get('frd_username')
    adv_name = data.get('adv_name')

    # Check if adventure belongs to the current user
    adventure = db.session.query(Adventure).filter_by(adventure_name=adv_name, user_id=current_user.id).first()
    if not adventure:
        return jsonify({'message': 'Adventure not found for the current user.'}), 400

    # Check if the friend's username exists
    friend = User.query.filter_by(Username=frd_username).first()
    if not friend:
        return jsonify({'message': 'Friend username not found.'}), 404

    # Add new UserFriend entry
    new_entry = UserFriend(user_id=current_user.id, frd_username=frd_username, adv_name=adv_name)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': f'Friend {frd_username} with adventure {adv_name} added.'})


@main.route('/get_friends_adventures', methods=['GET'])
@login_required
def get_friends_adventures():
    user_friends = UserFriend.query.filter_by(user_id=current_user.id).all()
    data = [{'friend_username': uf.frd_username, 'adventure_name': uf.adv_name} for uf in user_friends]
    return jsonify({'friends_adventures': data})


@main.route('/fetch-adventure-data', methods=['GET'])
@login_required
def fetch_adventure_data():
    try:
        # Get the current user's ID
        current_user_username = current_user.Username
        print(f"Current User ID: {current_user_username}")

        # Subquery to fetch user_id and adv_name for the current user
        subquery = db.session.query(
            UserFriend.user_id,
            UserFriend.adv_name
        ).join(User, UserFriend.user_id == User.id) \
         .filter(UserFriend.frd_username == current_user_username).subquery()

        # Main query to fetch data based on the subquery
        results = db.session.query(
            User.Username,
            Adventure.adventure_name,
            Recommendations.recommendation_1,
            Recommendations.recommendation_2,
            Recommendations.recommendation_3,
            Recommendations.recommendation_4
        ).join(Adventure, User.id == Adventure.user_id) \
         .join(UserSelection, Adventure.id == UserSelection.adventure_id) \
         .join(Recommendations, UserSelection.session_id == Recommendations.session_id) \
         .filter(
             tuple_(User.id, Adventure.adventure_name).in_(
                 db.session.query(subquery.c.user_id, subquery.c.adv_name)
             )
         ).all()

        # Transform results into a JSON-friendly format
        data = [
            {
                "username": result.Username,
                "adventure_name": result.adventure_name,
                "recommendation_1": result.recommendation_1,
                "recommendation_2": result.recommendation_2,
                "recommendation_3": result.recommendation_3,
                "recommendation_4": result.recommendation_4
            }
            for result in results
        ]

        return jsonify(data)

    except Exception as e:
        # Print the error to the console for debugging
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# TEMPORARY ROUTES FOR TESTING ONLY

@main.route('/analytics')
@login_required
def analytics():
    username = current_user.Username
    dummy_user = {'user_name': username}
    return render_template('analytics.html', user=dummy_user, active_tab='analytics')

@main.route('/trends')
@login_required
def trends():
    username = current_user.Username
    dummy_user = {'user_name': username}
    return render_template('trends.html', user=dummy_user, active_tab='trends')

@main.route('/recommendations')
@login_required
def recommendations():
    username = current_user.Username
    dummy_user = {'user_name': username}
    return render_template('recommendations.html', user=dummy_user, active_tab='recommendations')


# new

@main.route('/api/trends', methods=['GET'])
@login_required
def trends_data():
    user_id = current_user.id
    total_trips = Adventure.query.filter_by(user_id=user_id).count()

    recs = db.session.query(Recommendations.selected_state)\
        .join(UserSelection, Recommendations.session_id == UserSelection.session_id)\
        .join(Adventure, UserSelection.adventure_id == Adventure.id)\
        .filter(Adventure.user_id == user_id).all()

    state_counter = {}
    for rec in recs:
        state = rec[0]
        if state:
            state_counter[state] = state_counter.get(state, 0) + 1
    top_state = max(state_counter, key=state_counter.get) if state_counter else "N/A"

    categories = db.session.query(Adventure.choice).filter_by(user_id=user_id).all()
    cat_counter = {}
    for cat in categories:
        value = cat[0]
        if value:
            cat_counter[value] = cat_counter.get(value, 0) + 1
    top_category = max(cat_counter, key=cat_counter.get) if cat_counter else "N/A"

    return jsonify({
        'total_trips': total_trips,
        'top_state': top_state,
        'top_category': top_category,
        'trip_duration': 4.5  # Placeholder
    })

@main.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard_data():
    user_id = current_user.id

    # Total trips
    total_trips = Adventure.query.filter_by(user_id=user_id).count()

    # Top category
    categories = db.session.query(Adventure.choice).filter_by(user_id=user_id).all()
    cat_counter = {}
    for cat in categories:
        value = cat[0]
        if value:
            cat_counter[value] = cat_counter.get(value, 0) + 1
    top_category = max(cat_counter, key=cat_counter.get) if cat_counter else "N/A"
    top_category_percent = round((cat_counter.get(top_category, 0) / total_trips * 100), 1) if total_trips > 0 else 0

    # Top state
    states = db.session.query(Recommendations.selected_state)\
        .join(UserSelection, Recommendations.session_id == UserSelection.session_id)\
        .join(Adventure, UserSelection.adventure_id == Adventure.id)\
        .filter(Adventure.user_id == user_id).all()
    state_counter = {}
    for s in states:
        state = s[0]
        if state:
            state_counter[state] = state_counter.get(state, 0) + 1
    top_state = max(state_counter, key=state_counter.get) if state_counter else "N/A"

    # Placeholder rating
    avg_rating = 4.6

    return jsonify({
        'total_trips': total_trips,
        'top_category': top_category,
        'top_category_percent': top_category_percent,
        'top_state': top_state,
        'avg_rating': avg_rating
    })

@main.route('/api/user-analytics', methods=['GET'])
@login_required
def api_user_analytics():
    user_id = current_user.id

    adventures = Adventure.query.filter_by(user_id=user_id).all()
    total_trips = len(adventures)
    adults = sum(a.adults for a in adventures)
    children = sum(a.children for a in adventures)
    pets = sum(a.pets for a in adventures)

    category_data = [a.choice for a in adventures if a.choice]
    category_counts = {}
    for c in category_data:
        category_counts[c] = category_counts.get(c, 0) + 1

    recs = db.session.query(Recommendations.selected_state) \
        .join(UserSelection, Recommendations.session_id == UserSelection.session_id) \
        .join(Adventure, UserSelection.adventure_id == Adventure.id) \
        .filter(Adventure.user_id == user_id).all()

    state_counts = {}
    for rec in recs:
        state = rec[0]
        if state:
            state_counts[state] = state_counts.get(state, 0) + 1

    trip_names = [a.adventure_name for a in adventures if a.adventure_name]
    trip_counts = {}
    for name in trip_names:
        trip_counts[name] = trip_counts.get(name, 0) + 1

    group_sizes = [a.adults + a.children + a.pets for a in adventures if (a.adults + a.children + a.pets) > 0]
    average_group_size = round(sum(group_sizes) / len(group_sizes), 1) if group_sizes else 0

    group_size_bins = {'Solo/Pair': 0, 'Small Group': 0, 'Medium Group': 0, 'Large Group': 0}
    for size in group_sizes:
        if size <= 2:
            group_size_bins['Solo/Pair'] += 1
        elif size <= 4:
            group_size_bins['Small Group'] += 1
        elif size <= 6:
            group_size_bins['Medium Group'] += 1
        else:
            group_size_bins['Large Group'] += 1

    yes_count = category_counts.get("Yes", 0)
    exploration_index = round(
        (total_trips * 5) +
        (yes_count * 3) +
        (adults * 1.2 + children * 1.5 + pets * 2),
        1
    ) if total_trips > 0 else 0

    planning_intensity = round(((children + pets) / total_trips), 2) if total_trips else 0
    child_to_adult_ratio = round((children / adults), 2) if adults > 0 else 0

    return jsonify({
        'total_trips': total_trips,
        'state_data': state_counts,
        'category_data': category_counts,
        'trip_name_data': trip_counts,
        'adults': adults,
        'children': children,
        'pets': pets,
        'average_group_size': average_group_size,
        'group_size_bins': group_size_bins,
        'exploration_index': exploration_index,
        'planning_intensity': planning_intensity,
        'child_to_adult_ratio': child_to_adult_ratio
    })

@main.route('/user-analytics')
@login_required
def user_analytics():
    return render_template('user_analytics.html', user=current_user)
