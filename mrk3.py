import pandas as pd 


try:

	df = pd.read_csv("~/Documents/GitHub/ai-project/data.csv")
	for _ in df["username"]:
		print(_)

except:

	print("No Data Were Found")
	print("Creating New User")

	user = input("Enter username : ")
	passwd = input("Enter password : ")

	data = {"username" : [user],
			"password" : [passwd]}
	df = pd.DataFrame(data)
	df.to_csv("~/Documents/GitHub/ai-project/data.csv", index = False)