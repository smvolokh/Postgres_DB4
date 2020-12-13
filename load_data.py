import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

global functions


# init all sql
def init_functions():
    global functions
    functions = dict()

    # path to sql files
    sql_files = os.listdir(os.getcwd() + "\\functions")

    for file in sql_files:
        function = ""
        function_name = file.split(".")[0]

        # open curr file for reading
        opened_file = open(os.getcwd() + "\\functions\\" + file, "r")

        # adding from file to function var
        for item in opened_file:
            function += item + "\n"
        functions[function_name] = function


# initializing create_db and delete_db funcs (first init)
def init_create_delete_db(login, pass_):
    connection = psycopg2.connect(database="postgres", user=login,
                                  password=pass_, host="127.0.0.1",
                                  port="5432"
                                  )
    init_functions()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute("select 0 from current_database()")
    except():
        print("Error while connecting to postgres database")
        return None
    try:
        # print(functions)
        cursor.execute(functions["create_db"])
        cursor.execute(functions["delete_db"])
        cursor.execute("call install_dblink();")
    except:
        print("Error while installing dblink")
        return None
    return 1  # for check


# create database
def create_db(name, login, pass_):
    global functions

    # initialize all sql files
    init_functions()

    connection = psycopg2.connect(database="postgres", user=login,
                                  password=pass_, host="127.0.0.1",
                                  port="5432"
                                  )

    # change permissions
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    # check connection to postgres database
    try:
        cursor.execute("select 0 from current_database()")
    except():
        print("Error while connecting to postgres database")
        return

    # calling function create_db
    try:
        cursor.execute("call create_db('" + name + "','" + pass_ + "');")
    except:
        print("Database with name {0} exists".format(name))
        return
    cursor.close()

    # try to connect to new created database
    connection = psycopg2.connect(database=name, user=login,
                                  password=pass_, host="127.0.0.1",
                                  port="5432"
                                  )

    # permiss
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    # check connection
    try:
        cursor.execute("select 0 from current_database()")
    except():
        print("Error while creating database")
        return 1

    # init and call create_tables()
    cursor.execute(functions["create_tables"])
    cursor.execute("call create_tables();")

    # init remaining functions and procedures
    for function in functions:
        cursor.execute(functions[function])
    cursor.close()
    return 0


# delete existing database
def delete_db(name, login, pass_):
    connection_del = connect_db("postgres", login, pass_)
    cursor = connection_del.cursor()
    cursor.execute("call delete_db(\'" + name + "\',\'" + pass_ + "\');")
    try:
        connection_del = connect_db(name, login, pass_)
    except:
        return 0
    print("Error while deleting database")
    return 1


# just output information from the given table
def output_table(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute("select output_" + name + "();")
    except:
        return None

    # res = list of datas in table (in tuples)
    res = cursor.fetchall()

    rows = []
    for item in res:
        rows.append(list(item[0].replace('(', '').replace(')', '').split(",")))
    return rows


# clear all records from the table (with truncate, not delete)
def clear_table(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute("call clear_table('" + name + "');")
    except:
        print("Error while clearing table " + name)
        return 1
    return 0


# clear all records from all tables
def clear_all_tables(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("call clear_all();")
    except:
        print("Error while clearing tables")
        return 1
    return 0


# forming command with arguments for inserting into correct table
# also executes while updating information in tables
def insert_table(connection, name, args):
    cursor = connection.cursor()
    command = "call insert_" + name + "("
    # all arguments are strings, but some of them must be integers
    if (name == 'Automobiles'):
        command += "'" + args[0] + "'," + "'" + args[1] + "'," + args[2]
    if (name == 'Autosalons'):
        command += "'" + args[0] + "'," + "'" + args[1] + "'," + "'" + args[2] + "'," + args[3] + "," + args[4]
    if (name == 'Orders'):
        command += "'" + args[0] + "'," + "'" + args[1] + "'," + "'" + args[2] + "'," + "'" + args[3] + "'," + "'" + \
                   args[4] + "'"
    command += ");"

    print(command)
    try:
        cursor.execute(command)
    except:
        return 1
    return 0


# connect to database and return connection
def connect_db(name, login, pass_):
    connection = psycopg2.connect(database=name, user=login,
                                  password=pass_, host="127.0.0.1",
                                  port="5432"
                                  )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    try:
        cursor.execute("select 0 from current_database()")
    except():
        print("Error while connecting to database" + name)
        return None
    return connection


# find in autosalons by model
def find(connection, model):
    cursor = connection.cursor()
    try:
        cursor.execute("select find(\'" + model + "\');")
    except:
        print("Error while searching in autosalons by model = ", model)
    try:
        res = cursor.fetchall()
    except:
        return []
    rows = []
    for item in res:
        rows.append(list(item[0].replace('(', '').replace(')', '').split(",")))
    return rows


# delete from orders by model
def delete_model(connection, model):
    cursor = connection.cursor()
    try:
        # print("model for del: ", model, " ", len(model))
        cursor.execute("call delete_model(\'" + model + "\');")
    except:
        print("There is no such model ({0}) in the table".format(model))
        return 1
    return 0


# delete row from table 'name' = table_name with 'id' = if_of_rec
def delete_record(connection, table_name, id_of_rec):
    cursor = connection.cursor()
    try:
        cursor.execute("call delete_rec(\'" + table_name + "\',\'" + id_of_rec + "\');")
    except:
        return 1
    return 0


# output names of existing databases in the database menu (without postgres, template0 and other)
def output_dbs(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("select output_db();")
    except:
        return None
    res = cursor.fetchall()
    rows = []
    for item in res:
        rows.append(list(item[0].replace('(', '').replace(')', '').split(",")))
    return rows

# execute insert function for every table with some datas
def test_calls(connection):
    datas = {'Automobiles' : [('AM001', 'BMW', 1500000), ('AM002', 'Toyota', 1000000), ('AM003', 'Kia', 600000)],
             'Autosalons' : [('AS001', 'Moscow', 'BMW', False, 700000), ('AS002', 'Sochi', 'Toyota', True, 0),
                             ('AS003', 'Samara', 'Kia', True, 300000)],
             'Orders' : [('OR001', 'AM001', 'AS001', 'Pasha', 'BMW'), ('OR002', 'AM002', 'AS002', 'Semyon', 'Toyota'),
                         ('OR003', 'AM002', 'AS002', 'Alexander', 'Toyota'), ('OR004', 'AM003', 'AS003', 'Evgeniy', 'Kia')]
             }

    cursor = connection.cursor()
    try:
        for item in datas.items():
            command = "call insert_" + item[0] + "("
            for i in range(len(item[1])):
                if (item[0] == 'Automobiles'):
                    command += "'" + item[1][i][0] + "'," + "'" + item[1][i][1] + "'," + str(item[1][i][2]) + ");"
                if (item[0] == 'Autosalons'):
                    command += "'" + item[1][i][0] + "'," + "'" + item[1][i][1] + "'," + "'" + item[1][i][2] + "'," + str(item[1][i][3]) + "," + str(item[1][i][4]) + ");"
                if (item[0] == 'Orders'):
                    command += "'" + item[1][i][0] + "'," + "'" + item[1][i][1] + "'," + "'" + item[1][i][2] + "'," + "'" + item[1][i][3] + "'," + "'" + item[1][i][4] + "');"
                cursor.execute(command)
                #print(command)
                command = "call insert_" + item[0] + "("

    except:
        print("Error while inserting test calls")
        return 1
    return 0
