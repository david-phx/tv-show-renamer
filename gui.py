import os
import re
import tkinter as tk
import tkinter.font as tkFont
import webbrowser
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext

import config
from settings import Settings
from tmdb import TVShow, TVShows


# TODO: Add validations and warnings everywhere


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Get settings
        self.settings = Settings()

        # Control variables
        self.folder = tk.StringVar()
        self.show_name = tk.StringVar()
        self.show_year = tk.IntVar()
        self.show_tmdb_id = tk.IntVar()
        self.files = list()
        self.renamed_files = dict()

        # Root window settings
        self.title(config.app_title)
        self.iconbitmap(default="assets/icon.ico")
        self.geometry("1280x720")
        self.minsize(800, 600)

        # The only column and the second row are stretchy
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Menu bar
        self.menu_bar = tk.Menu(self)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Folder...", command=self.select_folder)
        self.file_menu.add_command(label="Settings...", command=self.settings_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.destroy)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=None)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.about_window)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.config(menu=self.menu_bar)

        # Folder and show selection frame
        self.folder_frame = ttk.Frame(self, padding=10)
        self.folder_frame.grid(column=0, row=0, sticky="WE")
        self.folder_frame.columnconfigure(1, weight=1)

        self.open_folder_button = ttk.Button(
            self.folder_frame, text="Open Folder", command=self.select_folder, width=18
        )
        self.open_folder_button.grid(column=0, row=0, padx=5, pady=0)

        self.folder_entry = ttk.Entry(
            self.folder_frame,
            textvariable=self.folder,
            font=("Segoe UI", 10),
            state="disabled",
        )
        self.folder_entry.grid(
            columnspan=7, column=1, row=0, padx=5, pady=0, sticky="WE"
        )

        self.show_name_label = ttk.Label(self.folder_frame, text="Show Name")
        self.show_name_label.grid(column=0, row=1, padx=5, pady=5, sticky="E")

        self.show_name_entry = ttk.Entry(
            self.folder_frame, textvariable=self.show_name, font=("Segoe UI", 10)
        )
        self.show_name_entry.grid(column=1, row=1, padx=5, pady=5, sticky="WE")

        self.show_name_lookup = ttk.Button(
            self.folder_frame, text="Look Up", width=15, command=self.lookup_window
        )
        self.show_name_lookup.grid(column=2, row=1, padx=5, pady=5)

        self.show_year_label = ttk.Label(self.folder_frame, text="Year")
        self.show_year_label.grid(column=3, row=1, padx=5, pady=5)

        self.show_year_entry = ttk.Entry(
            self.folder_frame,
            textvariable=self.show_year,
            width=5,
            justify="center",
            font=("Segoe UI", 10),
            state="disabled",
        )
        self.show_year_entry.grid(column=4, row=1, padx=5, pady=5)

        self.show_tmdb_id_label = ttk.Label(self.folder_frame, text="TMDB ID")
        self.show_tmdb_id_label.grid(column=5, row=1, padx=5, pady=5)

        self.show_tmdb_id_entry = ttk.Entry(
            self.folder_frame,
            textvariable=self.show_tmdb_id,
            width=7,
            justify="center",
            font=("Segoe UI", 10),
            state="disabled",
        )
        self.show_tmdb_id_entry.grid(column=6, row=1, padx=5, pady=5)

        self.generate_filenames = ttk.Button(
            self.folder_frame,
            text="Generate Filenames",
            width=25,
            command=self.generate_new_names,
        )
        self.generate_filenames.grid(column=7, row=1, padx=5, pady=5)

        # File panels frame
        self.panels_frame = ttk.Frame(self, padding=(10, 0))
        self.panels_frame.grid(column=0, row=1, sticky="NSWE")
        self.panels_frame.columnconfigure(0, weight=1)
        self.panels_frame.columnconfigure(1, weight=1)
        self.panels_frame.rowconfigure(0, weight=1)

        self.file_names_label_frame = ttk.LabelFrame(self.panels_frame, text="Files")
        self.file_names_label_frame.grid(column=0, row=0, padx=5, pady=0, sticky="NSWE")
        self.file_names_label_frame.columnconfigure(0, weight=1)
        self.file_names_label_frame.rowconfigure(0, weight=1)

        self.file_names = scrolledtext.ScrolledText(
            self.file_names_label_frame, state="disabled"
        )
        self.file_names.grid(padx=10, pady=10, sticky="NSWE")

        self.new_names_label_frame = ttk.LabelFrame(self.panels_frame, text="Rename to")
        self.new_names_label_frame.grid(column=1, row=0, padx=5, pady=0, sticky="NSWE")
        self.new_names_label_frame.columnconfigure(0, weight=1)
        self.new_names_label_frame.rowconfigure(0, weight=1)

        self.new_names = scrolledtext.ScrolledText(
            self.new_names_label_frame, state="disabled"
        )
        self.new_names.grid(padx=10, pady=10, sticky="NSWE")

        # Rename button frame
        self.rename_frame = ttk.Frame(self)
        self.rename_frame.grid(column=0, row=2, sticky="WE")
        self.rename_frame.columnconfigure(0, weight=1)

        self.rename_button = ttk.Button(
            self.rename_frame,
            text="Rename Files",
            command=self.rename_files,
            width=25,
            state="disabled",
        )
        self.rename_button.grid(column=0, row=0, pady=20)

    def settings_window(self):
        # Settings control variable(s)
        tmdb_api_key = tk.StringVar(value=self.settings["TMDB"]["api_key"])

        # Save and close function
        def save_settings():
            self.settings["TMDB"]["api_key"] = tmdb_api_key.get()
            self.settings.save()
            settings.destroy()

        # Toplevel Settings window
        settings = tk.Toplevel(self)
        settings.title("Settings")
        settings.geometry("400x120")
        settings.resizable(False, False)
        x = self.winfo_x() + self.winfo_width() / 2 - 200
        y = self.winfo_y() + self.winfo_height() / 2 - 60
        settings.geometry("+%d+%d" % (x, y))
        settings.transient(self)
        settings.grab_set()
        settings.focus_set()

        # Full width single column
        settings.columnconfigure(0, weight=1)

        # Full width TMDB settings LabelFrame
        tmdb_frame = ttk.LabelFrame(settings, text="The Movie Database", padding=5)
        tmdb_frame.grid(column=0, row=0, padx=10, pady=7, sticky="WE")
        tmdb_frame.columnconfigure(1, weight=1)

        # TMDB API key Label
        tmdb_api_key_label = ttk.Label(tmdb_frame, text="API Key:")
        tmdb_api_key_label.grid(column=0, row=0, padx=5, pady=5)

        # TMDB API key Entry field
        tmdb_api_key_entry = ttk.Entry(
            tmdb_frame, textvariable=tmdb_api_key, font=tkFont.Font(size=10)
        )
        tmdb_api_key_entry.grid(column=1, row=0, padx=5, pady=5, sticky="WE")

        # Full width buttons Frame
        buttons_frame = tk.Frame(settings, padx=10, pady=5)
        buttons_frame.grid(column=0, row=1, sticky="WE")
        buttons_frame.columnconfigure(0, weight=1)

        # OK button
        ok_button = ttk.Button(buttons_frame, text="OK", command=save_settings)
        ok_button.grid(column=0, row=0, padx=10, sticky="E")

        # Cancel button
        cancel_button = ttk.Button(
            buttons_frame, text="Cancel", command=settings.destroy
        )
        cancel_button.grid(column=1, row=0, sticky="E")

    def about_window(self):
        # Toplevel About window
        about = tk.Toplevel(self)
        about.title("About")
        about.geometry("500x500")
        about.resizable(False, False)
        x = self.winfo_x() + self.winfo_width() / 2 - 250
        y = self.winfo_y() + self.winfo_height() / 2 - 250
        about.geometry("+%d+%d" % (x, y))
        about.transient(self)
        about.grab_set()
        about.focus_set()

        # Full width single column
        about.columnconfigure(0, weight=1)

        # App logo
        logo_image = tk.PhotoImage(file="assets/logo.png")
        logo = ttk.Label(about, image=logo_image, padding=20)
        # Keep image reference to prevent it from being garbage collected
        logo.image = logo_image
        logo.grid(column=0, row=0)

        # App name and version label
        app_label = ttk.Label(
            about,
            text=f"{config.app_title} {config.app_version}",
            font=tkFont.Font(size=12, weight="bold"),
            padding=10,
        )
        app_label.grid(column=0, row=1)

        # Author and copyright label
        autor_label = ttk.Label(
            about,
            text=f"© {config.app_year} {config.app_author}",
            font=tkFont.Font(size=10),
        )
        autor_label.grid(column=0, row=2)

        # Link label
        link_label = ttk.Label(
            about,
            text=config.app_link[8:],  # Remove https://
            foreground="blue",
            font=tkFont.Font(size=9, underline=1),
            cursor="hand2",
        )
        link_label.grid(column=0, row=3)
        link_label.bind("<Button-1>", lambda event: webbrowser.open(config.app_link))

        # OK button
        ok_button = ttk.Button(about, text="OK", command=about.destroy)
        ok_button.grid(column=0, row=5, pady=20)

    def lookup_window(self):
        lookup = tk.Toplevel(self)
        lookup.transient(self)
        lookup.title("Look up TV Show on TMDB")
        lookup.geometry("800x600")
        x = self.winfo_x() + self.winfo_width() / 2 - 400
        y = self.winfo_y() + self.winfo_height() / 2 - 300
        lookup.geometry("+%d+%d" % (x, y))
        lookup.grab_set()
        lookup.focus_set()

        lookup.columnconfigure(1, weight=1)
        lookup.rowconfigure(1, weight=1)

        show_name = tk.StringVar()
        show_name.set(self.show_name.get())
        show_list = list()

        def refresh():
            tv_shows = TVShows()
            tv_shows.search(show_name.get())
            shows.delete(0, tk.END)
            show_list.clear()
            show_list.extend(tv_shows.results)

            for index, result in enumerate(show_list):
                shows.insert(
                    index,
                    "{} ({}, {}) - {}...".format(
                        result["name"],
                        result["year"] or "?",
                        result["country"] or "Unknown",
                        result["overview"][0:100],
                    ),
                )

        def select():
            self.show_name.set(show_list[shows.curselection()[0]]["name"])
            self.show_year.set(show_list[shows.curselection()[0]]["year"])
            self.show_tmdb_id.set(show_list[shows.curselection()[0]]["id"])
            lookup.destroy()

        show_name_label = ttk.Label(lookup, text="Show Name")
        show_name_label.grid(column=0, row=0, padx=10, pady=10)

        show_name_entry = ttk.Entry(
            lookup, textvariable=show_name, font=("Segoe UI", 10)
        )
        show_name_entry.grid(column=1, row=0, pady=10, sticky="WE")

        refresh_button = ttk.Button(lookup, text="Refresh", width=15, command=refresh)
        refresh_button.grid(column=2, row=0, padx=10, pady=10)

        shows_label_frame = ttk.LabelFrame(lookup, text="TV Shows")
        shows_label_frame.grid(
            column=0, row=1, columnspan=3, padx=10, pady=0, sticky="NSWE"
        )
        shows_label_frame.columnconfigure(0, weight=1)
        shows_label_frame.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(shows_label_frame)
        scrollbar.grid(column=1, row=0, padx=(0, 10), pady=10, sticky="NS")
        shows = tk.Listbox(
            shows_label_frame,
            activestyle="none",
            selectmode="single",
            font=("Segoe UI", 14),
            yscrollcommand=scrollbar.set,
        )
        shows.grid(column=0, row=0, padx=(10, 0), pady=10, sticky="NSWE")
        scrollbar.config(command=shows.yview)

        select_button = ttk.Button(lookup, text="Select", command=select, width=25)
        select_button.grid(column=0, row=2, columnspan=3, padx=0, pady=10)

        refresh()

    # TODO: Deal with cancel/empty folder value
    def select_folder(self):
        folder = filedialog.askdirectory()
        self.folder.set(folder)
        self.read_folder()

    def read_folder(self):
        folder_path = self.folder.get()
        folder = [
            file
            for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file))
        ]
        file_list = ""
        self.files.clear()

        for file in folder:
            if self.is_a_show_file(file):
                self.files.append(file)
                file_list += file + "\n"

        self.file_names.configure(state="normal")
        self.file_names.delete(1.0, tk.END)
        self.file_names.insert(tk.END, file_list[:-1])  # Skip the last \n
        self.file_names.configure(state="disabled")

        self.show_name.set(
            self.guess_the_show(self.files[0])
        )  # TODO: Validate, can return None

        tv_shows = TVShows()
        tv_shows.search(self.show_name.get())

        self.show_name.set(tv_shows.results[0]["name"])
        self.show_year.set(tv_shows.results[0]["year"])
        self.show_tmdb_id.set(tv_shows.results[0]["id"])

        self.generate_new_names()

    # True if filename contains season and episode numbers
    def is_a_show_file(self, filename):
        if re.search("s\d{1,2}e\d{1,2}", filename, re.IGNORECASE) != None:
            return True
        return False

    # Alphanumeric characters and spaces from start of the filname to s01e01, etc.
    def guess_the_show(self, filename):
        pattern = "^[a-z0-9\s]+?(?=[^a-z0-9]*s\d{1,2}e\d{1,2})"
        match = re.search(pattern, filename, re.IGNORECASE)
        try:
            return match.group()
        except:
            return None

    # TODO: CHANGE !!!
    def generate_new_names(self):
        tv_show = TVShow(self.show_tmdb_id.get())  # TODO: VALIDATE!!!!
        tv_show.get_info()

        renamed_file_list = ""
        self.renamed_files.clear()

        for file in self.files:
            if self.is_a_show_file(file):
                (filename, extension) = os.path.splitext(file)

                (start, end) = re.search("s\d{1,2}", filename, re.IGNORECASE).span()
                season = int(int(filename[int(start) + 1 : int(end)]))

                (start, end) = re.search("e\d{1,2}", filename, re.IGNORECASE).span()
                episode = int(int(filename[int(start) + 1 : int(end)]))

                new_file = tv_show.filename(season, episode) + extension

                self.renamed_files[file] = new_file

                renamed_file_list += new_file + "\n"

        self.new_names.configure(state="normal")
        self.new_names.delete(1.0, tk.END)
        self.new_names.insert(tk.END, renamed_file_list[:-1])  # Skip the last \n
        self.new_names.configure(state="disabled")

        self.rename_button.configure(state="normal")

    def rename_files(self):
        folder_path = self.folder.get()
        folder = os.listdir(folder_path)

        for file in folder:
            if self.is_a_show_file(file) and file in self.renamed_files:
                from_name = os.path.join(folder_path, file)
                to_name = os.path.join(folder_path, self.renamed_files[file])
                os.rename(from_name, to_name)

        self.read_folder()
