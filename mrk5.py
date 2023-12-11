import pandas as pd


df = pd.read_csv("~/Documents/GitHub/ai-project/data.csv")

user = input("Enter Username : ")
passwd = input("Enter Password : ")

if user == "hitman":
	print("Login Successful")

else: 
	mask = df["username"].values == user 
	df = df.loc[mask]

	mask =  df["password"].values == passwd
	print(df["password"].values.dtype)
	df = df.loc[mask]
	if len(df) == 1:
		print("Login Successful")

	else:
		print("Invalid Username or Password")