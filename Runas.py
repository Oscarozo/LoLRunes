from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import sqlite3

# ----------------------------sqlite stuff---------------------------------------------
conexion = sqlite3.connect("dbLoLpy.db")
my_cursor = conexion.cursor()  # Se define el cursor para ejecutar comandos SQL


# -----------------------------------------Funciones-------------------------------------------------------

def exit():  # Salir del programa
    if messagebox.askquestion('Exit', 'Are you sure you want to exit?') == "yes":

        conexion.close()  # cerramos la conexion con la base de datos
        ventana.destroy()

    else:
        pass


def borrar():  # Borrar todo
    champ_name.delete(0, END)  # borrar el contenido de ese textbox (inicio, final)
    main_rune.delete(0, END)
    rune1_1.delete(0, END)
    rune1_2.delete(0, END)
    rune1_3.delete(0, END)
    rune1_4.delete(0, END)
    rune2_1.delete(0, END)
    rune2_2.delete(0, END)
    second_rune.delete(0, END)
    bonus1.delete(0, END)
    bonus2.delete(0, END)
    bonus3.delete(0, END)


def conectar():  # conectarse a la base de datos

    messagebox.showinfo("Attention", "connection stablished")


def crear():
    try:
        # creación de la tabla
        my_cursor.execute("""

			CREATE TABLE '%s'(
				main_rune VARCHAR(30),
				rune1_1 VARCHAR(30),
				rune1_2 VARCHAR(30),
				rune1_3 VARCHAR(30),
				rune1_4 VARCHAR(30),
				second_rune VARCHAR(30),
				rune2_1 VARCHAR(30),
				rune2_2 VARCHAR(30),
				bonus1 VARCHAR(30),
				bonus2 VARCHAR(30),
				bonus3 VARCHAR(30)
			)
		""" % champ_name.get())

        conexion.commit()

        # Insertar datos en la tabla
        my_cursor.execute("""

			INSERT INTO %s(main_rune, rune1_1, rune1_2, rune1_3, rune1_4, second_rune, rune2_1, rune2_2, bonus1, bonus2, bonus3)
			VALUES(?,?,?,?,?,?,?,?,?,?,?)
		""" % champ_name.get(), (main_rune.get(), rune1_1.get(), rune1_2.get(), rune1_3.get(), rune1_4.get(), second_rune.get(), rune2_1.get(), rune2_2.get(), bonus1.get(), bonus2.get(), bonus3.get())
        )

        conexion.commit()

        messagebox.showinfo("Attention", "New champ added")

        # Actualizamos la lista de campeones
        obtener_champs()

    except Exception as e:
        messagebox.showerror("Error!", "Champ already exists")


def leer():
    try:
        my_cursor.execute("SELECT * FROM %s" % champ_name.get())
        runas = my_cursor.fetchone()  # cargamos los datos en la variable que se vuelve tupla

        # ponemos el contenido de la tupla en las cajas de texto (inicio, texto)
        bonus3.insert(0, runas[10])
        bonus2.insert(0, runas[9])
        bonus1.insert(0, runas[8])
        rune2_2.insert(0, runas[7])
        rune2_1.insert(0, runas[6])
        second_rune.insert(0, runas[5])
        rune1_4.insert(0, runas[4])
        rune1_3.insert(0, runas[3])
        rune1_2.insert(0, runas[2])
        rune1_1.insert(0, runas[1])
        main_rune.insert(0, runas[0])

        messagebox.showinfo("Attention", "Done!")

    except Exception as e:
        messagebox.showerror("Error!", "no data")


def actualizar():
    try:
        # actualizamos los datos
        my_cursor.execute("""

				UPDATE %s SET main_rune=?, rune1_1=?, rune1_2=?, rune1_3=?, rune1_4=?, second_rune=?, rune2_1=?, rune2_2=?, bonus1=?, bonus2=?, bonus3=?
			""" % champ_name.get(), (main_rune.get(), rune1_1.get(), rune1_2.get(), rune1_3.get(), rune1_4.get(), second_rune.get(), rune2_1.get(), rune2_2.get(), bonus1.get(), bonus2.get(), bonus3.get())
        )

        conexion.commit()
        messagebox.showinfo("Attention", "Done!")

        # Actualizamos la lista de campeones
        obtener_champs()

    except:
        messagebox.showerror("Error!", "table does no exist")


def eliminar_tabla():

    try:
        # eliminamos una tabla
        my_cursor.execute("DROP TABLE IF EXISTS %s" % champ_name.get())
        messagebox.showinfo("Attention", "Done!")

        # Actualizamos la lista de campeones
        obtener_champs()

    except Exception as e:
        messagebox.showerror("Error!", "table does not exist")


def obtener_champs():
    try:
        # Obetnemos el nombre de todas las tablas
        my_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        champs = my_cursor.fetchall()

        lista_champs.delete(0, END)  # Limpiamos la lista

        for champ in champs:
            lista_champs.insert(END, champ)

    except:
        messagebox.showwarning("Attention", "tables do not exist")


def seleccionar_campeon():
    try:
        champ_name.delete(0, END)
        # Poner un nombre seleccionado en la caja de texto
        champ_name.insert(0, lista_champs.get(ANCHOR))

    except:
        messagebox.showerror("Error!", "No champ selected")

