import nltk
import os
from nltk import LancasterStemmer
stemmer=LancasterStemmer()
import numpy
import tflearn
import tensorflow as tf
import json
import random
import pickle
import win32com.client
from tkinter import *
from googlesearch import search
import webbrowser
from datetime import datetime, timedelta
from cal_setup import get_calendar_service
import mysql.connector as sq
import time
import math
import winsound


with open("intents.json") as file:
    data=json.load(file)

try:
   with open("data.pickle","rb")as f:
      words,labels,training,output=pickle.load(f)


except: 
     
   words=[]
   labels=[]
   docs_x=[]
   docs_y=[]

   for i in data["intents"]:    
      
      for pattern in i["patterns"]:
         wrds=nltk.word_tokenize(pattern)
         words.extend(wrds)
         docs_x.append(wrds)
         docs_y.append(i["tag"])

      if i["tag"] not in labels:
         labels.append(i["tag"])

   words=[stemmer.stem(w.lower())for w in words if w not in "?"]
   words=sorted(list(set(words)))
   labels=sorted(labels)
   training=[]
   output=[]
   out_empty=[0 for _ in range(len(labels))]
   
   for x,doc in enumerate(docs_x):
      bag=[]
      wrds=[stemmer.stem(w)for w in doc]
      
      for w in words:
         if w in wrds:
            bag.append(1)
         else:
            bag.append(0)
      
      output_row=out_empty[:]
      output_row[labels.index(docs_y[x])]=1
      training.append(bag)
      output.append(output_row)
   
   training=numpy.array(training)
   output=numpy.array(output)

with open("data.pickle","wb")as f:
   pickle.dump((words,labels,training,output),f)

tf.reset_default_graph()
net=tflearn.input_data(shape=[None,len(training[0])])
net=tflearn.fully_connected(net, 8)
net=tflearn.fully_connected(net, 8)
net=tflearn.fully_connected(net,len(output[0]),activation="softmax")
net=tflearn.regression(net)
model=tflearn.DNN(net)

try:
   model.load("model.tflearn")
except:
   model.fit(training,output,n_epoch=1000,batch_size=8,show_metric=True)
   model.save("model.tflearn")

def alarm():

   def countdown(count):     
      seconds=math.floor(count%60)
      minutes=math.floor((count/60)%60)
      hours=math.floor((count/3600))
      label['text'] ="Hours: "+ str(hours)+ " Minutes:  " +str(minutes)+ " Seconds: " +str(seconds)

      if count >= 0:
          top.after(1000, countdown,count-1)
      
      else:
          for x in range(3):
              winsound.Beep(1000,1000)
          label['text']="Time is up!"
       
        
   def updateButton():
      hour,minute,sec=hoursE.get(),minuteE.get(),secondE.get()
   
      if hour.isdigit() and minute.isdigit() and sec.isdigit():
          time=int(hour)*3600+int(minute)*60+int(sec)
          countdown(time)
        
   top = tkinter.Tk()
   top.geometry("250x150")
   
   hoursT=tkinter.Label(top, text="Hours:")
   hoursE=tkinter.Entry(top)
   minuteT=tkinter.Label(top, text="Minutes:")
   minuteE=tkinter.Entry(top)
   secondT=tkinter.Label(top, text="Seconds:")
   secondE=tkinter.Entry(top)
   
   hoursT.grid(row=1,column=1)
   hoursE.grid(row=1,column=2)
   minuteT.grid(row=2,column=1)
   minuteE.grid(row=2,column=2)
   secondT.grid(row=3,column=1)
   secondE.grid(row=3,column=2)
   label = tkinter.Label(top)
   label.grid(row=5,column=2)

   button=tkinter.Button(top,text="Start Timer",command=updateButton)
   button.grid(row=4,column=2)

   top.mainloop()



def aud(l):
   speaker = win32com.client.Dispatch("SAPI.SpVoice")
   speaker.Speak(l)



