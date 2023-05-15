import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox


# Conectar con la base de datos
conn = sqlite3.connect('Cajero.db')
# Crear un cursor
c = conn.cursor()
# Crear la tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (nombre text, apellido text, nip integer, saldo real)''')
# Confirmar los cambios
conn.commit()





def registrar():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    nip = nip_entry.get()
    c.execute("SELECT * FROM usuarios WHERE nip=?", (nip,))
    resultado = c.fetchone()
    if resultado is not None:
        messagebox.showerror("Error", "NIP ya registrado")
    else:
        c.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)", (nombre, apellido, nip, 0))
        conn.commit()
        messagebox.showinfo("Registro", "Usuario registrado exitosamente")
        
def ingresar():
    nip = nip_entry.get()
    c.execute("SELECT * FROM usuarios WHERE nip=?", (nip,))
    resultado = c.fetchone()
    if resultado is None:
        messagebox.showerror("Error", "NIP no válido")
    else:
        saldo = resultado[3]
        saldo_actual = saldo
        messagebox.showinfo("Bienvenido", f"Bienvenido {resultado[0]}\nSaldo: ${saldo}")
        
        # Ocultar la ventana principal
        main_screen.withdraw()
        
        # Crear la ventana de operaciones
        operaciones_screen = tk.Toplevel(main_screen)
        operaciones_screen.title("Operaciones")
        operaciones_screen.geometry("250x200")
        operaciones_screen.resizable(False, False)
        
        # Crear el campo de entrada para el monto
        tk.Label(operaciones_screen, text="Monto a depositar o retirar: $").pack()
        monto_entry = tk.Entry(operaciones_screen)
        monto_entry.pack()
        
        # Crear las funciones para depositar y retirar
        def depositar():
            nonlocal saldo_actual
            monto = float(monto_entry.get())
            saldo_actual += monto
            c.execute("UPDATE usuarios SET saldo=? WHERE nip=?", (saldo_actual, nip))
            conn.commit()
            messagebox.showinfo("Depósito", f"Depósito exitoso\nSaldo actual: ${saldo_actual}")
            
        def retirar():
            nonlocal saldo_actual
            monto = float(monto_entry.get())
            if monto > saldo_actual:
                messagebox.showerror("Error", "Fondos insuficientes")
            else:
                saldo_actual -= monto
                c.execute("UPDATE usuarios SET saldo=? WHERE nip=?", (saldo_actual, nip))
                conn.commit()
                messagebox.showinfo("Retiro", f"Retiro exitoso\nSaldo actual: ${saldo_actual}")
        
        # Crear los botones para depositar y retirar
        depositar_button = tk.Button(operaciones_screen, text="Depositar", command=depositar)
        depositar_button.pack()
        retirar_button = tk.Button(operaciones_screen, text="Retirar", command=retirar)
        retirar_button.pack()
        
        def cerrar_ventana_operaciones():
            # Cerrar la ventana de operaciones
            operaciones_screen.destroy()
            # Mostrar la ventana principal
            main_screen.deiconify()
        
        # Crear el botón para cerrar la ventana de operaciones
        cerrar_button = tk.Button(operaciones_screen, text="Cerrar", command=cerrar_ventana_operaciones)
        cerrar_button.pack()
        

# Crear la pantalla principal
main_screen = tk.Tk()
main_screen.configure(background='white')
main_screen.title("Cajero automático")
main_screen.geometry("600x250")
main_screen.resizable(False, False)

# Crear los Labels de nombre, apellido y nip
nip_label = tk.Label(main_screen, text="CrediUaz", font=("Helvetica", 12, 'bold'), background='white')
nip_label.grid(row=0, column=1)

nombre_label = tk.Label(main_screen, text="Nombre:", font=("Helvetica", 12), background='white')
nombre_label.grid(row=1, column=0)

apellido_label = tk.Label(main_screen, text="Apellido:", font=("Helvetica", 12), background='white')
apellido_label.grid(row=2, column=0)

nip_label = tk.Label(main_screen, text="NIP:", font=("Helvetica", 12), background='white')
nip_label.grid(row=3, column=0)

# Creamos cajas de texto
nombre_entry = tk.Entry(main_screen, width=30, bd=0, highlightthickness=0)
nombre_entry.config({"background": main_screen.cget("background")})
nombre_entry.grid(row=1, column=1, pady=10, padx=10)

apellido_entry = tk.Entry(main_screen, width=30, bd=0, highlightthickness=0)
apellido_entry.config({"background": main_screen.cget("background")})
apellido_entry.grid(row=2, column=1, pady=10, padx=10)

nip_entry = tk.Entry(main_screen, show="*", width=30, bd=0, highlightthickness=0)
nip_entry.config({"background": main_screen.cget("background")})
nip_entry.grid(row=3, column=1, pady=10, padx=10)

# Agrega un borde inferior a las cajas de texto
nombre_entry.config({"relief": "solid", "borderwidth": 0, "highlightthickness": 1, "highlightbackground": "gray"})
apellido_entry.config({"relief": "solid", "borderwidth": 0, "highlightthickness": 1, "highlightbackground": "gray"})
nip_entry.config({"relief": "solid", "borderwidth": 0, "highlightthickness": 1, "highlightbackground": "gray"})



nombre_entry.config({"borderwidth": 1, "relief": "solid", "highlightthickness": 0})
apellido_entry.config({"borderwidth": 1, "relief": "solid", "highlightthickness": 0})
nip_entry.config({"borderwidth": 1, "relief": "solid", "highlightthickness": 0})

# Crear los botones de ingreso y registro de usuario
ingresar_button = tk.Button(main_screen, text="Ingresar", command=ingresar, background="#3479F0", foreground="white",  font=('Helvetica', 12, 'bold'), padx=5, pady=10)
ingresar_button.grid(row=4, column=1, pady=20, sticky="ew")

registrar_button = tk.Button(main_screen, text="Registrar", command=registrar, background="#3479F0", foreground="white",  font=('Helvetica', 12, 'bold'), padx=5, pady=10)
registrar_button.grid(row=4, column=0, pady=20, sticky="ew")

# Cargar la imagen
imagen = Image.open("image.png")
imagen = imagen.resize((250, 200)) # Redimensionar la imagen
imagen = ImageTk.PhotoImage(imagen)

# Crear el widget Label con la imagen
imagen_label = tk.Label(main_screen, image=imagen)
imagen_label.place(x=320, y=10) # Posicionar la imagen

# Cargar la imagen
imagen2 = Image.open("banlogo.png")
imagen2 = imagen2.resize((20, 20)) # Redimensionar la imagen
imagen2 = ImageTk.PhotoImage(imagen2)

# Crear el widget Label con la imagen
imagen_label2 = tk.Label(main_screen, image=imagen2)
imagen_label2.place(x=125, y=2) # Posicionar la imagen

# Iniciar la aplicación
main_screen.mainloop()