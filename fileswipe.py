import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import time
import re
import imageio
import os
import sys

root = tk.Tk()
root.geometry('800x500')
root.config(bg='gray10')
root.attributes('-alpha',0.85)
root.resizable(False,False)
root.title('Xfile')

namestate = False
finishing = False
deletionqueue = []
files = []
fileindex = 0
imageextensions = ['.png','.jpg','.jpeg','.webp','.gif']
videoextensions = ['.mp4','.mov','.mkv','.avi']

def finish():
    displaylabel.destroy()
    print('Finishing')
    namelabel.configure(text='Complete, enter "y" to confirm all deletions')
    if inputentryvar.get() == 'y':
        for path in deletionqueue:
            if not os.path.isdir(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            print(f'Removed {path}')
        sys.exit(1)
    else:
        inputentry.delete(0,tk.END)

def next():
    global fileindex, file
    print('Completing next operation')
    try:
        fileindex += 1
        file = files[fileindex]
    except IndexError:
        print('Cannot go any farther')
    if Path(f'{Path.home()}/{file}').suffix in videoextensions:
        reader = imageio.get_reader(f'{Path.home()}/{file}',format='ffmpeg')
        display = ImageTk.PhotoImage(Image.fromarray(reader.get_data(0)).resize((500,400)))
        reader.close()
    elif Path(f'{Path.home()}/{file}').suffix not in imageextensions or Path(f'{Path.home()}/{file}').is_dir():
        display = ImageTk.PhotoImage(Image.open(f'{Path.home()}/fileswipe/assets/placeholder.png').resize((500,400)))
    else:
        display = ImageTk.PhotoImage(Image.open(f'{Path.home()}/{file}').resize((500,400)))
    displaylabel.configure(image=display)
    displaylabel.image = display
    namelabel.configure(text=file)
    inputentry.delete(0,tk.END)
    root.update()

def takeinput(*args):
    global namestate, fileindex, file, finishing
    print('Input detected')
    if fileindex > len(files) - 1:
        print('All files finished')
        finish()
    else:
        if inputentryvar.get() == '/' or finishing:
            finishing = True
            finish()
        elif inputentryvar.get() == '[':
            print('Keep') #keep file
            namelabel.config(bg='green')
            root.update()
            time.sleep(0.5)
            namelabel.config(bg='gray20')
            next()
        elif inputentryvar.get() == ']':
            print('Delete') #delete file
            namelabel.config(bg='red')
            root.update()
            time.sleep(0.5)
            namelabel.config(bg='gray20')
            deletionqueue.append(f'{Path.home()}/{file}')
            print(f'Added to queue ({deletionqueue})')
            next()
        elif inputentryvar.get() == ';' or namestate:
            print('Renaming...') #rename file
            namestate = True
            name = inputentryvar.get()
            print(name)
            if inputentryvar.get() == '':
                namestate = False
                print('Exited namespace, empty field')
            for char in inputentryvar.get():
                if char == "'":
                    namestate = False
                    name = re.sub(r"[;']",'',name)
                    print(f'Exited namestate, saved as {name}')
                    try:
                        os.rename(f'{Path.home()}/{file}',f'{Path.home()}/{name}{Path(f'{Path.home()}/{file}').suffix}'.lower())
                    except Exception as e:
                        print(f'Issue occured! {e}')
                    next()

print(Path.home())
for fileobject in Path.home().iterdir():
    if not fileobject.name.startswith('.'):
        files.append(fileobject.name)
file = files[fileindex]
print(files)
print(file)
if Path(f'{Path.home()}/{file}').suffix in videoextensions:
    reader = imageio.get_reader(f'{Path.home()}/{file}',format='ffmpeg')
    display = ImageTk.PhotoImage(Image.fromarray(reader.get_data(150)).resize((500,400)))
    reader.close()
elif Path(f'{Path.home()}/{file}').suffix not in imageextensions or Path(f'{Path.home()}/{file}').suffix not in videoextensions or Path(f'{Path.home()}/{file}').is_dir():
    display = ImageTk.PhotoImage(Image.open(f'{Path.home()}/fileswipe/assets/placeholder.png').resize((500,400)))
else:
    display = ImageTk.PhotoImage(Image.open(f'{Path.home()}/{file}').resize((500,400)))
displaylabel = tk.Label(root,image=display)
displaylabel.place(x=150,y=50,width=500,height=400)
namelabel = tk.Label(root,text=file,bg='gray20',fg='white')
namelabel.place(x=150,y=50,width=500,height=25)
inputentryvar = tk.StringVar()
inputentryvar.trace_add('write', takeinput)
inputentry = tk.Entry(root,bg='gray20',textvariable=inputentryvar)
inputentry.place(x=275,y=450,width=250,height=25)
        
root.mainloop()