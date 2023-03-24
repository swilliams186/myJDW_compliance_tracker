import re
import string
from pprint import pprint

from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import values
import openpyxl
import logging

#
s = requests.session()
# homepage = s.get(values.URL)
# soup = bs(homepage.text, "html.parser")
# csrf_name = soup.find(attrs={"name":values.KEY_CSRF_NAME}).get("value")
# csrf_token = soup.find(attrs={"name":values.KEY_CSRF_TOKEN}).get("value")
#
# #print(tag_inputs)
# logging.info(f"{values.KEY_CSRF_NAME}: {csrf_name}")
# logging.info(f"{values.KEY_CSRF_TOKEN}: {csrf_token}")
#
#
# login_payload = {
#     values.KEY_LOGIN: values.LOGIN,
#     values.KEY_PASSWORD: values.PASSWORD,
#     values.KEY_CSRF_NAME: csrf_name,
#     values.KEY_CSRF_TOKEN: csrf_token
# }
#
# login_result = s.post(values.LOGIN_REQ_URL, headers=values.HEADERS, data=login_payload)
# #TODO ensure result is correct and login was succesfull.

with open("example-rota.html") as doc:
    # rota_html = s.get("./example-rota.html")
    soup = bs(doc, "html.parser")
    rotas = soup.findAll(attrs={"class": "employee-name"},
                         string=values.KITCHEN_NAMES)  # You can pass a list in? AWESOME!

    # TODO For each kitchen staff, jump to parent element then extract all class='day text-center"
    extracted_rotas = {}
    for manager in rotas:
        shifts = []
        managerName = manager.text
        week = manager.find_parent().findAll(attrs={"class": "day"})
        for day in week:
            strippedText = day.get_text("<br>").strip()  # Strips leading escape chars . Value will be
            # similar to '06:00am - 03:00pm                Kitchen)'

            # TODO figure out how to cope with split shifts . if len(splitText) > 4 indicates muktiple
            #This just strips out any split shifts for now
            #Could use [::2] to just extract times as that's how it's formatted
            #len% 4 could show how many shifts, and each 4th entry is the shift type

            splitText = strippedText.split()[:4]  # Now looks something like
                                            # ['12:00pm', '-', '10:00pm', '<br>(Kitchen)<br>']

            if(len(strippedText) != 0):

                # convert times to 24 hour clock
                # %H is the 24 hour clock, %I is the 12 hour clock and when using the 12 hour clock,
                # %p qualifies if it is AM or PM. strp = parse, strf = format
                startTime = datetime.strptime(splitText[0], "%I:%M%p")  #This will have year and date attached
                startTime = datetime.strftime(startTime,"%H:%M")    #Strips that out, is now 24 hour 14:45
                endTime = datetime.strptime(splitText[2], "%I:%M%p")
                endTime = datetime.strftime(endTime, "%H:%M")

                # TODO ignore meetings


                shifts.append({"start": startTime,
                               "end":   endTime})
                #Example data structure
                # 'ROBBINS, WILL': [None,
                #                   {'end': '20:30', 'start': '11:00'},
                #                   {'end': '23:45', 'start': '17:30'},

            else: #If no shift that day
                shifts.append({"start": "day",
                             "end":    "off"})


            extracted_rotas[managerName] = shifts


    wb = openpyxl.load_workbook(filename="compliance-tracker-template.xlsx")
    ws = wb["Kitchen LC Compliance"]      #wb workbook ws worksheet

    for row_index, manager in enumerate(extracted_rotas, values.NAME_COLUMN_START):
        ws[f"A{row_index}"] = manager

        #B - H for example
        day_colums = string.ascii_uppercase[values.MAPPINGS['MONDAY']:8:]  #6 kitchen staff
        print(day_colums)
        #TODO allow for dynamic amount of staff above

        for y, day in enumerate(day_colums):
            ws[f"{day}{row_index}"] = (f"{extracted_rotas[manager][y]['start']}"
                               f"-"
                               f"{extracted_rotas[manager][y]['end']}"
                                       )
                              #COULD USE INDEX OF day in colums




        # print(extracted_rotas[manager][0]["start"])

        # ws[f"{values.MAPPINGS['MONDAY']}{x}"] = f"{extracted_rotas[manager][0]['start']}-{extracted_rotas[manager][0]['end']}"



    wb.save(filename=("compliance-tracker-template.xlsx"))