def calci():
   expression = ""  
   
   def press(num): 
      global expression
      expression = expression + str(num)
      equation.set(expression)  
   
   def equalpress():
      try:
         global expression 
         total = str(eval(expression)) 
         equation.set(total)
         expression = ""  
      except:
         equation.set(" error ") 
         expression = ""  

   def clear():
      global expression
      expression = ""
      equation.set("") 
   if __name__ == "__main__":
      gui = Tk()
      gui.configure(background="light green")
      gui.title("Simple Calculator")
      gui.geometry("265x125")
      
      equation = StringVar()
      expression_field = Entry(gui, textvariable=equation)
      expression_field.grid(columnspan=4, ipadx=70)
      equation.set('enter your expression')
      
      button1 = Button(gui, text=' 1 ', fg='black', bg='white', 
               command=lambda: press(1), height=1, width=7)
      button1.grid(row=2, column=0) 
      button2 = Button(gui, text=' 2 ', fg='black', bg='white', 
               command=lambda: press(2), height=1, width=7)
      button2.grid(row=2, column=1) 
      button3 = Button(gui, text=' 3 ', fg='black', bg='white', 
               command=lambda: press(3), height=1, width=7)
      button3.grid(row=2, column=2)
      button4 = Button(gui, text=' 4 ', fg='black', bg='white', 
               command=lambda: press(4), height=1, width=7)
      button4.grid(row=3, column=0)
      button5 = Button(gui, text=' 5 ', fg='black', bg='white', 
               command=lambda: press(5), height=1, width=7)
      button5.grid(row=3, column=1)
      
      button6 = Button(gui, text=' 6 ', fg='black', bg='white', 
               command=lambda: press(6), height=1, width=7)
      button6.grid(row=3, column=2)
      button7 = Button(gui, text=' 7 ', fg='black', bg='white', 
               command=lambda: press(7), height=1, width=7)
      button7.grid(row=4, column=0)
      button8 = Button(gui, text=' 8 ', fg='black', bg='white', 
               command=lambda: press(8), height=1, width=7)
      button8.grid(row=4, column=1)
      button9 = Button(gui, text=' 9 ', fg='black', bg='white', 
               command=lambda: press(9), height=1, width=7)
      button9.grid(row=4, column=2)
      button0 = Button(gui, text=' 0 ', fg='black', bg='white', 
               command=lambda: press(0), height=1, width=7)
      button0.grid(row=5, column=0)
      
      plus = Button(gui, text=' + ', fg='black', bg='white', 
            command=lambda: press("+"), height=1, width=7)
      plus.grid(row=2, column=3)
      minus = Button(gui, text=' - ', fg='black', bg='white', 
            command=lambda: press("-"), height=1, width=7)
      minus.grid(row=3, column=3)
      multiply = Button(gui, text=' * ', fg='black', bg='white', 
               command=lambda: press("*"), height=1, width=7)
      multiply.grid(row=4, column=3)
      divide = Button(gui, text=' / ', fg='black', bg='white', 
               command=lambda: press("/"), height=1, width=7)
      divide.grid(row=5, column=3)
      equal = Button(gui, text=' = ', fg='black', bg='white', 
            command=equalpress, height=1, width=7)
      equal.grid(row=5, column=2)
      clear = Button(gui, text='Clear', fg='black', bg='red', 
            command=clear, height=1, width=7)
      clear.grid(row=5, column='1')
      gui.mainloop()



def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]
    s_words=nltk.word_tokenize(s)
    s_words=[stemmer.stem(word.lower())for word in s_words]
    
    for se in s_words:
    
        for i,w in enumerate(words):
             if w == se:
                 bag[i]=1
    return numpy.array(bag)



def create_event():
   # creates one hour event tomorrow 10 AM IST
   x=int(input("Enter from 00 to 23"))
   service = get_calendar_service()
   d = datetime.now().date()
   a=int(input("How many danys from now \'0 for today\'"))
   tomorrow = datetime(d.year, d.month, d.day,x)+timedelta(a)
   start = tomorrow.isoformat()
   end = (tomorrow + timedelta(hours=1)).isoformat()

   event_result = service.events().insert(calendarId='primary',
       body={
           "summary": 'Automating calendar',
           "description": 'This is a tutorial example of automating google calendar with python',
           "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
           "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
       }
   ).execute()

   print("created event")
   print("id: ", event_result['id'])
   print("summary: ", event_result['summary'])
   print("starts at: ", event_result['start']['dateTime'])
   print("ends at: ", event_result['end']['dateTime'])



