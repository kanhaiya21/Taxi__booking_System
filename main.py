import tkinter as tk
from tkinter import *
import datetime
from tkinter.messagebox import showerror, showinfo
from tkinter import messagebox as mb
import sqlite3 as sql
import regex as re
import os
# from PIL import ImageTk, Image
from functools import partial

def admin(frame):
    frame.master.destroy()
    def get_customer_list():
        conn = sql.connect("databases/reservation/reservation.db")
        query = conn.execute("SELECT id,email,pickaddress,picktime,dropaddress,name,phone,active,driver FROM RESERVED")
        temp = []
        for row in query:
            if row[7] == 0:
                temp.append(row)
        conn.close()
        return temp

    def get_available_driver():
        conn = sql.connect("databases/trips/trips.db")
        temp = []
        query = conn.execute("SELECT email,name,active FROM ACTIVE")
        for row in query:
            if row[2] == 0:
                temp.append(row[0])
        conn.close()
        return temp

    def refresh(frame):
        frame.destroy()
        frame = Frame(window, background="#F9F9F9")
        frame.pack(fill=BOTH, expand=YES)
        print(frame)
        body(frame)

    def register_driver(email, id, root):
        print(email.get(), id)
        verify = mb.askokcancel("Verify", "{} will be selected driver for this customer.".format(email.get()))
        if verify:
            conn = sql.connect("databases/reservation/reservation.db")
            conn.execute("UPDATE RESERVED set active=1,driver='{}' where id='{}'".format(email.get(), id))
            conn.commit()
            conn.close()
            conn = sql.connect("databases/trips/trips.db")
            conn.execute("UPDATE ACTIVE set active=1 where email='{}'".format(email.get()))
            conn.commit()
            conn.close()
            refresh(root)

    def card(canvas, datas, x, y, driver_var, root):
        driver_var.trace('w', lambda name, index, mode, email=driver_var: register_driver(email, datas[0], root))
        canvas.create_rectangle(40 + x, 50 + y, 290 + x, 200 + y, fill="#E7E6E6", outline="#E7E6E6")

        email = Label(root, text="Email : " + datas[1], bg="#E7E6E6")
        canvas.create_window(80 + x, 60 + y, window=email, anchor=NW)
        pcka_lbl = Label(root, text="From : " + datas[2], bg="#E7E6E6")
        canvas.create_window(80 + x, 80 + y, window=pcka_lbl, anchor=NW)
        drpa_lbl = Label(root, text="To : " + datas[4], bg="#E7E6E6")
        canvas.create_window(80 + x, 100 + y, window=drpa_lbl, anchor=NW)
        time_lbl = Label(root, text="Date : " + datas[3], bg="#E7E6E6")
        canvas.create_window(150 + x, 100 + y, window=time_lbl, anchor=NW)
        phn_lbl = Label(root, text="Phone : " + datas[6], bg="#E7E6E6")
        canvas.create_window(80 + x, 120 + y, window=phn_lbl, anchor=NW)
        name_lbl = Label(root, text="Name : " + datas[5], bg="#E7E6E6")
        canvas.create_window(80 + x, 140 + y, window=name_lbl, anchor=NW)
        drivers = get_available_driver()
        option_lbl = OptionMenu(root, driver_var, *drivers)
        option_lbl.configure(width=20, border=0)
        canvas.create_window(80 + x, 165 + y, window=option_lbl, anchor=NW)
        return email

    def body(root):
        Label(root, text="ADMIN PANEL", font=("Arial", 20, "bold"), fg="#C35D08").pack(ipady=(10))
        hscroll = Scrollbar(root, orient=VERTICAL)

        hscroll.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(root, bd=0, highlightthickness=0, yscrollcommand=hscroll.set, bg="#F9F9F9",
                        scrollregion=(0, 0, 500, 500))
        canvas.pack(fill=BOTH, expand=YES)

        customers = get_customer_list()
        x, y, count = 0, 0, 1

        for datas in customers:

            card(canvas, datas, x, y, StringVar(), root)
            x += 260
            if count % 2 == 0:
                x = 0
                y += 160

            count += 1

    window = tk.Tk()
    w = 600
    h = 600

    window.geometry(str(w) + 'x' + str(h))
    window.wm_resizable(False, False)
    frame = Frame(window)
    frame.pack(fill=BOTH, expand=YES)

    body(frame)

    window.mainloop()


