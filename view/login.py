import manager
import customtkinter as ctk 
import tkinter.messagebox as tkmb
import requests 
import viewer
from tkinter import messagebox
import admin
class Login:
	def __init__(self, root):
		self.root = root
		self.loginControlFrame()


	def login(self):
		username = self.user_entry.get()
		password = self.user_pass.get()
		response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password})
		if response.status_code == 200:
			role = response.json()['role']
			messagebox.showinfo('Login Success','Logged in')
			self.root.destroy()
			if role == 'admin':
				admin.Home().homeControlFrame("admin")
			elif role == 'manager':
				manager.Home().homeControlFrame("manager")
			
			elif role == 'viewer':
				viewer.Home().homeControlFrame("viewer")

			
			else :
				messagebox.showerror(' Access Denied', "Don't have access to page")
		

				

			

		else:
			messagebox.showerror('Login Failed', 'Invalid credentials')
		
		


	def loginControlFrame(self):
		# Set the label 
		label = ctk.CTkLabel(self.root,text="Inventory Manager",font=('Arial', 25)) 
		label.pack(pady=20) 

		# Create a frame 
		frame = ctk.CTkFrame(master=self.root) 
		frame.pack(pady=20,padx=40, 
				fill='both',expand=True) 

		# Set the label inside the frame 
		label = ctk.CTkLabel(master=frame, 
							text='Login',font=('Arial', 20)) 
		label.pack(pady=12,padx=10) 

		# Create the text box for taking 
		# username input from user 
		self.user_entry= ctk.CTkEntry(master=frame, 
								placeholder_text="Username") 
		self.user_entry.pack(pady=12,padx=10) 

		# Create a text box for taking 
		# password input from user 
		self.user_pass= ctk.CTkEntry(master=frame, 
								placeholder_text="Password", 
								show="*") 
		self.user_pass.pack(pady=12,padx=10) 
		# Create a login button to login 
		button = ctk.CTkButton(master=frame, 
							text='Login',command=self.login) 
		button.pack(pady=12,padx=10) 

