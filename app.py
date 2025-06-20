import tkinter
from tkinter import ttk

def add_book(): # Create
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    isbn = entry_isbn.get()
    publisher = entry_publisher.get()
    publish_year = entry_publish_year.get()

def search_book(): # Read
    pass

def edit_book(): # Update
    pass

def delete_book(): # Delete
    pass



app_interface = tkinter.Tk()
app_interface.title("Book Catalog")
app_interface.config(bg="#f0f0f0")

frame_form = tkinter.Frame(app_interface, padx=20, pady=20)
frame_form.pack(padx=10, pady=10, fill="x")

label_isbn = tkinter.Label(frame_form, text="ISBN:")
entry_isbn = tkinter.Entry(frame_form, width=20)

label_title = tkinter.Label(frame_form, text="Title:")
entry_title = tkinter.Entry(frame_form, width=40)

label_author = tkinter.Label(frame_form, text="Author:")
entry_author = tkinter.Entry(frame_form, width=40)

label_genre = tkinter.Label(frame_form, text="Genre:")
entry_genre = tkinter.Entry(frame_form, width=20)

label_publisher = tkinter.Label(frame_form, text="Publisher:")
entry_publisher = tkinter.Entry(frame_form, width=40)

label_publish_year = tkinter.Label(frame_form, text="Publish Year:")
entry_publish_year = tkinter.Entry(frame_form, width=20)

label_isbn.grid(row=0, column=0, sticky="w", pady=2)
entry_isbn.grid(row=0, column=1, pady=2, padx=5)

label_title.grid(row=1, column=0, sticky="w", pady=2)
entry_title.grid(row=1, column=1, pady=2, padx=5)

label_author.grid(row=2, column=0, sticky="w", pady=2)
entry_author.grid(row=2, column=1, pady=2, padx=5)

label_genre.grid(row=3, column=0, sticky="w", pady=2)
entry_genre.grid(row=3, column=1, pady=2, padx=5)

label_publisher.grid(row=4, column=0, sticky="w", pady=2)
entry_publisher.grid(row=4, column=1, pady=2, padx=5)

label_publish_year.grid(row=5, column=0, sticky="w", pady=2)
entry_publish_year.grid(row=5, column=1, pady=2, padx=5)

frame_buttons = tkinter.Frame(app_interface, padx=10, pady=10)
frame_buttons.pack(fill="x")

add_button = tkinter.Button(frame_buttons, text="Add Book", command=add_book)
search_button = tkinter.Button(frame_buttons, text="Search Book", command=search_book)
edit_button = tkinter.Button(frame_buttons, text="Edit Book", command=edit_book)
delete_button = tkinter.Button(frame_buttons, text="Delete Book", command=delete_book)

add_button.pack(side="left", padx=5)
search_button.pack(side="left", padx=5)
edit_button.pack(side="left", padx=5)
delete_button.pack(side="left", padx=5)

frame_list = tkinter.Frame(app_interface, padx=10, pady=10)
frame_list.pack(fill="both", expand=True)
columns = ("ISBN", "Title", "Author", "Genre", "Publisher", "Publish Year")
book_list = ttk.Treeview(app_interface, columns=columns, show="headings")

book_list.heading("ISBN", text="ISBN")
book_list.heading("Title", text="Title")
book_list.heading("Author", text="Author")
book_list.heading("Genre", text="Genre")
book_list.heading("Publisher", text="Publisher")
book_list.heading("Publish Year", text="Publish Year")

book_list.column("ISBN", width=50)
book_list.column("Title", width=150)
book_list.column("Author", width=100)
book_list.column("Genre", width=80)
book_list.column("Publisher", width=100)
book_list.column("Publish Year", width=80)



book_list.pack(fill="both", expand=True)

app_interface.mainloop()
