#!/usr/bin/env python3

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
"""
If program doesn't run run this command in terminal
pip install --upgrade pip
pip install --upgrade Pillow
"""
import re
import regex   #pip3 install regex
import emoji   #pip3 install emoji
import queue
import threading
import multiprocessing
import time
import numpy as np   #pip3 install numpy
from datetime import date
from collections import Counter
import matplotlib.pyplot as plt  #pip3 install matplotlib
from wordcloud import WordCloud, STOPWORDS #pip3 install wordcloud
from matplotlib import pylab
plt.rcParams.update({'font.size': 22})
def return_emoji(text):
    """This functino will return list of all the emoji present in the line
        i dont know why but this function is not working properly when i 
        use it to find all the emoji in whatsapp data file it is just returning 
        the are or the first sentence with the dual collon in side with that """
    text = emoji.demojize(text)
    text = re.findall(r'(:[^:]*:)', text)
    list_emoji = [emoji.emojize(x) for x in text]
    if list_emoji != text:
    	return list_emoji
    else:
    	return []

def data_collection():
    global notification,emojilist
    # path='/mnt/Partition_2/mycodes/python codes/data analysis/WhatsApp Chat with Mammi 4g.txt'
    # path=input('Enter the path here↓\n')
    # path='D:\mycodes\python codes\data analysis\WhatsApp Chat with Tanya Friend.txt'
    # path='/mnt/Partition_2/mycodes/python codes/data analysis/WhatsApp Chat with Gladin.txt'
    path='/mnt/Partition 2/mycodes/python codes/data analysis/WhatsApp Chat with Madhu Friend.txt'
    # path='/media/abhishek/Partition 2/mycodes/python codes/data analysis/WhatsApp Chat with Madhu Friend.txt'
    # path='/mnt/Partition_2/mycodes/python codes/data analysis/WhatsApp Chat with Happy Birthday Neelesh 🥳🎊.txt'
    # path='/mnt/Partition_2/mycodes/python codes/data analysis/WhatsApp Chat with Madhu.txt'
    # path = '/home/abhishek/Downloads/WhatsApp Chat with CSE...RKOC38.txt'  
    file=open(path,"r",encoding='utf8')
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
            ##sender
            totalcolon = time[1].count(':')
            sender = time[1].split(":")
            senderlist.append(sender[0])
            ##message
            if totalcolon > 1:
                message=":".join(time[1].split(":")[1:])
                counter = return_emoji(message)
                emojilist.extend(counter)                
                messagelist.append(message)
            elif totalcolon == 0:
                notification = notification +1
                senderlist.pop()
                datelist.pop()
                timelist.pop()
            else:
                counter = return_emoji(sender[1])
                emojilist.extend(counter)                
                messagelist.append(sender[1])

    file.close()

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

def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)
    z = [x for _, x in sorted(zipped_pairs)]
    return z


def data_cleaning():
    global count_of_sender,diffSdate,diffSname,messagelist1,senderlist1,location,nameoffilesender
    location=[]
    ##this will show the total no of member in the chat
    count_of_sender=Counter(senderlist)
    ##for getting the list of different date of when the sender sent the message
    counts=Counter(datelist)
    diffSdate=[i for i in counts]
    ##for getting the list of different sender
    counts = Counter(senderlist)
    diffSname=[i for i in counts]
    #clearning of data ie. removing file omitted and the chat is deleted
    stopwords=[' <Media omitted>',' This message was deleted']
    messagelist1 = list(filter(lambda w: w not in stopwords, messagelist))
    for i in range(len(stopwords)):
        index_pos_list = list(get_index_positions(messagelist,stopwords[i]))
        location.extend(index_pos_list)
    senderlist1 = [i for j, i in enumerate(senderlist) if j not in location]
    index_pos_list = get_index_positions(messagelist, ' <Media omitted>')
    nameoffilesender=list(np.array(senderlist)[index_pos_list])


def readable_table_of_chat():
    """for printing th dat ain readable format"""
    try:
        print('   DATE       DAY         NAME           MESSAGE     ')
        for i in range(0,len(datelist)):
            print(f'{datelist[i]}  {timelist[i]}   {senderlist[i]}   {messagelist[i]}')
    except:
        pass

