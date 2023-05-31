from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk     #pip install pillow
from tkinter import messagebox
import mysql.connector
from main import Face_Recognition_System


def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()



class Login_Window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1530x790+0+0")


        self.bg=ImageTk.PhotoImage(file=r"hotel_images\SDT_Zoom-Backgrounds_April-8_Windansea-1-logo-1.jpg")

        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

        frame=Frame(self.root,bg="black")
        frame.place(x=510,y=120,width=340,height=450)

        img1=Image.open(r"hotel_images\LoginIconAppl.png")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoimage1,bg="black",borderwidth=0)
        lblimg1.place(x=630,y=125,width=100,height=100)

        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="black")
        get_str.place(x=95,y=100)

        #label
        username=lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username.place(x=70,y=155)

        self.txtuser=StringVar()
        self.txtpass=StringVar()

        txtuser=ttk.Entry(frame,textvariable=self.txtuser,font=("times new roman",15,"bold"))
        txtuser.place(x=40,y=180,width=270)

        password=lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        password.place(x=70,y=225)

        txtpass=ttk.Entry(frame,show="*",textvariable=self.txtpass,font=("times new roman",15,"bold"))
        txtpass.place(x=40,y=250,width=270)

        # IconImages
        img2=Image.open(r"hotel_images\LoginIconAppl.png")
        img2=img2.resize((25,25),Image.ANTIALIAS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg1=Label(image=self.photoimage2,bg="black",borderwidth=0)
        lblimg1.place(x=550,y=273,width=25,height=25)

        img3=Image.open(r"hotel_images\lock-512.png")
        img3=img3.resize((25,25),Image.ANTIALIAS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg1=Label(image=self.photoimage3,bg="black",borderwidth=0)
        lblimg1.place(x=550,y=343,width=25,height=25)

        #Login button
        loginbtn=Button(frame,text="Login",borderwidth=3,relief=RAISED,command=self.login,font=("times new roman",15,"bold"),fg="white",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=110,y=300,width=120,height=35)

        #Register button
        loginbtn=Button(frame,text="New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="black",activebackground="red")
        loginbtn.place(x=10,y=350,width=170)

        #Forgot Password button
        loginbtn=Button(frame,text="Forgot Password",command=self.forgot_password_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="black",activebackground="red")
        loginbtn.place(x=10,y=370,width=160)

    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if not self.txtuser.get() or not self.txtpass.get():
            messagebox.showerror("Error", "All fields are required.")
        elif self.txtuser.get() == "friends" and self.txtpass.get() == "forever":
            messagebox.showinfo("Success", "Welcome")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="Tris@12345", database="mydata")
            my_cursor = conn.cursor()
            query = "SELECT * FROM register WHERE email=%s AND password=%s"
            values = (self.txtuser.get(), self.txtpass.get())
            my_cursor.execute(query, values)
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid username and password.")
            else:
                open_main = messagebox.askyesno("YesNo", "Access only admin")
                if open_main:
                    self.new_window = Toplevel(self.root)
                    self.app = Face_Recognition_System(self.new_window)
                conn.commit()
                self.clear()
                conn.close()


    def clear(self):
        self.txtuser.set("")
        self.txtpass.set("")


    #forgot password window
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the email address to reset password")
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="Tris@12345",database="mydata")
            my_cursor=conn.cursor()         
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            #print(row)
            if row==None:
                messagebox.showerror("My Error","Please enter the valid username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),bg="white",fg="red")
                l.place(x=0,y=10,relwidth=1)

                security_Q=Label(self.root2,text="Security Questions",font=("times new roman",20,"bold"),fg="black",bg="white")
                security_Q.place(x=50,y=80)

                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_Q["values"]=("select","Your Birth Place","Your Girlfriend Name","Your Pet Name")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)

                security_A=Label(self.root2,text="Security Answer",font=("times new roman",20,"bold"),fg="black",bg="white")
                security_A.place(x=50,y=150)

                self.txt_security=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_security.place(x=50,y=180,width=250)

                new_password=Label(self.root2,text="New Password",font=("times new roman",20,"bold"),fg="black",bg="white")
                new_password.place(x=50,y=220)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_newpass.place(x=50,y=250,width=250)

                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),fg="white",bg="green")
                btn.place(x=100,y=290)
        
    #reset password
    def reset_pass(self):
        if self.combo_security_Q.get()=="Select" or self.txt_security.get()=="" or self.txt_newpass=="":
            messagebox.showerror("Error","All fields are required",parent=self.root2)
        # elif self.txt_security.get()=="":
        #     messagebox.showerror("Error","Please enter the answer",parent=self.root2)
        # elif self.txt_newpass.get()=="":
        #     messagebox.showerror("Error","Please enter the new password",parent=self.root2)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",user="root",password="Tris@12345",database="mydata")
                my_cursor=conn.cursor()
                qury=("select * from register where email=%s and securityQ=%s and securityA=%s")
                value=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get(),)
                my_cursor.execute(qury,value)
                row=my_cursor.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please enter the correct Answer",parent=self.root2)
                else:
                    query=("update register set password=%s where email=%s")
                    value=(self.txt_newpass.get(),self.txtuser.get())
                    my_cursor.execute(query,value)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success","Your password has been reset, Please login with new password",parent=self.root2)
                    self.root2.destroy()
                    self.txtuser.focus()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root2)


