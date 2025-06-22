from datetime import datetime, date
import random
import hashlib
import json
import os  
import time

DB_FILE = 'db.json'
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




def hashpin(pin):
	return hashlib.sha256(pin.encode()).hexdigest()

def create_account(data):
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
	save_data(data)
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


def login(data):
    acc_num = input('Please enter your account number: ')
    user = data.get(acc_num)
    
    if not user:
        print('No data found for account number entered')
        return

    pin_trials = 4 
    while pin_trials > 0:
        pin = input('Please enter your 4-digit PIN: ')
        if hashpin(pin) == user['pin']:
            print (f'welcome once again {user['first_name']}, your account balance is {user['bal']}')
            
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
	print("Welcome to Wemma Bank")
	print(" To create account enter 1\n To login enter 2 ")
	option = int(input("Enter option >"))

	if option == 1:
		create_account(data)

	if option == 2:
		login(data)

interface()