def default_result():
    print('*'*100+'\n')
    """will give the name of person who is most active in the group with number of comversation only top 10"""
    print("+++++++ List of active in the chat +++++++")
    print("+++++++----------------------------+++++++")
    for item in count_of_sender.most_common(10):
        print(item)
    print('+----------------------------+\n')

    """who has send the most of the media file like audio, video, sticker etc"""
    sender=Counter(nameoffilesender)
    print("List of person who sent the most media file:-")
    print('+----------------------------+')
    for item in sender.most_common(10):
        print(item)
    print('+----------------------------+\n')

    """This will show the number of missed video calls"""
    video_call =messagelist.count(' Missed video call')
    print(f'Total no. of missesd video video_call are {video_call}\n')

    """"This will show you number of missed audio calls"""
    audio_call=messagelist.count(' Missed audio call')
    print(f'Total no. of missed audio calls are {audio_call}\n')

    """Total no. of notification in the chat this will include the notification realtead to how many people left or joied the chat or
        and also some whats data staring notificaiton which is due to phone number change or due to changing their account to an bussiness account"""
    print(f'Total no. of notification are {notification}\n')

    """this will show you total no of chats in the data"""
    totalchats = len(messagelist)
    print(f'The total no. of chats is {totalchats}\n')

    """this way is much smater and earier this will only take the average of the char on which the chat is happened not like
        above where it will take the aveage or all the day including the day in which the chat is not happened"""
    average=len(messagelist)//len(diffSdate)
    print(f'Total no. of messages per day is {average}\n')

    """This will show total no. of chat is which deleted"""
    totaldeleted = messagelist.count(' This message was deleted')
    print(f'Total no. of deleted messages are {totaldeleted}\n')

def total_words_in_chat(total_words):
    global wordlist
    wordlist=[]
    """This will show you total no. of words in the chat"""
    tword=0
    for i in range(len(diffSname)):
        index_pos_list = get_index_positions(senderlist1, diffSname[i])
        nameoffilesender=list(np.array(messagelist1)[index_pos_list])
        t=0
        for j in range(0,len(nameoffilesender)):
            res=len(nameoffilesender[j].split())
            t=t+res
            tword=tword+res
        wordlist.append(t)
    # print(wordlist,"asdfasdf")
    total_words.put(tword)
    # print(wordlist,"this is this")
        # print(f'The total no. of word send by {diffSname[i]} is {t}')
    # print(f'Total no. of word send is {tword}\n')

def total_emoji_in_chat(count_of_emoji):
    """This will show you the total no. of differrent emoji sent in the chat by only top 15 emoji in chat"""
    count_of_emoji.put(Counter(emojilist).most_common(15))

def graph_most_message(command) :
    """this will show the graph on which the most message were sent"""
    count_of_message=Counter(datelist)
    messagedata=[item for item in count_of_message.most_common(10)]
    x_value = [x[0] for x in messagedata]
    y_value = [x[1] for x in messagedata]
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 1')
    plt.bar(x_value,y_value ,color ='red',width = 0.4)
    plt.title("Graph of most message sent on a particular day") 
    plt.xlabel("DATE") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Number of messages')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_active(command):
    """"this will show the graph of the most active person in the chat but only list the top 10 person in the chat"""
    graphdata=[item for item in count_of_sender.most_common(10)]
    x_val = [x[0] for x in graphdata]
    y_val = [x[1] for x in graphdata]
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 2')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("No. of message sent by different member\nonly top 10") 
    plt.xlabel("Name of member") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of message')
    # show=command.get()
    # plt.show()
    # command.put(show)
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_media(command):
    """this will show the graph on mosty media sent by user in the chat """
    mediagraph=[item for item in Counter(nameoffilesender).most_common(10)]
    x_value = [x[0] for x in mediagraph]
    y_value = [x[1] for x in mediagraph]

    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n{:d}".format(pct, absolute)

    fig, ax = plt.subplots()
    ax.pie(y_value,autopct = lambda pct: func(pct, y_value),labels = x_value,shadow = True,)
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 3')
    ax.set_title("Percentage of media shared by the members")
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_word(command):
    """this will show the graph os most word sent by different user in the chat"""
    wordlist=[59785, 62117]
    diffsendername=sort_list(diffSname,wordlist)
    wordlists=sorted(wordlist)
    # print(diffSname)
    # print(diffsendername)
    # print(wordlist)

    x_value = diffsendername[-20:]
    y_value = wordlists[-20:]
    # print(x_value)
    # print(y_value)
    # print("jai shree ram")
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 4')
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
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass    

def graph_most_active_minute_hour(command):
    """This will show the hour and minute in which the most message were sent in the group by the person"""
    activetime=Counter(timelist)
    # print("Time when most are active:-")
    activegraph=[ item for item in activetime.most_common(15)]
    # print(item)
    x_val = [x[0] for x in activegraph]
    y_val = [x[1] for x in activegraph]
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 5')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("Maximum message is sent at this time") 
    plt.xlabel("Time") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of message')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_active_hour(command):
    """this will show the hour in which the most person the chat are active"""
    hourlytime=[]
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
    activehourlygraph=[item for item in activehourly.most_common(24)]
    # print(item)
    x_value = [x[0] for x in activehourlygraph]
    y_value = [x[1] for x in activehourlygraph]
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 6')
    plt.locator_params(axis="x", nbins=len(x_value))
    plt.bar(x_value,y_value ,color ='blue',width = 0.4)
    plt.title("Maximum message is sent in which hour of the day") 
    plt.xlabel("Hour") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of message')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def word_cloud(command):
    """this will make the word cloud of he word in the chat whcih has been sent by different user  multiple times"""
    unique_string=(" ").join(messagelist)
    stopwords = STOPWORDS.update(['hmm','this','message','was','deleted','Media','omitted','call','missed','video','lo','na','ok', 'will'])
    wordcloud = WordCloud(width = 1000, height = 500,stopwords = stopwords).generate(unique_string)
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Figure 7')
    fig.set_size_inches(15,8)
    # plt.figure(figsize=(15,8))
    plt.title("WordCloud of commanly used word") 
    plt.imshow(wordcloud)
    plt.axis("off")
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

