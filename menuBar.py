from tkinter import Menu, messagebox


class MenuBar:
    def __init__(self, master):
        self.master = master
        menubar = Menu(master)
        master.config(menu=menubar)

        file = Menu(menubar, tearoff=False)
        file.add_command(
            label='Exit',
            command=master.destroy,
        )
        menubar.add_cascade(
            label="File",
            menu=file
        )

        aboutMe = Menu(menubar, tearoff=False)
        aboutMe.add_command(
            label='Help',
            command=self.aboutMe
        )

        menubar.add_cascade(
            label="About Me",
            menu=aboutMe
        )

    def aboutMe(self):
        # show details of my twitter link in message box give button that opens link to twitter
        messagebox.showinfo(
            "About Me",
            "This is a simple image resizer. It was created by @jamesjosephdev. You can find more of my work at https://jamesjoseph.dev"
        )
