import urllib
import requests
from csv import reader, writer

KEY = "AIza_YOUR_API_KEY"

Addresses = """
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

AddressList = Addresses.split('\n')
# remove empty strings using list comprehension
AddressList = Unique([i.strip() for i in AddressList if i.strip()])
print(len(AddressList))

for Address in AddressList:
    add = urllib.parse.quote_plus(Address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={add}&sensor=true&key={KEY}"
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
    # store data to csv file
    AddToCSV("Address_Output.csv", [City, zipCode, ADDRESS])
