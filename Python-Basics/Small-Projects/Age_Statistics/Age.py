import pandas
import time
import os
import datetime

def exporting_Importing_values(user_number,user_name,user_age,birth_date):
    global main_df
    main_df = pandas.read_excel(r'Age_data.xlsx')
    
    date = datetime.datetime.now()
    date = f'{date.day}-{date.month}-{date.year}'
    main_df_t = main_df.T
    main_df_t[user_number] = [user_number,user_name,user_age,birth_date,date]
    main_df = main_df_t.T
    main_df = main_df.drop('Unnamed: 0',1)
        
    df_mean = main_df.mean(axis=0)
    main_df.to_excel("Age_data.xlsx",sheet_name='Age_Statistics ')
    return main_df

def Checking_integer(numberr):    
    try:
        numberr = int(numberr)
        return numberr
    except ValueError:
        print('Checking Age Value ...\n')
        time.sleep(10)
        print('Invalid-Input ... Closing Program')
        exit()

def thanking():
    print()
    print('Thank You !!')
    print('For Your Response.')
    exit()

# Collecting Data
user_name = input('Enter Your Name: ')
user_age = input('Enter Your Current Age: ')

user_age = Checking_integer(user_age)

user_number = input('Enter Your Favorite Number: ')
user_number = Checking_integer(user_number)

birth_date = input('Enter Your Birth Date: \n')

# Chacking path existance
if os.path.exists(r'Age_data.xlsx') == False:
    with open(r"Age_data.xlsx",'a+') as age:
        df1 = pandas.DataFrame([['Soham (Owner)','15','10/6/2005','10-6-2005']],index=[5],columns=['Name ','Age ','Date Of Birth ','Date Of Entry'])
        df1.to_excel("Age_data.xlsx",sheet_name='Age_Statistics ')
else:
    pass

main_df = exporting_Importing_values(user_number,user_name,user_age,birth_date)

# Fulfilling User Demands
user_input = input(r'Do You Want To Access Data? (y/n): ')
if user_input == 'y':
    print(main_df)
else:
    thanking()

mean = input('Do You Want To Access Data Mean? (y/n) : ')
if mean == 'y':
    mean_df = main_df.iloc[:,1:2]
    print(mean_df.mean())
else:
    thanking()

thanking()