###########################################################################


def show_frame(frame):

    if  (str(frame) == '.!frame8' ):
        frame.destroy()
        frame = Frame(root, background="#F9F9F9")
        frame.grid(row=0, column=0, sticky="nsew")
        print(frame)
        customer_home_page(frame)
    if (str(frame) == '.!frame9'):
        frame.destroy()
        frame = Frame(root, background="#F9F9F9")
        frame.grid(row=0, column=0, sticky="nsew")
        print(frame)
        driver_home_page(frame)

    if str(frame) == '.!frame' or str(frame) == '.!frame2' or str(frame) == '.!frame3' or str(
            frame) == '.!frame4' or str(frame) == '.!frame6':
        w = 600
        h = 440
    else:
        w = 600
        h = 600
    root.geometry("{}x{}".format(w, h))
    print(frame)

    frame.tkraise()


# def img_src(src, imgsize):
#     openimg = Image.open(src)
#     w, h = openimg.size
#     if sum(imgsize) > 1:
#         openimg = openimg.resize(imgsize, Image.CUBIC)
#     timg = ImageTk.PhotoImage(openimg)
#     return timg
#
#
# class ImageTk:
#     pass


# class ImageTk:
    pass


def create_rectangle(canvas,x1, y1, x2, y2, **kwargs):

    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        # image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        # images.append(ImageTk.PhotoImage(image))
        # canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


def img_src(param, param1):
    pass


def welcome_page(frame):
    canvas = Canvas(frame)

    canvas.pack(fill=BOTH, expand=YES)
    cvimg = img_src("images/bg/bgg.jpg",(600,600))
    canvas.image = cvimg
    im=canvas.create_image(0,0,image =cvimg ,anchor = NW )
    driverbtn = tk.Button(frame, text="Join as Worker", fg="#4B4B4B", background="#53F1A4", border=0,
                          command=lambda: show_frame(driver_loginsignup))
    driverbtn.configure(width=30, height=3)
    customerbtn = tk.Button(frame, text="Join as Customer", fg="white", background="#53A6F1", border=0,
                            command=lambda: show_frame(customer_loginsignup))
    customerbtn.configure(width=30, height=3)
    adminbtn = tk.Button(frame, text="Admin", fg="white", background="#D3AB6B", border=0,
                            command=lambda: admin(frame))
    adminbtn.configure(width=30, height=3)

    create_rectangle(canvas,150,110,450,360,fill="black",width=0,stipple="gray50")
    canvas.create_window(300, 175, window=driverbtn)
    canvas.create_window(300, 240, window=customerbtn)
    canvas.create_window(300, 305, window=adminbtn)



def title_img(frame):
    tsrc = img_src("images/title.png", (350, 37))
    title = tk.Label(frame, image=tsrc)
    title.image = tsrc
    title.pack()


def check_email(email):
    regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def pw_check(pw):
    if len(pw) > 5:
        return True
    else:
        return False


def check_empty(data):
    print(data)
    for d in data:
        if len(d) <= 0:
            return False

    return True

def add_id_to_temp(id):
    file = open('temp/temp.txt','w')
    file.write(id)
    file.close()
def get_id_from_temp():
    file = open('temp/temp.txt','r')
    id=file.readline()
    file.close()
    return id

def login(page):
    global temp_login
    raw_email = email_var.get()
    raw_pw = pw_var.get()
    e_chck = check_email(raw_email)
    p_chck = pw_check(raw_pw)
    if not p_chck:
        showerror("Invalid", "Password length must be greater than 8.")
        return None
    if not e_chck:
        showerror("Invalid", "Email not valid!")
        return None
    if page == 1:
        print("cusomer")
        conn = sql.connect("databases/customer/customer_login.db")
    elif page == 2:
        print("driver")
        conn = sql.connect("databases/driver/driver_login.db")
    tbl_exist = table_check(conn, "LOGIN")

    if tbl_exist:
        cursor = conn.execute("SELECT email,password FROM LOGIN")
        for row in cursor:

            if raw_email == row[0] and raw_pw == row[1]:
                conn.close()
                print("Login successful")
                temp_login = raw_email
                add_id_to_temp(raw_email)
                if page==1:

                    show_frame(customer_home_frame)
                elif page==2:
                    show_frame(driver_home)

                return True

        conn.close()
        print("Error credentials")
        return False
    else:
        conn.close()
        showerror("Empty", "Empty database!!")


