from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Chatter-box home</h1>'

# @app.route('/messages', methods = ['GET'])
# def messages():
#     if request.method == 'GET':
#         messages = Message.query.all()
#         message_list = [message.to_dict() for message in messages]
#         response = make_response(jsonify(message_list), 200)    
#         return response

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(jsonify(messages), 200)

        return response
    
    elif request.method == 'POST':
        new_message = Message(
            body=request.form.get("body"),
            username=request.form.get("username",)
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()
        response = make_response(jsonify(message_dict), 201)

        return response


@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if message == None:
        response_body = {
            "message": "No message of this nature was received" 
        }
        response = make_response(jsonify(response_body), 404)

        return response
    
    else:
        if request.method == 'GET':
            message_dict = message.to_dict()

            response = make_response(jsonify(message_dict), 200)

            return response
        
        elif request.method == 'PATCH':
            message = Message.query.filter_by(id=id).first()

            for attr in request.form:
                setattr(message, attr, request.form.get(attr))

            db.session.add(message)
            db.session.commit()

            message_dict = message.to_dict()

            response = make_response(jsonify(message_dict), 200)
            return response
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted!"
            }

            response = make_response(jsonify(response_body), 200)

            return response



if __name__ == '__main__':
    app.run(port=5555)


# POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
# DELETE /messages/<int:id>: deletes the message from the database