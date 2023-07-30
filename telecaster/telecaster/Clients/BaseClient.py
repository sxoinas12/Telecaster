import requests


class BaseClient:
    def get(self, url):
        response = requests.get(url)
        if response and response.status_code == 200:
            return response.content
        else:
            print('Something went wrong')
            return response.status_code

    def post(self, url, body):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass
