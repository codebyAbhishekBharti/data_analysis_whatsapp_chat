#!/usr/bin/env python3

#tested on linux

# Features of the programm:-
# 1 Able to show chat in readable format
# 2 will give the name of person who has have the most of conversation with how many conversations
# 3 total media file shared
# 4 total no of missed video call
# 5 total no of chats
# 6 total no of deleted chats
# 7 total no of poeple left of joined the group and left
# 8 who has send the most of the media file in a group or in the personal chat
# 9 graph of most media sent
# 10 graph of day in which most of the message were sent
# 11 To make the graph of the most active
# 12 the sharp time when most are active
# 13 hourly time when most are active
# 14 making word cloud for most commanly used word
# 15 able to find when the person is online

from collections import Counter
from datetime import date
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import regex
import emoji
plt.rcParams.update({'font.size': 22})
print('Enter the path of that WhatsApp file:-')
print('*path must in the format "E:\\file.txt"')
path=input('Enter the path here↓\n')
file=open(path,'r',encoding='utf')
# file = open('E:\\mycodes\\python codes\\data analysis\\WhatsApp Chat with Mammi 4g.txt', 'r',encoding='utf')
# file = open('E:\\mycodes\\python codes\\data analysis\\WhatsApp Chat with Harsh Call Of Duty.txt', 'r',encoding='utf')


def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list

def return_emoji(text):
	"""This functino will return list of all the emoji present in the line
		i dont know why but this function is not working properly when i 
		use it to find all the emoji in whatsapp data file it is just returning 
		the are or the first sentence with the dual collon in side with that """
	text = emoji.demojize(text)
	text = re.findall(r'(:[^:]*:)', text)
	list_emoji = [emoji.emojize(x) for x in text]
	return list_emoji

def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)
    z = [x for _, x in sorted(zipped_pairs)]
    return z

datelist=[]           #contains all the date from the chat
timelist=[]           #contains all the time time of the chat
senderlist=[]         #contains all the name of person who sent the chat
messagelist=[]        #contains all the messages in the chat
graphdata=[]          #contains total no of message sent by a person only top 10
messagedata=[]        #contains total no of messges send on particular date only top 10
activegraph=[]        #contains maximum no of messges send on particular time only top 15
hourlytime=[]         #contians all the hour in which messages were sent
mediagraph=[]         #contains total no of media file shared by a particular person
activehourlygraph=[]  #contains total no of messages sent on the particluar hour
emojilist=[]          #contains all list of all the emoji used in the chat
diffSname=[]          #contains list of all different person in the chat
diffSdate=[]          #contains list of all the different date on which the message was sent
wordlist=[]           #contains list of all the words in the chat by different person
location=[]           #contains list of line in which file is either deleted or ommited
ltofs=[]
htforS=[]
ahourlyforsgraph=[]
tword=0
notification=0

count=0
while True:
	line = file.readline()
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
			datelist.pop()
			timelist.pop()
			senderlist.pop()
			messagelist.pop()

		##date
		line = a.split(", ")
		datelist.append(line[0])
		#time
		time= line[1].split("-")
		timelist.append(time[0])
		##sendser
		totalcolon = time[1].count(':')
		sender = time[1].split(":")
		senderlist.append(sender[0])
		##message
		if totalcolon > 1:
			message=":".join(time[1].split(":")[1:])
			messagelist.append(message)
		elif totalcolon == 0:
			notification = notification +1
			senderlist.pop()
			datelist.pop()
			timelist.pop()
		else:	
			messagelist.append(sender[1])

file.close()

#clearning of data ie. removing file omitted and the chat is deleted
stopwords=[' <Media omitted>',' This message was deleted']
messagelist1 = list(filter(lambda w: w not in stopwords, messagelist))
for i in range(len(stopwords)):
	index_pos_list = list(get_index_positions(messagelist,stopwords[i]))
	location.extend(index_pos_list)
senderlist1 = [i for j, i in enumerate(senderlist) if j not in location]

##for getting the list of different sender
counts = Counter(senderlist)
for i in counts:
	diffSname.append(i)

##for getting the list of different date of when the sender sent the message
counts=Counter(datelist)
for i in counts:
	diffSdate.append(i)


#for checking the data is succesfully parsesd of not
# print(len(datelist))
# print(len(timelist))
# print(len(messagelist))
# print(len(senderlist))

# print(datelist)
# print('*'*100)
# print(timelist)
# print('*'*100)
# print(senderlist)
# print('*'*100)
# print(messagelist)

#for printing the data in readable format
# try:
# 	print('   DATE       DAY         NAME           MESSAGE     ')
# 	for i in range(0,len(datelist)):
# 		print(f'{datelist[i]}  {timelist[i]}   {senderlist[i]}   {messagelist[i]}')
# except:
# 	pass

print('*'*100)
##will give the name of person who has have the most of conversation with how many conversations
count_of_sender=Counter(senderlist)
print("List of most active person in the group:-")
print('+----------------------------+')
for item in count_of_sender.most_common(10):
	print(item)
print('+----------------------------+')

##graph of day in which most of the message were sent
count_of_message=Counter(datelist)
for item in count_of_message.most_common(10):
	messagedata.append(item)
x_value = [x[0] for x in messagedata]
y_value = [x[1] for x in messagedata]
plt.figure(1)
plt.bar(x_value,y_value ,color ='red',width = 0.4)
plt.title("Graph of most message sent on a particular day") 
plt.xlabel("DATE") 
plt.gcf().autofmt_xdate()
plt.ylabel('Number of messages')
# plt.show()      #if you only want to show the this value than only activate this or it will activated from word cloud

## To make the graph of the most active
for item in count_of_sender.most_common(10):
	graphdata.append(item)
x_val = [x[0] for x in graphdata]
y_val = [x[1] for x in graphdata]
plt.figure(2)
plt.bar(x_val,y_val ,color ='blue',width = 0.4)
plt.title("No. of message sent by different member\nonly top 10") 
plt.xlabel("Name of member") 
plt.gcf().autofmt_xdate()
plt.ylabel('Total number of message')
# plt.show()      #if you only want to show the this value than only activate this or it will activated from word cloud

##total media file shared
media=messagelist.count(' <Media omitted>')
print(f'Total no. of media file transferd is {media}')

##who has send the most of the media file
index_pos_list = get_index_positions(messagelist, ' <Media omitted>')
nameoffilesender=list(np.array(senderlist)[index_pos_list])
count_of_sender=Counter(nameoffilesender)
print("List of person who sent the most media file:-")
print('+----------------------------+')
for item in count_of_sender.most_common(10):
	print(item)
print('+----------------------------+')

##graph of most media sent
for item in Counter(nameoffilesender).most_common(10):
  mediagraph.append(item)
x_value = [x[0] for x in mediagraph]
y_value = [x[1] for x in mediagraph]
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct
fig, ax = plt.subplots()
plt.figure(3)
plt.gcf().autofmt_xdate()
plt.title("Percentage of media shared by the members")
plt.pie(y_value, labels=x_value, autopct=make_autopct(y_value),shadow = True)

##total no of missed video call
call=messagelist.count(' Missed video call')
print(f'Total no. of missed video call  are {call}')

##total no of poeple left of joined the group and left
print(f'Total no. of people left or joined the group are {notification}')

##total no of chats
totalchats = len(messagelist)
print(f"Total no of chats is {totalchats}")

##total no of chats per day
'''
#This function will calculate the chat per day by just getting the date of when the first chat happend
#and the when the last chat happended by dividing the length of all the chat
#ignoring that if the chat happened on the particular day or not 
if len(datelist[0].split('/')[2])==4:
	firstdate=date(int(datelist[0].split('/')[2]),int(datelist[0].split('/')[1]),int(datelist[0].split('/')[0]))
	lastdate=date(int(datelist[-1].split('/')[2]),int(datelist[-1].split('/')[1]),int(datelist[-1].split('/')[0]))
else:
	firstdate=date(int('20'+datelist[0].split('/')[2]),int(datelist[0].split('/')[1]),int(datelist[0].split('/')[0]))
	lastdate=date(int('20'+datelist[-1].split('/')[2]),int(datelist[-1].split('/')[1]),int(datelist[-1].split('/')[0]))
average=totalchats//(lastdate-firstdate).days             #it will remove decimal places in the result '''
average=totalchats//len(diffSdate)     #This will only take the average of the chat on which the caht is happend
print(f'Total no. of messages per day is {average}')

##total deleted chat
totaldeleted = messagelist.count(' This message was deleted')
print(f'Total no. of deleted messages are {totaldeleted}')

##total no of word in the chat
for i in range(len(diffSname)):
	index_pos_list = get_index_positions(senderlist1, diffSname[i])
	nameoffilesender=list(np.array(messagelist1)[index_pos_list])
	t=0
	for j in range(0,len(nameoffilesender)):
		res=len(nameoffilesender[j].split())
		t=t+res
		tword=tword+res
	wordlist.append(t)
	# print(f'The total no. of word send by {diffSname[i]} is {t}')
print(f'Total no. of word send is {tword}')
# print(f'{diffSname} = {wordlist}')

##graph of number of word sent by different memeber
diffSname=sort_list(diffSname,wordlist)
wordlist=sorted(wordlist)

x_value = diffSname[-20:]
y_value = wordlist[-20:]
plt.figure(4)
ax_sort = sorted(zip(y_value,x_value), reverse=True)
y_axis = [i[0] for i in ax_sort]
x_axis = [i[1] for i in ax_sort]
x_label_pos = range(len(x_axis))
plt.bar(x_label_pos, y_axis,align="center")
plt.xticks(x_label_pos,x_axis)
plt.title("Graph of number of word sent by different member") 
plt.xlabel("Name") 
plt.gcf().autofmt_xdate()
plt.ylabel('Number of messages')

##total no of emoji used
for i in range(0,len(messagelist)):
	counter = return_emoji(messagelist[i])
	emojilist.extend(counter)
# print(emojilist)
count_of_emoji=Counter(emojilist)
print("list of emoji used:-")
print('+----------------------------+')
for item in count_of_emoji.most_common(15):
	print(item)
print('+----------------------------+')

##the sharp time when most are active
activetime=Counter(timelist)
# print("Time when most are active:-")
for item in activetime.most_common(15):
	# print(item)
	activegraph.append(item)
x_val = [x[0] for x in activegraph]
y_val = [x[1] for x in activegraph]
plt.figure(5)
plt.bar(x_val,y_val ,color ='blue',width = 0.4)
plt.title("Maximum message is sent at this time") 
plt.xlabel("Time") 
plt.gcf().autofmt_xdate()
plt.ylabel('Total number of message')

##hourly time when most are active
for a in timelist:
	b=a.split(' ')
	if b[1]=='pm' or b[1]=='PM':
		time=a.split(':')[0]
		time=int(time)+12
		hourlytime.append(time)
	else:
		time=a.split(':')[0]
		hourlytime.append(int(time))
activehourly=Counter(hourlytime)
# print("Time when most are active hourly:-")
for item in activehourly.most_common(24):
	# print(item)
	activehourlygraph.append(item)
x_value = [x[0] for x in activehourlygraph]
y_value = [x[1] for x in activehourlygraph]
plt.figure(6)
plt.locator_params(axis="x", nbins=len(x_value))
plt.bar(x_value,y_value ,color ='blue',width = 0.4)
plt.title("Maximum message is sent in which hour of the day") 
plt.xlabel("Hour") 
plt.gcf().autofmt_xdate()
plt.ylabel('Total number of message')

##making word cloud for most commanly used word
unique_string=(" ").join(messagelist)
stopwords = STOPWORDS.update(['hmm','this','message','was','deleted','Media','omitted','call','missed','video','lo','na','ok', 'will'])
wordcloud = WordCloud(width = 1000, height = 500,stopwords = stopwords).generate(unique_string)
plt.figure(figsize=(15,8))
plt.title("WordCloud of commanly used word") 
plt.imshow(wordcloud)
plt.axis("off")

command=input('Enter "yes" if you want to see the graph:- ')
if 'y' in command:
	plt.show()    #show to show the  picture 
if 'exit' in command:
	exit()
else:
	plt.close('all')


##for getting the time when the particular person send the message with graph

def filter2():
	print("select the name of the sender to find the message sent by him")
	for i in range(len(diffSname)):
		print(f'For the detail of {diffSname[i]} type {i+1}')
	print('For previous option press "z"')
	a=input('Enter your value here:- ')
	if 'z' in a:
		option()
	elif 'exit' in a:
		exit()
	else:
		try:
			a=int(a)-1
			mainfilter(a)
		except:
			print('Please enter the right value')	

def mainfilter(a):
	if bool(diffSname[a])==True:
		print(diffSname[a])
		index_pos_list = list(get_index_positions(senderlist,diffSname[a]))
		print('\nTo apply filter by word press 1')
		print('To apply filter by date press 2')
		print('To apply filter by time press 3')
		print('For previous option press "z"')
		choice=input('Enter your choice:- ')
		if choice=='z':
			filter2(a)
		elif choice=='1':
			find=input('Enter to word to search in his chat:- ')
			print('    DATE     TIME          MESSAGE')
			for i in index_pos_list:
				if find in messagelist[i].lower():                   #only use this part if you want to filter the mesagges
					print(f'{datelist[i]} {timelist[i]} {messagelist[i]}')
		elif choice=='2':
			print('*Date must be in the format of "DD/MM/YYYY"')
			find=input('Enter to date to search in his chat:- ')
			print('    DATE     TIME          MESSAGE')
			for i in index_pos_list:
				if find in datelist[i]:                        #only use if you want to filter the message with cetain date
					print(f'{datelist[i]} {timelist[i]} {messagelist[i]}')
		elif choice=='3':    #if you want to get the message of a person about the certain time
			print('*After and before time must be in the form of "HH:MM am/pm"')
			after=input('Enter the after time in which you want to find all the chat:- ')
			before=input('Enter the before time in which you want to find all the chat:- ')
			between=[after,before]
			betweentime=[]
			for a in between:
				b=a.split(' ')
				if b[1]=='pm' or b[1]=='PM':
					time=b[0].split(':')
					if '12' in time[0]:
						time=720+int(time[1])
					else:
						time=(int(time[0])+12)*60+int(time[1])
					betweentime.append(time)
				else:
					time=b[0].split(':')
					if '12' in time[0]:
						time=int(time[1])
					else:
						time=(int(time[0]))*60+int(time[1])
					betweentime.append(int(time))
					
			for i in index_pos_list:
				b=timelist[i].split(' ')
				if b[1]=='pm' or b[1]=='PM':
					time=b[0].split(':')
					if '12' in time[0]:
						time=720+int(time[1])
					else:
						time=(int(time[0])+12)*60+int(time[1])
				else:
					time=b[0].split(':')
					if '12' in time[0]:
						time=int(time[1])
					else:
						time=(int(time[0]))*60+int(time[1])
				if  betweentime[0]-1 < time and betweentime[1]+1 > time:
					print(f'{datelist[i]} {timelist[i]} {messagelist[i]}')

def option():
	print("\nIf you want to get the detail of time of chat of particular person then press 1")
	print("If you want to apply filter on the chat for a particular person then press 2")
	print("If you want to get the detail of all the messages sent by a particular person then press 3")
	while True:
		command=input('Enter your command here:- ')
		if command=='1':
			print("select the name of the sender to find the time when the he send the messages")
			for i in range(len(diffSname)):
				print(f'For the detail of {diffSname[i]} type {i+1}')
			print('For previous option press "z"')
			while True:
				a=input('Enter your value here:- ')
				if 'z' in a:
					option()
				elif 'exit' in a:
					exit()
				else:
					try:
						a=int(a)-1
						if bool(diffSname[a])==True:
							print(diffSname[a])
							index_pos_list = list(get_index_positions(senderlist,diffSname[a]))

							for i in range(len(index_pos_list)):
								aa=timelist[index_pos_list[i]]
								ltofs.append(aa)
							for j in ltofs:
								f=j.split(' ')
								if f[1]=='pm' or f[1]=='PM':
									time=j.split(':')[0]
									time=int(time)+12
									htforS.append(str(time))
								else:
									time=j.split(':')[0]
									htforS.append(str(time))
							ahourlyfors=Counter(htforS)
							for item in ahourlyfors.most_common(24):
								ahourlyforsgraph.append(item)
							x_val = [x[0] for x in ahourlyforsgraph]
							y_val = [x[1] for x in ahourlyforsgraph]
							plt.figure(10)
							plt.bar(x_val,y_val ,color ='blue',width = 0.4)
							plt.title(f"Number of message sent by {diffSname[a]} with respect to time") 
							plt.xlabel("Time")
							plt.gcf().autofmt_xdate()
							plt.ylabel('Total number of message')
							plt.show()
							ltofs.clear()
							htforS.clear()
							ahourlyforsgraph.clear()
					except:
						print('please enter the right value')
		elif command=='2':
			while True:
				filter2()
			
		elif command=='3':
			print("\nSelect the name of the sender to show all the message sent by him:-")
			for i in range(len(diffSname)):
				print(f'For the detail of {diffSname[i]} type {i+1}')	
			print('For previous option press "z"')	
			while True:
				a=input('\nEnter your value here:- ')
				if 'z' in a :
					option()
				elif 'exit' in a:
					exit()
				else:
					try:
						a=int(a)-1
						if bool(diffSname[a])==True:
							print(diffSname[a])
							index_pos_list = list(get_index_positions(senderlist,diffSname[a]))	
							print('    DATE     TIME          MESSAGE')
							for i in index_pos_list:
								print(f'{datelist[i]} {timelist[i]} {messagelist[i]}')
					except:
						print("Please enter the right value")
		else:
			break

option()                      #to apply differnt filters  it the file