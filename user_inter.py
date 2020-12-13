from tkinter import *
import load_data

# globals
connection = None
window_in_table = None
del_upd_window = None
input_window = None
insert_args = []
args = []
header = []
del_lab = []
curr_table = []
curr_row = []


def model_del_trigger(event):
    global curr_table
    global connection
    # print(event.widget.get())
    load_data.delete_model(connection, event.widget.get())
    update_create_table(load_data.output_table(connection, curr_table), curr_table)


def del_trigger(event):
    global connection
    global curr_table
    global curr_row
    load_data.delete_record(connection, curr_table, curr_row)
    update_create_table(load_data.output_table(connection, curr_table), curr_table)  # update


def clear_all_trigger(event):
    global connection
    global curr_table
    load_data.clear_all_tables(connection)
    update_create_table(load_data.output_table(connection, curr_table), curr_table)  # update


def clear_trigger(event):
    global connection
    global curr_table
    load_data.clear_table(connection, curr_table)
    update_create_table(load_data.output_table(connection, curr_table), curr_table)  # update


def insert_trigger(event):
    global connection
    global curr_table
    global insert_args
    inp = []
    for i in insert_args:
        inp.append(i.get())
    load_data.insert_table(connection, curr_table, inp)
    update_create_table(load_data.output_table(connection, curr_table), curr_table)  # update


def moveto_table_trigger(event):
    global connection
    update_create_table(load_data.output_table(connection, event.widget.cget("text")), event.widget.cget("text"))


def find_car_trigger(event):
    global connection
    update_create_table(load_data.find(connection, event.widget.get()), 'Autosalons')


def updater_trigger(event):
    global connection
    global curr_table
    global insert_args
    global header
    inp = [curr_row]
    for i in insert_args:
        inp.append(i.get())
    load_data.insert_table(connection, curr_table, inp)
    update_create_table(load_data.output_table(connection, curr_table), curr_table)  # update


def test_calls_trigger(event):
    global connection
    global curr_table
    load_data.test_calls(connection)
    update_create_table(load_data.output_table(connection, curr_table), curr_table)



def inserting():
    global connection
    global curr_table
    global input_window
    global insert_args
    input_window = Frame()
    input_window.configure(width=250, height=180)
    input_window.place(x=620, y=320)
    header = []
    if curr_table == "Automobiles":
        header = ["ID", "Model", "Price"]
    if curr_table == "Autosalons":
        header = ["ID", "Adress", "Model", "In Stock", "Options"]
    if curr_table == "Orders":
        header = ["ID", "Automobile Id", "Autosalon Id", "Customer", "Model", "Summary price"]
    insert_args = []
    for i in range(len(header)):
        if (header[i] == "Summary price"):
            continue
        label_for_entry = Label(input_window, text=header[i] + ":", font=5)
        entry = Entry(input_window)
        entry.place(x=110, y=10 + 20 * i)
        label_for_entry.place(x=0, y=10 + 20 * i)
        insert_args.append(entry)
    accept_button = Button(input_window, text="Insert into " + str(curr_table), font=5, bg="#87CEFA")
    accept_button.place(x=75, y=120)
    accept_button.bind('<Button-1>', insert_trigger)
    init_buttons()


def upd_del_window_trigger(event):
    global del_upd_window
    global curr_row
    global input_window
    global header
    global insert_args
    if del_upd_window is not None:
        for i in del_upd_window.grid_slaves():
            i.destroy()
        del_upd_window.destroy()
    del_upd_window = Tk()
    del_upd_window['background'] = "#008B8B"
    del_upd_window.title("Delete-Update window")
    del_upd_window.resizable(width=False, height=False)
    del_upd_window.geometry("250x200+30+30")
    del_upd_window.configure(bg="grey")
    # del_upd_window.place(x=400, y=200)
    curr_row = event.widget.cget("text")
    delete_button = Button(del_upd_window, text='Delete', font=2, bg="red")
    delete_button.bind('<Button-1>', del_trigger)
    delete_button.place(x=140, y=165)
    header = []
    insert_args = []
    if curr_table == "Automobiles":
        header = ["Model", "Price"]
    if curr_table == "Autosalons":
        header = ["Address", "Model", "In Stock", "Options"]
    if curr_table == "Orders":
        header = ["Automobile ID", "Autosalon ID", "Customer", "Model"]
    j = 0
    for i in range(len(header)):
        label_for_entry = Label(del_upd_window, text=header[i] + ":")
        entry = Entry(del_upd_window)
        entry.place(x=110, y=40 + 22 * i)
        label_for_entry.place(x=0, y=40 + 22 * i)
        insert_args.append(entry)
        j = i
    accept_button = Button(del_upd_window, text="Update row with ID = " + str(curr_row), bg="green")
    accept_button.place(x=0, y=40 + 22 * (j + 1))
    accept_button.bind('<Button-1>', updater_trigger)


