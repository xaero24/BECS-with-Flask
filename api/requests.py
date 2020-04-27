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
    msg = f'Successfully pulled the following packs and amounts: {res}.'
    return render_template('front/confirmation.html', message=msg)

@becs.route('/<page>', methods=['GET', 'POST'])
def redirect(page):
    if page == 'amounts.html':
        return render_template(f'front/{page}', message=bloodbank.getPackCounts())
    else:
        return render_template(f'front/{page}')

@becs.route('/', methods=['GET', 'POST'])
def redirectToHome():
    return redirect('amounts.html')

if __name__ == "__main__":
    becs.run(debug=True, host="0.0.0.0", port="5000")