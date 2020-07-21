import os
import glob
from csv import writer

folderPath = r"Data"
separator = " | "


def AddToCSV(TextList):
    with open("Output.csv", "a+", newline='') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerow(TextList)


def main():
    if not os.path.exists(folderPath):
        print("Error: folder not exists")
    else:
        os.chdir(folderPath)
        for file in glob.glob("*.txt"):
            print(file)
            with open(file, 'r') as f:
                lineList = f.readlines()
                for line in lineList:
                    TextList = line.split(separator)
                    print(TextList)
                    AddToCSV(TextList)


if __name__ == '__main__':
    main()
