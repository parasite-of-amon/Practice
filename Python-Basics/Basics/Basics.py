student_grades = {'Soham': 9.1, 'Deepak': 8.8, 'Satpute': 7.5}

def mean(value):
    if isinstance(value,dict):
        mean = sum(value.values()) / len(value)
    else:
        mean = sum(value)/len(value)
    return mean

print(mean(student_grades))
