import requests
import json


class ConnectionManager():
    # __USER_NAME = ''
    # __PASSWORD = ''
    __SERVER_URL = 'http://10.55.42.159:5000'

    def __init__(self, username, password, token):
        self.__server_url = self.__SERVER_URL
        self.__token = token
        self.__authorized = False
        self.username = username
        self.password = password


    def authorize(self) -> bool:
        result = False
        data = json.dumps({
            'username': self.username,
            'password': self.password
        })
        r = requests.post(self.__server_url+'/login', json=data)
        if r.status_code == 200:
            r = json.loads(r.text)

            if r['access_token'] is not None:
                print(r['access_token'])
                self.__token = r['access_token']
                self.__authorized = True
                result = True

        else:
            print(['ERROR no token'])

        return result

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_token(self):
        return self.__token

    def get_events(self):
        headers = {'Authorization':'JWT ' + self.__token}
        r = requests.get(self.__server_url+'/events', headers=headers)
        if r.status_code == 200:
            r = json.loads(r.text)
            return r
        else:
            print('[ERROR] No events')
            return None

    def get_categories(self):
        headers = {'Authorization':'JWT ' + self.__token}
        r = requests.get(self.__server_url+'/categories', headers=headers)
        if r.status_code == 200:
            r = json.loads(r.text)
            return r
        else:
            print('[ERROR] No events')
            return None
