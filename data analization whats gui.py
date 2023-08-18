from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from collections import Counter
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import emoji
import regex

window = Tk()
window.title('whatsapp data visualisation')
window.geometry('1366x768')

datelist=[]
timelist=[]
senderlist=[]
messagelist=[]
diffSname=[]

graphdata=[]
messagedata=[]
activegraph=[]
hourlytime=[]
mediagraph=[]
activehourlygraph=[]
emojilist=[]
wordlist=[]
location=[]
ltofs=[]
htforS=[]
ahourlyforsgraph=[]
tword=0
notification=0

def filelocation():
	file = filedialog.askopenfile()
	if file: 
		pathcheck=file.name
		if pathcheck.endswith('.txt'):
			global path
			path=pathcheck
	datacleaning()
def datacleaning():
	f=open(path, 'r',encoding='utf')
	count=0
	while True:
		line = f.readline()

		if not line:
			break
		if count==0:
			count=1
		else:
			line = ' '.join(line.split('\n'))
			line =' '.join(line.split())

			test_string = line
			matched = re.match("\d+/\d+/\d+, \d+:\d+ [a-z]{2} -\s", test_string)
			matched1 = re.match("\d+/\d+/\d+, \d+:\d+ [A-Z]{2} -\s", test_string)
			if bool(matched)==True or bool(matched1)==True:
				a = test_string
			else:
				a = a+test_string
				global datelist
				datelist.pop()
				global timelist
				timelist.pop()
				global senderlist
				senderlist.pop()
				global messagelist
				messagelist.pop()

			##date
			line = a.split(", ")
			# global datelist
			datelist.append(line[0])
			#time
			time= line[1].split("-")
			# global timelist
			timelist.append(time[0])
			##sendser
			totalcolon = time[1].count(':')
			sender = time[1].split(":")
			# global senderlist
			senderlist.append(sender[0])
			##message
			if totalcolon > 1:
				message=":".join(time[1].split(":")[1:])
				# global messagelist
				messagelist.append(message)
			elif totalcolon == 0:
				global notification
				notification = notification +1
				# global senderlist
				senderlist.pop()
				# global datelist
				datelist.pop()
				# global timelist
				timelist.pop()
			else:
				messagelist.append(sender[1])
	f.close()
	# #clearning of data ie. removing file omitted and the chat is deleted
	# stopwords=[' <Media omitted>',' This message was deleted']
	# global messagelist1
	# messagelist1 = list(filter(lambda w: w not in stopwords, messagelist))
	# for i in range(len(stopwords)):
	# 	index_pos_list = list(get_index_positions(messagelist,stopwords[i]))
	# 	global location
	# 	location.extend(index_pos_list)
	# global senderlist1
	# senderlist1 = [i for j, i in enumerate(senderlist) if j not in location]

	# ##for getting the list of different sender
	# counts = Counter(senderlist)
	# for i in counts:
	# 	global diffSname
	# 	diffSname.append(i)
	dataarea.configure(text=datelist)


def removegrid():
	print("\n")
	try:
		print("removing the location of word")
		l6.grid_forget()
		aentry.grid_forget()
		cshow.grid_forget()
	except:
		pass
	try:
		print("removing the location of date")
		l7.grid_forget()
		bentry.grid_forget()
		bshow.grid_forget()
	except:
		pass
	try:
		print("removing the location of time")
		l8.grid_forget()
		l9.grid_forget()
		l10.grid_forget()
		afentry.grid_forget()
		bfentry.grid_forget()
		ashow.grid_forget()
	except:
		pass