def info():
	messagebox.showinfo(title='Info', message='Made by: Oscar Ozorio.\n\nosvaldo15963@fpuna.edu.py')


# ---------------------------------------------GUI----------------------------------------------------------------------------------------------
ventana = Tk()
ventana.iconbitmap('timo.ico')
ventana.geometry("450x540")
ventana.title("Runas LoL")
ventana.config(bg="black")  # No hace falta
ventana.option_add('*tearOff', False)  # Deshabilita submenús flotantes

# background image
image = ImageTk.PhotoImage(Image.open('back.png'))
mylabel = Label(image=image)
# row and columnspan para que la img esté en el fondo
mylabel.grid(row=0, column=0, rowspan=13, columnspan=3)

cadena = StringVar()
cadena.set("Hola gg")

champ_name = Entry(ventana, font="none 10 bold", justify="center", width=20, textvariable=cadena)
champ_name.grid(row=0, column=1, padx=10, pady=10)

lista_champs = Listbox(ventana, font="none 10 bold", width=15, height=5)
lista_champs.grid(row=1, column=1, padx=10, pady=5)
# cargamos la lista de campeones
obtener_champs()

# -------------------runas principales-----------------------------------------------------------------
main_rune = Entry(ventana, font="none 10 bold", width=15, justify="center")
main_rune.grid(row=1, column=0, padx=10, pady=10)

rune1_1 = Entry(ventana, font="none 10", width=15, justify="center")
rune1_1.grid(row=2, column=0, padx=10, pady=10)

rune1_2 = Entry(ventana, font="none 10", width=15, justify="center")
rune1_2.grid(row=3, column=0, padx=10, pady=10)

rune1_3 = Entry(ventana, font="none 10", width=15, justify="center")
rune1_3.grid(row=4, column=0, padx=10, pady=10)

rune1_4 = Entry(ventana, font="none 10", width=15, justify="center")
rune1_4.grid(row=5, column=0, padx=10, pady=10)

# --------------------------runas secundarias---------------------------------------------------------------------------
second_rune = Entry(ventana, font="none 10 bold", width=15, justify="center")
second_rune.grid(row=1, column=2, padx=10, pady=10)

rune2_1 = Entry(ventana, font="none 10", width=15, justify="center")
rune2_1.grid(row=2, column=2, padx=10, pady=10)

rune2_2 = Entry(ventana, font="none 10", width=15, justify="center")
rune2_2.grid(row=3, column=2, padx=10, pady=10)

# ------------------------bonus-----------------------------------------------------------------------------------------
bonus = Label(ventana, font="none 10 bold", text="Bonus", justify="left")
bonus.grid(row=5, column=2, padx=10, pady=10)

bonus1 = Entry(ventana, font="none 10", width=15, justify="center")
bonus1.grid(row=6, column=2, padx=10, pady=10)

bonus2 = Entry(ventana, font="none 10", width=15, justify="center")
bonus2.grid(row=7, column=2, padx=10, pady=10)

bonus3 = Entry(ventana, font="none 10", width=15, justify="center")
bonus3.grid(row=8, column=2, padx=10, pady=10)

# ---------------------------Botones CRUD-------------------------------------------------------------------------------
boton_create = Button(ventana, font="none 10 bold", width=7, justify="center",
                      text="CREATE", command=crear).grid(row=10, column=0, padx=1, pady=5)
boton_read = Button(ventana, font="none 10 bold", width=7, justify="center",
                    text="READ", command=leer).grid(row=10, column=1, padx=1, pady=5)
boton_update = Button(ventana, font="none 10 bold", width=7, justify="center",
                      text="UPDATE", command=actualizar).grid(row=11, column=0, padx=1, pady=5)
boton_delete = Button(ventana, font="none 10 bold", width=7, justify="center",
                      text="DELETE", command=eliminar_tabla).grid(row=11, column=1, padx=1, pady=5)

# boton para seleccionar un campeón
boton_select = Button(ventana, font="none 10 bold", width=7, text="Selec",
                      command=seleccionar_campeon).grid(row=2, column=1, padx=1, pady=5)

# --------------------------------Menú--------------------------------------------------------------------------------------
barramenu = Menu(ventana)
ventana['menu'] = barramenu

menu1 = Menu(barramenu)
#menu2 = Menu(barramenu)
menu3 = Menu(barramenu)
barramenu.add_cascade(menu=menu1, label='Options')
barramenu.add_command(label='Clean', command=borrar)
barramenu.add_cascade(menu=menu3, label='CRUD')
barramenu.add_cascade(label='About', command=info)

# --------------------------Submenu inicio----------------------------------------------
menu1.add_command(label='Connect', command=conectar)
menu1.add_separator()
menu1.add_command(label='Exit', command=exit)

# ---------------------------Submenu CRUD-----------------------------------------------
menu3.add_command(label='Create', command=crear)
menu3.add_command(label='Read', command=leer)
menu3.add_command(label='Update', command=actualizar)
menu3.add_command(label='Delete', command=eliminar_tabla)

ventana.mainloop()
