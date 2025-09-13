import time
import os 

while True:
    if os.path.exists(r'data.txt') == True: 
        with open('data.txt','r') as data:   
            print(data.read())
    else:
        print('File Doesnot Exist')
    time.sleep(10)