def filter_signup(email, data):
    conn = sql.connect("databases/{}/{}".format(data, data + '_login.db'))
    chck = table_check(conn, "LOGIN")
    cursor = conn.execute("SELECT email,password FROM LOGIN")
    for row in cursor:
        print(row[0])
        if row[0] == email:
            conn.close()
            return True
    conn.close()
    return False

def check_dublicate(email,table,data):
    conn = sql.connect("databases/{}/{}".format(data, data+'.db' ))
    chck = table_check(conn, "{}".format(table))
    print(chck)
    if chck:
        cursor = conn.execute("SELECT email FROM {}".format(table))
        for row in cursor:
            print(row[0])
            if row[0] == email:
                conn.close()
                return True
        conn.close()
        return False
    else:
        return None


def table_check(conn, tablename):
    chck = conn.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}'".format(name=tablename))
    if chck.fetchone()[0] == 1:
        return True
    else:
        return False


def signup(page):
    raw_email = email_var.get()
    raw_pw = pw_var.get()
    raw_address = address_var.get()
    raw_phone = phone_var.get()
    raw_acn = acn_var.get()
    raw_cvv = cvv_var.get()
    e_chck = check_email(raw_email)
    p_chck = pw_check(raw_pw)
    empty_chck = check_empty([raw_address, raw_phone, raw_acn, raw_cvv])
    print(empty_chck)
    if not empty_chck:
        showerror("Empty", "Incomplete form!")
        return None
    if page == 1:
        data = "customer"
    elif page == 2:
        data = "driver"
    if not p_chck:
        showerror("Invalid", "Password length must be greater than 8.")
        return None
    if not e_chck:
        showerror("Invalid", "Email not valid!")
        return None
    conn = sql.connect("databases/{}/{}".format(data, data + '_login.db'))
    newconn = sql.connect("databases/trips/trips.db")


    if page == 2:
        chck_tbl = table_check(newconn, "ACTIVE")
        print(chck_tbl, "olo")
        if not chck_tbl:
            print("hello")
            newconn.execute("CREATE TABLE ACTIVE (email TEXT NOT NULL,name TEXT NOT NULL, active int NOT NULL )")

    tbl_exist = table_check(conn, "LOGIN")
    if not tbl_exist:
        if page == 1:
            conn.execute(
                "CREATE TABLE LOGIN (email TEXT NOT NULL, password TEXT NOT NULL,address TEXT NOT NULL,phone TEXT NOT NULL,acn TEXT NOT NULL,cvv TEXT NOT NULL)")
        elif page == 2:

            conn.execute(
                "CREATE TABLE LOGIN (email TEXT NOT NULL, password TEXT NOT NULL,address TEXT NOT NULL,phone TEXT NOT NULL,name TEXT NOT NULL,license TEXT NOT NULL)")
    if filter_signup(raw_email, data):
        print("found")
        showerror("Invalid", "Email already used!")
        return None
    if page == 1:
        rslt = conn.execute(
            "INSERT INTO LOGIN(email,password,address,phone,acn,cvv) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                raw_email, raw_pw, raw_address, raw_phone, raw_acn, raw_cvv))
    elif page == 2:
        newconn.execute("INSERT INTO ACTIVE(email,name,active) VALUES ('{}','{}','{}')".format(raw_email, raw_acn, 0))
        rslt = conn.execute(
            "INSERT INTO LOGIN(email,password,address,phone,name,license) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                raw_email, raw_pw, raw_address, raw_phone, raw_acn, raw_cvv))

    print(rslt)
    newconn.commit()
    newconn.close()
    conn.commit()
    conn.close()
    if page==1:

        show_frame(customer_loginsignup)
    else:
        show_frame(driver_loginsignup)


def customer_login(frame):
    frame = Frame(frame, background="#F9F9F9")
    frame.grid(row=10, column=0, sticky="nsew", padx=175, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Customer Login", fg="#4D4D76", bg="#F9F9F9", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email:", bg="#F9F9F9")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Arial", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="#F9F9F9")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Arial", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))
    submit = Button(frame, text="Login", bg="#53A6F1", border="0", command=lambda: login(1))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="#53F1A4", fg="white", border="0", command=lambda: show_frame(welcome_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))

def customer_signup(frame):
    frame = Frame(frame, background="#F9F9F9")
    frame.grid(row=10, column=0, sticky="nsew", padx=130, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Customer Signup", fg="#4D4D76", bg="#F9F9F9", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email:", bg="#F9F9F9")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Arial", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="#F9F9F9")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Arial", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))

    address_label = Label(frame, text="Address:", bg="#F9F9F9")
    address_label.pack(padx=(0, 175), pady=(5, 0))
    address = Entry(frame, font=("Arial", 14, "normal"), textvariable=address_var)
    address.pack(ipady=(4))
    phone_label = Label(frame, text="Phone:", bg="#F9F9F9")
    phone_label.pack(padx=(0, 185), pady=(5, 0))
    phone = Entry(frame, font=("Arial", 14, "normal"), textvariable=phone_var)
    phone.pack(ipady=(4))

    credit_label_frame = tk.Frame(frame, background="#F9F9F9")
    credit_label_frame.pack()
    credit_frame = tk.Frame(frame, background="#F9F9F9")
    credit_frame.pack()

    credit_label = Label(credit_label_frame, text="A.C.N:", bg="#F9F9F9")
    credit_label.pack(padx=(0, 65), side=LEFT)
    credit_label = Entry(credit_frame, font=("Arial", 7, "normal"), textvariable=acn_var)
    credit_label.pack(ipady=(4), padx=(62, 0), side=LEFT)
    cvv_label = Label(credit_label_frame, text="CVV:", bg="#F9F9F9")
    cvv_label.pack(padx=(10, 65), pady=(0, 0), side=LEFT)
    cvv_label = Entry(credit_frame, font=("Arial", 7, "normal"), textvariable=cvv_var)
    cvv_label.pack(ipady=(4), padx=(10, 62), side=LEFT)

    submit = Button(frame, text="Signup", bg="#53F1A4", border="0", command=lambda: signup(1))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="#53A6F1", fg="white", border="0", command=lambda: show_frame(welcome_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))


def driver_login(frame):
    frame = Frame(frame, background="#F9F9F9")
    frame.grid(row=10, column=0, sticky="nsew", padx=175, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Driver Login", fg="#4D4D76", bg="#F9F9F9", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email:", bg="#F9F9F9")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Arial", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="#F9F9F9")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Arial", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))
    submit = Button(frame, text="Login", bg="#53A6F1", border="0", command=lambda: login(2))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="#53F1A4", fg="white", border="0", command=lambda: show_frame(welcome_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))


def driver_signup(frame):
    frame = Frame(frame, background="#F9F9F9")
    frame.grid(row=10, column=0, sticky="nsew", padx=130, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Driver Signup", fg="#4D4D76", bg="#F9F9F9", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email:", bg="#F9F9F9")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Arial", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="#F9F9F9")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Arial", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))

    address_label = Label(frame, text="Address:", bg="#F9F9F9")
    address_label.pack(padx=(0, 175), pady=(5, 0))
    address = Entry(frame, font=("Arial", 14, "normal"), textvariable=address_var)
    address.pack(ipady=(4))
    phone_label = Label(frame, text="Phone:", bg="#F9F9F9")
    phone_label.pack(padx=(0, 185), pady=(5, 0))
    phone = Entry(frame, font=("Arial", 14, "normal"), textvariable=phone_var)
    phone.pack(ipady=(4))
    credit_label_frame = tk.Frame(frame, background="#F9F9F9")
    credit_label_frame.pack()
    credit_frame = tk.Frame(frame, background="#F9F9F9")
    credit_frame.pack()

    name_label = Label(credit_label_frame, text="Full name:", bg="#F9F9F9")
    name_label.pack(padx=(45, 55), side=LEFT)
    name = Entry(credit_frame, font=("Arial", 7, "normal"), textvariable=acn_var)
    name.pack(ipady=(4), padx=(62, 0), side=LEFT)
    cvv_label = Label(credit_label_frame, text="License plate:", bg="#F9F9F9")
    cvv_label.pack(padx=(0, 80), pady=(0, 0), side=LEFT)
    lic = Entry(credit_frame, font=("Arial", 7, "normal"), textvariable=cvv_var)
    lic.pack(ipady=(4), padx=(10, 62), side=LEFT)

    submit = Button(frame, text="Signup", bg="#53F1A4", border="0", command=lambda: signup(2))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="#53A6F1", fg="white", border="0", command=lambda: show_frame(welcome_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))


def customer_main(frame):
    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=YES)
    cvimg = img_src("images/bg/bg2.jpg", (600, 600))
    canvas.image = cvimg
    im = canvas.create_image(0, 0, image=cvimg, anchor=NW)
    driverbtn = tk.Button(frame, text="Login as Customer", fg="#4B4B4B", background="#53F1A4", border=0,
                          command=lambda: show_frame(customer_login_frame))
    driverbtn.configure(width=30, height=3)
    driverbtn.pack(pady=(150, 10))
    customerbtn = tk.Button(frame, text="Signup as Customer", fg="white", background="#53A6F1", border=0,
                            command=lambda: show_frame(customer_signup_frame))
    customerbtn.configure(width=30, height=3)
    create_rectangle(canvas, 150, 110, 450, 300, fill="white",alpha=0.3, width=0)
    canvas.create_window(300, 175, window=driverbtn)
    canvas.create_window(300, 240, window=customerbtn)




def driver_main(frame):
    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=YES)
    cvimg = img_src("images/bg/bg4.jpg", (600, 600))
    canvas.image = cvimg
    im = canvas.create_image(0, 0, image=cvimg, anchor=NW)
    driverbtn = tk.Button(frame, text="Login as Worker", fg="#4B4B4B", background="#53F1A4", border=0,
                          command=lambda: show_frame(driver_login_frame))
    driverbtn.configure(width=30, height=3)
    customerbtn = tk.Button(frame, text="Signup as Worker", fg="white", background="#53A6F1", border=0,
                            command=lambda: show_frame(driver_signup_frame))
    customerbtn.configure(width=30, height=3)
    create_rectangle(canvas, 150, 110, 450, 300, fill="white", alpha=0.4, width=0)
    canvas.create_window(300, 175, window=driverbtn)
    canvas.create_window(300, 240, window=customerbtn)


