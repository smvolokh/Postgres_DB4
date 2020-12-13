from tkinter import *
import load_data
import user_inter

log = None
pass_ = None
root = None
connection = None
labels = None
db = None


def refresh_db(event):
    global connection
    global labels
    if labels is not None:
        for i in labels:
            i.destroy()
    labels = []
    db_data = load_data.output_dbs(connection)
    j = 0
    for i in range(len(db_data)):
        if db_data[i][0] == 'postgres':
            continue
        if db_data[i][0] == 'demo':
            continue
        if db_data[i][0] == 'lab1':
            continue
        if db_data[i][0] == 'template0':
            continue
        if db_data[i][0] == 'template1':
            continue
        l_db = Button(text=db_data[i][0], bg="green")
        l_db.place(x=10 + (j+1)*50, y=165)
        j += 1
        l_db.bind('<Button-3>', delete_db)
        l_db.bind('<Button-1>', connect_to_db)
        labels.append(l_db)


def delete_db(event):
    global login
    global password
    res = load_data.delete_db(event.widget.cget("text"), log, pas)
    if res == -1:
        print('Can`t successfully delete database')
    refresh_db(None)

def create_db(event):
    global login
    global password
    res = load_data.create_db(event.widget.get(), log, pas)
    refresh_db(None)
    if res == -1:
        print('Can`t successfully create database')
    else:
        event.widget.configure(bg="green")



def connect_to_db(event):
    global root
    global login
    global pas
    res = user_inter.main(event.widget.cget("text"), log, pas, root)
    if res == -1:
        print('Can`t successfully connect to database')


def main(login, password, entry_root):
    entry_root.destroy()
    global root
    global log
    global pas
    log = login
    pas = password
    root = Tk()
    root['background'] = "#008B8B"
    root.title("Database menu")
    global connection
    try:
        connection = load_data.connect_db('postgres', login, password)
    except:
        return -1
    root.geometry("350x200+30+30")
    label_welcome = Label(text="Homo Soveticus automotive salon!", font=3, bg="#87CEFA", fg="black")
    label_welcome.place(x=55, y=10)
    label_create_db = Label(text='Enter name of db and press enter to create it', font = 2)
    label_create_db.place(x=30, y=40)
    db = Entry(root)
    db.place(x=120, y=70)
    db.bind('<Return>', create_db)
    label_explain = Label(text="Left click on db - connect. Rigth click - delete.", font = 2)
    label_explain.place(x=30, y = 95)
    refresh_db(None)
    root.mainloop()
