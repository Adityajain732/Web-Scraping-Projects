import os
import shutil
import time
import math

names = ['LINKS','RECORDS']
high = 1/(1+math.exp(-2))

def confidence_level(c,o):
        if(c>=o):
                level = 1/(1+math.exp(-(c/o)))
        else:
                level = 1/(1+math.exp(-(o/c)))
                if(o/c<=2):
                        level = (o/c-2)*(high-0.5)+ high
        return str(level*100)[:5]+' %'

def delete_all_files_in_folder(folder):
	for file in os.listdir(folder):
		file_path = os.path.join(folder,file)
		os.remove(file_path)
def ask_input():
	answer = input()
	if(answer.lower() in ['yes','no']):
		return answer
	else:
		print('INVALID CHOICE........please choose from......(yes/no)',end='---->')
		return ask_input()

def version_control(name):
	time.sleep(2)
	print(f'\n\nVersion Manager started for {name.lower()}.csv')
	if(os.path.isfile(f'..\\DATA\\EXHIBITION {name}\\CURRENT VERSION\\{name.lower()}.csv')):
		current_size = os.path.getsize(f'..\\DATA\\EXHIBITION {name}\\CURRENT VERSION\\{name.lower()}.csv')
	else:
		current_size = 0
	if(os.path.isfile(f'..\\DATA\\EXHIBITION {name}\\OLDER VERSION\\{name.lower()}.csv')):
		older_size = os.path.getsize(f'..\\DATA\\EXHIBITION {name}\\OLDER VERSION\\{name.lower()}.csv')
	else:
		older_size = 0
	print('-'*80)
	print(f'{name.lower()}.csv current version size = {current_size} Bytes')
	print(f'{name.lower()}.csv older version size = {older_size} Bytes')
	print('-'*80)
	time.sleep(2)
	if(older_size==0 and current_size==0):
		decision = 'NOT UPDATE'
		print(f'Nothing to do since there is no file {name.lower()}.csv in OLDER and CURRENT VERSION')
	elif(older_size==0):
		decision = 'UPDATE'
		print(f'BOT\'s Decision is to UPDATE since there is no file {name.lower()}.csv in OLDER VERSION')
	elif(current_size==0):
		decision = 'NOT UPDATE'
		print(f'BOT\'s decision is to NOT UPDATE since there is no file {name.lower()}.csv in CURRENT VERSION')
	else:
		if(current_size>=older_size):
			decision = 'UPDATE'
			print(f'BOT\'s Decision is to UPDATE OLDER VERSION of {name.lower()}.csv with confidence_level = {confidence_level(current_size,older_size)}')
			print(f'Would prefer to NOT UPDATE instead...............(yes/no)',end='---->')
			answer = ask_input()
			print(f'Input Recorded : {answer}')
			if(answer=='yes'):
				decision = 'NOT UPDATE'
		else:
			decison = 'NOT UPDATE'
			print(f'BOT\'s decision is to NOT UPDATE OLDER VERSION {name.lower()}.csv with confidence_level = {confidence_level(current_size,older_size)}')
			print(f'Would Prefer to UPDATE instead...............(yes/no)',end='---->')
			answer = ask_input()
			print(f'Input Recorded : {answer}')
			if(answer=='yes'):
				decision = 'UPDATE'
		time.sleep(1)
		print(f'You chose to ---> {decison}')

	if(decision == 'UPDATE'):
		print('-'*80)
		time.sleep(2)
		print('Deleting all files in OLDER VEERSION')
		delete_all_files_in_folder(f'..\\DATA\\EXHIBITION {name}\\OLDER VERSION')
		time.sleep(1)
		print('Moving files from CURRENT VERSION to OLDER VERSION')
		if current_size!=0:
			shutil.move(f'..\\DATA\\EXHIBITION {name}\\CURRENT VERSION\\{name.lower()}.csv',f'..\\DATA\\EXHIBITION {name}\\OLDER VERSION')
		time.sleep(1)
		print(f'Deleting all files in CURRENT VERSION for fresh StartUp')
		delete_all_files_in_folder(f'..\\DATA\\EXHIBITION {name}\\CURRENT VERSION')
		print('-'*80)
	else:
		print('-'*80)
		time.sleep(2)
		print(f'Deleting all files in CURRENT VERSION for fresh StartUp')
		delete_all_files_in_folder(f'..\\DATA\\EXHIBITION {name}\\CURRENT VERSION')
		print('-'*80)

for name in names:
	version_control(name)
