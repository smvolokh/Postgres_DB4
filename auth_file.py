from tkinter import *
import load_data
import db_join
root = None
login = None
password = None
del_but = False

def init_trigger(event):
    global del_but
    if (not del_but):
        if load_data.init_create_delete_db("postgres", "postgres111") == 1:
            event.widget.configure(text = "Success!")
            print("Successfully installed\nDon't try to install it again!")
        else:
            print("Error.")
            event.widget.configure(text = "Error!")
    del_but = True

def authentication_trigger(event):
    global root
    global login
    global password
    if (login.get() != "" and password.get() != ""):
        res = db_join.main(login.get(), password.get(), root)
        if res == 1:
            print('Can`t successfully connect to database')

if __name__ == "__main__":
    root = Tk()
    root['background'] = "#008B8B"
    root.title("Login window")
    root.resizable(width=False, height=False)
    root.geometry("300x230+30+30")
# Entry window    
    label_welcome = Label(text="Homo Soveticus automotive salon!", font=("Helvetica", 13), fg="black", bg = "#87CEFA" )
    label_welcome.place(x=30, y=10)
    login_label = Label(text="Login:")
    login_label.place(x=90, y=40)
    login = Entry(root)
    login.place(x=90, y=70)

    password = Entry(root, show = "•")
    password.place(x=90, y=130)
    pass_label = Label(text="Password:")
    pass_label.place(x=90, y=100)
    auth = Button(text="Sign in", bg="#87CEFA", font=2)
    auth.place(x=120, y=165)
    auth.bind('<Button-1>', authentication_trigger)

    install = Button(text="First Init", font = 2)
    install.place(x=220, y=195)
    install.bind('<Button-1>', init_trigger)
    root.mainloop()

