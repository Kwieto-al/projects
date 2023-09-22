from tkinter import *
from tkinter.ttk import *
import socket
import pickle
from random import randint
from datetime import datetime
import time
from cryptography.fernet import Fernet
from hashlib import sha256

class Connection:
    def CreateConnection(self,statement,column):
        HOST='172.30.159.228'
        PORT=5223
        if column=="Other":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((HOST, PORT))
                        s.send(pickle.dumps(statement))
                        data = s.recv(4096)
                        data = pickle.loads(data)
                        revd=True
                    except ConnectionResetError:
                        s.shutdown(1)
                        s.close()
                        data=None
                        
        else:
            query=statement+"\""+str(column)+"\""
            revd=False
            while not(revd):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            s.connect((HOST, PORT))
                            s.send(pickle.dumps(query))
                            data = s.recv(4096)
                            data = pickle.loads(data)
                            revd=True
                        except ConnectionResetError:
                            s.shutdown(1)
                            s.close()        
        return data
class error:
    def __init__(self,message):
        self.message=message
        self.Problem=Tk()
        self.error(self.message)

    def error(self,message):
        self.Problem.title("Error")
        self.Problem.geometry("200x200")
        self.e = Label(self.Problem,text=message)
        self.e.pack(padx=5)
        self.b = Button(self.Problem, text="OK", command=lambda: self.destroy(self.Problem))
        self.b.pack(pady=5)

    def destroy(self,Problem):
        self.Problem.destroy()
        
class messagingprogram(Connection):
    def Login(self):
        login = Tk()
        login.title("Login")
        login.geometry("350x200")
        Logintext=Label(login,text="Messaging: Please login", font=("Arial",12)).grid(row=0,pady=10,columnspan=2)
        UsernameEntry=Entry(login)
        UsernameEntry.grid(row=2,column=1,columnspan=2)
        UsernameLabel=Label(login,text="Username:").grid(row=2,column=0)
        PasswordLabel=Label(login,text="Password:").grid(row=3,column=0)
        PasswordEntry=Entry(login,show="•")
        PasswordEntry.grid(row=3,column=1,pady=10,columnspan=2)
        SignIn=Button(login,text="Sign In",command= lambda : self.LoginAttempt(UsernameEntry.get(),login,PasswordEntry.get())).grid(row=4,column=0)
        SignUp=Button(login,text="Sign Up",command= lambda : self.SignUp(login)).grid(row=4,column=2)

    def SignUp(self,login):
        login.destroy()
        SignUp=Tk()
        SignUp.title("Sign Up")
        SignUp.geometry("470x110")
        FNameText=Label(SignUp,text="First Name:").grid(row=0,column=0)
        FNameEntry=Entry(SignUp)
        FNameEntry.grid(row=0,column=1,columnspan=2)
        SNameText=Label(SignUp,text="Surname:").grid(row=0,column=3)
        SNameEntry=Entry(SignUp)
        SNameEntry.grid(row=0,column=4,columnspan=2)
        EmailText=Label(SignUp,text="Email:").grid(row=1,column=0)
        EmailEntry=Entry(SignUp)
        EmailEntry.grid(row=1,column=1,columnspan=2)
        UsernameText=Label(SignUp,text="Username:").grid(row=2,column=0)
        UsernameEntry=Entry(SignUp)
        UsernameEntry.grid(row=2,column=1,columnspan=2)
        PasswordText=Label(SignUp,text="Password:").grid(row=2,column=3)
        PasswordEntry=Entry(SignUp,show="•")
        PasswordEntry.grid(row=2,column=4,columnspan=2)
        SignUpButton=Button(SignUp,text="Sign Up", command=lambda:self.SendOffData(SignUp,UsernameEntry.get(),FNameEntry.get(),SNameEntry.get(),EmailEntry.get(),PasswordEntry.get()))
        SignUpButton.grid(row=3,column=6)
        


    def SendOffData(self,SignUp,username,FName,SName,email,password):
        h=sha256()
        password=password.encode()
        h.update(password)
        password=h.hexdigest()
        userdata=["NewUser",FName,SName,email,username,password]
        problemTest=False
        for i in userdata:
            print(i)
            if i=="":
                problemTest=True
        if problemTest==True:
            problem=error("The Entry boxes cannot be blank.")
            return "Uh Oh"
        response=self.CreateConnection(userdata,"Other")
        if response=="All Good":
            SignUp.destroy()
            self.Login()

        
    def LoginAttempt(self,Username,login,Password):
        if Username=="" or Password=="":
            fail=Label(text="Your username or password are incorrect.").grid(row=1,column=0,columnspan=3)
        else:
            h=sha256()
            Password=Password.encode()
            h.update(Password)
            Password=h.hexdigest()
            PasswordCheck=str(self.CreateConnection("1"+Password+"ƨSELECT Password FROM users Where username=",Username))
            if PasswordCheck=="True":
                login.destroy()
                contacts=Contacts(Username)
            else:
                fail=Label(text="Your username or password are incorrect.").grid(row=1,column=0,columnspan=3)

