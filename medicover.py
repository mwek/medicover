from contextlib import contextmanager
import json
import os
import requests
import HTMLParser
from bs4 import BeautifulSoup

class Medicover:

    def __init__(self):
        self._session = requests.Session()

    def login(self, username, password):
        # Step 1: Open login page.
        r = self._session.get('https://mol.medicover.pl/Users/Account/LogOn')
        bs = BeautifulSoup(r.content)
        json_text = HTMLParser.HTMLParser().unescape(bs.select('#modelJson')[0].text)
        token = json.loads(json_text)['antiForgery']['value']

        # Step 2: Send login info.
        r = self._session.post(
            r.url,
            data={
                'username': username,
                'password': password,
                'idsrv.xsrf': token,
            },
        )
        r.raise_for_status()
        bs = BeautifulSoup(r.content)

        def getHiddenField(name):
            return bs.select('input[name="%s"]' % name)[0]['value']

        # Step 3: Forward auth info to main page.
        r = self._session.post(
            'https://mol.medicover.pl/Medicover.OpenIdConnectAuthentication/Account/OAuthSignIn',
            data={
                'code': getHiddenField('code'),
                'id_token': getHiddenField('id_token'),
                'scope': getHiddenField('scope'),
                'state': getHiddenField('state'),
                'session_state': getHiddenField('session_state'),
            },
        )
        r.raise_for_status()

    def logout(self):
        r = self._session.get('https://mol.medicover.pl/Users/Account/LogOff')
        r.raise_for_status()

    @contextmanager
    def logged_in(self, username, password):
        self.login(username, password)
        try:
            yield
        finally:
            self.logout()

    def get_appointments(self):
        appointments = []
        page = 1
        while True:
            r = self._session.post(
                'https://mol.medicover.pl/api/MyVisits/SearchVisitsToView',
                headers={
                    'X-Requested-With': 'XMLHttpRequest'
                },
                data={
                    'Page': page,
                    'PageSize': 12,
                },
            )
            r.raise_for_status()

            json_data = r.json()
            appointments += json_data['items']
            if len(appointments) >= json_data['totalCount']:
                return appointments
            page += 1


if __name__ == '__main__':
    username = os.environ['MEDICOVER_USERNAME']
    password = os.environ['MEDICOVER_PASSWORD']

    m = Medicover()
    with m.logged_in(username, password), open('appointments.json', 'wb') as f:
        json.dump(m.get_appointments(), f, indent=4)
