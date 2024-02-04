#!/usr/bin/env python
import requests
import json
import os

from pytimedinput import timedInput
from getpass import getuser

from fake_useragent import UserAgent
from email_validator import validate_email 


# Code
def load_json(file: str) -> None:
    try:
        with open(file, 'r+') as json_file:
            return json.load(json_file)
            
    except:
        return {}


def dump_2_json(data: dict | str, file: str) -> None:
    file = file.split('/')
    for folder in file[:-1]:
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        os.chdir(folder)
    
    with open(file[-1], 'xt') as json_file:
        json.dump(data, json_file, indent=4)


def temp_mail(email: str, api: str) -> None:
    email = email.split('@')

    # Fetching single message: https://www.1secmail.com/api/v1/?action=readMessage&login=demo&domain=1secmail.com&id=639
    print(f'Hey {getuser()}. Waiting for messages\n')

    while True:
        ua = UserAgent().random
        messages = requests.get(api + f'getMessages&login={email[0]}&domain={email[1]}', json={'user-agent': ua}).json()

        if messages:
            print(f'Geted {len(messages)} New Messages\n')
            data = load_json(f'files/json/{getuser()}.json')

            for index, message in enumerate(messages):
                if input(f'{index+1}. Message from {message["from"]}. Show ? '):
                    full_message = requests.get(api + f'readMessage&login={email[0]}&domain={email[1]}&id={message["id"]}', json={'user-agent': ua}).json()
                    
                    # writing to json file
                    if message["from"] not in data:
                        data.update({message["from"]: [full_message]})
                    
                    # Checking if any current message in data
                    elif not any(message["id"] == data_message['id'] for data_message in data[message["from"]]):
                        data[message["from"]].append(full_message)

                    for name, value in full_message.items():
                        print(f'   {name}: {value}')
            
            # Dumping data to json  file
            dump_2_json(data, f'files/json/{getuser()}.json')

        key, successful = timedInput(f'Press \'q\' to exit: ', timeout=3)

        if not successful and key == 'q':
            exit()

        

    
if __name__ == '__main__':
    print(f'{" Temp-Mail ":=^65}\n')
    
    API: str = 'https://www.1secmail.com/api/v1/?action='
    # EMAIL: str = requests.get(API + 'genRandomMailbox', ).json()[0]
    EMAIL = 'gnpk0ky@txcct.com'
    
    print(f'Your Temp Email: {EMAIL}')

    validate_email(EMAIL)
    temp_mail(email=EMAIL, api=API)