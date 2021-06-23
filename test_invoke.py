from misc_definitions import  *
import random
import pathlib
from datetime import datetime,timedelta
import json
import excel2json  #pip install excel2json
import xlsxwriter
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer
from al_to_Freq import *
from tx_marker import *



LUGER_AGBS = "Or5ik6zL73GAFSuLbhVdJGR5uwFelbMfU89iWIDafBB"


#RCU ONLY
CHROME_PATH = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
#CHROME_PATH = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = r'C:\\chromedriver.exe'
CHROME_Setup = [CHROME_PATH , CHROMEDRIVER_PATH]

app_path = pathlib.Path(__file__).parent.absolute()
app_path = str(app_path)
logPath = app_path + "\\" + "_LOG"

cmd_msg , cmd_returncode = tx_setReserve('THD' , CHROME_Setup , logPath , LUGER_AGBS)

