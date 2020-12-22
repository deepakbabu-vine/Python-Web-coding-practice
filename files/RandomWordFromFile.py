# filename = input("Enter the file name:")
#hardcoded for now.
import random

from pip._vendor.pep517.compat import FileNotFoundError

filename = "/users/deepak.babu/documents/sample.txt"
try:
    file = open(filename, "r")
except (FileNotFoundError, IOError):
    print("File does not exists!")
    exit()

line_count = sum(1 for line in file if line.rstrip())
random_line = random.randint(0, line_count)
file.seek(0)

for i, line in enumerate(file):
    if i == random_line:
        print(line.rstrip())
        break
