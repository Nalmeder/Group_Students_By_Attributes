import random

class Student:
    def __init__(self, name, role):
        self.name = name
        self.role = role

def create_list_of_students():
    list_of_students = []
    list_of_roles = []
    with open('student_list.csv', mode='r') as file:
        for line in file.readlines():
            line = line.split(', ')
            if line[-1][-1] == '\n':
                line[-1] = line[-1].rstrip('\n')
                line[-1] = line[-1].rstrip(' ')
            list_of_students.append(
                Student(name=line[0], role=line[1])
            )
            if line[1] not in list_of_roles:
                list_of_roles.append(line[1])

    return list_of_students, list_of_roles

def create_balanced_groups(students, list_of_roles):
    # Group students dynamically by roles from the list_of_roles
    # makes list for each set in list_of_roles
    role_dict = {role: [] for role in list_of_roles}
    for student in students:
        role_dict[student.role].append(student)

    # Shuffle the lists to randomize grouping
    for role in role_dict:
        random.shuffle(role_dict[role])

    groups = []

    # Form groups with one student from each role (balancing dynamically)
    while all(role_dict.values()):
        group = []
        for role in role_dict:
            if role_dict[role]:
                group.append(role_dict[role].pop())
        if len(group) > 1:  # Ensure the group has at least 1 student
            groups.append(group)

    # Handle leftover students
    leftovers = []
    for students_in_role in role_dict.values():
        leftovers.extend(students_in_role)

    return groups, leftovers

def count_roles(leftovers):
    # Count the number of students in each role
    role_counts = {}
    for student in leftovers:
        if student.role not in role_counts:
            role_counts[student.role] = 0
        role_counts[student.role] += 1

    return role_counts

def determine_max_role(role_counts):
    # Identify the role with the most students
    max_role = None
    max_count = -1
    for role, count in role_counts.items():
        if count > max_count:
            max_role = role
            max_count = count

    return max_role

def find_max_role_students(leftovers, max_role):
    # Find students of the max_role in the leftovers
    max_role_students = [s for s in leftovers if s.role == max_role]
    return max_role_students

def check_group_for_role(group, max_role):
    # Check if a group already has a student from the max_role
    return any(student.role == max_role for student in group)

def move_students_to_groups(groups, max_role_students, leftovers, max_role, num_roles):
    # Move students from leftovers to groups to balance the roles
    for student in max_role_students:
        # Try to find a group that doesn't have the max_role
        for group in groups:
            if len(group) < num_roles and not check_group_for_role(group, max_role):
                group.append(student)
                leftovers.remove(student)
                break

def adjust_groups_for_leftovers(groups, leftovers, num_roles):
    while len(leftovers) >= num_roles:
        # Form a new group with 'num_roles' students
        new_group = [leftovers.pop() for _ in range(num_roles)]
        groups.append(new_group)

    # If leftovers are still greater than 0, try replacing a less frequent role
    for group in groups:
        if len(group) == num_roles and leftovers:
            for i, student in enumerate(group):
                if leftovers:
                    # Replace any student with a leftover to maintain balance
                    replaced_student = group[i]
                    group[i] = leftovers.pop()
                    leftovers.append(replaced_student)
                    break  # Exit once replacement is done

    return groups, leftovers

def assign_leftovers_to_groups(groups, leftovers, num_roles):
    if leftovers:
        if len(groups) < len(leftovers):
            print("Not enough groups to assign leftover students")
            return
        
        for student in leftovers:
            rand_group = random.choice(groups)
            while len(rand_group) > num_roles:
               rand_group = random.choice(groups)
            rand_group.append(student)

        # Remove assigned leftovers from the list
        leftovers = [student for student in leftovers if student not in [group_student for group in groups for group_student in group]]

    return groups, leftovers

def display_groups(groups, leftovers):
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for student in group:
            print(f"  - {student.name} {student.role}")
        print()

    if leftovers:
        print("Leftover Students:")
        for student in leftovers:
            print(f"  - {student.name} {student.role}")
        print()

def adjust_groups_based_on_max_set(groups, leftovers, num_roles):
    # Count the roles
    role_counts = count_roles(leftovers)
    
    # Determine the role with the most students
    max_role = determine_max_role(role_counts)
    
    # Find students of the max_role
    max_role_students = find_max_role_students(leftovers, max_role)
    
    # Move students to groups
    move_students_to_groups(groups, max_role_students, leftovers, max_role, num_roles)
    
    return groups, leftovers


def main():
    students, list_of_roles = create_list_of_students()
    num_roles = len(list_of_roles)

    # Create groups and handle leftovers
    groups, leftovers = create_balanced_groups(students, list_of_roles)

    # Adjust groups based on the most abundant set in leftovers
    groups, leftovers = adjust_groups_based_on_max_set(groups, leftovers, num_roles)

    # Adjust groups for any remaining leftovers, ensuring balance
    groups, leftovers = adjust_groups_for_leftovers(groups, leftovers, num_roles)

    # Assign the leftovers to groups
    groups, leftovers = assign_leftovers_to_groups(groups, leftovers, num_roles)

    # Display the groups and leftover students
    display_groups(groups, leftovers)

main()
