import random

class Student:
    def __init__(self, name, set, had_before):
        self.name = name
        self.set = set
        self.had_before = had_before


def create_list_of_students():
    list_of_students = []
    with open('student_list.csv', mode = 'r') as file:
        for line in file.readlines():
            line = line.split(', ')
            if line[-1][-1] == '\n':
                line[-1] = line[-1].rstrip(' \n')
            print(line)
            list_of_students.append(Student(name = line[0], set = line[1], had_before = [2]))
            
    return list_of_students


def create_balanced_groups(students):
    # Separate students by roles
    creatives = [s for s in students if s.set == 'creative']
    leaders = [s for s in students if s.set == 'leader']
    organizers = [s for s in students if s.set == 'organizer']

    # Shuffle the lists to randomize grouping
    random.shuffle(creatives)
    random.shuffle(leaders)
    random.shuffle(organizers)

    groups = []

    # Form groups with one of each role
    while creatives and leaders and organizers:
        group = [
            creatives.pop(),
            leaders.pop(),
            organizers.pop()
        ]
        groups.append(group)

    # Handle leftover students
    leftovers = creatives + leaders + organizers
    return groups, leftovers


def display_groups(groups, leftovers):
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for student in group:
            print(f"  - {student.name} {student.set}")
        print()
    
    if leftovers:
        print("Leftover Students:")
        for student in leftovers:
            print(f"  - {student.name} {student.set}")
        print()


def main():
    students = create_list_of_students()

    # Create groups and handle leftovers
    groups, leftovers = create_balanced_groups(students)

    # Display the groups and leftover students
    display_groups(groups, leftovers)

main()
