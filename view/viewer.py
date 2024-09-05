import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
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
        # Define the view product function (keep this one enabled)
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


        # Keep only the "Product Info" button enabled
        view_button = ctk.CTkButton(bottom_menu_frame, text="Product Info", command=view_stock, width=button_size[0], height=button_size[1])
        view_button.grid(row = 0,column = 0,padx=5 , pady=5)
        excel_button = ctk.CTkButton(bottom_menu_frame, text="Excel File", command=download_excel, width=button_size[0], height=button_size[1])
        excel_button.grid(row=0, column=2, padx=5, pady=5)

        # Show default message initially
        show_default_message()

        app.mainloop()
