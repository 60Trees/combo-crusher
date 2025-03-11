import json
import csv

def csv_to_array(file_path):
    array_of_arrays = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            array_of_arrays.append(row)
    return array_of_arrays

def dump(f, path):
    try:
        with open(path, 'w') as file:
            json.dump(f, file, indent=4)
    except IOError as e:
        print(f"Error occured while dumping: {e}")
        
def load(path):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except IOError as e:
        print(f"Error occured while loading: {e}")