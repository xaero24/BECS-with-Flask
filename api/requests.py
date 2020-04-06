from flask import Flask, request, render_template, jsonify
import data.blood as becsClass
from csv import reader, writer

becs = Flask(__name__)
bloodbank = becsClass.BECS()

@becs.route('/add_portion', methods=['POST'])
def addPortion():
    data = request.form['bgr']+request.form['rh']
    res = bloodbank.addNewPortion(data)
    msg = f'Successfully added a new portion: {res[0]}. Current amount: {res[1]}.'
    return render_template('front/confirmation.html', message=msg)

@becs.route('/get_portion', methods=['POST'])
def getPortion():
    data = request.form['bgr']+request.form['rh']
    res = bloodbank.withdrawPortion(data)
    if res[0] == "None":
        msg = "No suitable donors were found."
    else:
        msg = f'Pulled portion is: {res[0]}. Current amount left: {res[1]}.'
    return render_template('front/confirmation.html', message=msg)

@becs.route('/get_portions', methods=['POST'])
def getPortions():
    op = ('O+', int(request.form['op']))
    ap = ('A+', int(request.form['ap']))
    bp = ('B+', int(request.form['bp']))
    abp = ('AB+', int(request.form['abp']))
    om = ('O-', int(request.form['om']))
    am = ('A-', int(request.form['am']))
    bm = ('B-', int(request.form['bm']))
    abm = ('AB-', int(request.form['abm']))
    data = (op, ap, bp, abp, om ,am ,bm ,abm)
    res = bloodbank.massWithdrawal(data)
    msg = f'Successfully pulled the following packs and amounts: {res}.'
    return render_template('front/confirmation.html', message=msg)

@becs.route('/<page>', methods=['GET', 'POST'])
def redirect(page):
    return render_template(f'front/{page}')