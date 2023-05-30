import requests

def send_http_request(url, method="POST", headers={}, body={}, timeout=5.0):
    resp = None

    try:
        if method.lower() == "post":
            resp = requests.post(url, data=body, headers=headers, timeout=timeout)
        else:
            resp = requests.get(url, params=body, headers=headers)
    except Exception as e:
        print("Failed to send HTTP request.")
        print(e)

    return resp