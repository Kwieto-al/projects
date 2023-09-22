import socket
import sqlite3
import pickle
from sqlite3 import Error
from time import sleep
import random
from cryptography.fernet import Fernet

def CreateConnection():
    #create a database connection to the SQLite database called db_file
    db_file=r"madatabase.db"
    con = None
    try:
        con = sqlite3.connect(db_file,isolation_level=None)
        return con
    except Error as e:
        print(e)
    return con
def CreateAccount(data):
    dbcon=CreateConnection()
    current=dbcon.cursor()
    found=False
    while not(found):
        userid=str(random.randint(1,10000))
        current.execute("Select name from conversations where conversationid="+userid)
        if current.fetchone()==None:
            found=True
            break
    data[0]=userid
    data=tuple(data)
    try:
        current.execute("insert into users values(?,?,?,?,?,?)",data)
        return "All Good"
    except:
        return "Problem"
    
def login(data): #checks the database for the password so the user can login
    dbcon=CreateConnection()
    current=dbcon.cursor()
    data=data[1:]
    password=data.split("ƨ")[0]
    data=data.split("ƨ")[1]
    current.execute(data)
    answer=str(current.fetchone())[2:-3]
    if answer==password:
        response=True
    else:
        response=False
    return response
def KeyCode(data):
    dbcon=CreateConnection()
    current=dbcon.cursor()
    data=data[1:]
    current.execute("select key from conversations where conversationid="+data)
    key=current.fetchone()
    key=str(key)[1:-2]
    return key
def CreateConversation(data):
    dbcon=CreateConnection()
    current=dbcon.cursor()
    data=data[1:]
    key = Fernet.generate_key()
    key=key.decode()
    found=False
    while not(found):
        coid=str(random.randint(1,1000))
        current.execute("Select name from conversations where conversationid="+coid)
        if current.fetchone()==None:
            found=True
            break
    information=(coid,data[0],key)
    current.execute("insert into conversations values(?,?,?)",information)
    for i in data[1]:
        current.execute("select userid from users where username=\""+i+"\"")
        userid=current.fetchone()
        current.execute("insert into relation values("+str(userid[0])+","+str(coid)+");")
    return True
    
def FindOne(data): #finds a single item in the database like the userid
    dbcon=CreateConnection()
    current=dbcon.cursor()
    data=data[1:]
    current.execute(data)
    test=current.fetchone()
    print(test)
    field=str(test)[1:-2]
    print(field)
    return field
def FindMany(data): # finds multiple items in the database like the conversations
    dbcon=CreateConnection()
    current=dbcon.cursor()
    data=data[1:]
    current.execute(data)
    field=current.fetchall()
    print(field)
    return field
def ReceiveMessage(data): #stores the message sent in the database so it can be received later
    dbcon=CreateConnection()
    current=dbcon.cursor()
    data=tuple(data)
    query="INSERT INTO messages values(?,?,?,?)"
    print(query)
    current.execute(query,data)
    print(current.fetchall())
    return "True"
def FindConversations(data): 
    username=str(data[1:])
    dbcon=CreateConnection()
    current=dbcon.cursor()
    current.execute("SELECT userid From users where username="+str(username))
    userid=str(current.fetchone()[0])
    current.execute("select conversationid from relation where userid="+userid)
    convos=current.fetchall()
    print(convos)
    users=[]
    for i in convos:
        current.execute("select userid from relation where conversationid=?",i)
        users.append(current.fetchall())
    print(users)
    for i in range(len(convos)):
        current.execute("select name from conversations where conversationid=?",convos[i])
        convos[i]=str(current.fetchone())[2:-3]
        print(convos[i])
        convos[i]=[convos[i]]
        print(convos[i])
        for j in range(len(users[i])):
            print(str(users[i][j]))
            current.execute("select username from users where userid="+str(users[i][j][0]))
            users[i][j]=str(current.fetchone())[2:-3]
            convos[i].append(users[i][j])
    print(convos)
    return convos
def FindUser(data):
    username=str(data[1:])
    dbcon=CreateConnection()
    current=dbcon.cursor()
    current.execute("Select userid from users where exists (select username from users where username="+username+")")
    userid=current.fetchone()
    return userid
PORT = 5223        
while True:
    print("opening socket.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(None)
        s.bind((socket.gethostname(), PORT))
        s.listen(10)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(8192)

                if not data:
                    break
                data=pickle.loads(data)
                print(data)
                if str(type(data))=="<class 'list'>":
                    if data[0]=="Create Conversation":
                        answer=pickle.dumps(CreateConversation(data))
                    elif data[0]=="NewUser":
                        answer=pickle.dumps(CreateAccount(data))
                    else:
                        answer=pickle.dumps(ReceiveMessage(data))
                elif data[0]=="1":
                    answer=pickle.dumps(login(data))
                elif data[0]=="2":
                    answer=pickle.dumps(FindOne(data))
                elif data[0]=="3":
                    answer=pickle.dumps(FindMany(data))
                elif data[0]=="5":
                    answer=pickle.dumps(FindConversations(data))
                elif data[0]=="6":
                    answer=pickle.dumps(KeyCode(data))
                elif data[0]=="S":
                    answer=pickle.dumps(FindUser(data))
                conn.send(answer)
            
            
