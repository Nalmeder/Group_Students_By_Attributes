import random

class Student:
    def __init__(self, name, set, had_before):
        self.name = name
        self.set = set  # 'creative', 'leader', 'organizer'
        self.had_before = had_before  # True or False

    def __str__(self):
        return f"{self.name} ({self.set}, {'Had before' if self.had_before else 'New'})"

def create_list_of_students():
    list_of_students = []
    with open('student_list.csv', mode = 'r') as file:
        for line in file.readlines():
            line = line.split(', ')
            if line[-1][-1] == '\n':
                line[-1] = line[-1].rstrip(' \n')
            list_of_students.append(
                Student(name=line[0], set=line[1], had_before=line[2] == '1')
            )
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

def adjust_groups_for_leftovers(groups, leftovers):
    while len(leftovers) >= 3:
        # Form a new group with 3 students
        new_group = [leftovers.pop(), leftovers.pop(), leftovers.pop()]
        groups.append(new_group)

    # If leftovers are still greater than 0, try replacing a leader/organizer with a creative
    for group in groups:
        if len(group) == 3 and leftovers:
            for i, student in enumerate(group):
                if student.set in ['leader', 'organizer'] and leftovers:
                    # Swap leader/organizer with a creative
                    replaced_student = group[i]
                    group[i] = leftovers.pop()
                    leftovers.append(replaced_student)
                    break  # Exit once replacement is done

    return groups, leftovers


def assign_leftovers_to_groups(groups, leftovers):
    if leftovers:
        if len(groups) < len(leftovers):
            print("not enough groups to assign leftover students")
            return
        
        filter_list = []

        for student in leftovers:
            rand_group = random.choice(groups)
            while len(rand_group) > 3: 
               rand_group = random.choice(groups)
            rand_group.append(student)
            filter_list.append(student)

        # I could use python's built in filter function, 
        # but I find list comprehensions to be unreadable,
        # thus difficult to debug or explain
        leftovers = filter_leftovers(leftovers, filter_list) 

    return groups, leftovers

def filter_leftovers(leftovers, filter_list):
    # Iterate over copy to avoid weirdness when removing
    for student in leftovers.copy():
        print(student.name)
        if student in filter_list:
            leftovers.remove(student)

    return leftovers

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

    # Adjust groups for leftovers, making sure groups are balanced with 3 students
    groups, leftovers = adjust_groups_for_leftovers(groups, leftovers)

    # Assign the leftovers to groups
    groups, leftovers = assign_leftovers_to_groups(groups, leftovers)

    # Display the groups and leftover students
    display_groups(groups, leftovers)

main()
