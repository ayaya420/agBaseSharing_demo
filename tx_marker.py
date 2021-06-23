from misc_definitions import  *
import random
import pathlib
from datetime import datetime,timedelta
import json
import excel2json  #pip install excel2json-3
import xlsxwriter
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer
from al_to_Freq import query_info_by_icao
from convertExcel2json import excel2json_nm
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import time
from os import path
import timeit
from hw_control import *


def tx_setReserve(al_code3 , CHROME_Setup , logPath , line_api):
  this_path = str(pathlib.Path(__file__).parent.absolute())+"\\DATABASE\\"
  excel2json_nm(this_path,"tx_database")

  with open(this_path+'tx_database.json') as f:
    tx = json.load(f)


  #print(len(tx) , tx[1]['tx_id'])


  AVA_List       = []
  AVA_weight_list     = []
  
  
  now_str = str(datetime.now())
  
  airLine_use = 0
  airLine_use_index = 0
  tx_fq = 0
  tx_fq_index = 0
  cmd_msg = ''
  cmd_returncode = 0

  #query data from al_to_freq
  hl_freq , hl_Grp , air_Name , _ , air_code3 , rcu_ipaddr = query_info_by_icao(al_code3)

  for i in range(len(tx)):

      #Scan เฉพาะตัวที่ไม่มีใครใช้ tx_sts = AVA
      if tx[i]['tx_sts'] == 'AVA': 
        AVA_List.append(tx[i]['tx_id'])
        AVA_weight_list.append(1/tx[i]['tx_weigth_score'])

      #Scan หาความถี่ที่มีคนใช้งานอยู่แล้ว
      if tx[i]['tx_usedBy'] == hl_Grp:
        airLine_use       = 1
        airLine_use_index = i

      #SCAN หาความถี่ของ tx handling นั้นมีเปิดค้างไว้ที่เครื่องไหนบ้าง
      if tx[i]['tx_Freq'] == hl_freq:
        tx_fq       = 1
        tx_fq_index = i



  #CASE#1 AVA > 0 and no Tx use for some AL by AL Name
  # มีเครื่องว่าง                       AVA  > 0
  # Airline นั้นๆ ไม่มีการใช้งานเครื่องส่ง  airLine_use == 0
  # ไม่มีเครื่องส่งไหน เปิดความถี่นั้นค้างไว้   tx_fq == 0
  if len(AVA_List) != 0 and airLine_use == 0 and tx_fq == 0:
    #>>>EXCEL
    tx_random = int(random.choices(AVA_List, weights = AVA_weight_list, k = 1)[0])
    #print(tx_random , tx[tx_random-1]['tx_id'] , tx[tx_random-1]['tx_name'])
    #Raise score

    #Assign to EXCEL Value
    tx[tx_random-1]['tx_weigth_score'] = tx[tx_random-1]['tx_weigth_score'] +1 
    tx[tx_random-1]['tx_sts']          = 'USE'
    tx[tx_random-1]['tx_usedBy']       = hl_Grp

    tx[tx_random-1]['tx_ALname']       = air_Name
    tx[tx_random-1]['tx_ALCode3']      = air_code3
    tx[tx_random-1]['tx_Freq']         = hl_freq

    tx[tx_random-1]['last_used']       = now_str
    tx[tx_random-1]['rcu_ipaddr']      = rcu_ipaddr

    #Get from EXCEL
    tx_ip = tx[tx_random-1]['tx_ipaddr']
    #input from outside CHROME_Setup , logPath , line_api
    #>>>TX SNMP CMD
    tx_cmdReturn = tx_setFreq(tx_ip , hl_freq , logPath , line_api)

    #>>>SET RCU POINT TO TX
    ip_list = [str(rcu_ipaddr) , str(tx_ip)]
    rcu_cmdReturn = rcu_control(ip_list , CHROME_Setup , logPath , line_api)

    #>>>FINAL PHASE
    cmd_msg = tx[tx_random-1]['tx_name'] + ' | id : ' + str(int(tx[tx_random-1]['tx_id'])) + " is on air at " + str(hl_freq) + ' for Handler : ' + hl_Grp
    cmd_returncode = 1
    #print(cmd_msg)


  #CASE#2 AVA > 0 and no Tx use for some AL by AL Name
  # มีเครื่องว่าง                           AVA  > 0
  # Airline ไม่มีการใช้งานอยู่              airLine_use == 0
  # เครื่องส่งไหน เปิดความถี่กับ AL นั้นค้างไว้   tx_fq == 1
  elif len(AVA_List) != 0 and airLine_use == 0 and tx_fq == 1:

    tx[tx_fq_index]['tx_sts']          = 'USE'
    tx[tx_fq_index]['tx_usedBy']       = hl_Grp
    tx[tx_fq_index]['tx_ALname']       = air_Name
    tx[tx_fq_index]['tx_ALCode3']      = air_code3
    tx[tx_fq_index]['tx_Freq']         = hl_freq

    tx[tx_fq_index]['last_used']       = now_str
    tx[tx_fq_index]['rcu_ipaddr']      = rcu_ipaddr


    #Get from EXCEL
    tx_ip = tx[tx_fq_index]['tx_ipaddr']
    #input from outside CHROME_Setup , logPath , line_api
    #>>>TX SNMP CMD
    tx_cmdReturn = tx_setFreq(tx_ip , hl_freq , logPath , line_api)

    #>>>SET RCU POINT TO TX
    ip_list = [str(rcu_ipaddr) , str(tx_ip)]
    rcu_cmdReturn = rcu_control(ip_list , CHROME_Setup , logPath , line_api)


    cmd_msg = tx[tx_fq_index]['tx_name'] + ' | id : ' + str(int(tx[tx_fq_index]['tx_id'])) + " WAS on air at " + str(hl_freq) + ' for Handler : ' + hl_Grp
    cmd_returncode =  1
    #print(cmd_msg)


  #CASE#3 AVA > 0 and no Tx use for some AL by AL Name
  # มีเครื่องว่าง                       AVA  > 0
  # Airline นั้นๆใช้งานเครื่องส่งอยู่แล้ว    airLine_use == 1
  # ไม่มีเครื่องส่งไหน เปิดความถี่นั้นค้างไว้   tx_fq == 0 <<<  CAN Be ignored
  elif len(AVA_List) != 0 and airLine_use == 1:

    tx[airLine_use_index]['tx_sts']          = 'USE'
    tx[airLine_use_index]['tx_usedBy']       = hl_Grp
    tx[airLine_use_index]['tx_ALname']       = air_Name
    tx[airLine_use_index]['tx_ALCode3']      = air_code3
    tx[airLine_use_index]['tx_Freq']         = hl_freq

    tx[airLine_use_index]['last_used']       = now_str
    tx[airLine_use_index]['rcu_ipaddr']      = rcu_ipaddr

    #Get from EXCEL
    #tx_ip = tx[tx_fq_index]['airLine_use_index']
    #input from outside CHROME_Setup , logPath , line_api
    #>>>TX SNMP CMD
    #tx_cmdReturn = tx_setFreq(tx_ip , hl_freq , logPath , line_api)

    #>>>SET RCU POINT TO TX
    ip_list = [str(rcu_ipaddr) , str(tx_ip)]
    rcu_cmdReturn = rcu_control(ip_list , CHROME_Setup , logPath , line_api)


    cmd_msg = tx[airLine_use_index]['tx_ALname'] + ' handling by ' + hl_Grp + " is already on air!!!" 
    cmd_returncode =  0
    #print(cmd_msg)
  
  elif len(AVA_List) == 0:
    cmd_msg = "ALL TX ARE BUSY !!!"
    cmd_returncode = 1
    #print(cmd_msg)


  #print(tx)
  conv = Converter()
  conv.convert(tx, Writer(file= this_path +"tx_database.xlsx"))

  return str(cmd_msg) , int(cmd_returncode)

