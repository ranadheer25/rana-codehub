import requests
import json

from python_api_extract import run_push_down_insert_query

var_url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json"

var_resp = requests.get(var_url)

#print (var_resp)

#print (type(var_resp.text))

var_json = var_resp.json()

#print (type(var_json))
var_other_vals = ""
cnt_un = ""
ind_un = ""
oth_un = ""
for item in var_json[1]:
   # print(item)
    for dict in item:
        if dict == 'indicator':
            #print("Insert this into indicator table")
            #print(item[dict])
            #ind_ins_qry = f"""Insert into indicator values ('{item[dict]["id"]}','{item[dict]["value"]}')"""
            ind_un += f"""SELECT '{item[dict]["id"]}','{item[dict]["value"]}' UNION\n"""
            
        elif dict == 'country':
            #print("Insert this into country table")
            #print(item[dict])
            #cnt_ins_qry = f"""Insert into country values ('{item[dict]["id"]}','{item[dict]["value"]}')"""
            cnt_un += f"""SELECT '{item[dict]["id"]}','{item[dict]["value"]}' UNION\n"""
            #print(cnt_ins_qry)
        else:
            #print(item[dict])
            var_other_vals += f"'{item[dict]}',"
    var_all_val = f"""'{item["indicator"]["id"]}','{item["country"]["id"]}',{var_other_vals[:-1]}"""
    oth_un += f"SELECT {var_all_val} UNION\n"
    var_other_vals = ""
    #oth_ins_qry = f'insert into other_table values ({var_other_vals[:-1]})'
#print(ind_un[:-12])
ind_ins_qry = f"INSERT INTO INDICATOR {ind_un[:-7]}"
cnt_ins_qry = f"INSERT INTO COUNTRY {cnt_un[:-7]}"
oth_ins_qry = f"INSERT INTO OTHERS {oth_un[:-7]}"
#print(cnt_un[:-12])
#print(cnt_un[:-11])
#print(oth_ins_qry)
run_push_down_insert_query(oth_ins_qry)


