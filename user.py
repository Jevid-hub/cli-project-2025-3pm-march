import csv
import sqlite3


# CLI application = command line interface

# go to git bash
# git config --global user.name "Jevid-hub"
# git config --global user.email "kunwarjevid@gmail.com"

# git init = first time
# git status = if you want to check what are the status of files
# git diff = if you want to check waht are the changes 
# git add = track file and folder 
# git commit -m "your message"
# copy paste git code from github


####################################

# 1. change the code
# 2. git add .
# 3. git commit -m "your message"
# 4. git push

####################################



def create_connection():
    try:
       con = sqlite3.connect("users.sqlite3")
       return con
    except Exception as e:
        print(e)


INPUT_STRING = """
Enter the option:
    1. CREATE TABLE
    2. DUMP users from csv INTO users TABLE
    3. ADD new users INTO user TABLE
    4. QUERY all users from TABLE
    5. QUERY users by id from TABLE
    6. QUARY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE users by id 
    9. UPDATE users
    10. Press any key to EXIT



"""


def create_table(con):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(225) NOT NULL,
            last_name CHAR(225) NOT NULL,
            company_name CHAR(225) NOT NULL,
            address CHAR(225) NOT NULL,
            city CHAR(225) NOT NULL,
            county CHAR(225) NOT NULL,
            state CHAR(225) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(225) NOT NULL,
            phone2 CHAR(225),
            email CHAR(225) NOT NULL,
            web text
        
        );
    """

    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User table was created successfully.")



def read_csv():
    users = []
    with open("sample_users.csv","r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]


def insert_users(con, users):
    user_add_query = """
        INSERT INTO users
        (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?);

    """
    cur = con.cursor()
    cur.executemany(user_add_query, users)
    con.commit()
    print(f"{len(users)}users were imported succesfully.")



def select_all_users(con):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users;")
    for user in users:
        print(user)


def select_user_by_id(con, user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users where id = ?;",(user_id,))
    for user in users:
        print(user)



def select_specified_no_of_users(con, no_of_users):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users LIMIT ?;",(no_of_users,))
    for user in users:
        print(user)




def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("all users were deleted successfully")


def delete_user_by_id(con, user_id):
    cur = con.cursor()
    cur.execute("delete from users where id = ?",(user_id,))
    con.commit()
    print(f"User with id [{user_id}] was successfully deleted.")





COLUMNS = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "country",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)


def update_user_by_id(con, user_id,column_name,column_value):
    cur = con.cursor()
    cur.execute(
        f"UPDATE users set {column_name}=? where id = ?;",(column_value,user_id)
    )
    con.commit()
    print(
        f"[{column_name}] was updated with value [{column_value}] of user with id [{user_id}]"
    )




def main():
    user_input = input(INPUT_STRING)
    con = create_connection()
    if user_input == "1":
        create_table(con)
    elif user_input == "2":
        users = read_csv()
        insert_users(con, users)
    elif user_input == "3":
        data = []
        for column in COLUMNS:
            column_value = input(f"Enter the value of {column}: ")
            data.append(column_value)
        insert_users(con, [tuple(data)])
    elif user_input == "4":
        select_all_users(con)
    elif user_input == "5":
        user_id = input("ENter user id:")
        if user_id.isnumeric():
            select_user_by_id(con,user_id)
    elif user_input == "6":
        no_of_users = input("ENTER no . of users:")
        if no_of_users.isnumeric():
            select_specified_no_of_users(con,no_of_users)
    elif user_input == "7":
        confirmation = input("Are u sure ? Please type y to continue: ")
        if confirmation == "y":
            delete_users(con)
    elif user_input == "8":
        user_id = input("Enter user id: ")
        if user_id.isnumeric():
            delete_user_by_id(con, user_id)
    elif user_input == "9":
        user_id = input("Enter id of user: ")
        if user_id.isnumeric():
            column_name = input(
                f"Enter the column you want to edit. Please make sure column is with in {COLUMNS}: "
            )
            if column_name in COLUMNS:
                column_value = input(f"Enter the value of {column_name}: ")
                update_user_by_id(con, user_id, column_name, column_value)
    else:
        pass


main()