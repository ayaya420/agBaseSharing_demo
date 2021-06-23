from pyflightdata import FlightData
from misc_definitions import   file_saver, json_fileSaver , line_sender
import pathlib

save_path = str(pathlib.Path(__file__).parent.absolute())+"\\DATABASE"


icao_airport = 'BKK'


f=FlightData()
#optional login
f.login('intouch2544@gmail.com','Easy0802463000')
f.get_airport_arrivals(icao_airport)

bkk_arr = f.get_airport_arrivals(icao_airport,page=1,limit=100)

print(type(bkk_arr))


#bkk_dep = f.get_airport_departures(icao_airport,page=1,limit=100)

#print(type(bkk_dep))


#bkk_og = f.get_airport_onground(icao_airport, page=1, limit=100)

#def file_saver(sav_path , file_name ,  content_Text):
#file_saver(save_path , "bkk_arr.json" ,  bkk_arr)

json_fileSaver(save_path , icao_airport+"_arr.json" ,  bkk_arr)
#json_fileSaver(save_path , icao_airport+"_dep.json" ,  bkk_dep)
#json_fileSaver(save_path , icao_airport+"_og.json" ,  bkk_og)


#NAKHON-K
LUGER_AGBS = "Or5ik6zL73GAFSuLbhVdJGR5uwFelbMfU89iWIDafBB"



from datetime import datetime,timedelta

lineMsg = "Flight schdule was created ! for : " + icao_airport + " at " + datetime.now().strftime("%H : %M") + " TST"

line_sender(LUGER_AGBS , lineMsg)