def reserve_taxi():
    temp_login = get_id_from_temp()
    print(temp_login)
    chck = check_empty([pck_adrs.get(), pck_time.get(), drp_adrs.get(), name_var.get(), phone_var.get()])
    if not chck:
        showerror("Empty", "Empty Field!!")
        return None
    else:
        conn = sql.connect("databases/reservation/reservation.db")
        chck_table = table_check(conn, "RESERVED")
        if not chck_table:
            query = conn.execute(
                "CREATE TABLE RESERVED (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT NOT NULL, pickaddress TEXT NOT NULL,picktime TEXT NOT NULL,dropaddress TEXT NOT NULL,name TEXT NOT NULL,phone TEXT NOT NULL,active int NOT NULL,driver TEXT NOT NULL)")

        query = conn.execute(
            "INSERT INTO RESERVED(email,pickaddress,picktime,dropaddress,name,phone,active,driver) VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(
               temp_login , pck_adrs.get(), pck_time.get(), drp_adrs.get(), name_var.get(),
                phone_var.get(),0,"Pending"))
        conn.commit()
        conn.close()
        showinfo("Successful", "Taxi reservation successfull!!")
        show_frame(customer_home_frame)

def logout():
    add_id_to_temp("")
    show_frame(welcome_frame)

def customer_home_page(frame):
    top_frame = Frame(frame, bg="#242424")
    top_frame.pack()

    body_frame = Frame(frame, bg="#F9F9F9")
    body_frame.pack(fill=BOTH, expand=YES, pady=(30, 10))

    bottom_frame = Frame(frame, bg="#F5F5F5")
    bottom_frame.pack(side=BOTTOM, fill=BOTH, ipady=(20))

    home_title = Label(top_frame, text="Customer Home", bg="#242424", fg="white", font=("Arial", 15, "bold"))
    home_title.configure(height=3)
    home_title.pack(padx=(222, 0), side=LEFT)
    # logoutimg = img_src("images/logout.png", (40, 40))
    # logout_ = Button(top_frame, image=logoutimg, bg="#242424", border=0, command=logout)
    # logout_.image = logoutimg
    # logout_.pack(padx=(178, 0), side=RIGHT)
    # c_email= Label(frame,text=temp_login,font=("Arial",15))
    # c_email.pack()

    already_booked = check_dublicate(get_id_from_temp(),"RESERVED","reservation")
    print("chck",already_booked)
    if  not already_booked:
        p_a_label = Label(body_frame, text="Pick-up Address:", bg="#F9F9F9")
        p_a_label.pack(padx=(0, 174))
        pick_address = Entry(body_frame, textvariable=pck_adrs)
        pick_address.pack(ipady=(6), ipadx=(70))

        p_t_label = Label(body_frame, text="Pick-up Date:", bg="#F9F9F9")
        p_t_label.pack(padx=(0, 190), pady=(2, 0))
        pick_time = Entry(body_frame, textvariable=pck_time)
        pick_time.pack(ipady=(6), ipadx=(70))

        d_a_label = Label(body_frame, text="Drop-off Address:", bg="#F9F9F9")
        d_a_label.pack(padx=(0, 167), pady=(2, 0))
        drop_address = Entry(body_frame, textvariable=drp_adrs)
        drop_address.pack(ipady=(6), ipadx=(70))

        name_label = Label(body_frame, text="Full name:", bg="#F9F9F9")
        name_label.pack(padx=(0, 207), pady=(2, 0))
        name_ = Entry(body_frame, textvariable=name_var)
        name_.pack(ipady=(6), ipadx=(70))

        phone_label = Label(body_frame, text="Contact:", bg="#F9F9F9")
        phone_label.pack(padx=(0, 217), pady=(2, 0))
        phone = Entry(body_frame, textvariable=phone_var)
        phone.pack(ipady=(6), ipadx=(70))

        find_taxi_btn = tk.Button(body_frame, text="Get a Taxi", bg="#B23E65", fg="white", border=0,
                                  command=reserve_taxi)
        find_taxi_btn.configure(height=2, width=37)
        find_taxi_btn.pack(pady=(50, 0))




    else:
        customer_recent_page(body_frame)
    copyright = Label(bottom_frame, bg="#F5F5F5", fg="#C1C1C1",
                      text="Copyright @ {}".format(datetime.date.today().year))
    copyright.pack(side=LEFT, padx=(255, 0))


