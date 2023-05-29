import requests

def send_http_request(url, method="POST", headers={}, body={}):
    resp = None

    if method.lower() == "post":
        resp = requests.post(url, data=body, headers=headers)
    else:
        resp = requests.get(url, data=body, headers=headers)

    return resp