# Author : ysh
# 2025/11/17 Mon 17:43:49
from core.general import *
from lib.general import *

import lib.model as model
import lib.game

from flask import Blueprint, send_file, make_response, request
import requests
import json

app = Blueprint('model', __name__)

@app.route('/model/ask_llm', methods = ['GET', 'POST'])
def ask_llm():
    info(f'Received Request sent from {request.remote_addr}')
    return ok(model.ask_llm(request.values['data']))

@app.route('/game/get_category', methods = ['GET', 'POST'])
def get_category():
    if not require(request, ['rules']):
        return fail('Key missing')
    
    rules = request.values['rules']

    ans = (lib.game.get_category(rules))
    if ans is None:
        return fail('Model Failed')
    
    return ok(category = ans[0], faith = ans[1], trial = ans[2])

@app.route('/game/get_strategy', methods = ['GET', 'POST'])
def get_strategy():
    if not require(request, ['rules']):
        return fail('Key Missing')
    
    rules = request.values['rules']

    ans = lib.game.get_strategy(rules)
    if ans is None:
        return fail('Model Failed')
    
    return ok(ans)

ds = {}

@app.route('/game/number', methods = ['GET', 'POST'])
def save_number():
    if not require(request, ['number', 'username']):
        return fail('Key missing')

    username = request.values['username']
    number = request.values['number']

    try:
        number = int(number)
        assert(0 <= number <= 100)
    except:
        return fail('Number needed')

    ds[username] = number

    return ok()

@app.route('/game/get_number', methods = ['GET', 'POST'])
def send_number():
    f = []
    for i in ds:
        f.append([i, ds[i]])
    mean = sum([i[1] for i in f]) * 2 / 3 / len(f)
    for i in range(len(f)):
        f[i].append(abs(f[i][1] - mean))
    f = sorted(f, key = lambda x: x[2])
    return ok(ls = f, mean = mean)