def get_your_trip(conn, userid):
    query = conn.execute("SELECT rowid,email,pickaddress,picktime,dropaddress,name,phone,active,driver FROM RESERVED")
    temp=[]
    for row in query:
        print(row)
        if row[1] == userid:
            temp.append(row)
    return temp


def list_to_str(data):
    temp=""
    for i in range(1,len(data)):
        temp+=data[i]
        temp+="               "
    return temp.rstrip()

def delete_customer_reservation(id,conn,frame,taxi_list):
    print(taxi_list,"chck list")
    row_id= taxi_list[id][0]
    if taxi_list[id][7]==1:
        newconn = sql.connect("databases/trips/trips.db")
        newconn.execute("UPDATE ACTIVE set active=0 WHERE email='{}'".format(taxi_list[8]))
        newconn.commit()
        newconn.close()
    conn.execute("DELETE FROM RESERVED WHERE id={}".format(row_id))
    conn.commit()
    conn.close()
    show_frame(customer_home_frame)



def complete_ride(data):
    conn = sql.connect("databases/reservation/reservation.db")
    row_id = data[0]
    if data[7] == 1:
        newconn = sql.connect("databases/trips/trips.db")
        newconn.execute("UPDATE ACTIVE set active=0 WHERE email='{}'".format(data[8]))
        newconn.commit()
        newconn.close()
    conn.execute("DELETE FROM RESERVED WHERE id={}".format(row_id))
    conn.commit()
    conn.close()
    show_frame(driver_home)

