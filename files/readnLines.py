import re


class ReadNLines:
    def __init__(self):
        self.number_of_lines = 0

    def read_n_lines(self, number_of_lines):

        with open("/users/deepak.babu/documents/sample.txt", "r") as target_file:
            line = re.split(r'[?!.]*', target_file.read())
        if number_of_lines == 0 or number_of_lines > len(line):
            print "Invalid line number!!! Range : 1 -", len(line)
            return
        for index in range(number_of_lines):
            print(line[index])

if __name__ == '__main__':
    print_lines = ReadNLines()
    required_lines = 0
    while True:
        try:
         required_lines = int(raw_input("Enter first N lines to be printed:"))
        except:
            print("Error Occurred!!! Please try again!")
            continue
        print_lines.read_n_lines(required_lines)