######################################################################
def tx_setPending(al_code3):

  this_path = str(pathlib.Path(__file__).parent.absolute())+"\\DATABASE\\"
  excel2json_nm(this_path,"tx_database")

  with open(this_path+'tx_database.json') as f:
    tx = json.load(f)

  pending_count = 0
  cmd_msg = ''
  cmd_returncode = 0


  #query data from al_to_freq
  hl_freq , hl_Grp , _ , _ , _ , _ = query_info_by_icao(al_code3)

  for i in range(len(tx)):


      if tx[i]['tx_usedBy'] == hl_Grp:
        pending_count = pending_count + 1

        tx[i]['tx_sts']      = 'PENDING'


        cmd_msg = cmd_msg + tx[i]['tx_name'] + ' | id : ' + str(int(tx[i]['tx_id'])) + ' service for : ' + hl_Grp + ' ' + str(hl_freq) + ' is PENDING to Release! ' +'\n'
        cmd_returncode = 1

  if pending_count == 0 : 
    #print("EVERY TX IS FREE FROM AIRLINE ICAO CODE : " , ALCODE3)
    cmd_msg = 'NO Tx service for : ' + hl_Grp + ' Freq : ' + str(hl_freq)
    cmd_returncode = 0

  conv = Converter()
  conv.convert(tx, Writer(file= this_path +"tx_database.xlsx"))

  return str(cmd_msg) , int(cmd_returncode)

