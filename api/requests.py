from flask import Flask, request, render_template, jsonify
import data.blood as becsClass
import json
from csv import reader, writer
import datetime

becs = Flask(__name__)
bloodbank = becsClass.BECS()
file = 'api/data/user.json'

#Handlers for API endpoints, mainly in forms

#User login helper function
def loggedIn(userName):
    with open(file) as data:
        decoded = json.load(data)
        if userName in decoded.keys():
            if decoded[userName]['logged_in'] == True:
                return True
    return False

#Blood pack handling API

@becs.route('/api/<string:user>/add_portion', methods=['POST'])
def addPortion(user):
    if loggedIn(user):
        data = request.form['bgr']+request.form['rh']
        res = bloodbank.addNewPortion(data)
        msg = f'Successfully added a new portion: {res[0]}. Current amount: {res[1]}.'
        resultData = ("one", msg)
        return render_template('front/confirmation.html', message=resultData, user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route('/api/<string:user>/get_portion', methods=['POST'])
def getPortion(user):
    if loggedIn(user):
        data = request.form['bgr']+request.form['rh']
        res = bloodbank.withdrawPortion(data)
        if res[0] == "None":
            msg = "No suitable donors were found."
        else:
            msg = f'Pulled portion is: {res[0]}. Current amount left: {res[1]}.'
        
        resultData = ("one", msg)
        return render_template('front/confirmation.html', message=resultData, user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route('/api/<string:user>/get_portions', methods=['POST'])
def getPortions(user):
    if loggedIn(user):
        ap = ('A+', int(request.form['ap']))
        op = ('O+', int(request.form['op']))
        bp = ('B+', int(request.form['bp']))
        abp = ('AB+', int(request.form['abp']))
        am = ('A-', int(request.form['am']))
        om = ('O-', int(request.form['om']))
        bm = ('B-', int(request.form['bm']))
        abm = ('AB-', int(request.form['abm']))
        data = (ap, op, bp, abp, am ,om ,bm ,abm)
        res = bloodbank.massWithdrawal(data)
        msg = f'Successfully pulled the following packs and amounts:'
        resultData = ("many", msg, res)
        return render_template('front/confirmation.html', message=resultData, user=user)
    else:
        return redirectToHome("Sign up or log in first")

#User profile control API

@becs.route('/api/signup', methods=['POST'])
def signup():
    userData = request.form
    user = {
        "first_name": userData["fname"],
        "last_name": userData["lname"],
        "id": userData["id"],
        "title": userData["title"],
        "pass": userData["pass"],
        "email": userData["mail"],
        "status": "user",
        "logged_in": False,
        "last_action": ""
    }
    with open(file) as data:
        decoded = json.load(data)
    
    if userData['id'] not in decoded.keys():
        decoded[userData['id']] = user
        with open(file, 'w') as data:
            json.dump(decoded, data)
        res = "User added successfully"
    else:
        res = "User exists, check your details"
    
    return render_template('front/signup.html', message=res)

@becs.route('/api/login', methods=['POST'])
def login():
    user = request.form

    with open(file) as data:
        decoded = json.load(data)
    
    print('========================')
    if user['id'] in decoded.keys():
        udata = decoded[user['id']]
        if user['pass'] == udata['pass']:
            udata['logged_in'] = True
            udata['last_action'] = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            decoded[user['id']] = udata
            with open(file, 'w') as outfile:
                json.dump(decoded, outfile)
            return render_template('front/amounts.html', message=bloodbank.getPackCounts(), user=udata['id'])
        else:
            msg = 'Wrong password'
    else:
        msg = 'User not signed up'
    
    return render_template('front/index.html', message=msg)

@becs.route('/api/<string:user>/update', methods=['POST'])
def updateDetails():
    return 3

@becs.route('/api/<string:user>/make_admin', methods=['POST'])
def makeAdmin():
    return 3

@becs.route('/api/<string:user>/make_user', methods=['POST'])
def makeUser():
    return 3

@becs.route('/api/<string:user>/logout', methods=['POST'])
def logout():
    return 3

#Route handling for HTML requests

@becs.route('/', methods=['GET', 'POST'])
def redirectToHome(msg=""):
    return render_template('front/index.html', message=msg)

@becs.route('/<string:user>/<page>', methods=['GET', 'POST'])
def redirect(user, page):
    if loggedIn(user):
        if page == 'amounts.html':
            return render_template(f'front/amounts.html', message=bloodbank.getPackCounts(), user=user)
        elif page == 'user.html':
            with open(file) as data:
                decoded = json.load(data)
            userData = decoded[user]
            return render_template(f'front/user.html', user=user, data=userData)
        else:
            return render_template(f'front/{page}', user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route('/signup.html', methods=['GET', 'POST'])
def signupPage():
    return render_template(f'front/signup.html', message="")


#Runner

if __name__ == "__main__":
    becs.run(debug=True, host='0.0.0.0', port='5000')