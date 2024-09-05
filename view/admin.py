import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import re
from tkinter import filedialog

class Home:
    def homeControlFrame(self, role):
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create the main application window
        app = ctk.CTk()
        app.geometry("500x600")  # Increased height for additional buttons and forms
        app.overrideredirect(False)
        app.title(role)

        # Create a frame for the top content (the form or default message)
        form_frame = ctk.CTkFrame(app)
        form_frame.pack(pady=100, fill="x", padx=20)

        # Function to display a default message
        def show_default_message():
            clear_form()
            message = "Welcome! Please select an action from the buttons below."
            label = ctk.CTkLabel(form_frame, text=message, anchor="center", wraplength=400)
            label.pack(pady=20)

        def clear_form():
            # Clear any widgets inside the form_frame
            for widget in form_frame.winfo_children():
                widget.destroy()

        # Define a function to handle the Add Product button click
        def add_stock():
            clear_form()

            # Define variables for input fields
            product_code_var = tk.StringVar()
            loading_date_var = tk.StringVar()
            sold_var = tk.BooleanVar()

            # Create and place labels and input fields using grid layout
            ctk.CTkLabel(form_frame, text="Product Code:", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            product_code_entry = ctk.CTkEntry(form_frame, textvariable=product_code_var)
            product_code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(form_frame, text="Date of Loading:", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
            loading_date_entry = ctk.CTkEntry(form_frame, textvariable=loading_date_var)
            loading_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(form_frame, text="Sold:", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
            sold_checkbox = ctk.CTkCheckBox(form_frame, text="Yes", variable=sold_var)
            sold_checkbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

            # Adjust column weights to make the entry fields expand
            form_frame.grid_columnconfigure(1, weight=1)

            def submit():
                product_code = product_code_var.get()
                loading_date = loading_date_var.get()
                sold = sold_var.get()
                print(product_code,loading_date,sold)

                # Validate input
                if not product_code or not loading_date:
                    messagebox.showwarning("Input Error", "Please fill in all fields")
                    return
                x = re.search("\d\d\d\d\-\d\d\-\d\d", loading_date)
                if not x :
                    messagebox.showwarning("Input Error", "Please enter valid date(yyyy-mm-dd)")
                    return

                response = requests.post('http://127.0.0.1:5000/addproduct',
                                         json={'productcode': product_code, 
                                               'dateofloading': loading_date,
                                               'sold': '1' if sold else '0'})
                if response.status_code == 201:
                    messagebox.showinfo("Product Information", 
                    f"Product Code: {product_code}\n"
                    f"Date of Loading: {loading_date}\n"
                    f"Sold: {'Yes' if sold else 'No'}")
                else: 
                    messagebox.showerror("Exists", response.json()['message'])

                show_default_message()  # Show default message after submission

            def cancel():
                show_default_message()  # Show default message on cancel

            # Create and place buttons
            button_frame = ctk.CTkFrame(form_frame)
            button_frame.grid(row=3, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(button_frame, text="Submit", command=submit)
            submit_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel)
            cancel_button.pack(side="left", padx=10)

        # Define the delete product function
        def delete_stock():
            clear_form()

            # Define a variable for the product code input
            product_code_var = tk.StringVar()

            # Create and place label and input field
            ctk.CTkLabel(form_frame, text="Product Code:", anchor="w").grid(row=0, column=0, padx=10, pady=20, sticky="w")
            product_code_entry = ctk.CTkEntry(form_frame, textvariable=product_code_var)
            product_code_entry.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

            # Adjust column weights to make the entry field expand
            form_frame.grid_columnconfigure(1, weight=1)

            def submit_delete():
                product_code = product_code_var.get()

                # Validate input
                if not product_code:
                    messagebox.showwarning("Input Error", "Please enter the product code")
                    return

                # Send delete request
                response = requests.delete('http://127.0.0.1:5000/deleteproduct',
                                           json={'productcode': product_code})
                if response.status_code == 200:
                    messagebox.showinfo("Success", f"Product {product_code} deleted successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to delete product: {response.json().get('message', 'Unknown error')}")

                show_default_message()  # Show default message after submission

            def cancel_delete():
                show_default_message()  # Show default message on cancel

            # Create and place buttons
            button_frame = ctk.CTkFrame(form_frame)
            button_frame.grid(row=1, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(button_frame, text="Delete", command=submit_delete)
            submit_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_delete)
            cancel_button.pack(side="right", padx=10)

        # Define the add user function
        def add_user():
            clear_form()

            # Define variables for input fields
            username_var = tk.StringVar()
            password_var = tk.StringVar()
            role_var = tk.StringVar()

            # Create and place labels and input fields using grid layout
            ctk.CTkLabel(form_frame, text="Username:", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            username_entry = ctk.CTkEntry(form_frame, textvariable=username_var)
            username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(form_frame, text="Password:", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
            password_entry = ctk.CTkEntry(form_frame, textvariable=password_var, show="*")
            password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(form_frame, text="Role:", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
            role_entry = ctk.CTkEntry(form_frame, textvariable=role_var)
            role_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

            # Adjust column weights to make the entry fields expand
            form_frame.grid_columnconfigure(1, weight=1)

            def submit_user():
                username = username_var.get()
                password = password_var.get()
                role = role_var.get()

                # Validate input
                if not username or not password or not role:
                    messagebox.showwarning("Input Error", "Please fill in all fields")
                    return

                response = requests.post('http://127.0.0.1:5000/adduser',
                                         json={'username': username, 
                                               'password': password,
                                               'role': role})
                if response.status_code == 201:
                    messagebox.showinfo("User Information", 
                    f"Username: {username}\n"
                    f"Role: {role}")
                else: 
                    messagebox.showerror("Error", response.json()['message'])

                show_default_message()  # Show default message after submission

            def cancel_user():
                show_default_message()  # Show default message on cancel

            # Create and place buttons
            button_frame = ctk.CTkFrame(form_frame)
            button_frame.grid(row=3, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(button_frame, text="Create User", command=submit_user)
            submit_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_user)
            cancel_button.pack(side="left", padx=10)

        # Define the delete user function
        def delete_user():
            clear_form()

            # Define a variable for the username input
            username_var = tk.StringVar()

            # Create and place label and input field
            ctk.CTkLabel(form_frame, text="Username:", anchor="w").grid(row=0, column=0, padx=10, pady=20, sticky="w")
            username_entry = ctk.CTkEntry(form_frame, textvariable=username_var)
            username_entry.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

            # Adjust column weights to make the entry field expand
            form_frame.grid_columnconfigure(1, weight=1)

            def submit_delete_user():
                username = username_var.get()

                # Validate input
                if not username:
                    messagebox.showwarning("Input Error", "Please enter the username")
                    return

                # Send delete request
                response = requests.delete('http://127.0.0.1:5000/deleteuser',
                                           json={'username': username})
                if response.status_code == 200:
                    messagebox.showinfo("Success", f"User {username} deleted successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to delete user: {response.json().get('message', 'Unknown error')}")

                show_default_message()  # Show default message after submission

            def cancel_delete_user():
                show_default_message()  # Show default message on cancel

            # Create and place buttons
            button_frame = ctk.CTkFrame(form_frame)
            button_frame.grid(row=1, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(button_frame, text="Delete User", command=submit_delete_user)
            submit_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_delete_user)
            cancel_button.pack(side="right", padx=10)

        # Define other button functions
        def update_stock():
            clear_form()

            # Define variables for input fields
            product_code_var = tk.StringVar()
            loading_date_var = tk.StringVar()
            sold_var = tk.BooleanVar()

            # Create and place labels and input fields using grid layout
            ctk.CTkLabel(form_frame, text="Product Code:", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            product_code_entry = ctk.CTkEntry(form_frame, textvariable=product_code_var)
            product_code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(form_frame, text="Date of Loading:", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
            loading_date_entry = ctk.CTkEntry(form_frame, textvariable=loading_date_var)
            loading_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(form_frame, text="Sold:", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
            sold_checkbox = ctk.CTkCheckBox(form_frame, text="Yes", variable=sold_var)
            sold_checkbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

            # Adjust column weights to make the entry fields expand
            form_frame.grid_columnconfigure(1, weight=1)

            def submit_update():
                product_code = product_code_var.get()
                loading_date = loading_date_var.get()
                sold = sold_var.get()

                # Validate input
                if not product_code or not loading_date:
                    messagebox.showwarning("Input Error", "Please fill in all fields")
                    return
                x = re.search("\d\d\d\d\-\d\d\-\d\d", loading_date)
                if not x :
                    messagebox.showwarning("Input Error", "Please enter valid date(yyyy-mm-dd)")
                    return

                response = requests.put('http://127.0.0.1:5000/updateproduct',
                                         json={'productcode': product_code, 
                                               'dateofloading': loading_date,
                                               'sold': '1' if sold else '0'})
                if response.status_code == 200:
                    messagebox.showinfo("Success", 
                    f"Product Code: {product_code}\n"
                    f"Date of Loading: {loading_date}\n"
                    f"Sold: {'Yes' if sold else 'No'}")
                else:
                    messagebox.showerror("Error", response.json()['message'])

                show_default_message()  # Show default message after submission

            def cancel_update():
                show_default_message()  # Show default message on cancel

            # Create and place buttons
            button_frame = ctk.CTkFrame(form_frame)
            button_frame.grid(row=3, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(button_frame, text="Update", command=submit_update)
            submit_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_update)
            cancel_button.pack(side="left", padx=10)
        def download_excel():
            try:
                # URL of the Flask endpoint
                url = 'http://127.0.0.1:5000/exportwarehouse'
                
                # Make a GET request to the Flask endpoint
                response = requests.get(url, stream=True)
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Ask the user where to save the file
                    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                        filetypes=[("Excel files", "*.xlsx")])
                    
                    if file_path:
                        # Write the response content to the file
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        
                        # Notify the user
                        messagebox.showinfo("Success", "File downloaded successfully!")
                else:
                    messagebox.showerror("Error", f"Failed to download file. Status code: {response.status_code}")
            
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        def view_stock():
            clear_form()

            # Define a variable for the product code input
            product_code_var = tk.StringVar()

            # Create and place label and input field
            ctk.CTkLabel(form_frame, text="Product Code:", anchor="w").grid(row=0, column=0, padx=10, pady=20, sticky="w")
            product_code_entry = ctk.CTkEntry(form_frame, textvariable=product_code_var)
            product_code_entry.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

            # Adjust column weights to make the entry field expand
            form_frame.grid_columnconfigure(1, weight=1)

            def submit_view():
                product_code = product_code_var.get()

                # Validate input
                if not product_code:
                    messagebox.showwarning("Input Error", "Please enter the product code")
                    return

                # Send view request
                response = requests.get('http://127.0.0.1:5000/viewproduct',
                                        params={'productcode': product_code})
                if response.status_code == 200:
                    product_data = response.json()
                    messagebox.showinfo("Product Information", 
                    f"Product Code: {product_data['productcode']}\n"
                    f"Date of Loading: {product_data['dateofloading']}\n"
                    f"Sold: {'Yes' if product_data['sold'] == '1' else 'No'}")
                else:
                    messagebox.showerror("Error", f"Failed to retrieve product: {response.json().get('message', 'Unknown error')}")

                show_default_message()  # Show default message after submission

            def cancel_view():
                show_default_message()  # Show default message on cancel

            # Create and place buttons
            button_frame = ctk.CTkFrame(form_frame)
            button_frame.grid(row=1, column=0, columnspan=2, pady=10)

            submit_button = ctk.CTkButton(button_frame, text="View", command=submit_view)
            submit_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=cancel_view)
            cancel_button.pack(side="right", padx=10)

        # Create a frame for the bottom menu
        bottom_menu_frame = ctk.CTkFrame(app)
        bottom_menu_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        # Create buttons for the bottom menu using grid layout for better control
        button_size = (150, 50)  # Width x Height in pixels

        add_button = ctk.CTkButton(bottom_menu_frame, text="Add Product", command=add_stock, width=button_size[0], height=button_size[1])
        add_button.grid(row=0, column=0, padx=5, pady=5)

        delete_button = ctk.CTkButton(bottom_menu_frame, text="Delete Product", command=delete_stock, width=button_size[0], height=button_size[1])
        delete_button.grid(row=0, column=1, padx=5, pady=5)

        update_button = ctk.CTkButton(bottom_menu_frame, text="Update Product", command=update_stock, width=button_size[0], height=button_size[1])
        update_button.grid(row=0, column=2, padx=5, pady=5)

        view_button = ctk.CTkButton(bottom_menu_frame, text="Product Info", command=view_stock, width=button_size[0], height=button_size[1])
        view_button.grid(row=0, column=3, padx=5, pady=5)

        add_user_button = ctk.CTkButton(bottom_menu_frame, text="Add User", command=add_user, width=button_size[0], height=button_size[1])
        add_user_button.grid(row=1, column=0, padx=5, pady=5)

        delete_user_button = ctk.CTkButton(bottom_menu_frame, text="Delete User", command=delete_user, width=button_size[0], height=button_size[1])
        delete_user_button.grid(row=1, column=1, padx=5, pady=5)
        excel_button = ctk.CTkButton(bottom_menu_frame, text="Excel File", command=download_excel, width=button_size[0], height=button_size[1])
        excel_button.grid(row=1, column=2, padx=5, pady=5)

        # Add stretching to ensure buttons are not clipped
        bottom_menu_frame.grid_columnconfigure(0, weight=1)
        bottom_menu_frame.grid_columnconfigure(1, weight=1)
        bottom_menu_frame.grid_columnconfigure(2, weight=1)
        bottom_menu_frame.grid_columnconfigure(3, weight=1)

        # Show default message initially
        show_default_message()

        app.mainloop()
