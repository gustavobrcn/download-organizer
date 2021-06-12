import os
from time import sleep
import datetime
import win32file
import win32event
import win32con

from win10toast_click import ToastNotifier


path_to_watch = os.path.abspath ("C:/Users/gusta/Downloads")

#
# FindFirstChangeNotification sets up a handle for watching
#  file changes. The first parameter is the path to be
#  watched; the second is a boolean indicating whether the
#  directories underneath the one specified are to be watched;
#  the third is a list of flags as to what kind of changes to
#  watch for. We're just looking at file additions / deletions.
#
change_handle = win32file.FindFirstChangeNotification(
  path_to_watch,
  0,
  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
)

# file types to look for

def move_file_and_toast(file):
    # Move the downloaded file to its proper destination folder and trigger toast
    doc_types = ['zip', 'txt', 'docx', 'pptx', 'xlsx', 'pdf']
    pic_types = ['png', 'jpg', 'jpeg', 'ico']
    vid_types = ['mov', 'mpg', 'mpeg', 'mp4', 'mpge4', 'avi']
    music_types = ['mp3', 'wav']
    root = 'C:/Users/gusta/'
    file_type = file.split('.')[-1]
    print(file_type)

    if file_type in doc_types:
        des_folder = root + 'Documents'
        os.rename(f'{path_to_watch}/{file}', f'{des_folder}/{file}')
        
    elif file_type in pic_types:
        des_folder = root + 'Pictures'
        os.rename(f'{path_to_watch}/{file}', f'{des_folder}/{file}')
        
    elif file_type in vid_types:
        des_folder = root + 'Videos'
        os.rename(f'{path_to_watch}/{file}', f'{des_folder}/{file}')
        
    elif file_type in music_types:
        des_folder = root + 'Music'
        os.rename(f'{path_to_watch}/{file}', f'{des_folder}/{file}')
    
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
    
    

# Loop forever, listing any file changes. The WaitFor... will
#  time out every half a second allowing for keyboard interrupts
#  to terminate the loop.
#

try:

  old_path_contents = dict([(f, None) for f in os.listdir(path_to_watch)])
  while 1:
    result = win32event.WaitForSingleObject(change_handle, 500)
    
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    if result == win32con.WAIT_OBJECT_0:
        
      sleep(1) # to prevent "couldn't download" error in browser event though file was downloaded
      new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in new_path_contents if not f in old_path_contents]
      
      if added: 
          for f in added:
            print(f)
            move_file_and_toast(f)
          

      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification(change_handle)

finally:
  win32file.FindCloseChangeNotification(change_handle)
