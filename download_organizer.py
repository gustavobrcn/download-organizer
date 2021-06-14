import os
from time import sleep
import datetime
import win32file
import win32event
import win32con

from win10toast_click import ToastNotifier


toast = ToastNotifier()
path_to_watch = os.path.abspath("C:/Users/gusta/Downloads")


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
    if not os.path.exists(des_folder):
        os.mkdir(des_folder)
        des_folder += '/' + curr_month
        os.mkdir(des_folder)
       
    else:
        des_folder += '/' + curr_month
        if not os.path.exists(des_folder):
            os.mkdir(des_folder)
    
    return des_folder
        

def toast_and_open_folder(des_folder, file_type):
    # Create windows toast for downloaded file
    open_folder = lambda: os.startfile(des_folder)
    file_types = {
        'Picture': 'icons/pic.ico',
        'Video': 'icons/vid.ico',
        'Document': 'icons/doc.ico',
        'Music': 'icons/music.ico',
        'Download': 'icons/down.ico'
    }
    toast.show_toast(f'{file_type[:-1]} Type File Downloaded', f'Open the {file_type} Library to view the downloaded file.', duration=3, icon_path=file_types[file_type],  threaded=False, callback_on_click=open_folder)
    
def move_file(file):
    # Move the downloaded file to its proper destination folder and trigger toast
    doc_types = ['zip', 'txt', 'docx', 'pptx', 'xlsx', 'pdf']
    pic_types = ['png', 'jpg', 'jpeg', 'ico']
    vid_types = ['mov', 'mpg', 'mpeg', 'mp4', 'mpge4', 'avi']
    music_types = ['mp3', 'wav']
    des_folder = 'C:/Users/gusta/'
    file_to_move = path_to_watch + '/' + file
    file_type = file.split('.')[-1]
    print(file_type)

    if file_type in doc_types:
        des_folder += 'Documents'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = des_folder + '/' + file
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Document')
        
        
    elif file_type in pic_types:
        des_folder += 'Pictures'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = des_folder + '/' + file
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Picture')
        
    elif file_type in vid_types:
        des_folder += 'Videos'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = des_folder + '/' + file
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Video')
        
    elif file_type in music_types:
        des_folder += 'Music'
        des_folder = check_year_and_month_folder(des_folder)
        file_path = des_folder + '/' + file
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Music')
    
    else: 
        des_folder += 'Downloads'    
        des_folder = check_year_and_month_folder(des_folder)
        file_path = des_folder + '/' + file
        os.rename(file_to_move, file_path)
        toast_and_open_folder(des_folder, 'Downloads')
    

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
      print(added)
      if added : 
        for file in added:
            if 'crdownload' in file:
                continue
            else:
              move_file(file)
          

      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification(change_handle)

finally:
  win32file.FindCloseChangeNotification(change_handle)