def filtertype():
	ftype=combo1.get()
	if ftype=='By word':
		global l6
		l6 =Label(window,text='Enter the word',font=('Arial Bold',10))
		l6.grid(column=0,row=9,pady=10)
		global aentry
		aentry =Entry(window,width=30)
		aentry.grid(column=0,row=10)
		global cshow
		cshow = Button(window,text='show',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation)
		cshow.grid(column=1,row=10,sticky=W,padx=7)

	elif ftype=='By date':
		global l7
		l7 =Label(window,text='Enter the date',font=('Arial Bold',10))
		l7.grid(column=0,row=9,pady=10)
		global bentry
		bentry =Entry(window,width=30)
		bentry.grid(column=0,row=10)
		global bshow
		bshow = Button(window,text='show',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation)
		bshow.grid(column=1,row=10,sticky=W,padx=7)

	elif ftype=='By time':
		global l8
		l8 =Label(window,text='Enter the time',font=('Arial Bold',10))
		l8.grid(column=0,row=9,pady=10)
		global l9
		l9 =Label(window,text='After',font=('Arial Bold',10))
		l9.grid(column=0,row=10)
		global afentry
		afentry =Entry(window,width=30)
		afentry.grid(column=0,row=11)
		global l10
		l10 =Label(window,text='Before',font=('Arial Bold',10))
		l10.grid(column=1,row=10)
		global bfentry
		bfentry =Entry(window,width=30)
		bfentry.grid(column=1,row=11)
		global ashow
		ashow = Button(window,text='show',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation)
		ashow.grid(column=2,row=11,sticky=W,padx=7)
		

# l1 =Label(window,text='WHATSAPP DATA VISUALISATION',font=('Arial Bold',20))
# l1.grid(column=5,row=0)

l2 =Label(window,text='Enter the file location',font=('Arial Bold',15))
l2.grid(column=1,row=1)

bt = Button(window,text='Enter',bg='orange',font=('Arial Bold',15),fg='red',command=filelocation,width=20)
bt.grid(column=2,row=1)

empty=Label(window)
empty.grid(column=0,row=2)

bt1 = Button(window,text='Basic details',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt1.grid(column=0,row=3,padx=30, pady=20)

bt2 = Button(window,text='All chat',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt2.grid(column=1,row=3)

bt3 = Button(window,text='Most media shared\n by whom',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt3.grid(column=2,row=3,padx=30, pady=20)

bt4 = Button(window,text='Graph of day in which\nmsot message sent',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt4.grid(column=3,row=3)

bt5 = Button(window,text='Graph of most active',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt5.grid(column=4,row=3,padx=40, pady=20)

bt6 = Button(window,text='Graph of most media\nsent',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt6.grid(column=5,row=3)

bt5 = Button(window,text='Graph of no. of word\nsent by different person',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt5.grid(column=0,row=4)

bt6 = Button(window,text='Graph of sharp time\nwhen most are active',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt6.grid(column=1,row=4)

bt7 = Button(window,text='Graph of hourly time\nwhen most are active',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt7.grid(column=2,row=4)

bt8 = Button(window,text='commanly used word',bg='orange',font=('Arial Bold',10),fg='red',command=filelocation,width=20,height=2)
bt8.grid(column=3,row=4)

l2 =Label(window,text='Graph with time when the\nperson sent the message',font=('Arial Bold',10))
l2.grid(column=0,row=5,pady=20)

combo = ttk.Combobox(window,width=30,height=15)
combo['value']=(1,2,3,'abhishek')
combo.current(3)
combo.grid(column=1,row=5,pady=20)

l3 =Label(window,text='Filters for message',font=('Arial Bold',15))
l3.grid(column=0,row=6)

l4 =Label(window,text='Select the member',font=('Arial Bold',10))
l4.grid(column=0,row=7)

combo1 = ttk.Combobox(window,width=30,height=15)
combo1['value']=(1,2,3,'abhishek')
# combo1.current(3)
combo1.grid(column=0,row=8)

l5 =Label(window,text='Select filter type',font=('Arial Bold',10))
l5.grid(column=1,row=7)

combo1 = ttk.Combobox(window,width=30,height=15)
combo1['value']=("By word",'By date','By time')
# combo1.current(0)
combo1.grid(column=1,row=8)

bt9 = Button(window,text='Apply',bg='orange',font=('Arial Bold',10),fg='red',command=lambda:[removegrid(),filtertype()])
bt9.grid(column=2,row=8,sticky=W,padx=7)

dataarea=Label(window,text='', bd=1, relief=SUNKEN, anchor=NW,width=90,height=33)
dataarea.grid(column=3,row=5,sticky=W,columnspan=4,rowspan=20)

window.mainloop()