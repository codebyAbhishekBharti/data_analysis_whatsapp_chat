import pdfplumber
import re
import queue
import threading
import multiprocessing
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import pylab

def data_collection():
    """This will open the pdf and collect all the ocr character from the pdf and put them all in 
       different collums of dictionary"""
    singled_data_call=[]
    singled_data_message=[]

    # path='/mnt/Partition_2/Statement1656999102183.pdf'
    with pdfplumber.open(path) as pdf:
        for i in pdf.pages:
            # page = pdf.pages[7]
            text = i.extract_text()
            singled_data_call.extend(re.findall('[\d]+ [0-9]{2}-[A-Z]{3}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [\d]+ [\d]+ [\d]+ [\d]+ [\d]+ [\d]+\.[0-9]{2}',text))
            singled_data_message.extend(re.findall('[\d]+ [0-9]{2}-[A-Z]{3}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [\d]+ [\d]+ [\d]+ [\d]+ [\d]+.[0-9]{2}',text))
    for i in singled_data_call:
        categoies_data=i.split(' ')
        data_dict_call['No.'].append(categoies_data[0])
        data_dict_call['Date'].append(categoies_data[1])
        data_dict_call['Time'].append(categoies_data[2])
        data_dict_call['Number'].append(categoies_data[3])
        data_dict_call['Used Usage(sec)'].append(int(categoies_data[4]))
        data_dict_call['Billed Usage(sec)'].append(int(categoies_data[5]))
        data_dict_call['Free Usage(sec)'].append(int(categoies_data[6]))
        data_dict_call['Chargeable Usage(sec)'].append(int(categoies_data[7]))
        data_dict_call['Amount'].append(float(categoies_data[8]))

    for i in singled_data_message:
        categoies_data=i.split(' ')
        data_dict_message['No.'].append(categoies_data[0])
        data_dict_message['Date'].append(categoies_data[1])
        data_dict_message['Time'].append(categoies_data[2])
        data_dict_message['Number'].append(categoies_data[3])
        data_dict_message['Total Usage'].append(int(categoies_data[4]))
        data_dict_message['Free Usage'].append(int(categoies_data[5]))
        data_dict_message['Billed Usage'].append(int(categoies_data[6]))
        data_dict_message['Amount'].append(float(categoies_data[7]))

def for_cleaning_no():
    """This will append the dictionary of all the different no in the pdf
        along with their position in the pdf for call"""
    for i in range(len(data_dict_call['Number'])):
        if data_dict_call['Number'][i] not in diff_No_with_position_call:
            diff_No_with_position_call[data_dict_call['Number'][i]]=[i]
        else:
            diff_No_with_position_call[data_dict_call['Number'][i]].append(i)

def for_cleaning_calls_date():
    """This will append the dictionary of position of all 
        the different dates in the pdf for call"""
    for i in range(len(data_dict_call['Date'])):
        if data_dict_call['Date'][i] not in diff_Date_with_position_call:
            diff_Date_with_position_call[data_dict_call['Date'][i]]=[i]
        else:
            diff_Date_with_position_call[data_dict_call['Date'][i]].append(i)

def for_cleaning_message():
    """This will append the dictionary of position of all different number in message"""
    for i in range(len(data_dict_message['Number'])):
        if data_dict_message['Number'][i] not in diff_No_with_position_message:
            diff_No_with_position_message[data_dict_message['Number'][i]]=[i]
        else:
            diff_No_with_position_message[data_dict_message['Number'][i]].append(i)

def for_cleaning_message_date():
    """This will append the dictionary of position of all different date in message"""
    for i in range(len(data_dict_message['Date'])):
        if data_dict_message['Date'][i] not in diff_Date_with_position_message:
            diff_Date_with_position_message[data_dict_message['Date'][i]]=[i]
        else:
            diff_Date_with_position_message[data_dict_message['Date'][i]].append(i)

def data_cleaning():
    """This will clean data quickly with the power of multithreading"""
    t1=threading.Thread(target=for_cleaning_no)
    t2=threading.Thread(target=for_cleaning_calls_date)
    t3=threading.Thread(target=for_cleaning_message)
    t4=threading.Thread(target=for_cleaning_message_date)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

