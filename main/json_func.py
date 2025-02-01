import json

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