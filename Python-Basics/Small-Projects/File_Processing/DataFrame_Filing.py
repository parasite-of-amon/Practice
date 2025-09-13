import pandas
import time

name_list = ['Soham (Owner)']
mathematics_list = [100]
science_list = [100]
IT_list = [100]

df1 = pandas.DataFrame({'Mathematics':mathematics_list, 'Science':science_list, 'IT':IT_list},index=name_list)


def basic_dataAnalysis():
    user_input = int(input(f'Data Entry(No. Of Students): '))
    if  user_input <= 0:
        return None
    elif isinstance(user_input,int) and user_input > 0:
        for real in range(user_input):
            Main = input(f'Enter Name Student {real + 1}: ')
            name_list.append(Main)
            Main = int(input(f'Enter Mathematics Marks {real + 1}: '))
            mathematics_list.append(Main)
            Main = int(input(f'Enter Science Marks {real + 1}: '))
            science_list.append(Main)
            Main = int(input(f'Enter IT Marks {real + 1}: '))
            IT_list.append(Main)
        df1 = pandas.DataFrame({'Mathematics':mathematics_list, 'Science':science_list, 'IT':IT_list},index=name_list)
        return df1
    else:
        return df1

print(basic_dataAnalysis())

            