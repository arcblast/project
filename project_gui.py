import tkinter as tk
import tkinter.ttk as ttk

from tkinter import scrolledtext
from tkinter import filedialog
import re
import textwrap

def wrap(string, lenght=20):#Wrap text so it looks neater in rows
    return '\n'.join(textwrap.wrap(string, lenght))

window = tk.Tk()#root

window.title("Lolcode interpreter")
label_lex =tk.Label(window, text="Lexemes",font=("Arial Bold",12))#text labels
label_symbol=tk.Label(window, text="Symbols",font=("Arial Bold",12))


#LEXEMES TABLE WIDGET
frameLex=tk.Frame(window)
treeLex = ttk.Treeview(frameLex, columns=('Code','Classification'),show="headings",selectmode='browse',height=6)#use treeLexview for table
treeLex.heading("#1",text="Code")
treeLex.heading("#2",text="Classification")

treeLex.column("#1",stretch=tk.YES)
treeLex.column("#2",stretch=tk.YES)

for i in range(4): #INSERT DATA
    treeLex.insert(parent='',index='end',iid=i,values=(wrap("Hello"+str(i)), wrap("Worwws\nwwwww\nwwww\nwwww")))

styleTree = ttk.Style()
styleTree.configure('Treeview',rowheight=30)

verticalScroll = ttk.Scrollbar(frameLex,  orient ="vertical",  command = treeLex.yview) 
treeLex.configure(yscrollcommand=verticalScroll.set)
#LEXEMES TABLE END


#SYMBOLS TABLE WIDGET
frameSymbol=tk.Frame(window)
treeSymbol = ttk.Treeview(frameSymbol, columns=('Code','Classification'),show="headings",selectmode='browse',height=6)#use treeLexview for table
treeSymbol.heading("#1",text="Code")
treeSymbol.heading("#2",text="Classification")

treeSymbol.column("#1",stretch=tk.YES)
treeSymbol.column("#2",stretch=tk.YES)

for i in range(4): #INSERT DATA
    treeSymbol.insert(parent='',index='end',iid=i,values=(wrap("Hello"+str(i)), wrap("Wowww\nwwww\nwwww")))

verticalScrollSymbol = ttk.Scrollbar(frameSymbol,  orient ="vertical",  command = treeSymbol.yview) 
treeSymbol.configure(yscrollcommand=verticalScrollSymbol.set)
#SYMBOLS TABLE END



lexemeList=[]#THIS IS WHERE SYMBOLS AND LEXEMES ARE STORED
symbolList=[]


def clicked():#File open dialog
    # fileName = filedialog.askopenfilename(filetypes = (("Lolcode","*.lol"),))#lol files only
    # ^ Commented out for ease of debugging

    fileName = "assignop.lol"
    try:
        with open(fileName,'r') as fileHandler:
            window_input.delete("1.0","end")#deletes old text from window
            window_input.insert(tk.INSERT,fileHandler.read())  

    except IOError:#in case user does not choose anything
        print("No file has been chosen")




def deleteTable():
    treeSymbol.delete(*treeSymbol.get_children())
    treeLex.delete(*treeLex.get_children())
    for row in treeSymbol.get_children():
    	treeSymbol.delete(row)
    lexemeList.clear()
    symbolList.clear()
    for row in treeLex.get_children():
    	treeLex.delete(row)



valid_keywords={
    "^I HAS A ":"Variable Declaration",
    "^HAI": "Code Delimiter",
    "^BTW ": "Single Comment",
    "^SUM OF ":"Addition Keyword",
    "\"": "String Delimter",
    "KTHXBYE": "Code Delimiter",
    "^OBTW": "Block Comment",
    "^OBTW\s.*\n.*TLDR$": "Block Comment"
}
def comments(line):
    if re.search("^BTW ",line):#single line comment
        print(line)
        print("Added")
        lexemeList.append( ("BTW ", "Single Line Comment Identifier"))
        comment = re.sub("^BTW ","",line)
        lexemeList.append( (comment,"Single Line Comment"))
    elif re.search("^OBTW\s.*\n.*TLDR",line):
        lexemeList.append( ("OBTW", "Multiline Comment Identifier"))

#Humongous if else
def identify(line,haiFlag,baiFlag): #break down into lexemes (long ass if else)
    if re.search("^BTW ",line):#single line comment

        lexemeList.append( ("BTW ", "Single Line Comment Identifier"))
        comment = re.sub("^BTW ","",line)
        lexemeList.append( (comment,"Single Line Comment"))
    elif re.search("^HAI",line):#HAI
        lexemeList.append( ("HAI", "Code Delimiter"))
    elif re.search("^I HAS A [A-Za-z][A-Za-z0-9_P]",line):#VARIABLE DECLARATION
        lexemeList.append( ("I HAS A", "Variable Declaration"))
        #get the variable
        possibleVar = re.sub("^I HAS A ","",line)

        if re.search("^[A-Za-z][A-Za-z0-9_]*$", possibleVar):
            symbolList.append((possibleVar,"Variable Identifier"))

        else:
            print("Wrong")
    else:
        a=1+1

def interpret(): #Add all the functions for interpeting here
    deleteTable()

    haiCounter=0#only comments are allowed before and after hai and bai
    baiCounter=0#use this as a flag


    inputLines=window_input.get("1.0","end")#Add code to the symbol and lexemes table
    inputList= re.split(', |\n', inputLines)
    inputList = list(map(str.strip,inputList))
    print(inputList)
    for line in inputList:
        identify(line,haiCounter,baiCounter)

    print(lexemeList)
    print(symbolList)
    for i in range(len(lexemeList)):#insert symbols and lexeme into the tables
        treeLex.insert(parent='',index='end',iid=i,values=(wrap(lexemeList[i][0]), wrap(lexemeList[i][1])))
    for i in range(len(symbolList)):
        treeSymbol.insert(parent='',index='end',iid=i,values=(wrap(symbolList[i][0]), wrap(symbolList[i][1])))
    window_output.configure(state="normal")#unlock window for output
    
    # window_output.insert(INSERT,"THE BIG GAY\n")#Add things here
    
    window_output.configure(state="disabled")#lock window for output
    # deleteTable()






open_btn = tk.Button(window, text="Open file",bg="gray", command=clicked)
execute_btn = tk.Button(window, text="Execute",bg="gray", command=interpret)

window.grid_rowconfigure(1,weight=1)
frameSymbol.grid_rowconfigure(0,weight=1)
frameLex.grid_rowconfigure(0,weight=1)

window_input = scrolledtext.ScrolledText(window,width=40,height=20)#Windows
window_output = scrolledtext.ScrolledText(window,width=120,height=20)

window_output.configure(state="disabled")#Disable input on the output window

#place widgets via grid manager
open_btn.grid(column=0, row=0,sticky="EW")
label_lex.grid(column=1,row=0)
label_symbol.grid(column=2,row=0)

window_input.grid(column=0,row=1,sticky="NSEW")
frameLex.grid(sticky="NSEW",column=1,row=1)

treeLex.grid(column=0,row=0,columnspan=1,sticky="NSEW")
verticalScroll.grid(column=1,row=0, columnspan=1, sticky="NSEW")


frameSymbol.grid(sticky="NSEW",column=2,row=1)
treeSymbol.grid(column=0,row=0,columnspan=1,sticky="NSEW")
verticalScrollSymbol.grid(column=1,row=0,columnspan=1,sticky="NSEW")


execute_btn.grid(column=0, row=2,sticky="EW", columnspan=3)
window_output.grid(column=0,row=3,columnspan=3,rowspan=1,sticky="nsew")


window.mainloop()