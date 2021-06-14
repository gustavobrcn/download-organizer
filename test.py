import datetime
import os
from time import process_time_ns
from win10toast_click import ToastNotifier

toast = ToastNotifier()

path = "C:/Users/gusta/Downloads"

def check_year_and_month_folder(des_folder):
    curr_year, curr_month = datetime.datetime.now().strftime('%Y-%b').split('-')
    # dir = os.listdir(des_folder)
    des_folder += '/' + curr_year
    if not os.path.exists(des_folder):
        os.mkdir(des_folder)
        des_folder += '/' + curr_month
        os.mkdir(des_folder)
       
    else:
        # dir = os.listdir(des_folder)
        des_folder += '/' + curr_month
        if not os.path.exists(des_folder):
            os.mkdir(des_folder)
    return des_folder
        
# check_year_and_month_folder(path)

def toast_and_open_folder(des_folder, file_type):
    callback = lambda: os.startfile(des_folder)
    file_types = {
        'Picture': 'icons/pic.ico',
        'Video': 'icons/vid.ico',
        'Document': 'icons/doc.ico',
        'Music': 'icons/music.ico'
    }
    toast.show_toast(f'{file_type} Type File Downloaded', f'Open the {file_type} Library to view the downloaded file.', duration=3, icon_path=file_types[file_type],  threaded=False, callback_on_click=callback)

# toast_and_open_folder(path, 'Picture')
# Keep changing value of des_folder
# curr_year, curr_month = datetime.datetime.now().strftime('%Y-%b').split('-')

# os.mkdir(path+'/'+ curr_year)

def check_for_dupes(des_folder, file):
    file_path = des_folder + '/' + file
    file_exists = os.path.isfile(file_path)
    print(file_path, file_exists)
    file_name = file[:-4] # filename is still the same
    file_type = file[-4:]
    while file_exists:
        print('beginning of loop')
        file_num = 1
        last_2 = file_name[-2:] # this needs a change
        print(file_name, file_type, last_2)
        # break
        if last_2[0] == '_' and last_2[-1].isdigit():
            print('if block')
            file_name = file_name[:-1] + str(int(last_2[-1]) + 1) 
            
            
        else:
            file_name = file_name + '_' + str(file_num) 
            file_num += 1
            print('in else block')
            print(file_name)
            # break
           
        new_file_path = des_folder + '/' + file_name + file_type
        print('new file path: ' + new_file_path)
        file_exists = os.path.isfile(new_file_path)
        print(file_exists, new_file_path)
        print('end of loop')
    return new_file_path
        
os.path.exists
check_for_dupes(path + '/New Folder', 'New Text Document.txt')
