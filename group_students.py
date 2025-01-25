class Student:
    def __init__(self, name, set, had_before):
        self.name = name
        self.set = set
        self.had_before = had_before

def main():
    with open('student_list.csv', mode = 'r') as file:
        for line in file.readlines():
            # line = line.rstrip(',  \n')
            line = line.split(', ')
            if line[-1][-1] == '\n':
                line[-1] = line[-1].rstrip(' \n')
            print(line)


main()