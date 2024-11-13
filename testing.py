import re

def remove_comments(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    
    # Remove single-line comments
    code = re.sub(r'#.*', '', code)
    
    # Remove multi-line comments (triple quotes)
    code = re.sub(r"'''(.*?)'''", '', code, flags=re.DOTALL)
    code = re.sub(r'"""(.*?)"""', '', code, flags=re.DOTALL)
    
    # Write the cleaned code back to the file
    with open(file_path, 'w') as file:
        file.write(code)
    
    # Print a message that comments have been removed
    print(f"All comments have been removed from {file_path}")

# Example usage:
file_path = 'timetable.py'
remove_comments(file_path)