def update_create_table(data, table):
    global curr_table
    curr_table = table
    global window_in_table
    global del_upd_window
    global input_window
    if window_in_table is not None:
        for i in window_in_table.grid_slaves():
            i.destroy()
        window_in_table.destroy()
        window_in_table = None
    if del_upd_window is not None:
        for i in del_upd_window.grid_slaves():
            i.destroy()
        del_upd_window.destroy()
        del_upd_window = None
    if input_window is not None:
        for i in input_window.grid_slaves():
            i.destroy()
        input_window.destroy()
        input_window = None
    window_in_table = Frame()
    window_in_table.configure(width=600, height=800, bg="grey")
    window_in_table.place(x=0, y=0)
    header = []
    if table == "Automobiles":
        header = ["ID", "Model", "Price"]
    if table == "Autosalons":
        header = ["ID", "Adress", "Model", "In Stock", "Options"]
    if table == "Orders":
        header = ["ID", "Auto Id", "Autosalon Id", "Customer", "Model", "Summary price"]
    for i in range(len(header)):
        l = Label(window_in_table)
        l.configure(width=80 // len(header), height=1, bg="green", text=str(header[i]))
        l.place(x=i * (600 // len(header)), y=0)
    for i in range(0, len(data)):
        b_id = Button(window_in_table)
        b_id.configure(width=78 // len(data[i]), height=1, bg="white", text=str(data[i][0]))
        b_id.bind('<Button-1>', upd_del_window_trigger)
        b_id.place(x=0, y=(i + 1) * 20)
        for j in range(1, len(data[i])):
            l = Label(window_in_table)
            l.configure(width=80 // len(data[i]), height=1, bg="white", text=str(data[i][j]))
            l.place(x=j * (600 // len(header)), y=(i + 1) * 21)
    inserting()


def init_buttons():
    global curr_table
    global del_lab
    automobile_button = Button(text='Automobiles', font=5, width=10, bg="#87CEFA")
    autosalons_button = Button(text='Autosalons', font=5, width=10, bg="#87CEFA")
    orders_button = Button(text='Orders', font=5, width=10, bg="#87CEFA")
    automobile_button.place(x=890, y=10)
    autosalons_button.place(x=890, y=50)
    orders_button.place(x=890, y=90)
    automobile_button.bind('<Button-1>', moveto_table_trigger)
    autosalons_button.bind('<Button-1>', moveto_table_trigger)
    orders_button.bind('<Button-1>', moveto_table_trigger)
    clear_db = Button(text="Clean all tables")
    clear_db.bind('<Button-1>', clear_all_trigger)

    # button for filling some data into the tables
    test_calls_button = Button(text='Fill data', font = 5, width=10, bg = "#87CEFA")
    test_calls_button.place(x=890, y = 550)
    test_calls_button.bind('<Button-1>', test_calls_trigger)

    if (curr_table == 'Autosalons'):
        if (len(del_lab) != 0):
            for i in range(len(del_lab)):
                del_lab[i][0].destroy()
                del_lab[i][1].destroy()
        label_for_entry = Label(text="Search Car by Model in Autosalons", font=6)
        entry = Entry(width=30)
        entry.bind('<Return>', find_car_trigger)
        entry.place(x=680, y=155)
        label_for_entry.place(x=650, y=125)
        del_lab.append([label_for_entry, entry])
    else:
        if (len(del_lab) != 0):
            for i in range(len(del_lab)):
                del_lab[i][0].destroy()
                del_lab[i][1].destroy()

    if (curr_table == 'Orders'):
        if (len(del_lab) != 0):
            for i in range(len(del_lab)):
                del_lab[i][0].destroy()
                del_lab[i][0].destroy()
        label_for_entry = Label(text="Clear Orders by Model in Orders", font=6)
        entry = Entry(width=30)
        entry.bind('<Return>', model_del_trigger)
        entry.place(x=680, y=155)
        label_for_entry.place(x=650, y=125)
        del_lab.append([label_for_entry, entry])

    if curr_table in ['Automobiles', 'Autosalons', 'Orders']:
        clear_tab = Button(text="Clear current table", bg="#87CEFA")
        clear_tab.bind('<Button-1>', clear_trigger)
        clear_tab.place(x=610, y=10)
        clear_tab = Button(text="Clear all tables", bg="#87CEFA")
        clear_tab.bind('<Button-1>', clear_all_trigger)
        clear_tab.place(x=610, y=50)


def main(db, login, password, entrypoint_root):
    global connection
    global window_in_table
    global del_upd_window
    entrypoint_root.destroy()
    window_in_table = None
    del_upd_window = None
    try:
        connection = load_data.connect_db(db, login, password)
    except:
        return 1
    root = Tk()
    root['background'] = "#008B8B"
    root.title("Database " + db)
    root.geometry("1000x600+30+30")
    update_create_table([], 'Automobiles')
    init_buttons()
    root.mainloop()