###############################################################################################################################
class Contacts(Connection):
    def __init__(self,username):
        self.Username=username
        self.contacts()
    def FindConversations(self,f):
        convos=self.CreateConnection("5",self.Username)
        for i in convos:
            i.remove(self.Username)
        return convos
    def contacts(self):
        contact=Tk()
        contact.title("Contacts")
        contact.geometry("450x645")
        ContactsScroll=Scrollbar(contact, orient=VERTICAL)
        listbox=Listbox(contact,height=30,width=50,yscrollcommand=ContactsScroll.set)
        ContactsScroll.config(command=listbox.yview)
        listbox.grid(row=1,column=1, columnspan=2)
        ContactsScroll.grid(row=1,column=3)
        chatbutton=Button(contact, text="Chat", command=lambda:Chat(listbox.get(listbox.curselection()),self.Username))
        chatbutton.grid(row=2,column=1)
        createbutton=Button(contact, text="Create Conversation", command= lambda: self.ConversationWindow(self.Username,contact))
        createbutton.grid(row=2,column=2)
        convos=self.FindConversations(self.Username)
        for i in convos:
            users=i[1:]
            users=",".join(users)
            listbox.insert(END,i[0]+" conversation with "+users)
    def ConversationWindow(self,username,contact):
        creator=Tk()
        creator.title("Create Conversation")
        creator.geometry("435x540")
        Title=Label(creator,text="New Conversation: Information", font=("Arial",12)).grid(row=0,pady=10,columnspan=2)
        Name=Label(creator,text="Conversation Name:").grid(row=2,column=0)
        NameEntry=Entry(creator)
        NameEntry.grid(row=2,column=1,columnspan=2)
        Search=Label(creator,text="Search Usernames:").grid(row=3,column=0)
        Searchentry=Entry(creator)
        Searchentry.grid(row=3,column=1,columnspan=2)
        SearchButton=Button(creator, text="Search", command= lambda: self.SearchUser(Searchentry.get(),userbox))
        SearchButton.grid(row=3,column=3)
        userbox=Listbox(creator,height=10, width=30)
        userbox.grid(row=4,column=1, columnspan=3)
        userbox.insert(END,self.Username)
        FinishButton=Button(creator, text="Create Conversation", command= lambda: self.CreateConversation(NameEntry.get(),userbox.get(0,END),creator,contact,username)).grid(row=5,column=1)

    def CreateConversation(self,name,users,windowconvo,windowcont,username):
        data=["Create Conversation",name,users]
        result=self.CreateConnection(data,"Other")
        windowconvo.destroy()
        windowcont.destroy()
        self.contacts()
    def SearchUser(self, username,userbox):
        exists=self.CreateConnection("S",username)
        if exists==None:
            Error=error("This user cannot be found")
        else:
            userlist=userbox.get(0,END)
            if username in userlist:
                Error=error("This user is already in the conversation")
            else:
                userbox.insert(END,username)
            
    
###########################################################################################################################