##for getting the time when the particular person send the message with graph

def person_specific_time_of_chat(a):
    ltofs=[]
    htforS=[]
    ahourlyforsgraph=[]

    a=int(a)-1
    if bool(diffSname[a])==True:
        # print(diffSname[a])
        index_pos_list = list(get_index_positions(senderlist,diffSname[a]))
        # ltofs=[timelist[index_pos_list[i]]
        for i in range(len(index_pos_list)):
            ltofs.append(timelist[index_pos_list[i]])
        for j in ltofs:
            f=j.split(' ')
            if f[1]=='pm' or f[1]=='PM':
                time=j.split(':')[0]
                htforS.append(str(int(time)+12))
            else:
                time=j.split(':')[0]
                htforS.append(str(time))
        ahourlyfors=Counter(htforS)
        ahourlyforsgraph=[item for item in ahourlyfors.most_common(24)]
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

def filter2():
    print("\nselect the name of the sender to find the message sent by him")
    for i in range(len(diffSname)):
        print(f'\nFor the detail of {diffSname[i]} type {i+1}')
    print('\nFor previous option press "z"')
    a=input('\nEnter your value here:- ')
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
        print('\nTo apply filter by date press 2')
        print('\nTo apply filter by time press 3')
        print('\nFor previous option press "z"')
        choice=input('\nEnter your choice:- ')
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
    print('+'+('*'*80)+'+')
    print("\nIf you want to get the detail of time of chat of particular person then press 1")
    print("\nIf you want to apply filter on the chat for a particular person then press 2")
    print("\nIf you want to get the detail of all the messages sent by a particular person then press 3")
    print("\nIf you want to exit type exit in command")
    while True:
        command=input('\nEnter your command here:- ')
        print('\n+'+('*'*80)+'+')
        if command=='1':
            print("\nSelect the name of the sender to find the time when the he send the messages")
            for i in range(len(diffSname)):
                print(f'\nFor the detail of {diffSname[i]} type {i+1}')
            print('\nFor previous option press "z"')
            while True:
                a=input('\nEnter your value here:- ')
                if 'z' in a:
                    option()
                elif 'exit' in a:
                    exit()
                else:
                    try:
                        p8=multiprocessing.Process(target=person_specific_time_of_chat,args=(a,),daemon=True)
                        p8.start()
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
        elif command.lower() == 'exit':
            exit()

        else:
            print('\n---------------: Please enter the right value :------------')
            option()


if __name__ == '__main__':
    datelist=[]
    timelist=[]
    senderlist=[]
    messagelist=[]
    emojilist=[]
    notification=0
    total_words=queue.Queue()
    count_of_emoji=queue.Queue()
    command=multiprocessing.Queue()
    data_collection()
    data_cleaning()
    # readable_table_of_chat()
    t1=threading.Thread(target=default_result)
    t2=threading.Thread(target=total_words_in_chat,args=(total_words,))
    t3=threading.Thread(target=total_emoji_in_chat,args=(count_of_emoji,))
    p1=multiprocessing.Process(target=graph_most_message,args=(command,),daemon=True)
    p2=multiprocessing.Process(target=graph_most_active,args=(command,),daemon=True)
    p3=multiprocessing.Process(target=graph_most_media,args=(command,),daemon=True)
    p4=multiprocessing.Process(target=graph_most_word,args=(command,),daemon=True)
    p5=multiprocessing.Process(target=graph_most_active_minute_hour,args=(command,),daemon=True)
    p6=multiprocessing.Process(target=graph_most_active_hour,args=(command,),daemon=True)
    p7=multiprocessing.Process(target=word_cloud,args=(command,),daemon=True)
    t1.start()
    t2.start()
    t3.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    t1.join()
    t2.join()
    t3.join()
    print(f'Total no. of word send is {total_words.get()}\n')
    print("list of emoji used:-")
    print('+----------------------------+')
    for items in count_of_emoji.queue:
        for item in items:
            print(item)
    print('+----------------------------+\n')

    while True:
        ans=input("Enter 'yes' if you want to see the graph:- \n\t")
        if 'yes' in ans or 'y' == ans:
            command.put('show')
        else:
            if ans=="exit" or ans=='z':
                exit()
            else:
                pass
        option()