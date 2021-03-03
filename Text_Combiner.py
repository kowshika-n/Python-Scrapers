# Useful to combine multiple text files extracted using userscripts
import os
import ast
import glob
from csv import writer

folderPath = os.path.expanduser("~") + "\\Downloads\\"
textFileNameFormat = "link"
separator = " | "
outputFile = "Output_links.csv"


def findFiles(name_match, file_format):
    match_format = "*" + name_match + "*" + file_format
    fileList = glob.glob(match_format)
    if not fileList:
        print(f'No files found matching {match_format}')
    else:
        # sort the files by modified time
        fileList.sort(key=os.path.getmtime)
        print(f'Found {len(fileList)} files matching {match_format}')
    return fileList


def AddToCSV(file_name, TextList):
    with open(file_name, "a+", newline='', encoding='utf-8') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerow(TextList)


def combineText(folderPath, text_filename_format, separator, output_filename, delete=False):
    if not os.path.exists(folderPath):
        print(f"Error: {folderPath} not exists")
    else:
        os.chdir(folderPath)
        fileList = findFiles(text_filename_format, ".txt")
        for file in fileList:
            print(file)
            with open(file, 'r', encoding='utf-8') as f:
                lineList = f.readlines()
                TextList = []
                for line in lineList:
                    TextList = line.split(separator)
                    Data_list = [elem.strip() if elem is not None else "" for elem in TextList]
                    #print(Data_list)
                    if Data_list:
                        AddToCSV(output_filename, Data_list)
            if delete:
                os.remove(file)


def extractLinks(folderPath, text_filename_format, separator, output_filename, delete=False):
    if not os.path.exists(folderPath):
        print(f"Error: {folderPath} not exists")
    else:
        os.chdir(folderPath)
        fileList = findFiles(text_filename_format, ".txt")
        linkList = set()
        for file in fileList:
            print(file)
            with open(file, 'r', encoding='utf-8') as f:
                lineList = f.readlines()
                TextList = []
                for line in lineList:
                    TextList = line.split(separator)
                    Data_list = [elem.strip() if elem is not None else "" for elem in TextList]
                    # print(Data_list)
                    if Data_list:
                        for item in Data_list:
                            if 'http' in item:
                                linkList.add(item)
            if delete:
                os.remove(file)
                            
        for link in linkList:
            AddToCSV(output_filename, [link])


def jsonTxt2csv(folderPath, text_filename_format, output_filename, delete=False):
    if not os.path.exists(folderPath):
        print(f"Error: {folderPath} not exists")
    else:
        os.chdir(folderPath)
        fileList = findFiles(text_filename_format, ".txt")
        for file in fileList:
            print(file)
            jsonDict = dict()
            with open(file, 'r', encoding='utf-8') as f:
                try:
                    lineList = f.readlines()
                    #print(lineList)
                    for line in lineList:
                        json = ast.literal_eval(line)
                        for key, value in json.items():
                            AddToCSV(output_filename, [key, value])
                except:
                    pass
            if delete:
                os.remove(file)
            

if __name__ == '__main__':
    combineText(folderPath, "Shop", separator, "Output_Shop.csv", True)
    jsonTxt2csv(folderPath, "link", "Output_links.csv", True)
