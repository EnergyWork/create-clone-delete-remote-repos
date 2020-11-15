import os
import re
import requests
import tkinter as tk
import tkinter.filedialog as fd
import github
import pygit2

from tkinter import messagebox
from tkinter.ttk import *
from github import Github

class Application:
    """
    Main class of application
    """

    choosed_programm = 0
    github_account = None
    root = None
    
    def __init__(self):
        pass

    def __center_window(self, window):
        w, h, sx, sy = map(int, re.split(r'x|\+', window.winfo_geometry()))
        sw = (window.winfo_rootx() - sx) * 2 + w
        sh = (window.winfo_rooty() - sy) + (window.winfo_rootx() - sx) + h
        sx = (window.winfo_screenwidth() - sw) // 2
        sy = (window.winfo_screenheight() - sh) // 2
        window.wm_geometry('+%d+%d' % (sx, sy))
    
    def __ccrr(self):
        repo_name = self.cbox_repository.get()
        clone = self.bl_clone_it.get()
        repo = self.github_account.get_user().create_repo(name=repo_name, homepage='https://github.com')
        if clone:
            clone_path = self.ent_clone_to.get()
            _ = pygit2.clone_repository(repo.git_url, clone_path)

    def __drr(self):
        repo_name = self.cbox_repository.get()
        repo = self.github_account.get_user().get_repo(repo_name)
        repo.delete()

    def __doit(self):
        if self.github_account == None:
            messagebox.showerror('ERROR', "You're not authenticated!\nMenu > Auth > insert you auth token")
            return
        if not self.bl_clone_it:
            if not (self.ent_clone_to.get() and not self.ent_clone_to.get().isspace()):
                messagebox.showerror('ERROR', "Choose a directory to clone")
                return

        if self.choosed_programm == 0:
            self.__ccrr()
        elif self.choosed_programm == 1:
            self.__drr()
        else:
            self.root.destroy()

    def __get_reposities(self):
        #*"https://api.github.com/users/$GHUSER/repos?access_token=$GITHUB_API_TOKEN"
        #response = requests.get('https://api.github.com/user/repos', headers=headers)
        repos_list = []
        for repo in self.github_account.get_user().get_repos():
            repos_list.append(repo.name)
        self.cbox_repository['values'] = repos_list

    def __clone_it(self):
        if self.bl_clone_it.get():
            self.chkbtn_clone_it['text'] = 'Clone to:'
            self.ent_clone_to['state'] = tk.NORMAL
            self.btn_done['text'] = 'Create and clone repository'
            self.btn_choose_dir.grid(column=1, row=0)
        else:
            self.chkbtn_clone_it['text'] = 'Clone it?'
            self.ent_clone_to['state'] = tk.DISABLED
            self.btn_done['text'] = 'Create repository'
            self.btn_choose_dir.grid_forget()

    def __on_enter(self, e):
        self.btn_choose_dir['foreground'] = '#3a5ae8'
    def __on_leave(self, e):
        self.btn_choose_dir['foreground'] = '#122faa'
    def __choose_dir(self, e):
        directory = fd.askdirectory(title='Выбирете директорию', initialdir='/')
        self.ent_clone_to.delete(0, last=tk.END)
        self.ent_clone_to.insert(0, directory)

    def __auth(self, userlogin, window):
        try:
            self.github_account = Github(login_or_token=userlogin)
            u = self.github_account.get_user().login
            messagebox.showinfo('Authenticated', f'Hi {u}') # BadCredentialsException: 401 {"message": "Bad credentials", "documentation_url": "https://docs.github.com/rest"}
            self.lbl_who['text'] = u
            self.__get_reposities()
            window.destroy()
        except github.BadCredentialsException:
            messagebox.showerror("ERROR", "Authentication error")

    def __auth_window_via_token(self):
        self.choosed_auth_method = 0

        window = tk.Toplevel(self.root)
        window.iconbitmap(self.path_to_label_image)
        window.resizable(0, 0)

        lbl_auth_token = Label(master=window, text='Authentication token')
        lbl_auth_token.grid(column=0, row=0, sticky='w', padx=15, pady=5)

        token = tk.StringVar()
        ent_auth_token = Entry(master=window, textvariable=token, show='*', width=50)
        ent_auth_token.grid(column=0, row=1, sticky='w', padx=15, pady=5)

        btn_done = Button(master=window, text='Auth', command=lambda:self.__auth(token.get(), window))
        btn_done.grid(column=0, row=2, padx=5, pady=5)

        self.__center_window(window)
        #window.transient()
        window.grab_set()
        #window.focus_set()
        window.wait_window()
        #window.mainloop()

    def __set_window_ccrr(self):
        self.choosed_programm = 0
        self.btn_done['text'] = 'Create repository'
        self.layout_h.grid(column=0, row=5, sticky='w', padx=5, pady=5)
        self.ent_clone_to.grid(column=0, row=6, sticky='w', padx=5, pady=5)

    def __set_window_drr(self):
        self.choosed_programm = 1
        self.btn_done['text'] = 'Delete'
        self.layout_h.grid_forget()
        self.ent_clone_to.grid_forget()

    def __main_window(self, parent):
        self.lbl_repos_name = Label(master=parent, text='Repository name')
        self.lbl_repos_name.grid(column=0, row=2, sticky='w', padx=5, pady=5)

        self.cbox_repository = Combobox(master=parent,width=47)
        #self.cbox_repository.bind("<<ComboboxSelected>>", callbackFunc)
        self.cbox_repository.grid(column=0, row=3, sticky='w', padx=5, pady=5)

        self.layout_h = tk.Frame(master=parent)

        self.bl_clone_it = tk.BooleanVar()
        self.chkbtn_clone_it = Checkbutton(master=self.layout_h, text='Clone it?', variable=self.bl_clone_it, onvalue=True, offvalue=False, command=self.__clone_it)
        self.chkbtn_clone_it.grid(column=0, row=0)

        self.btn_choose_dir = Label(master=self.layout_h, text='choose a directory', font="Verdana 8 underline", foreground='blue', cursor='hand2')
        self.btn_choose_dir.bind('<Button-1>', self.__choose_dir)
        self.btn_choose_dir.bind('<Enter>', self.__on_enter)
        self.btn_choose_dir.bind('<Leave>', self.__on_leave)

        self.layout_h.grid(column=0, row=5, sticky='w', padx=5, pady=5)

        self.ent_clone_to= Entry(master=parent, width=50, state=tk.DISABLED)
        self.ent_clone_to.grid(column=0, row=6, sticky='w', padx=5, pady=5)

        self.btn_done = Button(master=parent, text='Create repository', command=self.__doit)
        self.btn_done.grid(column=0, row=7, padx=5, pady=5)

        self.lbl_who = Label(master=parent, text='Not authenticated', foreground='gray')
        self.lbl_who.grid(column=0, row=8, padx=0, pady=0)

    def __menu(self):
        #
        choose_action = tk.Menu(tearoff=0)
        choose_action.add_cascade(label='Create/Clone remote repos', command=self.__set_window_ccrr) 
        choose_action.add_cascade(label='Delete remote repos', command=self.__set_window_drr)
        #
        menu_menu = tk.Menu(tearoff=0)
        menu_menu.add_cascade(label='Auth', command=self.__auth_window_via_token)
        menu_menu.add_cascade(label='Programm', menu=choose_action)
        menu_menu.add_separator()
        menu_menu.add_cascade(label='Exit', command=(lambda: exit(0)))
        #
        main_menu = tk.Menu(tearoff=0)
        main_menu.add_cascade(label='Menu', menu=menu_menu)
        main_menu.add_cascade(label='About') #TODO add command

        return main_menu

    def run(self):
        self.root = tk.Tk()
        self.root.title('Simple repository manipulation')
        self.path_to_label_image = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resourses\\angleicon.ico')
        self.root.iconbitmap(self.path_to_label_image)
        self.root.config(menu=self.__menu())
        #root.geometry('380x270')
        self.root.resizable(0, 0)

        main = Frame(self.root)
        self.__main_window(main)
        main.grid(column=0, row=0, padx=25, pady=20)
        
        self.__center_window(self.root)
        self.root.mainloop()

Application().run()