def hour_min_sec(total_time):
    """This will convert seconds data into hour minute second like '2 hr 15 min 45 sec'"""
    time=''
    if total_time>60:
        total_time_in_hour=total_time//3600
        total_time_in_seconds=total_time%3600
        if total_time_in_seconds>=60:
            total_time_in_minutes=total_time_in_seconds//60
            total_time_in_seconds=total_time_in_seconds%60
        else:
            total_time_in_minutes=0
    elif total_time==0:
        total_time_in_hour=0
        total_time_in_minutes=0        
        total_time_in_seconds=0
        time='0 sec'
    else:
        total_time_in_hour=0
        total_time_in_minutes=0
        total_time_in_seconds=total_time

    if total_time_in_hour != 0:
        time+=f"{total_time_in_hour} hr "
    if total_time_in_minutes != 0:
        time+=f"{total_time_in_minutes} min "
    if total_time_in_seconds !=0:
        time+=f"{total_time_in_seconds} sec "
    return time

def data_analysis():
    """This will print some analised data"""
    print("List of top 5 contacts")
    for contacts in Counter(data_dict_call['Number']).most_common(5):
        print(contacts)
    print(f"Total contacts contacted = {len(diff_No_with_position_call.keys())}")
    total_time=sum(data_dict_call['Used Usage(sec)'])
    time_hour_min_second=hour_min_sec(total_time)
    print(f"Total voice time = {time_hour_min_second}")
    print(f"Daily average talktime = {hour_min_sec(round(total_time/len(diff_Date_with_position_call.keys())))}/ day")
    print(f"Total messaage sent = {len(data_dict_message['No.'])}")

def graph_most_contacted(command):
    """This will make the graph of top 10 contacted person in graph 
        with total no of calls in whole pdf"""
    top_contacts=Counter(data_dict_call['Number']).most_common(10)
    x_val=[x[0] for x in top_contacts]
    y_val=[x[1] for x in top_contacts]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 1')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("Total No. of calls with contact no.\nonly top 10") 
    plt.xlabel("Contact No. ") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of calls')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_messaged(command):
    """This will make the graph of contacts which has messaged with most only top 10"""
    top_contacts=Counter(data_dict_message['Number']).most_common(10)
    x_val=[x[0] for x in top_contacts]
    y_val=[x[1] for x in top_contacts]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 4')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("Total No. of messaage with contact no.\nonly top 10") 
    plt.xlabel("Contact No. ") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of messaage')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_calls_which_day(command):
    """This will make the graph of most calls which day only top 10"""
    max_calls_day_data=Counter(data_dict_call['Date']).most_common(10)
    x_val=[x[0] for x in max_calls_day_data]
    y_val=[x[1] for x in max_calls_day_data]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 2')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("Maximum calls done in a certain day graph\nonly top 10") 
    plt.xlabel("Day") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of calls')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def graph_most_message_which_day(command):
    """This will make the graph of most message which day"""
    max_calls_day_data=Counter(data_dict_message['Date']).most_common(10)
    x_val=[x[0] for x in max_calls_day_data]
    y_val=[x[1] for x in max_calls_day_data]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 5')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("Maximum calls done in a certain day graph\nonly top 10") 
    plt.xlabel("Day") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of calls')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def manage_hour_and_duration(duration,index1,index2,time_in_secs_with_duration,time_in_secs,hour,hourly_with_total_duration):
    """This will make the dictionary of duration of call every hour"""
    if time_in_secs_with_duration>hour_list[index1] and time_in_secs_with_duration<=hour_list[index2]:
        if hour not in hourly_with_total_duration.keys():
            hourly_with_total_duration[hour]=duration
        else:
            hourly_with_total_duration[hour]=hourly_with_total_duration[hour]+duration
    else:
        if hour not in hourly_with_total_duration.keys():
            hourly_with_total_duration[hour]=hour_list[index2]-time_in_secs
        else:
            hourly_with_total_duration[hour]=hourly_with_total_duration[hour]+(hour_list[index2]-time_in_secs)
        duration1=duration-(hour_list[index2]-time_in_secs)
        time_in_secs=hour_list[index2]
        indexa=index1+1
        indexb=index2+1
        hour_new=hour+1
        if indexa==24:
            indexa=0
            indexb=1
            hour_new=0
            time_in_secs_with_duration_new=time_in_secs_with_duration-86400
            time_in_secs=0
        else:
            time_in_secs_with_duration_new=time_in_secs_with_duration
        manage_hour_and_duration(duration1,indexa,indexb,time_in_secs_with_duration_new,time_in_secs,hour_new,hourly_with_total_duration)

