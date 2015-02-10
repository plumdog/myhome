import requests

URL = 'https://raw.githubusercontent.com/plumdog/project_euler/master/answers.txt'

def count():
    r = requests.get(URL)
    s = r.content.decode('utf-8').strip()
    if s != 'Not Found':
        return len(s.split())
    else:
        return None
