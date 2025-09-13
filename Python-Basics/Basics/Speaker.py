start = ""
user_input_list = []
def checking_question(user_input):
    question_list = ['how','How','when','When','why','Why','What','what','Where','where']
    for word in question_list:
        if word in user_input:
            return True
    return False

while True:
    user_input = input('Say Something: ')
    if user_input == '\end':
        break
    else:
        if checking_question(user_input) == True:
            user_input = f'{user_input}?'
        else:
            user_input = f'{user_input}.'
        user_input_list.append(user_input.title())
        continue


for main_input in user_input_list:
    start = start + ' ' + main_input

print(start)


            