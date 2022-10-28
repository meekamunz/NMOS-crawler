import msvcrt as m
import os, requests
from json import JSONEncoder

# JSONEncoder
class DateTimeEncoder(JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

#clear screen
def clear():
    os.system('cls')

#wait for key press
def wait():
    print('Press any key to continue...')
    m.getch()
    #print('Where\'s the \'Any\' key?')

# check for IPv4 address
def isGoodIPv4(s):
    pieces = s.split('.')
    if len(pieces) != 4: return False
    try: return all(0<=int(p)<256 for p in pieces)
    except ValueError: return False

# rest_get
def rest_get(url):
    headers = {'accept': '*/*'}
    getRequest = requests.get(url, headers=headers)
    if getRequest.status_code == 200:
        return getRequest.json()
    else:
        return getRequest