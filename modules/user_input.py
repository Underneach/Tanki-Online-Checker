import os


def Input():

    while True:
        threads = '1'#input('\nВведите количетсво потоков: ')
        if threads:
            break
        else:
            print('Введите количетсво потоков: ')

    while True:
        base_file_path = 'Order12016279.txt'#input('\nВведите путь к базе с аккаунтами: ')
        if os.path.exists(base_file_path):
            break
        else:
            print('Файл не найден, введите путь еще раз: ')
    while True:
        captcha_key = 'e51ef23cb636b838cbb5a4ac6aa7dd2d'#input('\nВведите ключ от Captcha Guru: ')
        if captcha_key:
            break
        else:
            print('Введите ключ от Captcha Guru: ')

    return int(threads), base_file_path, captcha_key
