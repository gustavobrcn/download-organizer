import datetime
import os


path = "C:/Users/gusta/Downloads"

def check_year_and_month_folder(des_folder):
    curr_year, curr_month = datetime.datetime.now().strftime('%Y-%b').split('-')
    dir = os.listdir(des_folder)
    des_folder += '/' + curr_year
    if curr_year not in dir:
        os.mkdir(des_folder)
        des_folder += '/' + curr_month
        os.mkdir(des_folder)
        return des_folder
    else:
        dir = os.listdir(des_folder)
        des_folder += '/' + curr_month
        if curr_month not in dir:
            os.mkdir(des_folder)
        return des_folder
        
check_year_and_month_folder(path)

# Keep changing value of des_folder
# curr_year, curr_month = datetime.datetime.now().strftime('%Y-%b').split('-')

# os.mkdir(path+'/'+ curr_year)