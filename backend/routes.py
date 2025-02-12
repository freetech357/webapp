from app import app, db
from flask import request, jsonify
from model import Friend

@app.route('/api/friends', methods=['GET'])
def get_all_friends():
    friends = Friend.query.all()
    return jsonify([friend.to_json() for friend in friends]), 200

@app.route('/api/friends', methods=['POST'])
def create_friend():
    try:
        data = request.get_json()
        required_fields = ['name', 'role', 'gender', 'description']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Missing required field: {field}")
        
        name = data.get('name')
        role = data.get('role')
        description = data.get('description')
        gender = data.get('gender')

        if gender not in ['male', 'female', 'other']:
            raise ValueError('Invalid gender value')
        elif gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        elif gender == "other":
            img_url = f"https://avatar.iran.liara.run/public/other?username={name}"
        else:
            pass

        

        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()

        return jsonify({"msg": "Friend created successfully", "status":True}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e), "status":False}), 500
    

@app.route('/api/friends/<int:friend_id>', methods=['DELETE'])
def delete_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)

        if friend is None:
            return jsonify({'msg': 'Friend not found',"status":False}), 404
        
        db.session.delete(friend)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 404
    return jsonify({"msg": "Friend deleted successfully", "status":True}), 200

@app.route('/api/friends/<int:friend_id>', methods=['PUT'])
def update_friend(friend_id):
    try:
        data = request.get_json()
        friend = Friend.query.get(friend_id)

        if friend is None:
            return jsonify({'msg': 'Friend not found', 'status':False}), 404

        friend.name = data.get('name', friend.name)
        friend.role = data.get('role', friend.role)
        friend.description = data.get('description', friend.description)
        friend.gender = data.get('gender', friend.gender)
        friend.img_url = data.get('imgUrl', friend.img_url)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e), "status":False}), 404

    return jsonify({"msg": "Friend updated successfully", "status":True}), 200