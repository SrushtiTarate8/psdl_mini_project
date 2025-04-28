from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        # === Background Colors ===
        left_lbl = Label(self.root, bg="#8A3D2F", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)
        
        right_lbl = Label(self.root, bg="#031F3C", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        # === Frame ===
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=250, y=100, height=500, width=800)

        title = Label(login_frame, text="LOGIN HERE", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=250, y=30)

        lbl_email = Label(login_frame, text="EMAIL ADDRESS", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=100)
        self.txt_email = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=250, y=130, width=350, height=35)

        lbl_pass = Label(login_frame, text="PASSWORD", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=180)
        self.txt_pass = Entry(login_frame, font=("times new roman", 15), bg="lightgray", show='*')
        self.txt_pass.place(x=250, y=210, width=350, height=35)

        btn_login = Button(login_frame, text="Login", cursor="hand2", command=self.login, font=("times new roman", 15), bg="green", fg="white").place(x=250, y=270, width=120, height=35)
        btn_reg = Button(login_frame, text="Register", cursor="hand2", command=self.register_window, font=("times new roman", 15), bg="blue", fg="white").place(x=400, y=270, width=120, height=35)
        btn_forget = Button(login_frame, text="Forget Password", cursor="hand2", command=self.forget_password_window, font=("times new roman", 15), bg="red", fg="white").place(x=250, y=320, width=270, height=35)

    def reset(self):
        self.cmb_quest.current(0)
        self.txt_new_pass.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_pass.delete(0, END)
        self.txt_email.delete(0, END)

    def forget_password_window(self):
        if self.txt_email.get() == "":
            messagebox.showerror("Error", "Please enter your email to reset password", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=?", (self.txt_email.get(),))
                row = cur.fetchone()
                con.close()

                if row is None:
                    messagebox.showerror("Error", "Email not found", parent=self.root)
                else:
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("400x400+500+150")
                    self.root2.config(bg="white")

                    lbl_ques = Label(self.root2, text="Security Question", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=50)
                    self.cmb_quest = ttk.Combobox(self.root2, font=("times new roman", 13), state='readonly', justify=CENTER)
                    self.cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
                    self.cmb_quest.place(x=50, y=80, width=250)
                    self.cmb_quest.current(0)

                    lbl_answer = Label(self.root2, text="Answer", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=130)
                    self.txt_answer = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_answer.place(x=50, y=160, width=250)

                    lbl_new_pass = Label(self.root2, text="New Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=210)
                    self.txt_new_pass = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_new_pass.place(x=50, y=240, width=250)

                    btn_reset = Button(self.root2, text="Reset Password", font=("times new roman", 15, "bold"), bg="green", fg="white").place(x=90, y=300)

            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)


    def register_window(self):
        # Destroy the current window (which is the login window)
        self.root.destroy()

        # Open the registration window
        from register import Register  # Import Register class from register.py
        root = Tk()
        obj = Register(root)  # Create Register object
        root.mainloop()



        

    def login(self):
        if self.txt_email.get() == "" or self.txt_pass.get() == "":
            messagebox.showerror("Error", "All Fields are Required", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=? AND password=?", (self.txt_email.get(), self.txt_pass.get()))
                row = cur.fetchone()
                con.close()
                if row is None:
                    messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome {self.txt_email.get()}", parent=self.root)
                    self.root.destroy()
                    os.system("python dashboard.py")
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Login_window(root)
    root.mainloop()