def graph_hourly_call_duration(command):
    """This will make the graph duration of call in every hour"""
    time_list=data_dict_call['Time']
    duration_list=data_dict_call['Used Usage(sec)']

    hourly_with_total_duration={}

    for i in range(len(time_list)):
        time=time_list[i]
        duration=duration_list[i]
        time_splited=time.split(':')
        time_in_secs=(int(time_splited[0])*3600)+(int(time_splited[1])*60)+int(time_splited[2])
        index1=0
        index2=1
        while True:
            if time_in_secs>hour_list[index1] and time_in_secs<hour_list[index2]:
                hour=hour_list.index(hour_list[index1])
                break
            else:
                index1+=1
                index2+=1
        time_in_secs_with_duration=time_in_secs+duration
        manage_hour_and_duration(duration,index1,index2,time_in_secs_with_duration,time_in_secs,hour,hourly_with_total_duration)

    shorted_data=[]
    for i in range(24):
        if i in hourly_with_total_duration.keys():
            shorted_data.append((i,hourly_with_total_duration[i]))
        else:
            shorted_data.append((i,0))
    x_val=[x[0] for x in shorted_data]
    y_val=[x[1] for x in shorted_data]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 3')
    plt.plot(x_val,y_val)
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title("Duration of calls in every hour") 
    plt.xticks(x_val)
    plt.xlabel("Hour") 
    plt.ylabel('Total duration in seconds')
    while True:
        if command.empty()==False:
            plt.show()
            break
        else:
            pass

def day_most_call_specific_contact(number,list_of_date_of_call_specific_contact):
    """This will make the graph of most calls by specific contacts by day only top 10"""
    max_calls_day_data=Counter(list_of_date_of_call_specific_contact).most_common(10)
    x_val=[x[0] for x in max_calls_day_data]
    y_val=[x[1] for x in max_calls_day_data]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 8')
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title(f"Maximum calls by {number} on certain day graph\nonly top 10") 
    plt.xlabel("Day") 
    plt.gcf().autofmt_xdate()
    plt.ylabel('Total number of calls')
    plt.show()    

def hour_most_call_specific_contact(number):
    """This will make the graph of hour in which most calls happened"""
    list_hour=[[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0], [23, 0]]
    try:
        position_for_calls=diff_No_with_position_call[number]
        list_of_time_of_call_specific_contact=[]
        for i in position_for_calls:
            list_of_time_of_call_specific_contact.append(data_dict_call["Time"][i])

        for i in list_of_time_of_call_specific_contact:
            hour=int(i.split(':')[0])
            for i in list_hour:
                if hour==i[0]:
                    i[1]+=1
    except:
        pass
    x_val=[x[0] for x in list_hour]
    y_val=[x[1] for x in list_hour]
    fig = pylab.gcf()
    fig.canvas.set_window_title('Figure 9')
    plt.plot(x_val,y_val)
    plt.bar(x_val,y_val ,color ='blue',width = 0.4)
    plt.title(f"Most calls in which hour with {number}") 
    plt.xticks(x_val)
    plt.xlabel("Hour") 
    plt.ylabel('Total no. of calls')
    plt.show()

def data_analysis_specific_contacts(code,match_list,match_list1):
    """Showing the result of analysis of specific number"""
    try:
        number=list(diff_No_with_position_call)[match_list[code]]
    except:
        number=list(diff_No_with_position_message)[match_list1[code]]
    print(f"Showing deatils of {number}")
    try:
        position_for_calls=diff_No_with_position_call[number]
    except:
        position_for_calls=[]
    try:
        position_for_message=diff_No_with_position_message[number]
    except:
        position_for_message=[]
    print(f"Total no. of calls:- {len(position_for_calls)}")
    print(f"Total no. of messaage:- {len(position_for_message)}")
    total_time=0
    for i in position_for_calls:
        total_time+=data_dict_call['Used Usage(sec)'][i]
    print(f"Total talk duration:- {hour_min_sec(total_time)}")

    try:
        position_for_calls=diff_No_with_position_call[number]
        list_of_date_of_call_specific_contact=[]
        for i in position_for_calls:
            list_of_date_of_call_specific_contact.append(data_dict_call["Date"][i])
        unique_date_of_call=[]
        for i in list_of_date_of_call_specific_contact:
            if i not in unique_date_of_call:
                unique_date_of_call.append(i)
    except:
        unique_date_of_call=[]
        list_of_date_of_call_specific_contact=[]
    try:
        position_for_message=diff_No_with_position_message[number]
        list_of_date_of_message_specific_contact=[]
        for i in position_for_message:
            list_of_date_of_message_specific_contact.append(data_dict_call["Date"][i])
        unique_date_of_message=[]
        for i in list_of_date_of_message_specific_contact:
            if i not in unique_date_of_message:
                unique_date_of_message.append(i)
    except:
        unique_date_of_message=[]
    print(f"Total day contacted {len(unique_date_of_call)+len(unique_date_of_message)} ({len(unique_date_of_call)} day by calls and {len(unique_date_of_message)} day by messages)")
    p6=multiprocessing.Process(target=day_most_call_specific_contact,args=(number,list_of_date_of_call_specific_contact,),daemon=True)
    p7=multiprocessing.Process(target=hour_most_call_specific_contact,args=(number,),daemon=True)
    p6.start()
    p7.start()
    specific_contact_details()