class Chat(Connection):
    def __init__(self,conversation,Username):
        self.conversation=conversation
        self.Username=Username
        self.chat(self.conversation,self.Username)
    def chat(self,conversation,Username):
        chatwindow=Tk()
        chatwindow.title(self.conversation)
        chatwindow.geometry("500x725")
        scrollbar=Scrollbar(chatwindow,orient=VERTICAL)
        messagebox=Listbox(chatwindow,height=40, width=80,yscrollcommand=scrollbar.set)
        scrollbar.config(command=messagebox.yview)
        messagebox.bindtags((messagebox, chatwindow, "all"))
        messagebox.grid(row=0, column=0,columnspan=3)
        scrollbar.grid(row=0,column=4)
        messagentry=Entry(chatwindow, width=70)
        messagentry.grid(row=1,sticky=SW)
        send=Button(chatwindow,text="SEND",command= lambda: self.sendmessage(messagentry.get(),self.Username,self.conversation,messagebox,messagentry)).grid(row=1,sticky=SE)
        chatwindow.bind('<Return>',lambda event: self.sendmessage(messagentry.get(),self.Username,self.conversation,messagebox,messagentry))
        messagebox.delete(0,END)
        userid=self.CreateConnection("2SELECT userid From users where username=",Username)
        conversationname=self.conversation.split(" conversation with ")[0]
        conversationid=self.CreateConnection("2select conversationid from conversations where name=",conversationname)
        convos=self.CreateConnection("3select message, sender,timestamp from messages where conversation=",conversationid)
        key=self.CreateConnection("6",conversationid)
        f=Fernet(key.encode())
        convos=list(convos)
        userids={}
        for i in convos:
            i=list(i)
            if str(i[1]) in userids:
                i[1]=userids[str(i[1])]
            else:
                temp=self.CreateConnection("2select username from users where userid=",str(i[1]))
                userids[str(i[1])]=temp
                i[1]=userids[str(i[1])]
            i[0]=f.decrypt(str(i[0]).encode())
            i[0]=i[0].decode()
            i[2]=datetime.fromtimestamp(i[2])
            messagebox.insert(END,str(i[2])+", "+str(i[1])[1:-1]+":"+i[0])
        messagebox.after(10000,lambda: self.MessageCheck(messagebox,convos,conversationid,userids,f))
        
    def MessageCheck(self,messagebox,convos,conversationid,userids,f):
        convos=self.CreateConnection("3select message, sender,timestamp from messages where conversation="+str(conversationid),"Other")
        convos=list(convos)
        
        messagebox.delete(0,END)
        for i in convos:
            i=list(i)
            if str(i[1]) in userids:
                i[1]=userids[str(i[1])]
            else:
                temp=self.CreateConnection("2select username from users where userid=",str(i[1]))
                userids[str(i[1])]=temp
                i[1]=userids[str(i[1])]
            i[0]=f.decrypt(str(i[0]).encode())
            i[0]=i[0].decode()
            i[2]=datetime.fromtimestamp(i[2])
            messagebox.insert(END,str(i[2])+", "+str(i[1])[1:-1]+":"+i[0])
        messagebox.after(10000,lambda: self.MessageCheck(messagebox,convos,conversationid,userids,f))
        
    def sendmessage(self,message,Username,conversation,mb,me):
        HOST='172.30.159.228'
        PORT=5223
        conversation=self.conversation.split(" conversation with ")
        conversationid=self.CreateConnection("2select conversationid from conversations where Name=",conversation[0])
        key=self.CreateConnection("6",conversationid)
        f= Fernet(key.encode())
        mess=message
        message=message.encode()
        message=f.encrypt(message)
        message=message.decode()
        sender=self.CreateConnection("2select userid from users where username=",self.Username)
        time=round(datetime.timestamp(datetime.now()))
        data=[sender,conversationid,message,time]
        revd=False
        while not(revd):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((HOST, PORT))
                        s.send(pickle.dumps(data))
                        data = s.recv(4096)
                        data = pickle.loads(data)
                        revd=True
                    except ConnectionResetError:
                        s.shutdown(1)
                        s.close()
        mb.insert(END,str(datetime.fromtimestamp(time))+", "+Username+":"+mess)
        me.delete(0,END)
        
messapp=messagingprogram()
messapp.Login()

