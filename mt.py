from tkinter import *
from tkinter import ttk
import configparser
from tkinter.filedialog import *
from tkinter import scrolledtext


# Сохраняем положение окна после закрытия программы
def w_save():
	# перед получением выполняем:
	root.update_idletasks()
	conf = configparser.RawConfigParser()
	conf.read("mt.ini")
	if not conf.has_section("Geom"):
		conf.add_section("Geom")
	conf.set("Geom", "geometry", root.winfo_geometry())
	with open("mt.ini", "w") as config:
		conf.write(config)

def change_state():
	# Активируем кнопки
	btn3.state(["!disabled"])
	btn4.state(["!disabled"])
	btn5.state(["!disabled"])
	btn6.state(["!disabled"])
	btn7.state(["!disabled"])
	# Активируем пункты меню
	file_menu.entryconfigure(2, state="normal")
	run_menu.entryconfigure(0, state="normal")
	run_menu.entryconfigure(1, state="normal")
	run_menu.entryconfigure(2, state="normal")
	run_menu.entryconfigure(4, state="normal")
	
def win_del(env):
	w_save()

def f_exit():
	w_save()
	quit()
	
def hot_exit(env):
	f_exit()
	
def f_open():
	op = askopenfilename()
	if op:
		with open( op ) as f_in:
			scr.insert(END, f_in.read())
		scr.pack(side = BOTTOM, fill = BOTH)
		nb.select(0) # Выбираем первую закладку
		scr.focus_set() # Фокус в редактирование
		change_state()
		
def hot_open(env):
	f_open()
	
def f_new():
	scr.insert(END, "")
	scr.pack(side = BOTTOM, fill = BOTH)
	nb.select(0)    # Выбираем первую закладку
	scr.focus_set() # Фокус в редактирование
	change_state()

def hot_new(env):
	f_new()

def f_save():
	sa = asksaveasfilename()
	if sa:
		with open( sa, "w" ) as f_out:
			f_out.write( scr.get(0.0, END) )

			
def hot_save(env):
	f_save()

root = Tk()
root.title("Mikrotik Runner")
# Уголок для изменения размера мышей
#ttk.Sizegrip(root).pack(side='bottom', fill='both')
ttk.Sizegrip(root).pack(side=BOTTOM,anchor=SE)

# Если есть, считываем из конфига прошлое положение окна
conf = configparser.RawConfigParser()
conf.read("mt.ini")
if conf.has_option("Geom", "geometry"):
	root.geometry(conf.get("Geom", "geometry"))
else:
	root.geometry("400x300+300+250")

# Панеь для кнопок
tool_bar = ttk.Frame(root, relief=GROOVE)
tool_bar.pack(side=TOP, fill=X)

# Кнопки
im1 = PhotoImage(file='img/new.gif')
btn1 = ttk.Button(tool_bar, image=im1, text="New", width=10, compound=TOP, underline=0, command=f_new)
btn1.grid(row=0, column=0, padx=2, pady=2)
im2 = PhotoImage(file='img/edit.gif')
btn2 = ttk.Button(tool_bar, image=im2, text="Open", width=10, compound=TOP, underline=0, command=f_open)
btn2.grid(row=0, column=2, padx=2, pady=2)
im3 = PhotoImage(file='img/file_save_as.gif')
btn3 = ttk.Button(tool_bar, image=im3, text="Save", width=10, compound=TOP, underline=0, state="disabled", command=f_save)
btn3.grid(row=0, column=3, padx=2, pady=2)
#btn3.state(['disabled'])
# Разделитель
sep1=ttk.Separator(tool_bar, orient=VERTICAL)
sep1.grid(row=0, column=4, padx=2, pady=2, sticky="ns")

im4 = PhotoImage(file='img/user_add.gif')
btn4 = ttk.Button(tool_bar, image=im4, text="User Add", width=10, compound=TOP, underline=0, state="disabled")
btn4.grid(row=0, column=5, padx=2, pady=2)

im5 = PhotoImage(file='img/user_edit.gif')
btn5 = ttk.Button(tool_bar, image=im5, text="User Edit", width=10, compound=TOP, underline=0, state="disabled")
btn5.grid(row=0, column=6, padx=2, pady=2)

im6 = PhotoImage(file='img/user_delete.gif')
btn6 = ttk.Button(tool_bar, image=im6, text="User Del", width=10, compound=TOP, underline=0, state="disabled")
btn6.grid(row=0, column=7, padx=2, pady=2)

# Разделитель
sep2=ttk.Separator(tool_bar, orient=VERTICAL)
sep2.grid(row=0, column=8, padx=2, pady=2, sticky="ns")

im7 = PhotoImage(file='img/wrench.gif')
btn7 = ttk.Button(tool_bar, image=im7, text="Exec Any", width=10, compound=TOP, underline=0, state="disabled")
btn7.grid(row=0, column=9, padx=2, pady=2)


nb = ttk.Notebook(root)
nb.pack(fill='both', expand='yes')
frame1 = ttk.Frame(nb)
frame2 = ttk.Frame(nb)
nb.add(frame1, text='In File')
nb.add(frame2, text='Out Log')

scr = scrolledtext.ScrolledText(frame1, wrap=WORD)

main_menu = Menu()
file_menu = Menu(tearoff=False)
run_menu  = Menu(tearoff=False)
help_menu = Menu(tearoff=False)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Run",  menu=run_menu)
main_menu.add_cascade(label="Help", menu=help_menu)

file_menu.add_command(label="New", accelerator="Ctrl+N", command=f_new)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=f_open)
file_menu.add_command(label="Save", accelerator="Ctrl+S", state="disabled", command=f_save)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=f_exit)

run_menu.add_command(label="User Add", state="disabled")
run_menu.add_command(label="User Edit", state="disabled")
run_menu.add_command(label="User Del", state="disabled")
run_menu.add_separator()
run_menu.add_command(label="Exec Any Command", state="disabled")

root.config(menu=main_menu)

# Горячие кнопки меню:
root.bind('<Control-n>', hot_new)
root.bind('<Control-s>', hot_save)
root.bind('<Control-o>', hot_open)
root.bind('<Control-q>', hot_exit)

# Закрытие окна, вызываем функцию win_del
root.bind('<Destroy>', win_del)

root.mainloop()
