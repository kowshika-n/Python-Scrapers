# Useful to combine multiple text files extracted using userscripts
import os
import glob
from csv import writer

folderPath = r"C:\Users"
separator = " | "


def AddToCSV(file_name, TextList):
    with open(file_name, "a+", newline='', encoding='utf-8') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerow(TextList)


def combine(folderPath, text_filename_format, separator, output_filename):
    if not os.path.exists(folderPath):
        print(f"Error: {folderPath} not exists")
    else:
        os.chdir(folderPath)
        match_format = "*" + text_filename_format + "*.txt"
        fileList = glob.glob(match_format)
        if not fileList:
            print(f'No files found matching {match_format}')
        else:
            fileList.sort(key=os.path.getmtime)
            for file in fileList:
                print(file)
                with open(file, 'r', encoding='utf-8') as f:
                    lineList = f.readlines()
                    TextList = []
                    for line in lineList:
                        TextList = line.split(separator)
                        Data_list = [elem.strip() if elem is not None else "" for elem in TextList]
                        print(Data_list)
                        AddToCSV(output_filename, Data_list)



if __name__ == '__main__':
    combine(folderPath, "Listing", separator, "Output.csv")
