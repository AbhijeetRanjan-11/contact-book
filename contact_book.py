import json
import os
import re
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data["email"], data["address"])


class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def view_contacts(self):
        return self.contacts.copy()

    def search_contacts(self, search_term):
        search_term = search_term.lower()
        return [contact for contact in self.contacts
                if (search_term in contact.name.lower() or
                    search_term in contact.phone)]

    def update_contact(self, old_name, new_contact):
        for i, contact in enumerate(self.contacts):
            if contact.name == old_name:
                self.contacts[i] = new_contact
                self.save_contacts()
                return True
        return False

    def delete_contact(self, name):
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                del self.contacts[i]
                self.save_contacts()
                return True
        return False

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.contacts = [Contact.from_dict(item) for item in data]
            except (json.JSONDecodeError, IOError):
                self.contacts = []
        else:
            self.contacts = []


class ContactBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Contact Book")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.root.configure(bg="#f0f2f5")

        self.contact_book = ContactBook()

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0f2f5")
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.configure('TLabel', background="#f0f2f5", font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'))

        # Create GUI components
        self.create_header()
        self.create_search_frame()
        self.create_contact_form()
        self.create_contact_list()

        # Load initial data
        self.update_contact_list()

    def create_header(self):
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(pady=10, padx=10, fill=X)

        title_label = ttk.Label(header_frame, text="Contact Book", style='Header.TLabel')
        title_label.pack(side=LEFT, padx=10)

        # Add a small logo/icon
        try:
            # Using a placeholder icon - in a real app, you would use an actual image file
            icon = Image.new('RGB', (40, 40), color='#4e73df')
            photo = ImageTk.PhotoImage(icon)
            icon_label = Label(header_frame, image=photo, background="#f0f2f5")
            icon_label.image = photo
            icon_label.pack(side=RIGHT, padx=10)
        except:
            pass  # If PIL is not available, skip the icon

    def create_search_frame(self):
        search_frame = ttk.Frame(self.root, style='TFrame')
        search_frame.pack(pady=10, padx=10, fill=X)

        self.search_var = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Helvetica', 10))
        search_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.search_contacts)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_contacts)
        search_button.pack(side=LEFT)

    def create_contact_form(self):
        form_frame = ttk.Frame(self.root, style='TFrame')
        form_frame.pack(pady=10, padx=10, fill=X)

        # Name Field
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.name_var = StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, font=('Helvetica', 10))
        name_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)

        # Phone Field
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.phone_var = StringVar()
        phone_entry = ttk.Entry(form_frame, textvariable=self.phone_var, font=('Helvetica', 10))
        phone_entry.grid(row=1, column=1, sticky=EW, padx=5, pady=5)

        # Email Field
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.email_var = StringVar()
        email_entry = ttk.Entry(form_frame, textvariable=self.email_var, font=('Helvetica', 10))
        email_entry.grid(row=2, column=1, sticky=EW, padx=5, pady=5)

        # Address Field
        ttk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.address_var = StringVar()
        address_entry = ttk.Entry(form_frame, textvariable=self.address_var, font=('Helvetica', 10))
        address_entry.grid(row=3, column=1, sticky=EW, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame, style='TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        add_button = ttk.Button(button_frame, text="Add Contact", command=self.add_contact)
        add_button.pack(side=LEFT, padx=5)

        update_button = ttk.Button(button_frame, text="Update Contact", command=self.update_contact)
        update_button.pack(side=LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_form)
        clear_button.pack(side=LEFT, padx=5)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

    def create_contact_list(self):
        list_frame = ttk.Frame(self.root, style='TFrame')
        list_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

        self.contact_tree = ttk.Treeview(list_frame, columns=("Name", "Phone", "Email", "Address"),
                                         show="headings", selectmode="browse")

        self.contact_tree.heading("Name", text="Name", anchor=W)
        self.contact_tree.heading("Phone", text="Phone", anchor=W)
        self.contact_tree.heading("Email", text="Email", anchor=W)
        self.contact_tree.heading("Address", text="Address", anchor=W)

        self.contact_tree.column("Name", width=150, minwidth=100, stretch=NO)
        self.contact_tree.column("Phone", width=120, minwidth=100, stretch=NO)
        self.contact_tree.column("Email", width=180, minwidth=100, stretch=NO)
        self.contact_tree.column("Address", width=250, minwidth=100, stretch=YES)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)

        self.contact_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Double-click to load contact for editing
        self.contact_tree.bind("<Double-1>", self.load_selected_contact)

        # Right-click for delete option
        self.contact_tree.bind("<Button-3>", self.show_context_menu)

    def update_contact_list(self, contacts=None):
        if contacts is None:
            contacts = self.contact_book.view_contacts()

        self.contact_tree.delete(*self.contact_tree.get_children())

        for contact in contacts:
            self.contact_tree.insert("", END, values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.address
            ))

    def search_contacts(self, event=None):
        search_term = self.search_var.get().strip()
        if not search_term:
            self.update_contact_list()
            return

        results = self.contact_book.search_contacts(search_term)
        self.update_contact_list(results)

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        # Input validation
        if not name:
            messagebox.showerror("Error", "Name is required")
            return

        if not phone:
            messagebox.showerror("Error", "Phone number is required")
            return

        if not self.is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format")
            return

        if email and not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return

        # Check if contact already exists
        for contact in self.contact_book.contacts:
            if contact.name.lower() == name.lower():
                messagebox.showerror("Error", "Contact with this name already exists")
                return

        contact = Contact(name, phone, email, address)
        self.contact_book.add_contact(contact)
        self.update_contact_list()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully")

    def update_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        # Input validation
        if not name:
            messagebox.showerror("Error", "Name is required")
            return

        if not phone:
            messagebox.showerror("Error", "Phone number is required")
            return

        if not self.is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format")
            return

        if email and not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return

        contact = Contact(name, phone, email, address)
        if self.contact_book.update_contact(name, contact):
            self.update_contact_list()
            self.clear_form()
            messagebox.showinfo("Success", "Contact updated successfully")
        else:
            messagebox.showerror("Error", "Contact not found")

    def delete_contact(self):
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No contact selected")
            return

        name = self.contact_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm", f"Delete contact '{name}'?"):
            if self.contact_book.delete_contact(name):
                self.update_contact_list()
                self.clear_form()
                messagebox.showinfo("Success", "Contact deleted successfully")
            else:
                messagebox.showerror("Error", "Contact not found")

    def load_selected_contact(self, event):
        selected_item = self.contact_tree.selection()
        if selected_item:
            values = self.contact_tree.item(selected_item)['values']
            self.clear_form()
            self.name_var.set(values[0])
            self.phone_var.set(values[1])
            self.email_var.set(values[2])
            self.address_var.set(values[3])

    def show_context_menu(self, event):
        selected_item = self.contact_tree.identify_row(event.y)
        if selected_item:
            self.contact_tree.selection_set(selected_item)
            menu = Menu(self.root, tearoff=0)
            menu.add_command(label="Delete", command=self.delete_contact)
            menu.post(event.x_root, event.y_root)

    def clear_form(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")

    @staticmethod
    def is_valid_phone(phone):
        # Simple phone validation (10 digits, optionally with country code, spaces, dashes, etc.)
        return bool(re.match(r'^[\d\+\-\(\)\s]{7,15}$', phone))

    @staticmethod
    def is_valid_email(email):
        # Basic email validation
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))


def main():
    root = Tk()
    app = ContactBookGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
