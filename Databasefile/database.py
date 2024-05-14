import mysql.connector


def connetion():
    iscreated=None
    try:
        # Open the file in read mode and fetch the value
        with open('checker.txt', 'r') as file:
            lines = file.readlines()
            if lines:
                iscreated=lines[-1].strip()
    except FileNotFoundError:
        print("File Not Found")
    if iscreated:
        try:
            return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="01k2",
            database="multifeatureaidatabase")
        except:
            print("Some Error has Been Encountered please try again And Check All the credentials once Again") 
    else:
        table_creation()



def DatabaseCreation():
    projectdb='multifeatureaidatabase'
    created=False

    db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="01k2",
    )


    mycursor=db.cursor()
    print(mycursor)
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall()
    for db in databases:
        # print(db[0])
        if db[0] == projectdb:
            print("Database Exist")
            created=True
    if not created:
        try:
            mycursor=db.cursor()
            mycursor.execute(f"create database {projectdb}")
            print(f'Database name {projectdb} is Created')
        except:
            print("Some Error has Been Encountered please try again And Check All the credentials once Again")
    return created





def table_creation():
    db=None
    if DatabaseCreation():
        try:
            db=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="01k2",
            database="multifeatureaidatabase")
            mycursor=db.cursor()
            mycursor.execute("CREATE TABLE aitable (name varchar(50), email varchar(100), gender varchar(15), phno varchar(10), Address varchar(200),username varchar(50),image longblob,id int PRIMARY KEY AUTO_INCREMENT)")
        except:
            print("Some Error has Been Encountered please try again And Check All the credentials once Again")

    try:
        # Open the file in append mode and write the value
        with open('checker.txt', 'a') as file:
            value = 'True'
            file.write(value + '\n')  # Append the value to the file with a newline character
        print("Value appended successfully.")
    except IOError:
        print("Error: Could not write to the file.")


def storeData(name,email,phno,address,username,gender,image_binary):
    db=connetion()
    cur=db.cursor()
    with open(image_binary, "rb") as file:
            image = file.read()
    cur.execute("insert into aitable (name,email,gender,phno,Address,username,image) values (%s,%s,%s,%s,%s,%s,%s)",(name,email,gender,phno,address,username,image))
    print(name)
    print(email)
    print(phno)
    print(gender)
    db.commit()
    cur.close()
    db.close()
    return True


def fetch_DB_DATA(uname):
    print(uname)
    db=connetion()
    cur=db.cursor()
    cur.execute("SELECT username FROM aitable")
    usernames = cur.fetchall()
    for user in usernames:
        if uname==user[0]:
            # print('yes exists')
            return True
    return False

# storeData('name','email','gender','phno','Address','username')