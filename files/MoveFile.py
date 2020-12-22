import os

try:
    os.rename("/users/deepak.babu/documents/test/sample.txt", "/users/deepak.babu/documents/test/files/sample.txt")
    print("File moved successfully!")
except OSError:
    print("File Not found / Already moved to another location!")