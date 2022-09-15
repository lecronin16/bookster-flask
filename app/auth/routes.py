from flask import Blueprint,request

#import login funcitonality
from werkzeug.security import check_password_hash

# import models
from app.models import User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db


##### API ROUTES #########
@auth.route('/api/signup', methods=["POST"])
def apiSignMeUp():
    data = request.json
     
    username = data['username']
    email = data['email']
    password = data['password']

    # add user to database
    user = User(username, email, password)

    # add instance to our db
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully created user {username}"
    }

@auth.route('/api/editprofile/<int:id>', methods=["GET", "POST"])
def editProfileApi(id):
    user = User.query.get_or_404(id)
    data = request.json

    # img_url = data['imgUrl']
    username = data['username']
    email = data['email']
    password = data['password']
        
        #commit updates:
    user.updateUserInfo(username, email, password, )
    user.saveUpdates()

    return {
        'status': 'ok',
        'message': f"Successfully updated user {username}"
    }


from app.apiauthhelper import basic_auth, token_auth, token_required

@auth.route('/token', methods=['POST'])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }


@auth.route('/api/login', methods=["POST"])
def apiLogMeIn():
    data = request.json

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user:
        # check password
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }
        return {
            'status': 'not ok',
            'message': "Incorrect password."
        }
    return {
        'status': 'not ok',
        'message': 'Invalid username.'
    }



@auth.route('/api/editprofile/delete/<int:id>',methods = ['GET',"POST", "DELETE"])
def deleteUserAPI(id):
    user = User.query.get_or_404(id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully deleted user"
    }