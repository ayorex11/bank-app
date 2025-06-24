from datetime import datetime, date
import random
import hashlib
import json
import os  
import time

DB_FILE = 'db.json'
TRANSACTION_FILE = 'transaction.json'


def load_data():
	if not os.path.exists(DB_FILE):
		return{}

	try:
		with open (DB_FILE, 'r') as file:
			return json.load(file)
	except json.JSONDecodeError:
		print ('Warning:  File corrupted or empty. starting fresh')
		return {}

def save_data(data):
	with open(DB_FILE, 'w') as file:
		json.dump(data, file, indent=4)


def load_transaction_data():
	if not os.path.exists(TRANSACTION_FILE):
		return{}

	try:
		with open (TRANSACTION_FILE, 'r') as file:
			return json.load(file)
	except json.JSONDecodeError:
		print ('Warning:  File corrupted or empty. starting fresh')
		return {}

def save_transaction_data(data):
	with open(TRANSACTION_FILE, 'a') as file:
		json.dump(data, file, indent=4)

def hashpin(pin):
	return hashlib.sha256(pin.encode()).hexdigest()

def create_account(data, data2):
	print ('Welcome, we are happy to have you join us')
	first_name = input('first name:')
	last_name = input('last name:')
	DOB_str = input('Date of Birth (input in this format YYYY/MM/DD): ')
	DOB = datetime.strptime(DOB_str, '%Y/%m/%d').date()

	today = date.today()
	age = today.year - DOB.year - ((today.month, today.day) < (DOB.month, DOB.day))
	if age < 18:
		print('You are not allowed to open an account')
		return

	pin = input('input your desired pin:')
	if not any(char.isdigit() for char in pin):
		print('invalid input')
		return
	if len(pin)>4:
		print('pin cannot be greater than 4')
		return
	if len(pin)<4:
		print('pin cannot be lesser than 4')
		return

	hashedpin = hashpin(pin)
		
	while True:
		num = [1,2,3,4,5,6,7,8,9,0]
		acc_num_list = ["5"]
		acc_num_list.extend([str(random.choice(num)) for _ in range(9)])
		acc_num = "".join(acc_num_list)

		if acc_num not in data:
			break


	deets = {'first_name': first_name,
			  'last_name': last_name,
			  'DOB': DOB_str,
			  'pin': hashedpin,
			  'bal': 0
			}

	data[acc_num] = deets
	data2[acc_num] = {}
	save_data(data)
	save_transaction_data(data2)

	print(f'Welcome {first_name}, your account number is {acc_num}')
	print('To login to your account, enter 1')
	print('To close the app enter any other number')
	try:
		option = int(input("Enter option >"))
	except ValueError:
		print('invalid input')
		return
	if option == 1:
		login(data)
	else:
		print ('logging out...')
		time.sleep(3)
		print('you have been successfully logged out')
		return 


def login(data, data2):
    acc_num = input('Please enter your account number: ')
    user = data.get(acc_num)
    transaction = data2.get(acc_num)
    
    if not user:
        print('No data found for account number entered')
        return

    pin_trials = 4 
    while pin_trials > 0:
        pin = input('Please enter your 4-digit PIN: ')
        if hashpin(pin) == user['pin']:
            print (f'welcome once again {user['first_name']}, your account balance is #{user['bal']}')
            while True:
            	print("""\nTo check account balance, enter 1
            	To deposit money, enter 2
            	To transfer money, enter 3 
            	To withdraw money, enter 4
            	To logout, enter 5""")
            	try:
            		option = int(input('Enter an option \n >'))
            	except ValueError:
            		print('Invalid Input')

            	if option == 1:
            		pin = input('Please enter your pin to confirm \n >')
            		if hashpin(pin) == user['pin']:
            			print (f'Your account balance is #{user['bal']}')

            	elif option == 2:
            		try:
            			amount = int(input('Please enter amount you wish to deposit \n >'))
            		except ValueError:
            			print('Invalid Input')
            			return
            		data[acc_num]['bal'] += amount
            		save_data(data)
            		time = str(datetime.now())

            		deets = {'details': 'You money has been successfully deposited',
            				'amount':amount,
            				'Time' : time}

            		data2[acc_num] = deets
            		save_transaction_data(data2)
            		print(f'You have successfully deposited #{amount} into your account')
            
            
            return
        else:
            pin_trials -= 1
            if pin_trials > 0:
                print(f'Incorrect PIN. You have {pin_trials} attempt(s) left. Please try again.')
            else:
                print('Too many failed attempts. Access denied.')
                return



def interface():
	data = load_data()
	data2 = load_transaction_data()
	print("Welcome to Wemma Bank")
	print(" To create account enter 1\n To login enter 2 ")
	option = int(input("Enter option >"))

	if option == 1:
		create_account(data, data2)

	if option == 2:
		login(data, data2)

interface()
