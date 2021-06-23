import pathlib
import time


def file_saver(sav_path , file_name ,  content_Text):

    offineLog_file = file_name
    file = open(sav_path+"\\"+ offineLog_file, 'a')  # w = overwrite , r = read , a = append
    #time.strftime(dateFormat) + ',' + time.strftime(timeFormat) + ',' + content_Text + '\n'
    file.write(content_Text + '\n')
    file.close()

import requests
import urllib
#NAKHON-K
#Line Group
ATN_TOKEN = "zdUSVKvt4v2St7ZQ2KjytqpGFdBVPZCPaf87gAhAvhw"
#Line Nontify
CHZNontify_TOKEN = "8pWuC8XLWGRrwuEHPug6aa3T8jODedSi95adhrf6bTT"

#K (chz.kk)
ATN_log  = "3CvkWZd5vd4YYhXd71q2gwxKhL1dxuXBFEstLj1Jf0J"
iDEP_log  = "pPjjqpbBxOK4zJENgE0eHqmZbCZd6s9mo4y0PfE7a75"

def line_sender(token , lineMsg):

    url = "https://notify-api.line.me/api/notify"

    try:
        msg = urllib.parse.urlencode({"message": lineMsg})

        LINE_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded',
                        "Authorization": "Bearer " + token}

        session = requests.Session()

        a = session.post(url, headers=LINE_HEADERS, data=msg)

        print(a.text)


    except:
        print("cannot send Line")
#------------------------------------------------------------------------------
import json
def json_fileSaver(sav_path , file_name ,  content) :

    full_path = sav_path + "\\"+file_name
    
    with open(full_path , 'w') as jsonfile:
        json.dump(content, jsonfile)

#------------------------------------------------------------------------------
from datetime import datetime,timedelta
def time_int_subtracter(date_str , time_str , offset_int , time_zone):
    #Time interger HHMM format
    
    hour   = time_str[0:2]
    minute = time_str[2:4]
    time_str = hour + ':' + minute

    #Date
    year  = date_str[0:4]
    month = date_str[4:6]
    date  = date_str[6:8]
    date_str = year+'/'+month+'/'+date

    #Date + TIME combinded
    date_time = date_str + " " + time_str

    datetime_object = datetime.strptime(date_time, '%Y/%m/%d %H:%M')


    #print(type(datetime_object))
    #print(datetime_object)  # printed in default format


    offset_subtracter = timedelta(minutes=offset_int)


    checkpoint_time = datetime_object - offset_subtracter

    if time_zone == 'tst' or time_zone == 'TST':
        checkpoint_time = checkpoint_time - timedelta(hours=7)

    #print(checkpoint_time)
    return checkpoint_time

def time_int_converter(date_str , time_str , time_zone):

    #HHMM (integer to datetime obj)
    #Time 
    hour   = time_str[0:2]
    minute = time_str[2:4]
    time_str = hour + ':' + minute

    #Date
    year  = date_str[0:4]
    month = date_str[4:6]
    date  = date_str[6:8]
    date_str = year+'/'+month+'/'+date

    #Date + TIME combinded
    date_time = date_str + " " + time_str

    datetime_object = datetime.strptime(date_time, '%Y/%m/%d %H:%M')


    #print(type(datetime_object))
    #print(datetime_object)  # printed in default format
    if time_zone == 'tst' or time_zone == 'TST':
        datetime_object = datetime_object - timedelta(hours=7)
    return datetime_object