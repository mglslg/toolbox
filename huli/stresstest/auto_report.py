import requests


def report_me():
    url = "http://localhost:8080/saas-workflow/health/dbTest"
    data = {
        "number": 10
    }
    res = requests.post(url, data)
    print(res.json())


if __name__ == '__main__':
    report_me()
