import customtkinter as ctk 
import  login

# Selecting GUI theme - dark, 
# light , system (for system default) 
ctk.set_appearance_mode("dark") 

# Selecting color theme-blue, green, dark-blue 
ctk.set_default_color_theme("blue") 

app = ctk.CTk() 
app.geometry("400x400") 
app.title("") 
#Parsing the root window to the Login class
#Initiating the System
login.Login(app)
app.mainloop()
