from modules.user_input import Input
from modules.parse_mail_list import Parse_Mail_List
from modules.checker.checker import Checker


def main():
    threads, base_file_path, captcha_key = Input()
    mail_list = Parse_Mail_List(base_file_path)
    Checker(threads, mail_list, captcha_key)


if __name__ == '__main__':
    main()
