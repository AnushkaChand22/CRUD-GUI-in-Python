import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Global states
isUpdateVisible = False
isDeleteVisible = False
update_frame = None
delete_frame = None

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ClassDatabase"]
collection = db["studentdata"]

# Main window
app = tk.Tk()
app.title("414 Anushka Chand")
app.geometry("1000x650")
app.configure(bg="lightgreen")  # Changed color

# Title
tk.Label(app, text="CRUD Operation Using GUI", font=("Arial", 16), bg="lightgreen").pack(anchor="w", padx=20, pady=10)

# College ID
tk.Label(app, text="College ID:", bg="lightgreen").pack(anchor="w", padx=20)
id_entry = tk.Entry(app, width=40)
id_entry.pack(anchor="w", padx=20)

# Name
tk.Label(app, text="Name:", bg="lightgreen").pack(anchor="w", padx=20)
name_entry = tk.Entry(app, width=40)
name_entry.pack(anchor="w", padx=20)

# Age
tk.Label(app, text="Age:", bg="lightgreen").pack(anchor="w", padx=20)
age_entry = tk.Entry(app, width=40)
age_entry.pack(anchor="w", padx=20)

# Phone Number
tk.Label(app, text="Phone Number:", bg="lightgreen").pack(anchor="w", padx=20)
phone_entry = tk.Entry(app, width=40)
phone_entry.pack(anchor="w", padx=20)


# Insert Function
def insert():
    id = id_entry.get().strip()
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    phone = phone_entry.get().strip()  # Changed

    if not (id and name and age and phone):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    if collection.find_one({"id": id}):
        messagebox.showwarning("Duplicate ID", "A record with this College ID already exists.")
        return

    try:
        collection.insert_one({
            "id": id,
            "name": name,
            "age": age,
            "phone": phone  # Changed
        })
        messagebox.showinfo("Success", "Data inserted successfully!")
        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)  # Changed
    except:
        messagebox.showerror("Error", "Failed to insert data.")


# Display Function
def read():
    win = tk.Toplevel(app)
    win.title("Display Records")
    win.geometry("600x400")
    result_label = tk.Label(win, text="", justify="left", anchor="w", bg="lightgreen")
    result_label.pack(anchor="w", padx=20, pady=10)

    try:
        documents = collection.find()
        result = ""
        for doc in documents:
            result += f"Id: {doc['id']}\nName: {doc['name']}\nAge: {doc['age']}\nPhone Number: {doc.get('phone', '')}\n\n"
        result_label.config(text=result)
    except:
        messagebox.showerror("Error", "Failed to display data.")


# Update Function
def update():
    global isUpdateVisible, update_frame, delete_frame, isDeleteVisible

    if delete_frame:
        delete_frame.destroy()
        isDeleteVisible = False

    if not isUpdateVisible:
        isUpdateVisible = True
        update_frame = tk.Frame(app, bg="lightgreen")
        update_frame.pack(anchor="w", padx=20, pady=100)

        id_label = tk.Label(update_frame, text="Enter College ID to Update:", bg="lightgreen")
        id_label.pack(anchor="w", pady=5)
        id_input = tk.Entry(update_frame, width=40)
        id_input.pack(anchor="w", pady=2)

        name_label = tk.Label(update_frame, text="Update Your Name:", bg="lightgreen")
        name_label.pack(anchor="w", pady=2)
        name_input = tk.Entry(update_frame, width=40)
        name_input.pack(anchor="w", pady=2)

        age_label = tk.Label(update_frame, text="Update Your Age:", bg="lightgreen")
        age_label.pack(anchor="w", pady=2)
        age_input = tk.Entry(update_frame, width=40)
        age_input.pack(anchor="w", pady=2)

        phone_label = tk.Label(update_frame, text="Update Your Phone Number:", bg="lightgreen")
        phone_label.pack(anchor="w", pady=2)
        phone_input = tk.Entry(update_frame, width=40)
        phone_input.pack(anchor="w", pady=2)

        def updateinfo():
            global isUpdateVisible
            old_id = id_input.get().strip()
            new_name = name_input.get().strip()
            new_age = age_input.get().strip()
            new_phone = phone_input.get().strip()

            if not old_id:
                messagebox.showwarning("Warning", "Please enter a College ID to update.")
                return

            update_fields = {}
            if new_name:
                update_fields["name"] = new_name
            if new_age:
                update_fields["age"] = new_age
            if new_phone:
                update_fields["phone"] = new_phone

            if not update_fields:
                messagebox.showwarning("Warning", "Please enter at least one field to update.")
                return

            result = collection.update_one({"id": old_id}, {"$set": update_fields})
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Record updated successfully!")
            else:
                messagebox.showinfo("No Match", "No matching record found.")

            update_frame.destroy()
            isUpdateVisible = False

        tk.Button(update_frame, text="Confirm Update", command=updateinfo).pack(anchor="w", pady=10)

    else:
        update_frame.destroy()
        isUpdateVisible = False


# Delete Function
def delete():
    global isDeleteVisible, delete_frame, update_frame, isUpdateVisible

    if update_frame:
        update_frame.destroy()
        isUpdateVisible = False

    if not isDeleteVisible:
        isDeleteVisible = True
        delete_frame = tk.Frame(app, bg="lightgreen")
        delete_frame.pack(anchor="w", padx=20, pady=100)

        id_label = tk.Label(delete_frame, text="Enter College ID to Delete:", bg="lightgreen")
        id_label.pack(anchor="w", pady=5)
        id_input = tk.Entry(delete_frame, width=40)
        id_input.pack(anchor="w", pady=2)

        def deleteInfo():
            global isDeleteVisible
            old_id = id_input.get().strip()
            if not old_id:
                messagebox.showwarning("Warning", "Please enter a College ID to delete.")
                return

            result = collection.delete_one({"id": old_id})
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showinfo("No Match", "No matching record found.")

            delete_frame.destroy()
            isDeleteVisible = False

        tk.Button(delete_frame, text="Confirm Delete", command=deleteInfo).pack(anchor="w", pady=10)

    else:
        delete_frame.destroy()
        isDeleteVisible = False


# Buttons
tk.Button(app, text="Insert", command=insert).place(x=20, y=250)
tk.Button(app, text="Display Users", command=read).place(x=100, y=250)
tk.Button(app, text="Update", command=update).place(x=220, y=250)
tk.Button(app, text="Delete", command=delete).place(x=320, y=250)

# Run app
app.mainloop()