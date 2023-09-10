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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = Message.query.all()
    if request.method == 'GET':
        chat = []
        for message in messages:
            dict_message = message.to_dict()
            chat.append(dict_message)

        response = make_response(
            chat,
            200
        )
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get("body"),
            username=data.get("username")
        )
        db.session.add(new_message)
        db.session.commit()

        dict_message = new_message.to_dict()

        response = make_response(
            dict_message,
            200
        )
        return response


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    dict_message = message.to_dict()

    if request.method == 'GET':
        response = make_response(
            dict_message,
            200
        )

        return response
    
    elif request.method == 'PATCH':
        data = request.get_json()
        message.body=data.get("body", message.body)

        db.session.commit()

        response = make_response(
            dict_message,
            200
        )

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }

        response = make_response(
            response_body, 
            200
        )

        return response


if __name__ == '__main__':
    app.run(port=5555)
