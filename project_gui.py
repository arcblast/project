from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

window = Tk()

window.title("Lolcode interpreter")

label_lex =Label(window, text="Lexemes",font=("Arial Bold",12))#text labels
label_symbol=Label(window, text="Symbol Table",font=("Arial Bold",12))

def clicked():#file open
	fileName = filedialog.askopenfilename(filetypes = (("Lolcode","*.lol"),))#lol files only
	fileHandler = open(fileName, 'r')
	window_input.insert(INSERT,fileHandler.read())


def interpret(): #Add all the functions for interpeting here
	inputLines=window_input.get("1.0","end")
	print(inputLines)
	window_output.configure(state="normal")#unlock window for output
	
	window_output.insert(INSERT,"THE BIG GAY\n")#Add things here
	
	window_output.configure(state="disabled")#lock window for output

open_btn = Button(window, text="Open file",bg="gray", command=clicked)
execute_btn = Button(window, text="Execute",bg="gray", command=interpret)


window_input = scrolledtext.ScrolledText(window,width=40,height=20)#Windows
window_lexemes = scrolledtext.ScrolledText(window,width=40,height=20)
window_symbols = scrolledtext.ScrolledText(window,width=40,height=20)
window_output = scrolledtext.ScrolledText(window,width=120,height=20)

window_lexemes.configure(state="disabled")#only input window should accept text
window_symbols.configure(state="disabled")
window_output.configure(state="disabled")


open_btn.grid(column=0, row=0)#place widgets on grid
label_lex.grid(column=1,row=0)
label_symbol.grid(column=2,row=0)
execute_btn.grid(column=0, row=3,sticky=E+W, columnspan=3)
window_input.grid(column=0,row=2)
window_lexemes.grid(column=1,row=2)
window_symbols.grid(column=2, row=2)
window_output.grid(column=0,row=4,columnspan=3)


window.mainloop()