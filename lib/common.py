import csv

def read_processed_files_list(filepath):
    # Read the processed files list and return a set of tuples with file name and size.
    processed_files = set()
    
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            for row in reader:
                if len(row) >= 2:
                    processed_files.add((row[0], int(row[1])))
    except FileNotFoundError:
        # If the file does not exist, return an empty set
        return processed_files
    
    return processed_files