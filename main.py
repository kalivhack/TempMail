#!/usr/bin/python
from time import sleep
from colorama import Fore
import requests
import string
import random


# Variables
API = 'https://www.1secmail.com/api/v1/'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'}
domains = requests.get(API + '?action=getDomainList', headers=headers).json()
json_data = " \"from\": \"{e_from}\",\n \"subject\": \"{sub}\",\n \"date\": \"{date}\",\n \"body\": \"{body}\",\n \"htmlBody\": \"{h_body}\""
letters = string.ascii_letters

# Generating mail from random symbols
def generate_mail():
    username = "".join(letters[random.randint(0, len(letters) - 1)]
                       for i in range(15))

    return f"{username}@{random.choice(domains)}"


# Check Message Count And return comma if that > 1...
def check_comma(msg_len, inter_n):
    if msg_len > 1 and inter_n < msg_len:
        return ','
    return ''


# Geting Message From Mail
def get_messages(email):
    print(f'{Fore.LIGHTCYAN_EX}[ INFO ] Waiting For Messages \n')
    while True:
        msg_n = 0
        messages = requests.get(
            API + f'?action=getMessages&login={email.split("@")[0]}&domain={email.split("@")[1]}', headers=headers).json()

        if len(messages) > 0:
            print(f'{Fore.LIGHTGREEN_EX}[ + ]', len(messages), 'Message(s) Geted')

            with open('messages/messages.json', 'w+') as messages_json:
                messages_json.write('[')
                for message in messages:
                    i_message = requests.get(
                        API + f'https://www.1secmail.com/api/v1/?action=readMessage&login={email.split("@")[0]}&domain={email.split("@")[1]}&id={message["id"]}', headers=headers).json()
                    
                    i_message['body'] = i_message['body'].replace('"', '\\"')
                    i_message['htmlBody'] = i_message['htmlBody'].replace('"', '\\"')

                    print(
                        f"{Fore.LIGHTMAGENTA_EX}[ MESSAGE ][ + ] id {i_message['id']}: Message Geted From {i_message['from']} in {i_message['date']}")

                    messages_json.write("\n{\n" + json_data.format(e_from=i_message['from'], sub=i_message['subject'],
                                                                   date=i_message['date'], body=i_message['body'].split('\n')[0], h_body=i_message['htmlBody'].split('\n')[0]) + f"\n}}{check_comma(len(messages), msg_n + 1)}")
                    
                    msg_n += 1
                print('\n')

            with open('messages/messages.json', 'a+') as messages_json:
                messages_json.write('\n]')

        sleep(10)


def main():
    try:
        mail = generate_mail()
        print(f'{Fore.LIGHTGREEN_EX}[ + ] Temp Mail Successfully Generated: {mail}')
        get_messages(mail)

    except:
        print(f' {Fore.LIGHTRED_EX}Error happened in proccess')
        exit()


if __name__ == '__main__':
    main()
