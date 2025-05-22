from datetime import datetime, date
import random
db_file = open("db.txt", "r+")
data = {}
def file_to_dict(file_path, separator = ':'):
	data_dict = {}
	try:
		with open(file_path, 'r') as file:
			for line in file:
				line = line.strip()
				if line:
					key, value = line.split(separator, 1)
					data_dict[key.strip()] = value.strip()

	except FileNotFoundError:
		print('File not found')
		return {}

	except ValueError:
		print(f"Error: Invalid format in line : {line}. Ensure each line is separated by '{separator}'")
		return {}

	return data_dict

def create_account():
	print ('Welcome, we are happy to have you join us')
	first_name = input('first name:')
	last_name = input('last name:')
	DOB_str = input('Date of Birth (input in this format YYYY/MM/DD): ')
	DOB = datetime.strptime(DOB_str, '%Y/%m/%d').date()

	today = date.today()
	age = today.year - DOB.year - ((today.month, today.day) < (DOB.month, DOB.day))
	if age < 18:
		print('You are not allowed to open an account')
		exit()

	pin = input('input your desired pin:')
	if not any(char.isdigit() for char in pin):
		print('invalid input')
		exit()
	if len(pin)>4:
		print('pin cannot be greater than 4')
		exit()
	if len(pin)<4:
		print('pin cannot be lesser than 4')
		exit()

		

	check = False
	while check == False:
		num = [1,2,3,4,5,6,7,8,9,0]
		acc_num_list = ["5"]
		acc_num_list.extend([str(random.choice(num)) for _ in range(9)])
		acc_num = "".join(acc_num_list)

		data_dict = file_to_dict('db.txt')
		user = data_dict.get(acc_num)
		if user:
			check = False
		else:
			check = True

	deets = [('first_name', first_name),
			  ('last_name', last_name),
			  ('DOB', DOB_str),
			  ('pin', pin),
			  ('bal', 0)]

	data[acc_num] = dict(deets)
	acc_create = open('db.txt', 'a')
	acc_create.write(str(data))
	acc_create.close()
	print(f'Welcome {first_name}, your account number is {acc_num}')

def login():
	#feeling sleepy, would be back tomorrow
def interface():
	print("Welcome to Wemma Bank")
	print(" To create account enter 1\n To login enter 2 ")
	option = int(input("Enter option >"))

	if option == 1:
		create_account()

	if option == 2:
		login()

interface()