def specific_contact_details():
    """This will filter the details of specific contact"""
    number=input("\nPlease enter the number you want detailed analysis:- \n\t")
    if number=='exit' or number=='z':
        exit()
    match_list=[]
    match_list1=[]
    possible_number=[]
    for i in diff_No_with_position_call.keys():
        possible_number.append(i)
    for i in diff_No_with_position_message.keys():
        if i not in possible_number:
            possible_number.append(i)
    check=0
    for i in possible_number:
        if number in i:
            try:
                match_list.append(list(diff_No_with_position_call).index(i))
                check=1
            except:
                match_list1.append(list(diff_No_with_position_message).index(i))
                check=1
    if check!=1:
        print(f"Data not available for this Number {number}")
        specific_contact_details()

    if len(match_list)>1:
        print(f"Found {len(match_list)} results:-")
        print("Code    Number")
        Sl_no=0
        for i in match_list:
            Sl_no+=1
            number=list(diff_No_with_position_call)[i]
            print(f"{Sl_no}{' '*(18-len(number)-len(str(Sl_no)))}{number}")
        
        while True:
            code=int(input("\nPlease provide the code to get detailed data of number:- "))
            if code=='exit' or code=='z':
                exit()
            if Sl_no<code:
                print("Please provide the right value....")
                print("Type 'exit' to exit the program")
                pass
            else:
                break
    else:
        code=1
    code=code-1
    data_analysis_specific_contacts(code,match_list,match_list1)

