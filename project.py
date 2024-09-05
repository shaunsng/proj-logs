#!/usr/bin/env python3

# importing time library to use sleep for readability.  

import time

# Read var/log/auth.log. Open with readlines. List format facilitates parsing. 
# Commented out earlier test auth2.log.
# raw = open("auth2.log", 'r')

raw = open("/var/log/auth.log", 'r')
data = raw.readlines()

def trim_date(stamp):
	date = stamp.split('T')[0]
	day = date[8:10]
	month = date [5:7]
	year = date[0:4]
	time= stamp.split('T')[1][0:8]
	
	cleaned = day + "-" + month + "-" + year + " " + time
	
	return cleaned

# Output to screen to show user script is running. 

print("\n")
print("1. Checking for executed commands:\n") 
time.sleep(1)

# Extracting record of commands executed, by searching for 'COMMAND' keyword.
# Processing each line twice into x and y variable. 
# Split using 'COMMAND=' easier to extract command.
# Split without arguments facilitates slicing to get Timestamp and User. 

for line in data:
	if 'COMMAND' in line:
		y = line.split()
		x = line.split('COMMAND=')
		full_command=x[-1][:-1]
		exec_user=y[3]
		exec_date=trim_date(y[0])
		
		# Print results in sentence for readability, highlighting key info.
		print(f"User \033[1m{exec_user}\033[0m executed the command:\033[96m{full_command}\033[0m on \033[1m{exec_date}\033[0m")
				
# Prompt user again, to also slow down the output. 

print("\n")
print("2. Checking for newly added users:\n") 
time.sleep(1)

# Straightforward check for newly added user by searching for keyphrase 'new user'.

for line in data:
	if 'new user' in line:
		line=line.split()
		new_user=line[5][5:-1]
		new_date=trim_date(line[0])
		print(f"New user \033[96m{new_user}\033[0m was added on \033[1m{new_date}\033[0m")


# Usual prompt for each stage. 

print("\n")
print("3. Checking for deleted users:\n") 
time.sleep(1)

# Extracting log record of deleted users, using keyphrase 'delete user'.

for line in data:
	if 'delete user' in line:
		line=line.split()
		# The log format for deleted user has quotation marks. Quick slicing to remove quotes.
		deleted_user=line[-1][1:-1]
		del_date=trim_date(line[0])
		print(f"User \033[96m{deleted_user}\033[0m was deleted on \033[1m{del_date}\033[0m")

# Usual prompt for each stage. 

print("\n")
print("4. Checking for password change:\n") 
time.sleep(2)

# Extracting log record of password change using keyphrase 'password changed'.
 
for line in data:
	if 'password changed' in line:
		line=line.split()
		pass_user=line[-1]
		pass_date=trim_date(line[0])
		print(f"Password was changed for user \033[96m{pass_user}\033[0m on \033[1m{pass_date}\033[0m")

# Usual prompt for each stage. 

print("\n")
print("5. Checking for use of su command:\n") 
time.sleep(1)

# List of keywords to narrow the search, extract only one line per SU command. Drop other "duplicate" lines related to the same 	. 
su_success=['su','to']

print("Successful SU command execution are:\n")

for line in data:
	# checking if all keywords appear in line. 
	if all(x in line for x in su_success):
		# filtering out the failed attempts
		if 'FAILED' not in line:
			line=line.split()
			# print(line)
			start = line[-3]
			target = line[-4][:-1]
			su_time=trim_date(line[0])
			print(f"From user \033[96m{start}\033[0m to user \033[1m{target}\033[0m on {su_time}")

# Another prompt, slow down to check failed SU attempts. 

time.sleep(2)
print("\n")
print("Unsuccessful SU attempts were:\n")

# Extracting unsuccessful SU using keyphrase 'FAILED SU'.

for line in data:
	if 'FAILED SU' in line:
		line=line.split()
		# print(line)
		start = line[-3]
		target = line[-4][:-1]
		su_time=trim_date(line[0])
		print(f"From user \033[96m{start}\033[0m to user \033[1m{target}\033[0m on {su_time}")


# Prompt for last batch of SUDO command. 
		
print("\n")
print("5. Checking for use of SUDO command:\n") 
time.sleep(2)

# Similar to SU section. List of keywords to check for both successful (good) and failed (bad) SUDO command execution. 
sudo_good =['sudo','COMMAND']
sudo_bad =['sudo','incorrect password']

print("Following users and commands were successfully executed with SUDO privilege:\n") 

# Extracting successful SUDO execution.
for line in data:
	if all(x in line for x in sudo_good):
		y = line.split()
		x = line.split('COMMAND=')
		sudo_command=x[-1][:-1]
		exec_user=y[3]
		sudo_time=trim_date(y[0])
		print(f"User \033[96m{exec_user}\033[0m executed sudo \033[1m{sudo_command}\033[0m on {su_time}")

print("\n")
print("Failed execution of SUDO commands were:\n") 
time.sleep(2)

# Extracting failed SUDO execution.
for line in data:
	if all(x in line for x in sudo_bad):
		# print(line)
		y = line.split()
		x = line.split('COMMAND=')
		sudo_command=x[-1][:-1]
		exec_user=y[3]
		sudo_time=trim_date(y[0])
		print(f"\033[31mALERT!\033[0m User \033[96m{exec_user}\033[0m attempted to execute sudo \033[1m{sudo_command}\033[0m on {su_time} with incorrect password.")
		