class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1530x790+0+0")

        #variables
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_securityA=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()
        

        #background image
        self.bg=ImageTk.PhotoImage(file=r"hotel_images\0-3450_3d-nature-wallpaper-hd-1080p-free-download-new.jpg")

        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

        # #left image
        self.bg1=ImageTk.PhotoImage(file=r"hotel_images\thought-good-morning-messages-LoveSove.jpg")

        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=50,y=100,width=470,height=550)

        #main frame
        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="green",bg="white")
        register_lbl.place(x=20,y=20)

        #labels and entry
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=50,y=130,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",20,"bold"),fg="black",bg="white")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=130,width=250)

        #row2

        contact=Label(frame,text="Contact No",font=("times new roman",20,"bold"),fg="black",bg="white")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame,text="Email",font=("times new roman",20,"bold"),fg="black",bg="white")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)

        #row3
        
        security_Q=Label(frame,text="Security Questions",font=("times new roman",20,"bold"),fg="black",bg="white")
        security_Q.place(x=50,y=240)

        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security_Q["values"]=("select","Your Birth Place","Your Girfriend Name","Your Pet Name")
        self.combo_security_Q.place(x=50,y=270,width=250)
        self.combo_security_Q.current(0)

        security_A=Label(frame,text="Security Answer",font=("times new roman",20,"bold"),fg="black",bg="white")
        security_A.place(x=370,y=240)

        self.txt_security=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15))
        self.txt_security.place(x=370,y=270,width=250)

        #row4
        pswd=Label(frame,text="Password",font=("times new roman",20,"bold"),fg="black",bg="white")
        pswd.place(x=50,y=310)

       
        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15))
        self.txt_pswd.place(x=50,y=340,width=250)
    
        confirm_pswd=Label(frame,text="Password",font=("times new roman",20,"bold"),fg="black",bg="white")
        confirm_pswd.place(x=370,y=310)
        
        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15))
        self.txt_confirm_pswd.place(x=370,y=340,width=250)
    
        #checkbutton
        self.var_check=IntVar()
        self.Checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree The Terms & Conditions",font=("times new roman",12,"bold"),onvalue=1,offvalue=0)
        self.Checkbtn.place(x=50,y=380) 

        #buttons
        img=Image.open(r"hotel_images\register-now-button1.jpg")
        img=img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage,command=self.register_data,borderwidth=0,cursor="hand2",font=("times new roman",20,"bold"),bg="black",fg="white")
        b1.place(x=10,y=420,width=200)

        img1=Image.open(r"hotel_images\loginpng.png")
        img1=img1.resize((200,50),Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimage1,command=self.return_login,borderwidth=0,cursor="hand2")
        b1.place(x=330,y=420,width=200)      

        #function declaration
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="Select":
            messagebox.showerror("Error","All fields are required")
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror("Error","Password & Confirm password must be same")
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please agree our terms and condition")
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="Tris@12345",database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist","please try another email")
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_contact.get(),
                    self.var_email.get(),
                    self.var_securityQ.get(),
                    self.var_securityA.get(),
                    self.var_pass.get(),
                    

                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Register Successfully")



if __name__=="__main__":
    main()