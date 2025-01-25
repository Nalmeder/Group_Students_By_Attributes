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

"""
import random

class Student:
    def __init__(self, name, set, had_before):
        self.name = name
        self.set = set  # e.g., 'creative', 'leader', 'organizer'
        self.had_before = had_before  # e.g., True or False

    def __str__(self):
        return f"{self.name} ({self.set}, {'Had before' if self.had_before else 'New'})"

def create_list_of_students():
    list_of_students = []
    with open('student_list.csv', mode='r') as file:
        for line in file.readlines():
            line = line.split(', ')
            if line[-1][-1] == '\n':
                line[-1] = line[-1].rstrip(' \n')
            list_of_students.append(
                Student(name=line[0], set=line[1], had_before=line[2] == '1')
            )
    return list_of_students

def create_groups(students):
    # Separate students by roles
    creatives = [s for s in students if s.set == 'creative']
    leaders = [s for s in students if s.set == 'leader']
    organizers = [s for s in students if s.set == 'organizer']

    # Shuffle the lists to randomize grouping
    random.shuffle(creatives)
    random.shuffle(leaders)
    random.shuffle(organizers)

    groups = []
    in_groups = set()

    # Form groups of 3 or 4 students
    while creatives or leaders or organizers:
        group = []

        # Add one creative to the group
        if creatives:
            group.append(creatives.pop())

        # Add one leader or organizer to the group
        if leaders:
            group.append(leaders.pop())
        elif organizers:
            group.append(organizers.pop())

        # Fill the group to 3 or 4 members
        while len(group) < 3 and (creatives or leaders or organizers):
            if creatives:
                group.append(creatives.pop())
            elif leaders:
                group.append(leaders.pop())
            elif organizers:
                group.append(organizers.pop())

        # Add students with 'had_before' as a constraint
        had_before_students = [s for s in group if s.had_before]
        if len(had_before_students) > 1:
            # Remove excess 'had_before' students if necessary
            for student in had_before_students[1:]:
                group.remove(student)
                if creatives:
                    group.append(creatives.pop())
                elif leaders:
                    group.append(leaders.pop())
                elif organizers:
                    group.append(organizers.pop())

        groups.append(group)

    return groups

def display_groups(groups):
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for student in group:
            print(f"  - {student}")
        print()

def main():
    students = create_list_of_students()

    groups = create_groups(students)

    display_groups(groups)

main()

"""