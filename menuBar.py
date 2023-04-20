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
            "About This Software",
            """An application that resized images for twitch badges and bits.
            For Bugs, issues and suggesstions, you can contact me on

            Twitter: @kayleberries
            Github: https://github.com/MohammadMazin
            """
        )
