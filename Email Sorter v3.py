#Email Sorter V3
import imaplib, email
import time
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import threading

class MailSorter():
    def __init__(self,email,password):
        self.log = []
        
        self.email = email
        self.password = password
        self.inboxName = 'Inbox'
        
        self.mail = None    

    def login(self):
        #Login
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")#Goes to google
        self.mail.login(self.email,self.password)#Logins into google

    def fetchEmailId(self):
        self.mail.select(self.inboxName)#Access all mail
        result,emailsID = self.mail.search(None,"ALL")#Acess all email emails
        inbox_item_list = emailsID[0].split()#Stores into an array
        return inbox_item_list

    def fetchFrom(self,emailIDs):
        EmailAmount = dict() #Dict of emails and amounts
        Email = [] #Array of emails and ID
        for emailId in emailIDs:
            #Converts email into string
            result2,email_data = self.mail.fetch(emailId,'(RFC822)')
            try:
                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)
                #Fetches email address sent from
                From = email_message["From"]
                Email.append((From,emailId))
                if From in EmailAmount:
                    EmailAmount[From] = EmailAmount[From] + 1
                else:
                    EmailAmount[From] = 1
            except Exception as e:
                self.log.append((emailId,e))
                
        return EmailAmount,Email

    def displayEmails(self,Dict):
        for email,amount in Dict.items():
            print(email,amount)

    def deleteEmail(self, emailName, EmailArray):
        for x in range(len(EmailArray)-1):
            if EmailArray[x][0] == emailName:
                print("Deleting email...")
                self.mail.store(EmailArray[x][1], '+X-GM-LabelS', '\\Trash')
                EmailArray.remove(EmailArray[x])
                self.deleteEmail(emailName,EmailArray)
            else:
                print("All deleted")
        return True

    def closeCon(self):
        self.mail.close()
        self.mail.logout()


class GUI():
    def __init__(self,root):
        #GUI
        self.master = root
        self.master.geometry("750x175")
        self.master.title("Folder Sorter")
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        self.master.grid_columnconfigure(0, weight=1)

        #Login details
        self.email = None
        self.password = None

    def loginScreen(self):
        #Labels
        mainTitle = tk.Label(self.frame, text = "Welcome To The Email Sorter 1.0")
        mainTitle.config(font=("Courier","25"))
        Email = tk.Label(self.frame, text = "Email")
        password = tk.Label(self.frame, text = "Password")
        text = tk.Label(self.frame, text = "Program takes around 5 to minutes to load please wait")
        
        #Entry Boxes
        self.usernameEntry = tk.Entry(self.frame)
        self.passwordEntry = tk.Entry(self.frame)

        #Buttons
        loginButton = tk.Button(self.frame, text = "Login", command = self.signIn)

        #Placment
        mainTitle.grid(row = 0,column = 3)
        Email.grid(row=2,column=3)
        self.usernameEntry.grid(row=3, column=3)
        password.grid(row=4,column=3)
        self.passwordEntry.grid(row=5, column=3)
        loginButton.grid(row=7, column=3)
        text.grid(row=9, column=3)


    def signIn(self):
        self.email = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        self.Mail = MailSorter(self.email,self.password)
        try:
            self.Mail.login()
            self.mainScreenInterface()
        except:
            tk.messagebox.showwarning("Invaild Credentials","Error\nPlease Check Permissions And Login Credentials\nRead the 'ReadMe.txt' For Information On How To Change Your Psermissions")        
        
    def loadingPage(self):
        pass
                            
    def mainScreenInterface(self):
        #Process
        print("Loading program")
        EmailIds = self.Mail.fetchEmailId()
        self.EmailDict, self.EmailArray = self.Mail.fetchFrom(EmailIds)
        
        self.master.geometry("750x600")
        self.master.title("Main Screen")
        self.destoryWidget()
        
        #New Frame
        self.mainScreen = tk.Frame(self.master)
        self.mainScreen.pack()

        #Labels
        mainText = tk.Label(self.mainScreen,text = "All Emails")
        mainText.config(font=("Courier","25"))
        
        #Buttons
        delete = tk.Button(self.mainScreen,text="Delete", command = self.Delete)
        
        #Scrollbar
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side="right",fill="y")
        
        #Listbox
        self.listbox = tk.Listbox(root,width = root.winfo_screenwidth(), height = 25)
        #Attach a scrool wheel to the listbox
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        #Add items to the list box
        count = 1
        for x,y in self.EmailDict.items():
            self.listbox.insert(count,(x,y))
            count += 1
        
        #Placement
        paddingValue = 40
        mainText.pack(side="top")
        self.listbox.pack(side="top")
        delete.pack(side="left",padx=paddingValue)
        


    def Delete(self):
        orignal = self.listbox.get(tk.ANCHOR)
        emailName = orignal[0]
        done = self.Mail.deleteEmail(emailName,self.EmailArray)
        #Update List Box
        self.listbox.delete(tk.ANCHOR)

    def test(self):
        pass
    
    def destoryWidget(self):
        for widgets in self.master.winfo_children(): #Loops through the widgets
            widgets.grid_forget()#Destroy Widgets


root = tk.Tk()
gui = GUI(root)
gui.loginScreen()
root.mainloop()



