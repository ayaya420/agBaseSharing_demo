import xlrd
from collections import OrderedDict
import json
import pathlib


def excel2json_nm(path,excelFileName):

    excel_full_path = path + "\\" + excelFileName + ".xlsx"
    json_full_path  = path + "\\" + excelFileName + ".json"


    wb = xlrd.open_workbook(excel_full_path)
    sh = wb.sheet_by_index(0)
    data_list = []

    #iterature inevery row
    for rownum in range(1, sh.nrows):
        data = OrderedDict()

        row_values = sh.row_values(rownum)
        #print(row_values)      #AL len = 5
        #print(len(row_values)) #TX len = 9

        for row_values_i in range(0, sh.ncols):
            
            col_name = str(sh.cell(0, row_values_i).value)
            xy_value = row_values[row_values_i]
            #print(col_name , xy_value)

            data[col_name] = xy_value
    
        data_list.append(data)
   
    with open(json_full_path, "w", encoding="utf-8") as writeJsonfile:
        json.dump(data_list, writeJsonfile, indent=4,default=str) 

#this_path = str(pathlib.Path(__file__).parent.absolute())+"\\DATABASE"
#name = "tx_database"
#excel2json_nm(this_path,name)
