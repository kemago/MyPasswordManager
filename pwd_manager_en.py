#!/usr/bin/python python3
# **********************************************************************)
# * Programnév:       Password-manager app                             *)
# * Fájlnév:          pwd_manager_en.py                                *)
# * Verzió:           2.0                                              *)
# * Leírás:           Jelszó-menedzser program - fájlkezeléssel        *)
# * Készítette:       Kemenesi Ágoston                                 *)
# * Készítés dátuma:  2020.12.14.                                      *)
# * Utolsó módosítás: 2021.01.11.                                      *)
# *********************************************************************')

from random import randint
import time, json, os
import pandas as pd  # to format a json file

# ----------------- Variables ------------------

small = 'abcdefghijklmniopqrstuvwxyz'
large = small.upper()
numbers = '0123456789'
specials = '!@#&%^=+-_?'
password = ''
need_password = ''
accounts = {}

# ---------------- File management----------------
if os.path.exists('pwd.json'):
    with open('pwd.json') as source_file:
        accounts = json.load(source_file)
# e.g. {"Agoston Kemenesi" : {"username": "ago", "password": "1234"}}

# ----------------- Procedures --------------------
# Login or saving the master account
def login_to_my_system():
    print('######                                                   ')
    print('#     #   ##    ####   ####  #    #  ####  #####  #####  ')
    print('#     #  #  #  #      #      #    # #    # #    # #    # ')
    print('######  #    #  ####   ####  #    # #    # #    # #    # ')
    print('#       ######      #      # # ## # #    # #####  #    # ')
    print('#       #    # #    # #    # ##  ## #    # #   #  #    # ')
    print('#       #    #  ####   ####  #    #  ####  #    # #####  ')

    if os.path.exists('my_pwd.json'):
        with open('my_pwd.json') as source_file:
            my_account = json.load(source_file)

        print(' Password-manager application '.center(58, '='))
        print('Welcome in the app!')
        login_mode = input('Do you already have an account in this system? (y/n) ')

        # Login the app with exits account
        if login_mode == 'y':
            your_password = input('Please enter your password: ')

            while your_password != my_account['owner_password']:
                print('Password is invalid')
                your_password = input('Please enter your password: ')

            print(f"Welcome back to the system, {my_account['owner_name'].title()}!")

        # Create a new account
        if login_mode == 'n':
            master_name = input('Please choose a username: ')
            master_pwd = input('Please choose a password: ')

            my_account = {
                'owner_name': master_name,
                'owner_password': master_pwd
            }

            print('Saving data to database...')
            time.sleep(2)

            with open('my_pwd.json', 'w') as target_file:
                json.dump(my_account, target_file)
            # e.g.: {'owner_name': "kemago", 'owner_password': "password"}

def waiting_for_the_user():
    time.sleep(1)
    print('')
    input('Press ENTER to proceed!')
    print('')
    menus()

# The main menu of program
def menus():
    global menu
    print(' Password-manager application '.center(38, '='))
    print('=' * 4, ' [1] Password recording     ', '=' * 4)
    print('=' * 4, ' [2] Existing accounts      ', '=' * 4)
    print('=' * 4, ' [3] Generate a password    ', '=' * 4)
    print('=' * 4, ' [4] Modify master account  ', '=' * 4)
    print('=' * 4, ' [0] Exit                   ', '=' * 4)
    print('=' * 38)
    time.sleep(1)
    menu = int(input('Enter a number based on your preference [0-4]: '))

# ---------------- Main program ----------------
# administrator login to the program
login_to_my_system()

# display the main menu
menus()

while 0 <= menu <= 4:
    if menu == 1:
        print('')
        print('=' * 4, ' [1] Generate recording     ', '=' * 4)

        accounts_number = int(input('How many users do you record? '))

        for account in range(0, accounts_number): # we record the new data
            name = input('What is the real name of the user? ') # 	input name of the user
            username = input('What is the username of this user? ')  # input username of the user

            # insert generated password
            if need_password != '':  # paste a previously generated password
                do_i_insert = input('Paste the generated password? (y/n) ')
                if do_i_insert == 'y':
                    password = need_password
                    print(f'The pasted password: {password}')
                else:
                    password = input('Enter the password for the current user: ')
            else:
                password = input('What is the password for current user? ')  # read user password

            # write data to an external file
            accounts[name] = {
                'username': username,
                'password': password
            }

            print('')
            print('Saving data to database...')

            with open('pwd.json', 'w') as target_file:
                json.dump(accounts, target_file)

        waiting_for_the_user()

    if menu == 2:
        print('')
        print('=' * 4, ' [2] Recorded accounts      ', '=' * 4)

        # formatted display of data with pandas
        accounts = pd.read_json('pwd.json')
        print('')
        print(accounts.head())

        waiting_for_the_user()

    if menu == 3: # Based on: "Program Your Own Password Generator With Python" - In: https://zsecurity.org/ by SAI SATHVIK RUPPA
        print('')
        print('=' * 4, ' [3] Make a password        ', '=' * 4)

        character_stuff = small + large + numbers + specials
        password_length = int(input('Enter the length of password: '))

        # generate a secure password
        if password_length < 8:
            print('The password must be at least 8 characters long!')
            password_length = int(input('Enter the length of password: '))
        if password_length >= 8:
            password = ''
            length = 0
            while length < password_length:
                password = password + character_stuff[randint(0, len(character_stuff)-1)]
                length += 1
        print('Generated password is: ', password)
        print('')

        # save password for later use
        answer = input('Do you want to use this password? (y/n) ')
        if answer == 'y':
            need_password = password
        if answer == 'n':
            need_password = ''

        waiting_for_the_user()

    if menu == 4:  # Modify my account
        print('')
        print('=' * 4, ' [4] Modify master account ', '=' * 4)

        # reading datas from external file
        with open('my_pwd.json') as source_file:
            my_account = json.load(source_file)

        # enter the new datas
        master_name = input('Please enter your NEW username: ')
        master_pwd = input('Please enter your NEW password: ')

        my_account = {
            'owner_name': master_name,
            'owner_password': master_pwd
        }

        with open('my_pwd.json', 'w') as target_file:
            json.dump(my_account, target_file)

        print('')
        print('Saving data to database...')
        time.sleep(1)
        print('Password changed successfully!')

        waiting_for_the_user()

    if menu == 0:
        print('You are logged out.')
        time.sleep(1)
        break