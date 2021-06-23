from misc_definitions import *
import random
import pathlib
from datetime import datetime,timedelta
import json
import excel2json
import xlsxwriter
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer
from convertExcel2json import excel2json_nm

def query_info_by_icao(ALCODE3):

  this_path = str(pathlib.Path(__file__).parent.absolute())+"\\DATABASE\\"


  excel2json_nm(this_path,"airlines_to_freq")

  with open(this_path+'airlines_to_freq.json') as f:
    airlines = json.load(f)

  query_target_id = 0
  air_Name = ''
  air_code2 = ''
  air_code3 = ''

  freq   = 0
  hl_Grp = ''
  rcu_ipaddr = ''

  for i in range(len(airlines)):
      #print('tx_id : '            , tx[i]['tx_id'] , 
      #      'tx_sts : '           , tx[i]['tx_sts'] ,
      #      'tx_weigth_score  : ' , tx[i]['tx_weigth_score'])
      if airlines[i]['icao'] == ALCODE3: 
        #FOUND!!!!!
        query_target_id = i

  #print(query_target_id)
  if query_target_id != 0 :
    air_Name = airlines[query_target_id]['fullname']
    air_code2 = airlines[query_target_id]['iata']
    air_code3 = airlines[query_target_id]['icao']

    freq   = airlines[query_target_id]['freq']
    hl_Grp = airlines[query_target_id]['handling_group']

    rcu_ipaddr = str(airlines[query_target_id]['rcu_ipaddr'])

  info  = 'Name : ' + air_Name+' ('+ air_code2 + '/' + air_code3 + ')'
  info2 = 'Service Handling Group : '+ hl_Grp + ' freq : '+ str(freq) + ' MHz'
  info3 = 'RCU IP addr : ' + rcu_ipaddr
  #print(info)
  #print(info2)
  #print(info3)

  return freq , hl_Grp , air_Name , air_code2 , air_code3 , rcu_ipaddr

  