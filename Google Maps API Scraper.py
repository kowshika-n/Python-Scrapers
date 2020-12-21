import urllib
import requests
from csv import reader, writer

KEY = "AIza_YOUR_API_KEY"

Add = """
650 WARRENVILLE ROAD STE 500 IL
2150 E LAKECOOK RD SUITE 320 IL
"""

def Unique(List):
    if List is not None and len(List) > 0:
        return list(dict.fromkeys(List))
    else:
        return List

def AddToCSV(file_name, TextList):
    """Appends a new row with input text list"""
    with open(file_name, "a+", newline='', encoding='utf-8') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerow(TextList)

ADDRESSList = Add.split('\n')
# remove empty strings using list comprehension
ADDRESSList = Unique([i.strip() for i in ADDRESSList if i.strip()])
print(len(ADDRESSList))

for ADDRESS in ADDRESSList:
    ADD = urllib.parse.quote_plus(ADDRESS)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={ADD}&sensor=true&key={KEY}"
    resp = requests.get(url)
    data = resp.json()
    zipCode = "-"
    City = "-"
    try:
        datatype = data['results'][0]['address_components'][-1]['types'][0]
        if datatype == 'postal_code':
            zipCode = data['results'][0]['address_components'][-1]['long_name']
            City = data['results'][0]['address_components'][-4]['long_name']
    except:
        pass
    AddToCSV("Address_Output.csv", [City, zipCode, ADDRESS])