def customer_recent_page(frame):
    title_frame = Frame(frame,bg="#F9F9F9")
    title_frame.pack(pady=(150,0))

    body = tk.Frame(frame, bg="#F9F9F9")
    body.pack()

    conn = sql.connect("databases/reservation/reservation.db")
    chck_table = table_check(conn,"RESERVED")
    if chck_table:
        taxi_list = get_your_trip(conn, get_id_from_temp())
        print("tc",taxi_list)
        if len(taxi_list) ==0:
            txt= "No Reservation!"
            error = Label(body, text=txt, fg="#AFADAD", background="#F5F5F5", font=("Arial", 20, "bold"))
            error.configure(height=3, width=20)
            error.pack(pady=(200, 0))
        else:
            id_label = Label(title_frame, text="Id", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
            id_label.configure(width=7, height=2)
            id_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            pckadrs_label = Label(title_frame, text="Pick-Address", font=("arial", 9, "bold"), fg="#454545",
                                  bg="#E6E6E6")
            pckadrs_label.configure(width=12, height=2)
            pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            pcktme_label = Label(title_frame, text="Pick-Date", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
            pcktme_label.configure(width=10, height=2)
            pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            drpadrs_label = Label(title_frame, text="Drop-Address", font=("arial", 9, "bold"), fg="#454545",
                                  bg="#E6E6E6")
            drpadrs_label.configure(width=12, height=2)
            drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            name_label = Label(title_frame, text="Name", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
            name_label.configure(width=12, height=2)
            name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            phone_label = Label(title_frame, text="Phone", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
            phone_label.configure(width=12, height=2)
            phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))

            count = 1
            del_btn_list=[]
            for data in taxi_list:
                id=IntVar()
                id.set(data[0])
                body = tk.Frame(frame, bg="#F9F9F9")
                body.pack()
                id_label = Label(body, text=str(count))
                id_label.configure(width=7, height=2)
                id_label.pack(side=LEFT, padx=(20, 1), pady=(0, 3))
                pckadrs_label = Label(body, text=data[2])
                pckadrs_label.configure(width=12, height=2)
                pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                pcktme_label = Label(body, text=data[3])
                pcktme_label.configure(width=10, height=2)
                pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                drpadrs_label = Label(body, text=data[4])
                drpadrs_label.configure(width=12, height=2)
                drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                name_label = Label(body, text=data[5])
                name_label.configure(width=12, height=2)
                name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                phone_label = Label(body, text=data[6])
                phone_label.configure(width=12, height=2)
                phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))

                delimg = img_src("images/delete.png",(20,20))
                delete = Button(body,image=delimg,border=0,bg="#F9F9F9",textvariable =id ,command=partial(delete_customer_reservation,taxi_list.index(data),conn,frame,taxi_list))
                delete.image=delimg
                delete.pack(side=LEFT)
                del_btn_list.append(delete)
                count += 1
    else:
        conn.close()
    status_frame=Frame(frame,bg="#F9F9F9")
    status_frame.pack(fill=BOTH)
    dr_label=Label(status_frame,text="Driver email: ",font=("Arial",10,"bold"),bg="#F9F9F9")
    dr_label.pack(side=LEFT,pady=(10,0),padx=(50,0))
    driver=Label(status_frame,text=data[8])
    driver.pack(side=LEFT,pady=(10,0))



