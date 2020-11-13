import os
from tkinter import *
from tkinter.ttk import *

class Application:
    """
    Main class of application
    """
    def __init__(self):
        pass

    @classmethod
    def run(self):
        root = Tk()
        root.title('CCDRR')
        path_to_label_image = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resourses\\angleicon.ico')
        root.iconbitmap(path_to_label_image)
        #root.geometry('380x270')

        ccrr = Frame(root)

        lbl_auth_token = Label(master=ccrr, text='Authentication token')
        lbl_auth_token.grid(column=0, row=0, sticky='w', padx=5, pady=5)

        ent_auth_token = Entry(master=ccrr, width=50)
        ent_auth_token.grid(column=0, row=1, sticky='w', padx=5, pady=5)

        lbl_repos_name = Label(master=ccrr, text='Repository name')
        lbl_repos_name.grid(column=0, row=2, sticky='w', padx=5, pady=5)

        cbox_repository = Combobox(master=ccrr,width=47)
        cbox_repository['values'] = [1, 2, 3]
        cbox_repository.grid(column=0, row=3, sticky='w', padx=5, pady=5)

        bl_clone_it = BooleanVar()
        chkbtn_clone_it = Checkbutton(master=ccrr, text='Clone it?', variable=bl_clone_it, onvalue=True, offvalue=False)
        chkbtn_clone_it.grid(column=0, row=4, sticky='w', padx=5, pady=5)

        lbl_clone_to = Label(master=ccrr, text='Clone to')
        lbl_clone_to.grid(column=0, row=5, sticky='w', padx=5, pady=5)

        ent_clone_to= Entry(master=ccrr, width=50)
        ent_clone_to.grid(column=0, row=6, sticky='w', padx=5, pady=5)

        btn_done = Button(master=ccrr, text='do it')
        btn_done.grid(column=0, row=7, padx=5, pady=5)

        ccrr.grid(column=0, row=0, padx=25, pady=20)

        root.mainloop()

Application.run()