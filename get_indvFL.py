from pyflightdata import FlightData
from misc_definitions import   file_saver, json_fileSaver
import pathlib

this_path = pathlib.Path(__file__).parent.absolute()
this_path = str(this_path)


icao_airport = 'BKK'


f=FlightData()
#optional login
f.login('intouch2544@gmail.com','Easy0802463000')
f.get_airport_arrivals(icao_airport)

bkk_arr = f.get_airport_arrivals(icao_airport,page=1,limit=100)

print(type(bkk_arr))




for i in range(len(bkk_arr)):
    fl_allData  = bkk_arr[i]
    fl_id       = bkk_arr[i]['flight']['identification']['number']['default']
    fl_callsign = bkk_arr[i]['flight']['identification']['callsign']

    fl_sts_type = bkk_arr[i]['flight']['status']['text']
    fl_sts_2 = bkk_arr[i]['flight']['status']['generic']['status']['text']
                #landed , schduled , delayed , estimated

    print(fl_id , fl_callsign , fl_sts_type , fl_sts_2)