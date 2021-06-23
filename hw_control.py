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


def tx_setFreq(tx_ip , freq , logPath , line_api):

  #input
  #tx_ip = '172.86.110.101'
  #freq = '112000000'
  #freq = 131
  str_freq = str(freq)
  str_freq = str_freq.replace('.', '')

  while(1):
      if len(str_freq)<9:
          str_freq = str_freq + '0'
      else:
          break
  freq = str_freq
  #print(freq , type(freq) , len(freq))


  #start here
  oid = '1.3.6.1.4.1.2566.127.2.2.1.1.6.5.0'
  #ProcessHERE
  #try to get
  port_lists  = ['160','161','162']
  #snmpport = ''
  SET_CMD_out = ''

  for i in range(len(port_lists)):
    
    tx_ip_port = tx_ip+':'+str(port_lists[i])
    #print(tx_ip_port)
    snmpget_Args=["snmpget" , "-v1", "-c" , "public" , tx_ip_port ,  oid]
    snmpCMD = subprocess.run(snmpget_Args,  shell=False, stdout=subprocess.PIPE, universal_newlines="\r\n")
    CMD_out = snmpCMD.stdout

    
    if len(CMD_out) > 0 :
        #snmpport = port_lists[i]
        #print(tx_ip_port , snmpport , CMD_out)
        

        snmpset_Args=["snmpset" , "-v1", "-c" , "public" , tx_ip_port ,  oid , 'u' , freq]
        snmpsetCMD = subprocess.run(snmpset_Args,  shell=False, stdout=subprocess.PIPE, universal_newlines="\r\n")
        SET_CMD_out = snmpsetCMD.stdout

        break

  
  dateFormat = "%Y.%m.%d"
  timeFormat = "%H:%M:%S"
  date_time = time.strftime(dateFormat) + ',' + time.strftime(timeFormat)

  chg_text = 'TX_ip : ' + tx_ip + ' : Freq ' + freq


  if  len(SET_CMD_out) == 0 :
    log_content = date_time + ', -FAILED- ' + chg_text + '\n'
    file_saver(logPath , "tx_chgLog.txt" ,  log_content)

    if line_api != 0:
        line_sender (line_api , log_content)
    else:
        print('Not send to Line')

    return 0
  else:
    log_content = date_time + ', ++OK!++ ' + chg_text + '\n'
    file_saver(logPath , "tx_chgLog.txt" ,  log_content)

    
    if line_api != 0:
        line_sender (line_api , log_content)
    else:
        print('Not send to Line')


    return 1

######################################################################
def rcu_control(ip_list , chrome_setup , logPath , line_api):
    #check everything is exist
    print(chrome_setup[0] , path.exists(chrome_setup[0]))
    print(chrome_setup[1] , path.exists(chrome_setup[1]))
    print(logPath     , path.exists(logPath))

    go_flag = path.exists(chrome_setup[0]) and path.exists(chrome_setup[1]) and path.exists(logPath)


    if go_flag == False:
        return 0
    

    rcu_ipaddr = str(ip_list[0])
    tx_ipaddr  = str(ip_list[1])
    #rx_ipaddr  = str(ip_list[2])


    #text combination and inside varriable------------------
    tx_uri = "tx@"+tx_ipaddr
    #rx_uri = "rx@"+rx_ipaddr
    rcu_config_url = "http://"+rcu_ipaddr+"/config_voip"
    rcu_status_url = "http://"+rcu_ipaddr+"/config"
    #-------------------------------------------------------

    dateFormat = "%Y.%m.%d"
    timeFormat = "%H:%M:%S"

    date_time = time.strftime(dateFormat) + ',' + time.strftime(timeFormat)


    dateFormat_png = "%Y%m%d"
    timeFormat_png = "%H%M%S"

    date_time_png = time.strftime(dateFormat_png) + '_' + time.strftime(timeFormat_png)

    #lOGGING Path--------------------------------------------


    #print('RCU %s , RX : %s , TX : %s' , rcu_ipaddr , rx_ipaddr , tx_ipaddr)
    #print(tx_uri , rx_uri , rcu_config_url , rcu_status_url )


    #lOGGING Path--------------------------------------------
    png_before_change = logPath + "\\" +"rcu"+rcu_ipaddr+"--01_befre"+date_time_png+".png"
    png_after_change  = logPath + "\\" +"rcu"+rcu_ipaddr+"--02_after"+date_time_png+".png"

    #-BROWSER CONFIG---------------------------------------------

    CHROME_PATH = chrome_setup[0]
    CHROMEDRIVER_PATH = chrome_setup[1]

    WINDOW_SIZE = "640,400"

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    rcu_browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=chrome_options)

    #- SETUP and SAVE --------------------------------------------
    rcu_browser.get(rcu_status_url)
    location_info = rcu_browser.find_element_by_name("locationInfo").get_attribute("value")
    print("LOCATION INFO : " , location_info)


    rcu_browser.get(rcu_config_url)
    rcu_browser.get_screenshot_as_file(png_before_change)

    #
    #rcu_browser.find_element_by_name("mainUriRx").get_attribute("value")
    #rcu_browser.find_element_by_name("mainUriRx").clear()
    #rcu_browser.find_element_by_name("mainUriRx").send_keys(rx_uri)


    #name=
    rcu_browser.find_element_by_name("mainUriTx").get_attribute("value")
    rcu_browser.find_element_by_name("mainUriTx").clear()
    rcu_browser.find_element_by_name("mainUriTx").send_keys(tx_uri)

    rcu_browser.find_element_by_name("send").click()


    time.sleep(5)
    rcu_browser.find_element_by_xpath("(//input[@name='send'])[2]").click()
    
    time.sleep(30)
    rcu_browser.get(rcu_config_url)
    rcu_browser.get_screenshot_as_file(png_after_change)
    rcu_browser.close()



    chg_text = location_info + " ip : " + rcu_ipaddr + " point to " + tx_uri #+ " | " + rx_uri
    log_content = date_time + ', --- ' + chg_text + '\n'
    file_saver(logPath , "rcu_chgLog.txt" ,  log_content)
    

    return 1