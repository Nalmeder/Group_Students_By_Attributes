import random

class Student:
    def __init__(self, name, set):
        self.name = name
        self.set = set  # 'creative', 'leader', 'organizer'


def create_list_of_students():
    list_of_students = []
    with open('student_list.csv', mode = 'r') as file:
        for line in file.readlines():
            line = line.split(', ')
            if line[-1][-1] == '\n':
                line[-1] = line[-1].rstrip(' \n')
            list_of_students.append(
                Student(name=line[0], set=line[1])
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

def count_roles(leftovers):
    # Count the number of students in each role
    creative_count = 0
    leader_count = 0
    organizer_count = 0

    for student in leftovers:
        if student.set == 'creative':
            creative_count += 1
        elif student.set == 'leader':
            leader_count += 1
        elif student.set == 'organizer':
            organizer_count += 1

    return creative_count, leader_count, organizer_count

def determine_max_role(creative_count, leader_count, organizer_count):
    # Identify the set with the most students
    role_counts = {
        'creative': creative_count,
        'leader': leader_count,
        'organizer': organizer_count
    }
    
    # Find the role with the highest count
    max_role = None
    max_count = -1
    for role, count in role_counts.items():
        if count > max_count:
            max_role = role
            max_count = count
    
    return max_role

def find_max_role_students(leftovers, max_role):
    # Find students of the max_role in the leftovers
    max_role_students = []
    for student in leftovers:
        if student.set == max_role:
            max_role_students.append(student)
    
    return max_role_students

def check_group_for_role(group, max_role):
    # Check if a group already has a student from the max_role
    role_found = False
    for student in group:
        if student.set == max_role:
            role_found = True
            break
    return role_found

def move_students_to_groups(groups, max_role_students, leftovers, max_role):
    # Move students from leftovers to groups to balance the roles
    for student in max_role_students:
        # Try to find a group that doesn't have the max_role
        for group in groups:
            if len(group) < 4:
                role_found = check_group_for_role(group, max_role)
                if not role_found:
                    group.append(student)
                    leftovers.remove(student)
                    break


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
                    # Swap less abundant roll with most abundant
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


def adjust_groups_based_on_max_set(groups, leftovers):
    # Count the roles
    creative_count, leader_count, organizer_count = count_roles(leftovers)
    
    # Determine the role with the most students
    max_role = determine_max_role(creative_count, leader_count, organizer_count)
    
    # Find students of the max_role
    max_role_students = find_max_role_students(leftovers, max_role)
    
    # Move students to groups
    move_students_to_groups(groups, max_role_students, leftovers, max_role)
    
    return groups, leftovers


def main():
    students = create_list_of_students()

    # Create groups and handle leftovers
    groups, leftovers = create_balanced_groups(students)

    # Adjust groups based on the most abundant set in leftovers
    groups, leftovers = adjust_groups_based_on_max_set(groups, leftovers)

    # Adjust groups for any remaining leftovers, ensuring balance
    groups, leftovers = adjust_groups_for_leftovers(groups, leftovers)

    # Assign the leftovers to groups
    groups, leftovers = assign_leftovers_to_groups(groups, leftovers)

    # Display the groups and leftover students
    display_groups(groups, leftovers)

main()
