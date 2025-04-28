from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # === Background Image ===
        self.bg = ImageTk.PhotoImage(file="images/b2.jpg")
        bg = Label(self.root, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)

        # === Left Image ===
        self.left = ImageTk.PhotoImage(file="images/side.png")
        left = Label(self.root, image=self.left).place(x=80, y=100, width=400, height=500)

        # === Register Frame ===
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=700, height=500)

        title = Label(frame1, text="REGISTER HERE", font=("times new roman", 20, "bold"), bg="white", fg="green").place(x=50, y=30)

        # ================= Row 1
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_answer = StringVar()
        self.var_password = StringVar()
        self.var_cpassword = StringVar()

        f_name = Label(frame1, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, textvariable=self.var_fname, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        l_name = Label(frame1, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=100)
        self.txt_lname = Entry(frame1, textvariable=self.var_lname, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # ================= Row 2
        contact = Label(frame1, text="Contact No.", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=170)
        self.txt_contact = Entry(frame1, textvariable=self.var_contact, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=200, width=250)

        lemail = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=170)
        self.txt_email = Entry(frame1, textvariable=self.var_email, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=200, width=250)

        # ================= Row 3
        question = Label(frame1, text="Security Question", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=240)
        self.cmb_quest = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
        self.cmb_quest.place(x=50, y=270, width=250)
        self.cmb_quest.current(0)

        answer = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=240)
        self.txt_answer = Entry(frame1, textvariable=self.var_answer, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=270, width=250)

        # ================= Row 4
        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=310)
        self.txt_password = Entry(frame1, textvariable=self.var_password, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_password.place(x=50, y=340, width=250)

        cpassword = Label(frame1, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, textvariable=self.var_cpassword, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_cpassword.place(x=370, y=340, width=250)

        # ================= Terms and Conditions
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I Agree to the Terms & Conditions", variable=self.var_chk, onvalue=1, offvalue=0, bg="white", font=("times new roman", 12))
        chk.place(x=50, y=380)

        # ================= Buttons
        self.btn_img = ImageTk.PhotoImage(file="images/register.png")
        btn_register = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data)
        btn_register.place(x=50, y=420)

        btn_login = Button(self.root, text="Sign In", command=self.login_window, font=("times new roman", 20), bd=0, cursor="hand2")
        btn_login.place(x=200, y=500)

    def login_window(self):
        self.root.destroy()
        import login

    def clear(self):
        self.var_fname.set("")
        self.var_lname.set("")
        self.var_contact.set("")
        self.var_email.set("")
        self.var_answer.set("")
        self.var_password.set("")
        self.var_cpassword.set("")
        self.cmb_quest.current(0)
        self.var_chk.set(0)

    def register_data(self):
        if self.var_fname.get() == "" or self.var_contact.get() == "" or self.var_email.get() == "" or self.var_answer.get() == "":
            messagebox.showerror("Error", "All Fields are Required", parent=self.root)
        elif self.var_password.get() != self.var_cpassword.get():
            messagebox.showerror("Error", "Password & Confirm Password should be same", parent=self.root)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please agree to our Terms & Conditions", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=?", (self.var_email.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "User already exists. Please try with another email", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee (fname, lname, contact, email, question, answer, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (self.var_fname.get(),
                                self.var_lname.get(),
                                self.var_contact.get(),
                                self.var_email.get(),
                                self.cmb_quest.get(),
                                self.var_answer.get(),
                                self.var_password.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Register Successful", parent=self.root)
                    self.clear()
                    self.login_window()  # THIS WILL NOW OPEN LOGIN WINDOW
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()