######################################################################
def tx_setPending2Free(min_time , CHROME_Setup , logPath , line_api):

  cmd_msg = ''
  cmd_returncode = 0

  this_path = str(pathlib.Path(__file__).parent.absolute())+"\\DATABASE\\"
  excel2json_nm(this_path,"tx_database")

  with open(this_path+'tx_database.json') as f:
    tx = json.load(f)

    #pending_index = []
    for i in range(len(tx)):
        if tx[i]['tx_sts'] == 'PENDING':
            
            tx_usedBy = tx[i]['tx_usedBy']
            #tx_ALCODE3 = tx[i]['tx_ALCODE3']
            #tx_ALname = tx[i]['tx_ALname']
            tx_Freq   = tx[i]['tx_Freq']
            last_used = tx[i]['last_used']

            last_used_timeObj = datetime.strptime(last_used, '%Y-%m-%d %H:%M:%S.%f')

            release_Time = last_used_timeObj + timedelta(minutes=min_time)

            delta = datetime.now() > release_Time


            #print(last_used, ' ' , type(last_used) )
            print('USER : ' , tx_usedBy , ' FREQ : ' , tx_Freq , ' Last used : ' , last_used_timeObj.time() , ' Release Time : ' , release_Time.time() , ' Delta : ' , delta )

            if delta :
              tx_ip = str(tx[i]['tx_ipaddr'])
              change_list = [str(tx[i]['rcu_ipaddr']) , '0.0.0.0' ]

              #UNMARK in MACHINE TX
              freq  = 131.1
              #release freq from real tx
              tx_setFreq(tx_ip , freq , logPath , line_api)
              #UNMARK in MACHINE RCU
              rcu_control(change_list ,CHROME_Setup, logPath , line_api)

              #UNMARK IN EXCEL
              cmd_returncode = cmd_returncode + 1
              #print( 'TX ID : ' , tx[i]['tx_id'] , ' service for USER : ' , tx_usedBy , ' FREQ : ' , tx_Freq , ' is expired ')

              txi_msg = 'Release TX ID : ' + str(tx[i]['tx_id']) + ' service for USER : ' + tx_usedBy + ' FREQ : ' + str(tx_Freq)

              cmd_msg = cmd_msg + txi_msg +'\n'

              tx[i]['tx_sts']      = 'AVA'
              tx[i]['tx_usedBy']   = ''
              tx[i]['tx_ALname']   = ''
              tx[i]['tx_ALCode3']  = ''

              tx[i]['last_used']   = ''
              tx[i]['rcu_ipaddr']  = ''




    if cmd_returncode == 0 :
      cmd_msg = 'No Tx is released'


    conv = Converter()
    conv.convert(tx, Writer(file= this_path +"tx_database.xlsx"))

    return str(cmd_msg) , int(cmd_returncode)