if __name__ == '__main__':
    data_dict_call={'No.':[],'Date':[],'Time':[],'Number':[],'Used Usage(sec)':[],'Billed Usage(sec)':[],'Free Usage(sec)':[],'Chargeable Usage(sec)':[],'Amount':[]}
    data_dict_message={'No.':[],'Date':[],'Time':[],'Number':[],'Total Usage':[],'Free Usage':[],'Billed Usage':[],'Amount':[]}
    # data_dict_call={'No.': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263', '264', '265', '266', '267', '268', '269', '270', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'], 'Date': ['04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '04-JUL-22', '03-JUL-22', '03-JUL-22', '03-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '01-JUL-22', '01-JUL-22', '01-JUL-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '23-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '22-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '21-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '20-JUN-22', '19-JUN-22', '19-JUN-22', '19-JUN-22', '19-JUN-22', '19-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '18-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '17-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '15-JUN-22', '15-JUN-22', '15-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '11-JUN-22', '10-JUN-22', '10-JUN-22', '10-JUN-22', '10-JUN-22', '10-JUN-22', '10-JUN-22', '10-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '09-JUN-22', '08-JUN-22', '08-JUN-22', '08-JUN-22', '03-JUL-22', '02-JUL-22', '28-JUN-22', '27-JUN-22', '26-JUN-22', '26-JUN-22', '25-JUN-22', '23-JUN-22', '22-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '10-JUN-22', '10-JUN-22'], 'Time': ['22:42:16', '22:24:17', '22:23:39', '19:34:56', '18:03:03', '18:00:11', '17:58:51', '16:04:06', '15:14:27', '13:47:14', '20:23:45', '17:27:49', '00:33:00', '21:44:09', '20:29:09', '19:00:47', '18:50:04', '18:49:39', '18:45:34', '14:00:51', '09:45:37', '19:29:39', '19:27:55', '09:40:47', '23:32:16', '23:20:32', '23:20:19', '22:48:32', '21:04:21', '20:44:39', '20:23:26', '20:11:08', '19:33:49', '18:49:33', '18:44:03', '18:42:41', '22:51:25', '22:50:22', '22:42:54', '22:36:05', '20:46:44', '20:27:14', '20:25:49', '20:25:11', '19:58:03', '18:39:33', '18:17:21', '17:18:55', '16:58:56', '16:17:43', '13:52:54', '13:39:39', '13:30:27', '11:06:40', '11:00:02', '10:40:19', '10:39:34', '20:12:51', '20:06:29', '19:17:12', '19:16:12', '18:40:43', '18:33:07', '18:24:01', '17:15:50', '17:10:36', '17:10:12', '14:03:35', '13:49:00', '13:36:57', '10:36:02', '08:56:09', '08:55:33', '22:44:37', '22:42:04', '21:19:39', '20:37:16', '20:08:24', '18:10:14', '17:33:37', '17:14:25', '13:48:08', '13:39:10', '13:09:51', '23:07:05', '21:42:26', '21:41:50', '20:50:46', '20:49:53', '20:33:41', '19:15:27', '19:08:07', '18:37:24', '17:21:56', '17:04:36', '17:02:46', '13:27:51', '13:27:35', '10:46:41', '22:57:47', '18:26:19', '18:21:29', '18:01:59', '17:56:17', '14:51:31', '19:19:51', '19:10:15', '18:38:13', '18:35:21', '17:46:42', '17:04:07', '16:58:28', '16:21:52', '16:18:23', '16:17:32', '15:55:54', '15:46:30', '10:22:24', '20:31:18', '19:58:51', '19:24:17', '17:19:45', '17:19:21', '15:17:26', '14:51:42', '13:26:10', '11:36:04', '11:18:43', '22:51:53', '22:00:01', '21:59:18', '21:29:59', '21:07:03', '20:20:39', '20:18:43', '19:05:03', '18:39:57', '18:36:40', '18:21:45', '18:13:57', '14:16:49', '14:13:47', '13:53:16', '12:01:05', '09:14:52', '00:04:24', '23:31:54', '23:31:40', '22:59:57', '22:59:06', '22:48:57', '19:17:20', '18:42:31', '15:17:29', '12:25:48', '08:36:34', '07:46:57', '07:40:42', '22:45:09', '22:41:44', '18:45:23', '17:17:42', '17:13:22', '20:15:20', '19:21:37', '14:11:11', '13:39:22', '13:14:14', '06:28:20', '06:20:23', '06:01:33', '05:59:56', '05:56:30', '00:11:57', '00:02:00', '23:55:35', '23:26:44', '23:18:53', '23:14:59', '22:12:52', '22:05:10', '21:56:47', '21:47:28', '21:42:44', '20:52:18', '19:47:08', '19:32:21', '18:47:54', '18:43:42', '18:41:04', '18:28:29', '16:19:26', '11:08:22', '20:16:11', '19:30:42', '19:29:24', '12:42:46', '07:21:58', '22:26:45', '18:40:55', '17:25:06', '22:12:11', '21:43:08', '20:07:07', '15:00:35', '13:36:11', '13:35:13', '13:18:51', '13:16:25', '08:34:22', '08:27:55', '08:21:14', '20:55:26', '19:03:12', '17:39:58', '17:28:09', '17:25:33', '13:19:13', '08:46:02', '07:48:39', '21:08:32', '21:04:20', '21:02:04', '20:06:57', '18:06:47', '17:53:54', '17:48:51', '17:10:25', '11:32:49', '11:23:27', '11:19:43', '09:02:07', '22:50:10', '22:45:01', '22:31:41', '20:46:02', '19:53:38', '19:47:53', '17:40:16', '17:37:40', '17:37:33', '15:37:37', '15:26:45', '15:17:42', '13:12:03', '12:55:36', '21:19:02', '20:01:42', '17:29:25', '13:50:33', '13:22:52', '11:29:48', '07:43:53', '19:12:35', '18:44:18', '18:26:41', '18:10:59', '17:54:27', '17:48:31', '17:35:08', '17:34:31', '17:33:44', '17:31:45', '14:22:23', '14:02:50', '12:34:07', '08:01:49', '22:51:31', '22:01:12', '21:58:42', '13:24:20', '18:42:42', '19:59:32', '14:44:26', '21:05:53', '18:11:57', '14:34:33', '22:49:45', '21:11:45', '21:00:54', '20:33:32', '00:27:24', '00:26:49', '00:25:56', '00:22:45', '12:38:34', '12:34:36'], 'Number': ['917091765672', '919905863812', '917372030881', '919798823368', '919523949944', '919523949944', '916206262657', '919798823368', '919798823368', '919798823368', '916206262657', '918235355697', '919798823368', '918539874461', '916207736121', '916206262657', '917209083642', '917209083642', '916206262657', '919798823368', '919798823368', '919905863812', '919798823368', '919798823368', '919798823368', '919798823368', '919905863812', '919798823368', '916200883522', '917372030881', '919905863812', '919905464304', '919905863812', '919006853101', '919905464304', '916206262657', '918210795352', '919798823368', '919798823368', '919798823368', '916207736121', '917858803528', '917858803528', '919905464304', '917209083642', '919798823368', '919835226865', '919905613099', '916206262657', '918210795352', '919905863812', '919905863812', '919798823368', '918210795352', '918210795352', '917209083642', '917209083642', '919905863812', '919905464304', '919031885354', '919905464304', '919905863812', '919798823368', '919798823368', '916206262657', '916206262657', '916206262657', '918210795352', '918210795352', '917858803528', '919798823368', '918797235679', '918235355697', '917372030881', '917372030881', '919905863812', '917372030881', '916207736121', '919905863812', '919798823368', '919905863812', '918210795352', '918235355697', '919798823368', '919798823368', '919546081467', '919546081467', '916206262657', '916206262657', '919546081467', '919546081467', '919546081467', '919113715677', '919798823368', '919798823368', '919905863812', '917858803528', '917858803528', '919835260824', '919798823368', '916206262657', '916206262657', '918235355697', '919835260824', '919798823368', '919905863812', '919905863812', '919798823368', '919905464304', '919905464304', '919905464304', '919798823368', '919835260824', '919798823368', '919798823368', '917858803528', '919798823368', '919798823368', '918797235679', '919905863812', '916206262657', '919798823368', '919798823368', '919798823368', '919031885354', '919523949944', '919798823368', '918797235679', '919905863812', '918210795352', '918210795352', '919386663368', '918709138281', '919798823368', '917858803528', '918797235679', '919905863812', '919798823368', '917858896461', '919905863812', '918797235679', '918235355697', '919798823368', '918210795352', '918210795352', '919798823368', '919798823368', '919798823368', '919798823368', '919798823368', '919798823368', '919905863812', '918235355697', '919798823368', '919798823368', '916206262657', '919973251705', '919973251705', '919798823368', '918709138281', '919905863812', '919798823368', '919905863812', '916206262657', '919905863812', '919546081467', '917372030881', '919905863812', '919031885354', '919905863812', '919798823368', '919905863812', '919798823368', '919905863812', '919798823368', '919905863812', '919798823368', '919798823368', '919798823368', '919708250915', '919708250915', '919905863812', '916200883522', '919905863812', '918709138281', '918709138281', '919798823368', '917858803528', '919031885354', '919031885354', '919546081467', '919798823368', '919798823368', '919905863812', '916206262657', '916206262657', '918235355697', '919905863812', '919905863812', '916206262657', '919798823368', '917488645703', '917488645703', '919798823368', '919798823368', '919798823368', '919835260824', '917461807112', '919835260824', '919798823368', '916206262657', '919798823368', '918797235679', '918210795352', '918210795352', '919798823368', '919798823368', '918235355697', '919798823368', '916206262657', '916206262657', '918757467754', '918235355697', '918235355697', '919708250915', '919708250915', '919708250915', '916206262657', '919798823368', '919798823368', '919798823368', '918210795352', '919798823368', '918210795352', '918210795352', '918521027097', '916206262657', '918210795352', '919835260824', '919031885354', '919031885354', '919798823368', '919798823368', '919546081467', '918235355697', '916206262657', '917858803528', '916206262657', '918235355697', '919031885354', '918235355697', '919798823368', '919835260824', '916206262657', '917371830418', '917858896461', '918757467754', '919798823368', '919798823368', '919798823368', '918235355697', '919905464304', '919798823368', '919708250915', '919798823368', '919031885354', '919798823368', '919798482108', '917371830418', '917371830418', '919509308814', '917877402151', '917877402151', '919306381427', '917297065240', '919306381427', '919306381427', '918651054254', '918651054254', '918651054254', '918651054254', '918376800709', '918376800709', '918376800709', '918376800709', '912230430101', '912230430101'], 'Used Usage(sec)': [61, 81, 120, 17, 927, 112, 36, 371, 2872, 16, 86, 29, 8, 20, 44, 1024, 628, 13, 223, 181, 26, 189, 49, 30, 140, 592, 609, 582, 1525, 82, 2278, 9, 454, 18, 23, 33, 4115, 44, 433, 13, 47, 46, 40, 25, 73, 207, 17, 152, 117, 2326, 320, 362, 28, 457, 205, 19, 30, 783, 32, 28, 42, 970, 441, 535, 42, 61, 25, 2669, 297, 12, 150, 82, 21, 9, 75, 380, 39, 117, 68, 780, 686, 112, 47, 30, 23, 553, 5, 26, 39, 25, 4487, 432, 1789, 369, 1022, 24, 52, 9, 43, 44, 5, 23, 8, 94, 79, 686, 481, 101, 19, 14, 40, 184, 8, 98, 41, 18, 22, 209, 78, 22, 695, 153, 14, 294, 24, 692, 238, 47, 1368, 110, 26, 43, 1203, 36, 83, 219, 398, 85, 18, 170, 28, 85, 157, 732, 325, 44, 6, 4, 14, 6, 150, 31, 14, 3, 633, 306, 1677, 145, 601, 136, 157, 105, 146, 71, 138, 13, 327, 243, 47, 94, 177, 86, 188, 744, 559, 156, 1887, 38, 51, 144, 246, 416, 531, 150, 63, 61, 47, 38, 10, 61, 78, 74, 3688, 3004, 281, 37, 13, 51, 2582, 105, 178, 647, 547, 22, 781, 31, 19, 26, 15, 17, 126, 103, 10, 568, 26, 61, 106, 37, 302, 708, 113, 191, 16, 3, 42, 36, 36, 65, 1240, 500, 191, 322, 35, 276, 7, 50, 1838, 304, 34, 91, 7, 50, 570, 470, 16, 25, 70, 301, 5, 10, 93, 765, 13, 140, 39, 42, 37, 111, 309, 65, 25, 16, 94, 205, 1, 52, 13, 14, 174, 109, 1418, 158, 315, 2074, 809, 9, 64, 1653, 1997, 191, 531, 16, 25, 40, 27, 46, 114], 'Billed Usage(sec)': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Free Usage(sec)': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Chargeable Usage(sec)': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Amount': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]}
    # data_dict_message={'No.': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240'], 'Date': ['04-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '02-JUL-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '30-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '28-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '27-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '26-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '25-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '24-JUN-22', '22-JUN-22', '22-JUN-22', '19-JUN-22', '18-JUN-22', '17-JUN-22', '17-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '16-JUN-22', '15-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '14-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '13-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '12-JUN-22', '09-JUN-22'], 'Time': ['22:22:55', '18:46:35', '18:46:15', '18:45:52', '14:02:17', '22:57:47', '22:57:42', '22:57:30', '22:56:38', '22:56:35', '22:56:32', '14:56:39', '13:46:01', '13:21:14', '13:21:10', '13:20:34', '19:50:54', '19:49:03', '19:47:30', '19:46:39', '13:37:22', '22:59:50', '22:43:37', '18:48:02', '18:48:01', '18:41:54', '22:43:12', '22:41:25', '22:41:19', '21:40:48', '18:51:07', '18:48:03', '18:15:16', '19:02:54', '19:02:19', '19:01:11', '18:48:22', '18:47:09', '18:47:06', '18:46:56', '18:46:40', '18:46:34', '18:46:30', '18:46:26', '18:27:23', '18:26:52', '18:26:23', '17:59:25', '16:33:42', '15:24:53', '15:02:31', '14:52:50', '11:20:18', '22:38:20', '00:11:59', '18:49:07', '11:06:51', '23:35:33', '23:34:32', '23:31:06', '23:29:05', '23:27:29', '23:24:46', '23:24:03', '23:24:01', '23:24:00', '23:22:57', '23:22:46', '23:22:04', '23:20:52', '23:20:12', '23:19:45', '23:19:01', '23:18:58', '23:17:52', '23:17:25', '23:16:55', '23:16:52', '23:16:28', '23:15:16', '23:14:53', '23:13:52', '23:13:22', '23:12:19', '23:12:11', '23:10:40', '23:10:34', '23:08:54', '23:08:19', '23:08:10', '23:08:03', '23:07:56', '23:07:36', '23:07:36', '23:07:19', '23:06:57', '23:06:18', '23:06:14', '23:06:14', '23:06:06', '23:06:04', '23:06:04', '23:05:37', '23:04:57', '23:04:20', '23:03:45', '23:03:01', '23:02:42', '23:01:02', '23:00:27', '22:59:49', '22:59:36', '22:59:12', '22:58:43', '22:58:25', '22:58:10', '22:57:13', '22:56:58', '22:56:25', '22:56:23', '22:55:59', '22:55:38', '22:55:08', '22:54:34', '22:54:06', '22:54:00', '22:53:40', '22:53:13', '22:52:54', '22:52:48', '22:52:46', '22:52:38', '22:52:19', '22:51:56', '22:51:02', '22:50:58', '22:50:49', '22:50:44', '22:49:50', '22:49:37', '22:48:57', '22:46:25', '10:02:31', '23:04:33', '23:03:28', '23:01:26', '23:01:19', '23:01:17', '22:53:54', '22:47:16', '22:37:59', '22:37:56', '22:36:41', '22:35:40', '22:34:07', '21:30:16', '21:30:06', '21:30:06', '20:54:43', '08:22:58', '07:48:39', '07:48:21', '07:47:55', '07:47:53', '07:47:50', '07:46:00', '07:42:26', '07:41:37', '07:41:04', '07:40:49', '07:39:17', '07:38:08', '07:37:45', '07:37:38', '07:37:33', '07:37:23', '07:37:14', '07:36:36', '07:36:25', '07:35:47', '07:35:10', '07:34:30', '07:34:21', '07:33:52', '07:33:45', '07:31:48', '07:30:46', '07:30:06', '07:29:26', '07:23:35', '07:22:13', '23:06:28', '23:06:19', '23:06:14', '23:05:59', '23:05:46', '23:05:33', '23:05:30', '23:05:27', '23:04:46', '23:04:15', '23:03:40', '23:03:34', '23:03:23', '23:03:13', '23:02:52', '23:02:24', '23:02:20', '23:01:55', '23:01:47', '23:01:36', '23:01:16', '23:01:12', '23:00:42', '22:59:58', '22:59:47', '22:59:04', '22:58:59', '22:58:24', '22:57:53', '22:57:30', '22:56:52', '22:56:45', '22:56:41', '22:56:33', '22:56:24', '22:55:39', '22:55:27', '22:54:25', '22:53:58', '22:52:32', '22:51:59', '22:50:38', '22:50:22', '19:35:29', '18:55:15', '18:54:52', '18:54:52', '18:54:52', '14:04:27'], 'Number': ['919905863812', '919509308814', '919509308814', '917877402151', '919905863812', '919798823368', '919798823368', '919798823368', '919798823368', '919798823368', '919798823368', '919798823368', '919031885354', '919031885354', '919031885354', '919798823368', '918210795352', '918210795352', '918210795352', '918210795352', '917858803528', '918210795352', '917372030881', '918210795352', '918210795352', '918797235679', '919546081467', '919546081467', '919546081467', '919546081467', '919905613099', '919546081467', '919798823368', '919798823368', '919798823368', '919798823368', '917091765672', '917091765672', '917091765672', '919798823368', '917091765672', '917091765672', '917091765672', '917091765672', '916206262657', '916206262657', '916206262657', '917091765672', '919798823368', '919798823368', '919798823368', '919031885354', '918797235679', '918709138281', '919798823368', '919798823368', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919798823368', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '918797235679', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '919546081467', '918757467754', '919546081467', '919546081467', '919546081467', '919546081467', '0000'], 'Total Usage': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'Free Usage': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'Billed Usage': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Amount': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
    hour_list=[0,3600,7200,10800,14400,18000,21600,25200,28800,32400,36000,39600,43200,46800,50400,54000,57600,61200,64800,68400,72000,75600,79200,82800,86400]
    diff_No_with_position_call={}
    diff_No_with_position_message={}
    diff_Date_with_position_call={}
    diff_Date_with_position_message={}
    command=multiprocessing.Queue()
    path=input("Enter the path of the file:- ")
    print("Collecting data....")
    data_collection()
    print("Cleaning data....")
    data_cleaning()
    print("Analising data....\n")
    data_analysis()
    p1=multiprocessing.Process(target=graph_most_contacted,args=(command,),daemon=True)
    p2=multiprocessing.Process(target=graph_most_calls_which_day,args=(command,),daemon=True)
    p3=multiprocessing.Process(target=graph_hourly_call_duration,args=(command,),daemon=True)
    p4=multiprocessing.Process(target=graph_most_messaged,args=(command,),daemon=True)
    p5=multiprocessing.Process(target=graph_most_message_which_day,args=(command,),daemon=True)    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    while True:
        ans=input("\nEnter 'yes' if you want to see the graph:- \n\t")
        if 'yes' in ans or 'y' == ans:
            command.put('show')
        else:
            if ans=="exit" or ans=='z':
                exit()
            else:
                pass
        specific_contact_details()
