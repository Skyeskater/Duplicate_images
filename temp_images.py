'''
Check for identical images.
You have to add path_to_main_imagefolder on line 12 and 21 (where all your images are) and path_to_duplicates on line 43 and 109 (where you want your duplicates stored).

'''

import cv2
import os
import shutil
import re

path_to_main_imagefolder = r'C:\Users\Pictures'

def check_duplicate_images(abs_folder = None, foldername=None):
    '''abs_folder is when an absolute path to a folder is given 
    (i.e. when looping over all folders). foldername is when only 
    one folder is specified.'''
    
    
    if foldername == None and abs_folder == None:
        root_folder = r'C:\Users\Pictures'              #add root_folder
        foldername = input('Enter foldername: ')
        for root, dirs, files in os.walk(root_folder):
            for name in dirs:
                if name == foldername:
                    file_path_os = os.path.abspath(os.path.join(root, name))
    
    elif foldername != None:
        root_folder = r'E:\Computer\Afbeeldingen\Spitsbergen'
        file_path_os = os.path.join(root_folder, foldername)
        
    elif abs_folder != None:
        file_path_os = abs_folder
        #create foldername with regex for the duplicate folder:
        name_regex = re.compile(r'(.*)\\(.*)')
        mo = name_regex.search(file_path_os)
        foldername = mo.group(2)
    
    '''Change directory to given foldername'''
    os.chdir(file_path_os)
    
    '''Create duplicate folder, if not already created'''
    file_path_os_dupl = r'C:\Users\Duplicates'                                  #add path to duplicates
    if not os.path.exists(os.path.join(file_path_os_dupl, foldername)):
        os.makedirs(os.path.join(file_path_os_dupl, foldername))
    
    '''Make sure that files are sorted by size'''
    files = os.listdir(file_path_os)
    files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
    
    '''Make sure there no spaces in filenames'''
    for filename in os.listdir(file_path_os):
        if ' ' in filename:
            print('The following filenames have been altered:\n')
            print(filename)
            space_regex = re.compile(' ')
            filename_new = space_regex.sub('_', filename)
            shutil.move(os.path.join(file_path_os, filename), os.path.join(file_path_os, filename_new))
            print(filename_new)
        
    '''Checking for identical images'''
    def identical_images(file_1, file_2):
        file1 = cv2.imread(file_1)
        file2 = cv2.imread(file_2)
        
        '''check if filenames are images (only jpeg and jpg files, so no videos and .ini files)'''
        if not file_1.endswith('.jpg') and not file_1.endswith('.jpeg'):
            return False
        elif not file_2.endswith('.jpg') and not file_2.endswith('.jpeg'):
            return False
        
        '''check if filenames have same .jpg or .jpeg'''
        if file_1[-3:] != file_2[-3:]:
            return False #images are not equal
        
        elif file1.shape != file2.shape:
            return False #images are not equal
        
        elif file1.shape == file2.shape:
    #        print('The images have same size and channels')
        
            difference = cv2.subtract(file1, file2)
            b, g, r = cv2.split(difference)
            
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                return True #images are equal
            else:
                return False #images are not equal


    folder = os.listdir()
    total = 0
    
    '''check for duplicate images, and if True: move them to duplicate folder (ignore other directories within the directory)'''
    for x,y in zip(folder, folder[1:]):
        if identical_images(x,y) == True:
            print('\nDUPLICATES:\n' + str('\n'+x) + str('\n'+y))
            shutil.move(os.path.join(file_path_os, x), os.path.join(file_path_os_dupl, foldername, x))
            total += 1
    
    '''Delete duplicate folder if there are no duplicates'''
    path = os.path.join(file_path_os_dupl, foldername)
    directory = os.listdir(path)
    if len(directory) == 0:
        os.rmdir(path)
    
    print(f'There was a total of {total} duplicate(s).')
    if total:
        print('They have now been moved to:\n\n' + os.path.join(r'C:\Users\Duplicates', foldername))    #add path to duplicates


'''
Loop over every directory and subdirectory (including files within 
root directory) and over all files to change al names (so it doesn't 
contain spaces)
'''
def altering_names():
    root_folder = path_to_main_imagefolder
    for root, dirs, files in os.walk(root_folder):
        print('The following directorynames have been altered:\n')
        for name in dirs:
    #        print(os.path.abspath(os.path.join(root, name)))
            if ' ' in name:
                 print('old:  ' + name)
                 space_regex = re.compile(' ')
                 name_new = space_regex.sub('_', name)
                 shutil.move(os.path.join(root, name), os.path.join(root, name_new))
                 print('new:  ' + name_new)
        
        print('\nThe following filenames have been altered:\n')
        for name in files:
    #        print(os.path.abspath(os.path.join(root, name)))
            if ' ' in name:
                 print('old:  ' + name)
                 space_regex = re.compile(' ')
                 name_new = space_regex.sub('_', name)
                 shutil.move(os.path.join(root, name), os.path.join(root, name_new))
                 print('new:  ' + name_new)

#altering_names()

'''Finally, check for duplicates (can also do this per foldername).'''
for x in [x[0] for x in os.walk(path_to_main_imagefolder)]:
    print('\n'+x)
    check_duplicate_images(abs_folder = x)
