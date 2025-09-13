import os
import pandas

def mean(value):
    if isinstance(value,dict):
        mean = sum(value.values()) / len(value)
    else:
        mean = sum(value)/len(value)
    return mean

def reading_files_txt(data_location):
    if os.path.exists(data_location):
        with open(data_location,'r') as read_only:
            data = read_only.read()
            return data
    else:
        return 'Error 404: File Not Found'

def reading_csv_files(datalocation2):
    if os.path.exists(datalocation2):
        data = pandas.read_csv(datalocation2)
        process = input('Enter "Y for obtaining Mean" OR "N for printing the data"')
        if process == 'Y':
            return mean(data)
        elif process == 'N':
            return data
        else:
            return None
            



