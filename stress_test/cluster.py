"""

Code adapted from https://github.com/Anaconda-Platform/ae5_controller

"""
from lxml import html
from os.path import basename


import requests


requests.packages.urllib3.disable_warnings()


class AECluster(object):
    request_args = dict(verify=False, allow_redirects=True)

    def __init__(self, host):
        self.host = host
        self._logged_in = False

    def login(self, username='anaconda-enterprise',
              password='anaconda-enterprise'):

        self.session = requests.Session()
        url = (
            f'https://{self.host}/auth/realms/AnacondaPlatform/protocol/'
            'openid-connect/auth?client_id=anaconda-platform&scope=openid+'
            'email+offline_access&response_type=code&redirect_uri='
            f'https%3A%2F%2F{self.host}%2Flogin'
        )
        r = self.session.get(url, **self.request_args)
        tree = html.fromstring(r.text)
        form = tree.xpath("//form[@id='kc-form-login']")

        login_url = form[0].action

        data = {'username': username, 'password': password}
        r = self.session.post(login_url, data=data, **self.request_args)

        headers = {'x-xsrftoken': r.cookies['_xsrf']}
        self.session_args = {'headers': headers, 'cookies': r.cookies}

        self._logged_in = True

    def sessions(self):
        url = f"https://{self.host}/api/v2/sessions"
        response = self.session.get(
            url,
            **self.session_args,
            **self.request_args
        )
        return response.json()

    def stop_session(self, session_id):
        self.session.delete(
            f'https://{self.host}/api/v2/sessions/{session_id}',
            **self.session_args,
            **self.request_args
        )

    def deployments(self):
        url = f"https://{self.host}/api/v2/deployments"

        response = self.session.get(
            url,
            **self.session_args,
            **self.request_args
        )
        return response.json()

    def stop_deployments(self, deployment_id):
        url = f"https://{self.host}/api/v2/deployments/{deployment_id}"

        response = self.session.delete(
            url,
            **self.session_args,
            **self.request_args
        )
        return response.json()

    def upload_project(self, project_archive, name=None):
        url = f'https://{self.host}/api/v2/projects/upload'

        if name is None:
            name = basename(project_archive).split('.', 1)[0]

        with open(project_archive, 'rb') as f:
            response = self.session.post(
                url,
                files={'project_file': f},
                data={'name': name},
                **self.session_args,
                **self.request_args
            )

        return response

    def _get(self, endpoint, **kwargs):
        response = self.session.get(
            f'https://{self.host}/api/v2/{endpoint}',
            **kwargs,
            **self.session_args,
            **self.request_args)

        return response

    def _delete(self, endpoint, **kwargs):
        response = self.session.delete(
            f'https://{self.host}/api/v2/{endpoint}',
            **kwargs,
            **self.session_args,
            **self.request_args)

        return response

    def _post(self, endpoint, **kwargs):
        response = self.session.post(
            f'https://{self.host}/api/v2/{endpoint}',
            **kwargs,
            **self.session_args,
            **self.request_args)

        return response

    def _put(self, endpoint, **kwargs):
        response = self.session.put(
            f'https://{self.host}/api/v2/{endpoint}',
            **kwargs,
            **self.session_args,
            **self.request_args)

        return response

    def _patch(self, endpoint, **kwargs):
        response = self.session.patch(
            f'https://{self.host}/api/v2/{endpoint}',
            **kwargs,
            **self.session_args,
            **self.request_args)

        return response
