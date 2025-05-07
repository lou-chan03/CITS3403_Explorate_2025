from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Adventure, UserSelection

# Define the Blueprint
main = Blueprint('main', __name__)

# Define routes using the Blueprint
@main.route('/')
def home():
    return render_template('Data_Entry.html')  # Replace 'index.html' with your main HTML file name

@main.route('/adventure')
def adventure():
    return render_template('Adv_name.html')  # Assumes the file is in the `templates/` directory


# @main.route('/questions', methods=['POST', 'GET'])
# def questions():
#     if request.method == 'POST':
#         # Parse JSON data from the request
#         data = request.get_json()
#         adventure_name = data.get('adventure_name', 'Default Adventure Name')
#         adults = data.get('adults', 0)
#         children = data.get('children', 0)
#         pets = data.get('pets', 0)
#         choice = data.get('choice', 'No')

#         # Log or process the data as needed
#         print(f"Received data: {data}")

#         # Render the next page dynamically
#         return render_template(
#             'Data_Ent_Q1.html',
#             adventure_name=adventure_name,
#             adults=adults,
#             children=children,
#             pets=pets,
#             choice=choice
#         )
    
#     # Handle GET request
#     return render_template('Data_Ent_Q1.html', adventure_name="Default Adventure Name")


#@main.route('/questions', methods=['POST', 'GET'])
# def questions():
#     if request.method == 'POST':
#         # Parse JSON data from the request
#         data = request.get_json()
#         adventure_name = data.get('adventure_name', 'Default Adventure Name')
#         adults = data.get('adults', 0)
#         children = data.get('children', 0)
#         pets = data.get('pets', 0)
#         choice = data.get('choice', 'No')

#         # Save data to the database
#         new_trip = TripDetails(
#             adventure_name=adventure_name,
#             adults=adults,
#             children=children,
#             pets=pets,
#             choice=choice
#         )
#         db.session.add(new_trip)
#         db.session.commit()

#         # Log the operation
#         print(f"Data saved to database: {data}")

#         # Render the next page dynamically
#         return render_template(
#             'Data_Ent_Q1.html',
#             adventure_name=adventure_name,
#             adults=adults,
#             children=children,
#             pets=pets,
#             choice=choice
#         )
    
#     # Handle GET request
#     return render_template('Data_Ent_Q1.html', adventure_name="Default Adventure Name")

@main.route('/questions', methods=['POST', 'GET'])
def questions():
    if request.method == 'POST':
        # Parse JSON data from the request
        data = request.get_json()
        adventure_name = data.get('adventure_name', 'Default Adventure Name')
        adults = data.get('adults', 0)
        children = data.get('children', 0)
        pets = data.get('pets', 0)
        choice = data.get('choice', 'No')

        # Save data to the Adventure table
        new_trip = Adventure(
            adventure_name=adventure_name,
            adults=adults,
            children=children,
            pets=pets,
            choice=choice
        )
        db.session.add(new_trip)
        db.session.commit()

        # Get the generated adventure_id from the newly added adventure
        adventure_id = new_trip.id

        # Log the operation
        print(f"Adventure saved with ID: {adventure_id}")

        # Render the next page dynamically
        return render_template(
            'Data_Ent_Q1.html',
            adventure_name=adventure_name,
            adults=adults,
            children=children,
            pets=pets,
            choice=choice,
            adventure_id=adventure_id  # Pass the adventure_id to the template for later use
        )
    
    # Handle GET request
    return render_template('Data_Ent_Q1.html', adventure_name="Default Adventure Name")


@main.route('/email_share')
def email_share():
    return render_template('email_share.html')

# Share page routes
@main.route('/share_page')
def share_page():
    return render_template('share-page.html')

@main.route('/share_blog')
def share_blog():
    return render_template('share-blog.html')

@main.route('/rate_page')
def rate_page():
    return render_template('rate-page.html')

@main.route('/other_trips')
def other_trips():
    return render_template('other-trips.html')

# @main.route('/save_selections', methods=['POST'])
# def save_selections():
#     data = request.json
#     selections = data.get('selections', [])
#     adventure_id = data.get('adventure_id')  # Assuming adventure_id is passed in the request

#     # Create a new UserSelection row
#     selection = UserSelection(
#         session_id="user123",  # Replace with a dynamically generated session ID if needed
#         answer_1=selections[0] if len(selections) > 0 else None,
#         answer_2=selections[1] if len(selections) > 1 else None,
#         answer_3=selections[2] if len(selections) > 2 else None,
#         answer_4=selections[3] if len(selections) > 3 else None,
#         answer_5=selections[4] if len(selections) > 4 else None,
#         adventure_id=adventure_id  # Link to Adventure
#     )
#     db.session.add(selection)
#     db.session.commit()

#     return jsonify({'message': 'Data saved successfully'})



# @main.route('/save_selections', methods=['POST'])
# def save_selections():
#     data = request.json
#     selections = data.get('selections', [])
#     adventure_id = data.get('adventure_id')  # Get adventure_id from the request

#     print(f"Adventure ID: {adventure_id}")

#     # Check if adventure_id is present and valid
#     if not adventure_id:
#         return jsonify({'message': 'Adventure ID is required'}), 400

#     adventure = Adventure.query.get(adventure_id)
#     if not adventure:
#         return jsonify({'message': 'Adventure not found'}), 404

#     # Create a new UserSelection row
#     selection = UserSelection(
#         session_id="user123",  # Replace with a dynamically generated session ID if needed
#         answer_1=selections[0] if len(selections) > 0 else None,
#         answer_2=selections[1] if len(selections) > 1 else None,
#         answer_3=selections[2] if len(selections) > 2 else None,
#         answer_4=selections[3] if len(selections) > 3 else None,
#         answer_5=selections[4] if len(selections) > 4 else None,
#         adventure_id=adventure_id  # Link to the Adventure
#     )
#     db.session.add(selection)
#     db.session.commit()

#     return jsonify({'message': 'Data saved successfully'})


@main.route('/save_selections', methods=['POST'])
def save_selections():
    data = request.json
    selections = data.get('selections', [])
    adventure_id = data.get('adventure_id')  # Get adventure_id from the request

    # Check if adventure_id exists in the Adventure table
    adventure = Adventure.query.get(adventure_id)
    if not adventure:
        return jsonify({'message': 'Adventure not found'}), 404  # Handle missing adventure

    # Create a new UserSelection entry with the provided adventure_id
    selection = UserSelection(
        session_id="user123",  # Replace with a dynamically generated session ID if needed
        answer_1=selections[0] if len(selections) > 0 else None,
        answer_2=selections[1] if len(selections) > 1 else None,
        answer_3=selections[2] if len(selections) > 2 else None,
        answer_4=selections[3] if len(selections) > 3 else None,
        answer_5=selections[4] if len(selections) > 4 else None,
        adventure_id=adventure_id  # Link to the Adventure using the adventure_id
    )
    
    db.session.add(selection)
    db.session.commit()

    return jsonify({'message': 'Data saved successfully'})

