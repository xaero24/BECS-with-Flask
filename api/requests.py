from flask import Flask, request, render_template


becs = Flask(__name__)

@becs.route('/api/signup', methods=['POST'])
def signup():
    pass

@becs.route('/api/login', methods=['POST'])
def login():
    pass

@becs.route('/api/logout', methods=['POST'])
def logout():
    pass

@becs.route('/api/checkSession/<uname>', methods=['POST'])
def checkSession(uname):
    pass

@becs.route('/api/add_portion', methods=['POST'])
def addPortion():
    data = request.get_json()

@becs.route('/api/add_portions', methods=['POST'])
def addPortions():
    data = request.get_json()

@becs.route('/api/get_portion', methods=['GET'])
def getPortion():
    data = request.get_json()

@becs.route('/api/get_portions', methods=['GET'])
def getPortions():
    data = request.get_json()

@becs.route('/<user>/<page>.html', methods=['GET'])
def getUserPage(user, page):
    # TODO: Add user check in session
    return render_template(f'front/html/{page}.html', message=f'{user}')

@becs.route('/<page>.html', methods=['GET'])
def getPublicPage(page):
    pass