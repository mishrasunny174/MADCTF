#!/usr/bin/env python3

import sys
import mysql.connector
import yaml
import requests
import hashlib
import string 
import random
from checklib import *

# yml = yaml.load(open('/app/config/config.yml'), Loader=yaml.FullLoader)
# yml_teams_ip = (lambda team_list: {k['ip']: k['name'] for k in team_list})
# teams_ip = yml_teams_ip(yml['teams'])

teams_ip = {'172.19.10.11': 'byteforc3', '172.19.10.12': 'invaders', '172.19.10.13': 'dadac0c0', '172.19.10.14': '69ingdeadbabies', '172.19.10.15': 'mr', '172.19.10.16': 'abs0lut3pwn4g3', '172.19.10.17': 'inv4sion', '172.19.10.18': 'infoseciitr', '172.19.10.19': 'zh3r0', '172.19.10.20': 'c4r3t4k3r5', '172.19.10.21': 'noobsinthehouse', '172.19.10.22': 'd4rkc0de', '172.19.10.23': 'citadel', '172.19.10.24': 'dc1ph3r', '172.19.10.25': 'cicada3301', '172.19.10.26': 'batsquad', '172.19.10.27': 'hackrangers', '172.19.10.28': 'teammeta', '172.19.10.29': 'cybercaliphate', '172.19.10.30': 'warmachinelab', '172.19.10.31': 'hijackers', '172.19.10.32': 'cyberknight00', '172.19.10.33': 'deamons', '172.19.10.34': 'noobmaster69', '172.19.10.35': 'teampaladin', '172.19.10.36': 'cyberdefecers', '172.19.10.37': 'boot2noob', '172.19.10.38': 'airbenders', '172.19.10.39': 'pwnth3ml1k3y0u0wnth3m', '172.19.10.40': 'foobar', '172.19.10.41': '3p1d3m1c', '172.19.10.42': 'rougewolves', '172.19.10.43': 'dcua', '172.19.10.44': 'redpwn'}
STOCK_VALUE = 10001
ROOT_PASS = 'MyVeryEpicMysqlR00tp@ssword'
res = (lambda N: ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))) 

USERNAME = res(10)
NAME = res(10)
EMAIL = "flagcheckertester@flagcheckertester.com"
PASSWORD = res(10)
md5pass = hashlib.md5(PASSWORD.encode()).hexdigest()
IP = "0.0.0.0"

REGISTER_URI = '/scripts/register-action.php'
LOGIN_URI = '/scripts/login.php'
STONKS_URI = '/home/stonks.php'

def insertOrUpdateStock(cursor, ticker, name):
    value = STOCK_VALUE
    c= cursor.execute(f"""INSERT INTO stonks(ticker, name, value) VALUES('{ticker}', '{name}', {value}) ON DUPLICATE KEY UPDATE ticker='{ticker}', name='{name}', value='{value}';""")

def registerNewUser(host, username, password):
    r = requests.post(f'http://{host}:8080{REGISTER_URI}', data={'username':username, 'password':password, 'email': EMAIL, 'name': NAME})
    return r

def createUser(cursor):
    c = cursor.execute(f"""INSERT INTO players(name, email, username, password, usertype, money, ip) VALUES('{NAME}','{EMAIL}','{USERNAME}','{md5pass}','1','10000','{IP}')""")

def deleteUser(cursor):
    cursor.execute(f"""DELETE FROM players WHERE username='{USERNAME}'""")

def getLoggedInSession(host, username, password):
    s = requests.Session()
    while not s.cookies.get('PHPSESSID', False):
        r = s.post(f'http://{host}:8080{LOGIN_URI}', data={'username':username, 'password':password})
        print(r.text)
    
    return s

def put(host, flagid, flag, vuln):
    try:
        r = requests.get(f"http://{host}:8080/")
        if r.status_code != 200 and 'BIEX' not in r.text:
            cquit(Status.DOWN, 'Connection error')
    except:
            cquit(Status.DOWN, 'Connection error')
    
    mydb = mysql.connector.connect(
        host='172.19.10.10',
        user='root',
        database=teams_ip[host], 
        passwd=ROOT_PASS,
        autocommit=True
    )

    cursor = mydb.cursor()
    insertOrUpdateStock(cursor, flagid, flag)
    mydb.commit()
    cquit(Status.OK, flagid)


def get(host, flagid, flag, vuln):
    mydb = mysql.connector.connect(
        host='172.19.10.10',
        user='root',
        database=teams_ip[host], 
        passwd=ROOT_PASS,
        autocommit=True
    )

    cursor = mydb.cursor()
    createUser(cursor)
    mydb.commit()
    
    s = getLoggedInSession(host, USERNAME, PASSWORD)
    r = s.get(f'http://{host}:8080/home/dashboard.php')
    if r.status_code != 200 and USERNAME not in r.text:
        deleteUser(cursor)
        mydb.commit()
        cquit(Status.DOWN, 'Connection error')

    r = s.post(f'http://{host}:8080{STONKS_URI}', data={'submit': True, 'q':flagid})
    if r.status_code != 200:
        deleteUser(cursor)
        mydb.commit()
        cquit(Status.MUMBLE, 'Invalid response')
    
    if flagid in r.text and flag in r.text:
        deleteUser(cursor)
        mydb.commit()
        cquit(Status.OK, 'Found flagid:'+flagid)
    else:
        deleteUser(cursor)
        mydb.commit()
        print(r.text)
        cquit(Status.CORRUPT, "Flag Corrupt")

    deleteUser(cursor)
    cquit(Status.MUMBLE, "Unknown")

def check(host):
    mydb = mysql.connector.connect(
        host='172.19.10.10',
        user='root',
        database=teams_ip[host], 
        passwd=ROOT_PASS,
        autocommit=True
    )

    cursor = mydb.cursor()
    createUser(cursor)
    mydb.commit()
    s = getLoggedInSession(host, USERNAME, PASSWORD)
    r = s.get(f'http://{host}:8080/home/dashboard.php')
    if r.status_code != 200 and USERNAME not in r.text:
        deleteUser(cursor)
        mydb.commit()
        cquit(Status.DOWN, 'Connection error')

    deleteUser(cursor)
    mydb.commit()
    cquit(Status.OK, 'valueInvestor alive.')

if __name__ == '__main__':
    action, *args = sys.argv[1:]
    if action == "check":
        host, *argsextra = args
        check(host)

    elif action == "get":
        host, flagid, flag, vuln = args
        get(host, flagid, flag, vuln)

    elif action == "put":
        host, flagid, flag, vuln = args
        put(host, flagid, flag, vuln)
    else:
        cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)