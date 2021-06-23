from misc_definitions import *
from tx_marker import *
import pathlib
from datetime import datetime,timedelta
import json
from al_to_Freq import query_info_by_icao
import time
from os import path
import subprocess
#------------------------------------------------------


this_path = str(pathlib.Path(__file__).parent.absolute())+"\\Database\\"
with open(this_path+"bkk_arr.json") as f:
  bkk_arr = json.load(f)


#get all arr data once a day then partial update for a flight
freeTxTime = 2
tunedTxtime = 60 #min

update_time = []
txChkPnt_time = []

now = datetime.now()

lineMsg = ""


#----------------------------------------------------------------------------------------
#FOR ALL DEBUGGING
LUGER_AGBS = "Or5ik6zL73GAFSuLbhVdJGR5uwFelbMfU89iWIDafBB"


#RCU ONLY
#CHROME_PATH = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROME_PATH = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = r'C:\\chromedriver.exe'
CHROME_Setup = [CHROME_PATH , CHROMEDRIVER_PATH]

app_path = str(pathlib.Path(__file__).parent.absolute())
logPath = app_path + "\\" + "_LOG"

#----------------------------------------------------------------------------------------

inbound_sts = ['estimated','delayed','landed']
schduled_sts = ['scheduled']
schduled_flg = []

for i in range(len(bkk_arr)):
    
    fl_allData  = bkk_arr[i]
    fl_id       = bkk_arr[i]['flight']['identification']['number']['default']
    fl_callsign = bkk_arr[i]['flight']['identification']['callsign']

    fl_sts_type = bkk_arr[i]['flight']['status']['text']
    fl_sts_2 = bkk_arr[i]['flight']['status']['generic']['status']['text'] #landed , scheduled , delayed , estimated

    if  bkk_arr[i]['flight']['airline'] == 'None':
        print('++++skip , ' , fl_id)
        continue

    fl_airLineName = bkk_arr[i]['flight']['airline']['name']
    #fl_airLineCod2 = bkk_arr[i]['flight']['airline']['code']['iata']
    fl_airLineCod3 = bkk_arr[i]['flight']['airline']['code']['icao']

    #print(fl_id ,'|', fl_callsign ,'|', fl_sts_1 ,'|', fl_sts_2)

    if fl_sts_2 in inbound_sts:

        fl_date = bkk_arr[i]['flight']['status']['generic']['eventTime']['local_date']
        fl_time = bkk_arr[i]['flight']['status']['generic']['eventTime']['local_time']

        fl_datetime = time_int_converter(fl_date , fl_time , 'tst') #in datetime object

        tx_chkpnt_time = time_int_subtracter(fl_date , fl_time , tunedTxtime , 'tst')

        #fake_now = datetime(2021, 1, 14 , 11 , 40 , 00)
        #print(fake_now)
        #print(type(tx_chkpnt_time) , type(now))

        #chkpnt_delta
        inbound_delta  = tx_chkpnt_time - now
        arrived_delta = fl_datetime - now

        check_flag = inbound_delta.days  + arrived_delta.days
        
        handling_freq , handling_group , _ , _ , _ , _  = query_info_by_icao(fl_airLineCod3)
        cmd_msg = ''

        if check_flag == -2  and handling_freq > 0:
            
            flg_msg = fl_airLineName + ' ' + fl_callsign
            sts_msg = 'Status : Landed'
            tx_msg  = 'Pending : Tx ' +  str(handling_freq) + ', Group : ' + handling_group


            #cmd_msg , cmd_returncode = tx_setFree(fl_airLineCod3)
            cmd_msg , cmd_returncode = tx_setPending(fl_airLineCod3)

            #Summary message
            msg =  flg_msg + '\n\t\t ' + sts_msg +  '\n\t\t ' + tx_msg + '\n\t\t ' + cmd_msg + ' cmd_returncode : ' + str(cmd_returncode)

            if cmd_returncode == 1 :
                line_sender(LUGER_AGBS , msg)

        elif check_flag == -1 and handling_freq > 0 :
           
            flg_msg = fl_airLineName + ' ' + fl_callsign
            sts_msg = 'Status : INBOUND!!' + str(inbound_delta)
            tx_msg  = 'TUNE : Tx to ' +  str(handling_freq) + ', Group : ' + handling_group

            cmd_msg , cmd_returncode = tx_setReserve(fl_airLineCod3 , CHROME_Setup , logPath , LUGER_AGBS)

            #Summary message
            msg =  flg_msg + '\n\t\t ' + sts_msg +  '\n\t\t ' + tx_msg + '\n\t\t ' + cmd_msg + ' cmd_returncode : ' + str(cmd_returncode)

            if cmd_returncode == 1 :
                line_sender(LUGER_AGBS , msg)

        elif handling_freq == 0:
            flg_msg = fl_airLineName + ' ' + fl_callsign
            sts_msg = 'Status : NO FREQ PROVIDED'

            msg =  flg_msg + '\n\t\t ' + sts_msg
            #line_sender(LUGER_AGBS , msg)
        
        else :
            msg = 'NO ACTION'

        #Reduced
        if check_flag < 0 :
            #print(fl_callsign ,'|', fl_sts_2,'|',  fl_datetime.strftime('%H:%m') ,' | chkpnt : ' , tx_chkpnt_time.strftime('%H:%m') , ' | now : ' , now.strftime('%H:%m'))
            print(fl_callsign ,'|', fl_sts_2,'|',  fl_datetime.strftime('%H:%M') ,' | chkpnt : ' , tx_chkpnt_time.strftime('%H:%M') , ' | now : ' , now.strftime('%H:%M'))
            print('Status : TX delta  = ', inbound_delta.days , '| Landed delta = ',arrived_delta.days , ' // FLAG = ' , check_flag)
            print('Result :' ,  msg)
            print('---------------------------------------------------------------------------------------------------------------------')

        update_time.append(fl_datetime)
        txChkPnt_time.append(tx_chkpnt_time)

    elif fl_sts_2 in schduled_sts:
        schduled_flg.append(fl_id)

print('PENDING CHECK')
p2f_msg , p2f_returncode = tx_setPending2Free(freeTxTime , CHROME_Setup , logPath , LUGER_AGBS)
print('Release code : ' , p2f_returncode)
print(p2f_msg)

print("Next scheduled  flight " , schduled_flg)

last_msg = 'p2f return code = ' + str(p2f_returncode) + '\n' + p2f_msg + '\n' + 'Next scheduled  flight ' + str(len(schduled_flg))

line_sender(LUGER_AGBS , last_msg)