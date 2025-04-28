from tkinter import *
from PIL import Image, ImageTk

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Student Result Management System")
        self.root.geometry("500x500+500+200")
        self.root.config(bg="white")

        # Logo
        self.logo = ImageTk.PhotoImage(file="images/logo_p.png")
        Label(self.root, image=self.logo, bg="white").place(x=200, y=20)

        # Title
        title = Label(self.root, text="Login to your account", font=("goudy old style", 20, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=100, relwidth=1, height=50)

        # Username
        lbl_username = Label(self.root, text="Username", font=("goudy old style", 15), bg="white", fg="#0b5377")
        lbl_username.place(x=50, y=180)
        txt_username = Entry(self.root, font=("goudy old style", 15), bg="#e9ecef")
        txt_username.place(x=50, y=210, width=400)

        # Password
        lbl_password = Label(self.root, text="Password", font=("goudy old style", 15), bg="white", fg="#0b5377")
        lbl_password.place(x=50, y=250)
        txt_password = Entry(self.root, font=("goudy old style", 15), bg="#e9ecef", show="*")
        txt_password.place(x=50, y=280, width=400)

        # Buttons
        btn_login = Button(self.root, text="Login", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2")
        btn_login.place(x=150, y=350, width=200, height=40)

        footer = Label(self.root, text="Forgot Password? Contact admin", font=("goudy old style", 12), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

if __name__ == "__main__":
    root = Tk()
    Login(root)
    root.mainloop()