def tasks():
   print("What do you want me to do?? :) \n1. Add to list\n2. Read the list\n3. Remove from list")
   x=input("..")
   
   if x=="1"or x=="add":
      ri=input("What should I add? ")
      with open("todo.txt","a")as f:
         f.write(ri+"\n")
   
   elif(x=="2"or x=="read"):
      with open("todo.txt","r")as f:
         ri=f.read()
         if ri==" ":
            ri="nothing here"
         print(ri)      
   
   elif(x=="3"or x=="remove"):
      f=open("todo.txt","r")
      ri=f.readlines()
   
      for i in range(0,len(ri)):
         print(i,ri[i])
      az=input("Which one should i remove") 
      f.close()
      f=open("temp.txt","w")
   
      for i in range(1,len(ri)):
         if i==az:
            continue
         else:
            f.write(ri[i])
      f.close()
      os.remove("todo.txt")
      os.rename("temp.txt","todo.txt")
      print("done")                 



def webs(query):
   i=1 
   history=[] 
   
   for j in search(query,num=10, stop=8, pause=2): 
       print(i,". ",j)
       i+=1
       history.append(j)
   ur=int(input("no."))
   
   if ur==0:
       return
   else:        
       url=history[ur-1]
       webbrowser.open_new(url)



def user_details():
   import mysql.connector as sq
   mydb = sq.connect(host="localhost",user="root",password="Saturday7",database="sys") 
   
   if mydb.is_connected()==False:
       print("Error connecting to mysql database")
   
   else:
       cursor=mydb.cursor()
       name=input("name")
       pho=input("phone_no.")
       ri="insert into users(name,phone_no)values("
       a="\""+name+"\""+","+pho+")"
       rias=ri+a
       #"\"john\",5239556)"
       cursor.execute(rias)
       mydb.commit()



def user_history():
   import mysql.connector as sq
   mydb = sq.connect(host="localhost",user="root",password="Saturday7",database="sys")
   cursor=mydb.cursor()
   cursor.execute("select * from users")
   data=cursor.fetchall()
   
   for i in data:
      print(i)   




def chat():
   print("User details required first")
   user_details()
   print("Start talking with the bot")
   while True:
      inp=input("You: ")
      import speech_recognition as sr
      if inp==" ":
         r=sr.Recognizer()
         with sr.Microphone() as source:
            print("Speak:")
            audio=r.listen(source)
         try:
            print(r.recognize_google(audio))
            inp=r.recognize_google(audio)
            results=model.predict([bag_of_words(inp,words)])[0]
            results_index=numpy.argmax(results)
            tag=labels[results_index]
            if results[results_index] >= 0.9:
       
               for tg in data["intents"]:
       
                  if tg["tag"]==tag:
                     responses=tg["responses"]  
                     a=(random.choice(responses))
                     aud(a)
                     print(a)
       
                     if tag == "goodbye":
                        exit()
         
                     elif tag == "alarm":
                        alarm()
         
                     elif tag == "calculator":
                        calci()
         
                     elif tag=="web":
                        webs()
         
                     elif tag=="todo":
                        tasks()      
         
                     elif tag=="users":
                        user_history() 
         
                     elif tag=="remainder":
                         create_event()
      
            else:
                x=("I dont have an answer for it but i will find it for you")    
                aud(x)
                print(x)
                webs(inp)         
         except:
            pass
      else:
          results=model.predict([bag_of_words(inp,words)])[0]
          results_index=numpy.argmax(results)
          tag=labels[results_index]
          
       
          if results[results_index] >= 0.9:
       
             for tg in data["intents"]:
       
               if tg["tag"]==tag:
                   responses=tg["responses"]  
                   a=(random.choice(responses))
                   aud(a)
                   print(a)
       
                   if tag == "goodbye":
                      exit()
       
                   elif tag == "alarm":
                      alarm()
       
                   elif tag == "calculator":
                      calci()
       
                   elif tag=="web":
                      webs()
       
                   elif tag=="todo":
                      tasks()      
       
                   elif tag=="users":
                      user_history() 
       
                   elif tag=="remainder":
                       create_event()
      
          else:
              x=("I dont have an answer for it but i will find it for you")    
              aud(x)
              print(x)
              webs(inp)
chat()     