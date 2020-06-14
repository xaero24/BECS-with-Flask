from flask import Flask, request, render_template, jsonify
import data.blood as becsClass
from csv import reader, writer

becs = Flask(__name__)
bloodbank = becsClass.BECS()

def loggedIn(userName):
    return True

@becs.route('/api/<string:user>/add_portion', methods=['POST'])
def addPortion(user):
    if loggedIn(user):
        data = request.form['bgr']+request.form['rh']
        res = bloodbank.addNewPortion(data)
        msg = f'Successfully added a new portion: {res[0]}. Current amount: {res[1]}.'
        return render_template('front/confirmation.html', message=msg, user=user)
    else:
        redirectToHome()

@becs.route('/api/<string:user>/get_portion', methods=['POST'])
def getPortion(user):
    if loggedIn(user):
        data = request.form['bgr']+request.form['rh']
        res = bloodbank.withdrawPortion(data)
        if res[0] == "None":
            msg = "No suitable donors were found."
        else:
            msg = f'Pulled portion is: {res[0]}. Current amount left: {res[1]}.'
        return render_template('front/confirmation.html', message=msg, user=user)
    else:
        redirectToHome()

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
        return render_template('front/confirmation.html', message=msg, packs=res, user=user)
    else:
        redirectToHome()

@becs.route('/<string:user>/<page>', methods=['GET', 'POST'])
def redirect(user, page):
    if page == 'amounts.html':
        return render_template(f'front/{page}', message=bloodbank.getPackCounts(), user=user)
    else:
        return render_template(f'front/{page}', user=user)

@becs.route('/', methods=['GET', 'POST'])
def redirectToHome():
    return render_template(f'front/index.html')

if __name__ == "__main__":
    becs.run(debug=True, host='0.0.0.0', port='5000')