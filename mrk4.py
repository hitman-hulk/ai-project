import pandas as pd 
import re


df = pd.read_csv("~/Documents/GitHub/ai-project/data.csv")

while(True):
	name = input("Enter username : ")

	if name in df["username"]:
		print("User existing")
		print("Make Changes")

	else:
		print("Username Available")
		break

while(True):
	count = 0
	passwd = input("Enter password : ")

	if len(passwd) > 7 and len(passwd) < 17:
		count += 1

	else:
		print("Password length must be in between 8 and 16")

	if bool(re.match(r'\w*[A-Z]\w*', test_str)):
		count += 1

	else:
		print("Password doesn't contain any Uppercase Character")

	if bool(re.search(r'\d', str1)):
		count += 1

	else:
		print("Password doesn't contain any Numbers")

	if count == 3:
		break

	else:
		print("Make Corrections")

data = pd.DataFrame([{
						"username" : name,
						"password" : passwd,
	}])

df = pd.concat([df, data], ignore_index = True)
df.to_csv("~/Documents/GitHub/ai-project/data.csv", index = False)