def get_driver_trip():
    conn = sql.connect("databases/reservation/reservation.db")
    chck_tbl = table_check(conn,"RESERVED")
    temp = []
    if chck_tbl:
        query = conn.execute(
            "SELECT rowid,email,pickaddress,picktime,dropaddress,name,phone,active,driver FROM RESERVED")

        for row in query:
            print(row[1])
            if row[8] == get_id_from_temp():
                temp.append(row)

    return temp


def driver_home_page(frame):
    top_frame = Frame(frame, bg="#242424")
    top_frame.pack()

    body_frame = Frame(frame, bg="#F9F9F9")
    body_frame.pack(pady=(10, 10))

    title_frame = Frame(frame, bg="#F9F9F9")
    title_frame.pack(pady=(10, 0))

    body = tk.Frame(frame, bg="#F9F9F9")
    body.pack()

    bottom_frame = Frame(frame, bg="#F5F5F5")
    bottom_frame.pack(side=BOTTOM, fill=BOTH, ipady=(20))



    home_title = Label(top_frame, text="Driver Home", bg="#242424", fg="white", font=("Arial", 15, "bold"))
    home_title.configure(height=3,width=13)
    home_title.pack(padx=(222, 0), side=LEFT)
    logoutimg = img_src("images/logout.png", (40, 40))
    logout_ = Button(top_frame, image=logoutimg, bg="#242424", border=0, command=logout)
    logout_.image = logoutimg
    logout_.pack(padx=(178, 0), side=RIGHT)


    title=Label(body_frame,text="My Trips",bg="#F5F5F5", font=("Arial", 10, "bold"))
    title.pack()


    id_label = Label(title_frame, text="Id", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
    id_label.configure(width=7, height=2)
    id_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    pckadrs_label = Label(title_frame, text="Pick-Address", font=("arial", 9, "bold"), fg="#454545",
                          bg="#E6E6E6")
    pckadrs_label.configure(width=12, height=2)
    pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    pcktme_label = Label(title_frame, text="Pick-Date", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
    pcktme_label.configure(width=10, height=2)
    pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    drpadrs_label = Label(title_frame, text="Drop-Address", font=("arial", 9, "bold"), fg="#454545",
                          bg="#E6E6E6")
    drpadrs_label.configure(width=12, height=2)
    drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    name_label = Label(title_frame, text="Name", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
    name_label.configure(width=12, height=2)
    name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    phone_label = Label(title_frame, text="Phone", font=("arial", 9, "bold"), fg="#454545", bg="#E6E6E6")
    phone_label.configure(width=12, height=2)
    phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))



    if len(get_driver_trip())>0:
        data = get_driver_trip()[0]

        id = IntVar()
        id.set(data[0])
        body = tk.Frame(frame, bg="#F9F9F9")
        body.pack()
        id_label = Label(body, text=str(1))
        id_label.configure(width=7, height=2)
        id_label.pack(side=LEFT, padx=(20, 1), pady=(0, 3))
        pckadrs_label = Label(body, text=data[2])
        pckadrs_label.configure(width=12, height=2)
        pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        pcktme_label = Label(body, text=data[3])
        pcktme_label.configure(width=10, height=2)
        pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        drpadrs_label = Label(body, text=data[4])
        drpadrs_label.configure(width=12, height=2)
        drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        name_label = Label(body, text=data[5])
        name_label.configure(width=12, height=2)
        name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        phone_label = Label(body, text=data[6])
        phone_label.configure(width=12, height=2)
        phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        conn=sql.connect("databases/trips/trips.db")
        complete_img = img_src("images/check.png", (20, 20))
        complete_lbl = Button(body, image=complete_img, border=0, bg="#F9F9F9",command = lambda : complete_ride(data))
        complete_lbl.image = complete_img
        complete_lbl.pack(side=LEFT)
    else:
        Label(body,text="No Trips!!",font=("Arial",15)).pack(pady=(100,0),ipadx=(50),ipady=(10))


    copyright = Label(bottom_frame, bg="#F5F5F5", fg="#C1C1C1",
                      text="Copyright @ {}".format(datetime.date.today().year))
    copyright.pack(side=LEFT, padx=(250, 0))

root = tk.Tk()
root.wm_title("Trans Fast")
w = 600
h = 440
images = []
temp_login = "sarthak@gmail.com"
email_var = StringVar()
pw_var = StringVar()
address_var = StringVar()
phone_var = StringVar()
acn_var = StringVar()
cvv_var = StringVar()
am_pm = StringVar()
am_pm.set("AM")
pck_adrs = StringVar()
pck_time = StringVar()
drp_adrs = StringVar()
name_var = StringVar()

root.geometry(str(w) + 'x' + str(h))
root.wm_resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

welcome_frame = tk.Frame(root,background="#F9F9F9")
customer_loginsignup = tk.Frame(root, background="#F9F9F9")
driver_loginsignup = tk.Frame(root, background="#F9F9F9")
customer_login_frame = tk.Frame(root)
customer_signup_frame = tk.Frame(root)
driver_login_frame = tk.Frame(root)
driver_signup_frame = tk.Frame(root)
customer_home_frame = tk.Frame(root, background="#F9F9F9")
driver_home = tk.Frame(root, background="#F9F9F9")
print(driver_home)
for frame in (welcome_frame, customer_loginsignup, driver_loginsignup, customer_login_frame, customer_signup_frame,
              driver_login_frame, driver_signup_frame, customer_home_frame,driver_home):
    frame.grid(row=0, column=0, sticky="nsew")
welcome_page(welcome_frame)
customer_main(customer_loginsignup)
driver_main(driver_loginsignup)
customer_login(customer_login_frame)
customer_signup(customer_signup_frame)
driver_login(driver_login_frame)
driver_signup(driver_signup_frame)
customer_home_page(customer_home_frame)

driver_home_page(driver_home)


show_frame(welcome_frame)

root.mainloop()
