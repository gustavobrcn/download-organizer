from dotenv import load_dotenv
from logging import error
import os
from time import sleep
import datetime
import win32file
import win32event
import win32con

from win10toast_click import ToastNotifier

load_dotenv()


toast = ToastNotifier()
dir_path = os.path.dirname(os.path.realpath(__file__))
custom_user_path = os.environ['HOME_PATH']
user_path = os.environ['USERPROFILE'] if custom_user_path == '' else custom_user_path
downloads_path = user_path + '/Downloads'
path_to_watch = os.path.abspath(downloads_path)
year = datetime.datetime.now().strftime('%Y')

# FindFirstChangeNotification sets up a handle for watching
#  file changes. The first parameter is the path to be
#  watched; the second is a boolean indicating whether the
#  directories underneath the one specified are to be watched;
#  the third is a list of flags as to what kind of changes to
#  watch for. We're just looking at file additions / deletions.

change_handle = win32file.FindFirstChangeNotification(
  path_to_watch,
  0,
  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
)


def check_year_and_month_folder(des_folder):
    # Check the directory for current month and year folders. If they do not exist, create them
    curr_year, curr_month = datetime.datetime.now().strftime('%Y-%b').split('-')
    des_folder += '/' + curr_year
    
    if os.path.exists(des_folder):
        des_folder += '/' + curr_month
        if not os.path.exists(des_folder):
            os.mkdir(des_folder)
       
    else:
        os.mkdir(des_folder)
        des_folder += '/' + curr_month
        os.mkdir(des_folder)
        
    return des_folder

def check_for_dupes(des_folder, file):
    # Check for duplicate files in the destination folder and rename file if needed
    file_path = des_folder + '/' + file
    file_exists = os.path.isfile(file_path)
    file_name = file[:-4] 
    file_type = file[-4:]
    
    while file_exists:
        file_num = 1
        last_2 = file_name[-2:] 
        
        if last_2[0] == '_' and last_2[-1].isdigit():
            file_name = file_name[:-1] + str(int(last_2[-1]) + 1) 

        else:
            file_name = file_name + '_' + str(file_num) 
            file_num += 1
           
        file_path = des_folder + '/' + file_name + file_type
        file_exists = os.path.isfile(file_path)
        
    return file_path   

def toast_and_open_folder(des_folder, file_type):
    # Create windows toast for downloaded file
    open_folder = lambda: os.startfile(des_folder)
    file_types = {
        'Pictures': '/icons/pic.ico',
        'Videos': '/icons/vid.ico',
        'Documents': '/icons/doc.ico',
        'Music': '/icons/music.ico',
        'Downloads': '/icons/down.ico'
    }
    icon = dir_path + file_types[file_type]
    toast.show_toast('File Downloaded', f'Open the {file_type} Library to view the downloaded file.', duration=3, icon_path=icon,  threaded=False, callback_on_click=open_folder)
    
def move_file(file):
    # Move the downloaded file to its proper destination folder and trigger toast
    doc_types = ['txt', 'docx', 'pptx', 'xlsx', 'pdf']
    pic_types = ['png', 'jpg', 'jpeg', 'ico']
    vid_types = ['mov', 'mpg', 'mpeg', 'mp4', 'mpge4', 'avi']
    music_types = ['mp3', 'wav']
    des_folder = user_path
    file_to_move = path_to_watch + '/' + file
    file_type = file.split('.')[-1]

    if file_type in doc_types:
        des_folder += '/Documents'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = check_for_dupes(des_folder, file)
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Documents')
        
        
    elif file_type in pic_types:
        des_folder += '/Pictures'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = check_for_dupes(des_folder, file)
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Pictures')
        
    elif file_type in vid_types:
        des_folder += '/Videos'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = check_for_dupes(des_folder, file)
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Videos')
        
    elif file_type in music_types:
        des_folder += '/Music'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = check_for_dupes(des_folder, file)
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Music')
    
    else: 
        des_folder += '/Downloads'    
        des_folder = check_year_and_month_folder(des_folder)
        file_path = check_for_dupes(des_folder, file)
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Downloads')
    
def script_start_fail(start):
    # Create toast to notify that the script has started or failed
     if start:
         msg = 'Download organizer script has started'
         icon = dir_path + '/icons/start.ico'
     else:
         msg = 'Download organizer script has failed'
         icon = dir_path + '/icons/err.ico'
     toast.show_toast('Download Organizer', msg, duration=3, icon_path=icon, threaded=False)

# Loop forever, listing any file changes. The WaitFor... will
#  time out every half a second allowing for keyboard interrupts
#  to terminate the loop.

ignores = ['crdownload','.tmp']

try:
  script_start_fail(True)
  old_path_contents = dict([(f, None) for f in os.listdir(path_to_watch)])
  while True:
    result = win32event.WaitForSingleObject(change_handle, 500)
    
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    if result == win32con.WAIT_OBJECT_0:
        
      sleep(2) # to prevent "couldn't download" error in browser event though file was downloaded
      new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in new_path_contents if not f in old_path_contents and f != year]
      
      if added: 
        for file in added:
            should_continue = False
            for name in ignores:
                if name in file:
                    should_continue = True
            if should_continue:
                continue
            else:
              move_file(file)
          
      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification(change_handle)

except:
    script_start_fail(False)
    
finally:
  win32file.FindCloseChangeNotification(change_handle)