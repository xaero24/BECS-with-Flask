from flask import Flask, request, render_template
import data.blood as bl
from csv import reader, writer

becs = Flask(__name__)

@becs.route('/api/add_portion', methods=['POST'])
def addPortion():
    data = request.get_json()

@becs.route('/api/get_portion', methods=['POST'])
def getPortion():
    data = request.get_json()

@becs.route('/api/get_portions', methods=['POST'])
def getPortions():
    data = request.get_json()
