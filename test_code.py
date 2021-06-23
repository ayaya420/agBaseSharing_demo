import random
from time import sleep
import time
import pathlib
from misc_definitions import file_saver , line_sender
import timeit
from os import path
import subprocess
from tx_marker import *
import random
from time import sleep
import time
import pathlib
from misc_definitions import *
import timeit
from tx_marker import *
from os import path



#snmpget -v 1 -c public 172.86.110.101:161 1.3.6.1.4.1.2566.127.2.2.1.1.6.5.0 
#snmpset -v 1 -c publuc 182.86.110.101:161 1.3.6.1.4.1.2566.127.2.2.1.1.6.5.0 u 112000000


#COMMON SETUP
Line_api = "Or5ik6zL73GAFSuLbhVdJGR5uwFelbMfU89iWIDafBB"

app_path = pathlib.Path(__file__).parent.absolute()
app_path = str(app_path)
logPath = app_path + "\\" + "_LOG"

#RCU ONLY
CHROME_PATH = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = r'C:\\chromedriver.exe'
CHROME_Setup = [CHROME_PATH , CHROMEDRIVER_PATH]




#SIMULATE
#RCU 1 > 131.6
#RCU 2 > 131.7

rcu1 = '172.86.110.111' 
rcu2 = '172.86.110.112'
freq_list = [131.6 , 131.7]
rand_freq = random.choice(freq_list)

tx = '172.86.110.101'

blank_tx = '0.0.0.0'

#SET TX
#tx_returnCMD = tx_setFreq(tx , rand_freq , logPath , Line_api)
#print(tx_returnCMD)

#SET RCU
#change_list = [rcu1 , tx]
#rcu1_returnCMD = rcu_control(change_list ,CHROME_Setup, logPath , Line_api)
#print(rcu1_returnCMD)


#RELEASE OLD RCU
change_list = [rcu1 , blank_tx]
rcu2_returnCMD = rcu_control(change_list ,CHROME_Setup, logPath , Line_api)
print(rcu2_returnCMD)




