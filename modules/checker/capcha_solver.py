import httpx
import time


def Capcha_Solver(captcha_key):
    with httpx.Client() as client:
        response = client.post(
            url='http://api.captcha.guru/in.php',
            headers={'Content-Type': 'application/json'},
            json={
                "key": captcha_key,
                "method": "userrecaptcha",
                "googlekey": "6LeV5AITAAAAAI3U1V8jsU-bsPuSqjKa4th1Zy7a",
                "pageurl": "https://ru.tankiforum.com/login/",
                "json": 1
            }
        )
        request_id = response.json()['request']
        time.sleep(5)

        while True:
            response = client.post(
                url=f'http://api.captcha.guru/res.php',
                headers={'Content-Type': 'application/json'},
                json={
                    "key": captcha_key,
                    "action": "get",
                    "id": request_id,
                    "json": 1
                }
            )
            if response.json()['request'] == 'CAPCHA_NOT_READY':
                time.sleep(5)
            else:
                return response.json()['request']
