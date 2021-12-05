import tkinter as tk
import tkinter.ttk as ttk

from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import simpledialog
import re
import textwrap

print("+++++++++++++++++++++++++++")
#============ GUI RELATED ============#



def wrap(string, lenght=20):#Wrap text so it looks neater in rows
    return '\n'.join(textwrap.wrap(string, lenght))

window = tk.Tk()#root

window.title("Lolcode interpreter")
buttonPress = tk.StringVar()

label_lex =tk.Label(window, text="Lexemes",font=("Arial Bold",12))#text labels
label_symbol=tk.Label(window, text="Symbols",font=("Arial Bold",12))

#Lexemes table
frameLex=tk.Frame(window)
treeLex = ttk.Treeview(frameLex, columns=('Code','Classification'),show="headings",selectmode='browse',height=6)#use treeLexview for table
treeLex.heading("#1",text="Code")
treeLex.heading("#2",text="Classification")

treeLex.column("#1",stretch=tk.YES)
treeLex.column("#2",stretch=tk.YES)

# for i in range(4): #Insert data
#     treeLex.insert(parent='',index='end',iid=i,values=(wrap("Hello"+str(i)), wrap("Worwws\nwwwww\nwwww\nwwww")))

styleTree = ttk.Style()
styleTree.configure('Treeview',rowheight=30)

verticalScroll = ttk.Scrollbar(frameLex,  orient ="vertical",  command = treeLex.yview) 
treeLex.configure(yscrollcommand=verticalScroll.set)
#Lexemes table end


#Symbols table end

frameSymbol=tk.Frame(window)
treeSymbol = ttk.Treeview(frameSymbol, columns=('Code','Classification'),show="headings",selectmode='browse',height=6)#use treeLexview for table
treeSymbol.heading("#1",text="Code")
treeSymbol.heading("#2",text="Value")

treeSymbol.column("#1",stretch=tk.YES)
treeSymbol.column("#2",stretch=tk.YES)

# for i in range(4): #INSERT DATA
#     treeSymbol.insert(parent='',index='end',iid=i,values=(wrap("Hello"+str(i)), wrap("Wowww\nwwww\nwwww")))

verticalScrollSymbol = ttk.Scrollbar(frameSymbol,  orient ="vertical",  command = treeSymbol.yview) 
treeSymbol.configure(yscrollcommand=verticalScrollSymbol.set)

#Symbols table end

#============ GUI RELATED END ============#




#===== DATA STRUCTURES ===== 

lexemeList=[]#List of Lexemes

symbolList={"IT":None}#List of Symbols

valid_operators={
    "SUM OF ":"+",
    "QUOSHUNT OF ":"/",
    "PRODUKT OF ":"*",
    "MOD OF ":"%",
    "DIFF OF ":"-",  
    "BIGGR OF ":"max",
    "SMALLR OF ":"min",
}

valid_bool_operators=[
    "BOTH OF ",
    "EITHER OF ",
    "WON OF ",
    "NOT ",
    "ALL OF",
    "ANY OF"
]

valid_comparison_operators=[
"BOTH SAEM ", #==
"DIFFRINT ", # !=
"BIGGR OF ",
"SMALLR OF "
]


#===== DATA STRUCTURES END ===== 


def clicked():#File open dialog
    fileName = filedialog.askopenfilename(filetypes = (("Lolcode","*.lol"),))#lol files only
    # fileName = "io.lol"

   
    try:
        with open(fileName,'r') as fileHandler:
            window_input.delete("1.0","end")#deletes old text from window
            window_input.insert(tk.INSERT,fileHandler.read())  

    except IOError:#in case user does not choose anything
        print("No file has been chosen")



def deleteTable():#Delete everything every time you execute the program
    treeSymbol.delete(*treeSymbol.get_children())
    treeLex.delete(*treeLex.get_children())
    for row in treeSymbol.get_children():
    	treeSymbol.delete(row)
    lexemeList.clear()
    symbolList.clear()
    for row in treeLex.get_children():
    	treeLex.delete(row)
    window_output.configure(state="normal")
    window_output.delete("1.0","end")


def evaluateExpression(line):#Recursive function for nested conditions


    if re.search("^-?[0-9]+$",line): #Base Case = only NUMBR left
        print("Returning Variable "+str(line)) 
        return line
    elif re.search("^-?[0-9]+?.[0-9]+$",line): #Base Case = only NUMABR left
        print("Returning Variable "+str(line))
        return line
    else:
        print("LINE [",line,"]")

        for operator in valid_operators.keys():
           
            solve = re.search(operator+"((-?[0-9]+.[0-9]+)|(-?[0-9]+)) AN ((-?[0-9]+.[0-9]+)|(-?[0-9]+))", line)
           

            if solve!=None:
                print("New: ["+solve.group()+"]")
                print("Solve")

                term1 = re.sub(" AN ((-?[0-9]+.[0-9]+)|(-?[0-9]+))$","", solve.group())
                term1 = re.sub(operator,"", term1)
                print("Term1: "+term1)

                term2 = re.sub(operator+"((-?[0-9]+.[0-9]+)|(-?[0-9]+)) AN ","",solve.group())
                print("Term2: "+term2)

                lexemeList.append((operator,"Arithmetic Operator"))
                dataType(term1,"Never")
                dataType(term2,"Gonna")

                if(operator=="PRODUKT OF "):

                    if re.search('\.',term1) or re.search('\.',term2):
                        variable=float(term1)*float(term2)
                    else:
                        variable=int(term1)*int(term2)

                elif(operator=="QUOSHUNT OF "):

                    if re.search('\.',term1) or re.search('\.',term2):
                        variable=float(term1)/float(term2)
                    else:
                        variable=int(term1)/int(term2)
                        variable=int(variable) 

                elif(operator=="MOD OF "):

                    if re.search('\.',term1) or re.search('\.',term2):
                        variable=float(term1)%float(term2)
                    else:
                        variable=int(term1)%int(term2)

                elif(operator=="SUM OF "):
                    print("ADD")
                    if re.search('\.',term1) or re.search('\.',term2):
                        variable=float(term1)+float(term2)
                    else:
                        variable=int(term1)+int(term2)
                    
                    
                elif(operator=="DIFF OF "):

                    if re.search('\.',term1) or re.search('\.',term2):
                        variable=float(term1)-float(term2)
                    else:
                        variable=int(term1)-int(term2)


                elif(operator=="BIGGR OF "):

                    if re.search('\.',term1) or re.search('\.',term2):
                        if float(term1)>float(term2):
                            variable = float(term1)
                        else:
                            variable = float(term2)
                    else:
                        if int(term1)>int(term2):
                            variable = int(term1)
                        else:
                            variable = int(term2)

                else: #SMALLR OF

                    if re.search('\.',term1) or re.search('\.',term2):
                        if float(term1)>float(term2):
                            variable = float(term2)
                        else:
                            variable = float(term1)
                    else:
                        if int(term1)>int(term2):
                            variable = int(term2)
                        else:
                            variable = int(term1)

                print("Calc: ",variable)
                print("Remaining: "+re.sub(solve.group(0), str(variable),line) )
                remaining = re.sub(solve.group(0), str(variable),line).strip()

                # print("Remaining: "+re.sub(solve, str(variable),line) )
                return evaluateExpression(remaining)
            
               
  
        return line


def evaluateBoolExpression(line): #Recursive function for nested conditions

    line = line.replace("NOT WIN","FAIL")#Remove at the start every time because it is possible to have "NOT [bool_operator]"
    line = line.replace("NOT FAIL","WIN")

    if re.search("^WIN$", line) or re.search("^FAIL$", line) :#BASE CASE
        print("Final Answer: ", line)
        return line

    else:
        
        if re.search("^ALL OF", line):#Infinite arity and
            
            no_operators_left = True

            for operator in valid_bool_operators[:-2]:#Check if there is a boolean operator that still needs to be solved          
                solve = re.search(operator, line)
                if solve!=None:
                    no_operators_left=False
                    break

            if no_operators_left==True:#if no boolean operators left, try to find one "FAIL"

                lexemeList.append(("ALL OF ","Infinite Arity And"))

                if re.search("FAIL", line):
                    print("Final Answer: FAIL")
                    return "FAIL"
                else:
                    print("Final Answer: WIN")
                    return "WIN"
        
        elif re.search("^ANY OF", line): #Infinite arity or
           
            no_operators_left = True

            for operator in valid_bool_operators[:-2]:#Check if there is a boolean operator that still needs to be solved        
                solve = re.search(operator, line)
                if solve!=None:
                    no_operators_left=False
                    break

            if no_operators_left==True: #if no boolean operators left, try to find one "TRUE"

                lexemeList.append(("ANY OF ","Infinite Arity And"))
                if re.search("WIN", line):
                    print("Final Answer: WIN")
                    return "WIN"
                else:
                    print("Final Answer: FAIL")
                    return "FAIL"



        print("LINE <",line,">")

        for operator in valid_bool_operators:

            solve = re.search(operator+"(WIN|FAIL) AN (WIN|FAIL)", line)

            if solve!=None:

                print("New: ["+solve.group()+"]")               
                term1 = re.sub(" AN (WIN|FAIL)$","", solve.group())
                term1 = re.sub(operator,"", term1)

                print("Term1: "+term1)

                term2 = re.sub(operator+"(WIN|FAIL) AN ","",solve.group())

                print("Term2: "+term2)
                variable = "meow"

                lexemeList.append((operator,"Boolean Operator"))
                dataType(term1,"Give")
                dataType(term2,"You")


                if(operator=="BOTH OF "):#AND

                    if term1=="FAIL" or term2=="FAIL":
                        variable = "FAIL"
                    else:
                        variable = "WIN"

                elif(operator=="EITHER OF "):#OR 
                    if term1=="WIN" or term2=="WIN":
                        variable = "WIN";
                    else:
                        variable = "FAIL"

                elif(operator=="WON OF "):#XOR 
                    if term1!=term2:
                        variable = "WIN"
                    else: 
                        variable = "FAIL"

                print("Calc: ",variable)
            
                remaining = re.sub(solve.group(0), variable,line).strip()
                print("Remaining [",remaining,"]")
    
                return evaluateBoolExpression(remaining)

                break

        return line


def evaluateCompExpression(line): #Recursive function for nested conditions

    if re.search("^WIN$", line) or re.search("^FAIL$", line):#BASE CASE
        return line
    else:

        print("Current Line <", line,">")
        for operator in valid_comparison_operators:
            
            solve = re.search(operator+"((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL)|(\".*\")) AN ((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL)|(\".*\"))", line)###PROBLEM

            if solve!=None:
     

                print("New: ["+solve.group()+"]")
                print("Solve")

                term1 = re.sub(" AN ((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL)|(\".*\"))$","", solve.group())
                term1 = re.sub(operator,"", term1)
                print("Term1: "+term1)

                term2 = re.sub(operator+"((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL)|(\".*\")) AN ","",solve.group())
                print("Term2: ",term2)

                lexemeList.append((operator,"Comparison Operator"))
                lexemeList.append(("OMG","Switch Condition"))
                dataType(term1,"Up")
                dataType(term2,"Never")

                if(operator=="BOTH SAEM "):

               

                    if re.search('\.',term1) and not re.search('\.',term2): #If only one is a NUMBAR
                        variable =  "FAIL"
                    if not re.search('\.',term1) and re.search('\.',term2): #If only one is a NUMBAR
                        variable = "FAIL"

                    if term1==term2:
                        variable =  "WIN"
                    else:
                        variable =  "FAIL"

                elif(operator=="DIFFRINT "):

                    if re.search('\.',term1) and not re.search('\.',term2): #If only one is a NUMBAR
                        variable = "FAIL"
                    elif not re.search('\.',term1) and re.search('\.',term2): #If only one is a NUMBAR
                        variable = "FAIL"

                    if term1!=term2:
                        variable = "WIN"
                    else:
                        variable = "FAIL"

                elif(operator=="BIGGR OF "):

                    if re.search('\.',term1) or re.search('\.',term2):

                        if float(term1)>=float(term2):
                            variable = float(term1)
                        else:
                            variable = float(term2)

                    else:
                        if int(term1)>=int(term2):
                            variable = int(term1)
                        else:
                            variable = int(term2)

                elif(operator=="SMALLR OF "):

                    if re.search('\.',term1) or re.search('\.',term2):
                        if (float(term1)<=float(term2)):
                            variable = float(term1)
                        else:
                            variable = float(term2)
                    else:
                        if (int(term1)<=int(term2)):
                            variable = int(term1)
                        else:
                            variable = int(term2)
                    


                print("Calc: ",variable)
    
                print("Remaining: "+re.sub(solve.group(0), str(variable),line) )
                remaining = re.sub(solve.group(0), str(variable),line).strip()

                # print("Remaining: "+re.sub(solve, str(variable),line) )
                return evaluateCompExpression(remaining)
            
                


        return line



def dataType(value,possibleName):

    if re.search("^\".*\"", value):#YARN or STRING
        lexemeList.append(("\"","String delimiter"))
        value1=re.sub("^\"","",value)
        value1=re.sub("\"$","",value1)
        print("String: "+value1 )
        lexemeList.append((value1,"YARN"))
        lexemeList.append(("\"","String delimiter"))

    elif re.search("(-?[0-9]+)", value):
        lexemeList.append((value,"NUMBR"))
    elif re.search("(-?[0-9]+.[0-9]+)", value):
        lexemeList.append((value,"NUMBAR"))
    elif re.search("(WIN)|(FAIL)", value):
        lexemeList.append((value,"Boolean Value"))
    else:
        print("Value Unknown ",value)

def checkifBoolExpression(value): #Check if boolean expression
    for operator in valid_bool_operators:
        if(re.search(operator,value)):
            print("Boolean Expression")
            return True
    return False

def checkifCompExpression(value): #Check if comparison expression
    for operator in valid_comparison_operators:
        if(re.search(operator,value)):
            print("Comp Expression")
            return True
    return False


def checkifExpression(value): #Check if arithmetic expression
    
    for operator in valid_operators.keys():
        if(re.search("^"+operator,value)):
            print("Arithmetic Expression")
            return True

    return False

def varRemoval_For_Expressions(line): #Remove variables from expressions

    for symbol in symbolList.keys():
        if(re.search(" "+symbol,line)):
            lexemeList.append((symbol,"Variable"))
            line=re.sub(" "+symbol," "+str(symbolList[symbol]),line)
    print("Current Line [",line,"] after variable removal")
    return line

def checkifAnyExpression(line):
    if checkifBoolExpression(line) or checkifCompExpression(line) or checkifExpression(line):
        return True
    return False

def evaluateAnyExpression(value, possibleName):#Recursive function for solving expressions with different operators

  if re.search("^((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL))$", value):#BASE CASE
    print("Evaluate Any Expression Return <",value,">")
    symbolList['IT']=value
    return value

  else:
    value = re.sub(possibleName+" R", "",value )

    value = varRemoval_For_Expressions(value)

    value = evaluateExpression(value)

    value = evaluateBoolExpression(value)
      
    value = evaluateCompExpression(value )

    evaluateAnyExpression(value, possibleName)
    
    return value
  



def visibleStatement(line):
    line=line.strip()
    if line=="":
      print("Visible Return")
      return
    else:
      print("Current Line [",line,"]")


   
      if re.match("^\"[^\"]+\"", line):#STRING

        if re.match("^\"[^\"]+\"$", line):
          print("First")
          newString = re.match("^\"[^\"]+\"$", line)
        else:
          print("Second")
          newString = re.match("\"[^\"]+\" ", line)

        window_output.configure(state="normal")#unlock window for output
        window_output.insert(tk.INSERT,str(newString.group())+"\n")
        window_output.configure(state="disabled")#unlock window for output

        if newString.group()==line:
            print("They are equal")
        else:
            print("Nope")


        print("Visible string: <",newString.group(),">")
        line=re.sub(newString.group().replace("?","\?"), "", line).strip() #If you don't replace "?" with "/?" in regex, it will cause infinite loops for strings with "?"

        print("Remaining: <",line,">")

        visibleStatement(line)

      elif checkifAnyExpression(line):

        value = evaluateAnyExpression(line,"IT")
        print("Visible Expression: ",value)

        window_output.configure(state="normal")#unlock window for output
        window_output.insert(tk.INSERT,value+"\n")
        window_output.configure(state="disabled")#unlock window for output
        return
        

      elif re.search("^((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL)|[A-Za-z][A-Za-z0-9_]+)*",line):
        newData=re.search("((-?[0-9]+.[0-9]+)|(-?[0-9]+)|(WIN|FAIL)|[A-Za-z][A-Za-z0-9_]+)*",line)


        window_output.configure(state="normal")#unlock window for output
        if newData.group() in symbolList:
          line = re.sub(newData.group(),symbolList[newData.group()],line)

        else:
          window_output.insert(tk.INSERT,str(newData.group())+"\n")
          line = re.sub(newData.group(),"",line)
          print("Visible Data: ", str(newData.group()))

        
        
        window_output.configure(state="disabled")#unlock window for output


        


        visibleStatement(line)

def identify(line,haiFlag,baiFlag, multiLine,stop, falseFlag ): #break down into lexemes (VERY LONG if else, reads lines seperated by newline)

    print("Current line <"+line+">")
    comment=''
    line = line.strip()

    if re.search("^\s*$",line):#Skip line if blank
        return haiFlag, baiFlag, multiLine, False, falseFlag

    if not haiFlag: #Accept only comments and HAI for the start of the file

        if multiLine:#Multiline comments
            if re.search("^TLDR$",line):
                comment = re.sub("^TLDR$","",line).strip()
                lexemeList.append(("TLDR", "Multiline Comment end"))
                multiLine=False
            else:
                lexemeList[len(lexemeList)-1]=((lexemeList[len(lexemeList)-1][0]+"\n"+line).strip(),"Multiline comment")

        elif re.search("^HAI",line):#HAI
            lexemeList.append( ("HAI", "Code Delimiter"))
            haiFlag=True
        elif re.search("^BTW",line):#COMMENTS
            lexemeList.append( ("BTW", "Single Line Comment Identifier"))
            comment = re.sub("^BTW","",line).strip()
            lexemeList.append( (comment,"Single Line Comment"))

        elif re.search("^OBTW",line):#MULTILINE COMMENTS
            lexemeList.append(("OBTW", "Multiline Comment Identifier"))
            comment=re.sub("^OBTW","",line).strip()
            lexemeList.append((comment, "Multiline comment"))
            multiLine=True


    elif falseFlag:#Indicates if the statements should be skipped
        
        if re.search("GTFO",line):#If-else checks if the statements should not be skipped
            lexemeList.append(("GTFO","Break"))
            falseFlag=False 

        elif re.search("^OMGWTF",line):
            lexemeList.append(("OMGWTF","Default Switch Condition"))
            falseFlag=False     

        elif re.search("^OMG",line):
            lexemeList.append(("OMG","Switch Condition"))
            value = re.sub("OMG ","",line)
            print("Value: ",value)
            if int(value)==int(symbolList["IT"]):
                print("Condition is True")
                falseFlag=False

        elif re.search("NO WAI",line):
            lexemeList.append(("NO WAI","False Condition"))
            falseFlag=False

    else:

        if multiLine:#Check if multiline comment
            if re.search("^TLDR$",line):
                comment = re.sub("^TLDR$","",line).strip()
                lexemeList.append(("TLDR", "Multiline Comment end"))
                multiLine=False
            else:
                lexemeList[len(lexemeList)-1]=((lexemeList[len(lexemeList)-1][0]+"\n"+line).strip(),"Multiline comment")


        elif re.search("^I HAS A [A-Za-z][A-Za-z0-9_P]*",line):#Variable Declaration
            
            print("Variable Declaration")


            lexemeList.append( ("I HAS A", "Variable Declaration"))
            possibleVar = re.sub("^I HAS A ","",line)

            if re.search("^[A-Za-z][A-Za-z0-9_]*$", possibleVar):#uninitialized = noob
                print("No data type");
                symbolList[possibleVar]="NOOB"
                lexemeList.append((possibleVar,"Variable Identifier"))

            else:#has a data type
                possibleName = re.sub(" ITZ .+$","",possibleVar)
                lexemeList.append(("ITZ", "Variable assignment"))
                print("Name: "+possibleName)
                value = re.sub("^[A-Za-z][A-Za-z0-9_]* ITZ ","",possibleVar)#Check what Type value is
                print("Value Orig: "+value)

                if checkifAnyExpression(value):

                    value = evaluateAnyExpression(value, possibleName)


                if value in symbolList:
                    print("ITS IN SYMBOL LIST")
                    symbolList[possibleName]=symbolList[value]
                else:
                    symbolList[possibleName]=value

               
                dataType(value,possibleName)

        elif re.search("^[A-Za-z][A-Za-z0-9_]* R .+$", line):#Variable Assignment
            print("Variable Assignment")
            possibleName = re.sub(" R .+$","",line)
            lexemeList.append(("R","Variable Assignment"))
            value = re.sub("^[A-Za-z][A-Za-z0-9_]* R ","",line)
            value=value.strip()  
            print("Value:["+value+"]")


            if checkifAnyExpression(value):
                value = evaluateAnyExpression(value, possibleName)

            print("Assign Name: ["+possibleName+"]"," = ",value)

            if possibleName in symbolList:#Assign to existing variable

                symbolList[possibleName]=value#add value to symbolList
                # dataType(value,possibleName)#add lexemes

            elif re.search("IT$",possibleName):#FOR IT VARIABLE
                symbolList["IT"]=value
            else:#Variable doesn't exist
                window_output.configure(state="normal")#unlock window for output
                window_output.insert(tk.INSERT,possibleName+" does not exist\n")
                window_output.configure(state="disabled")#unlock window for output
                return haiFlag, baiFlag, multiLine, True, falseFlag




        elif re.search("^BTW",line):#Comments
            lexemeList.append( ("BTW", "Single Line Comment Identifier"))
            comment = re.sub("^BTW","",line).strip()
            lexemeList.append( (comment,"Single Line Comment"))

        elif re.search("^OBTW",line):#Multiline comment
            lexemeList.append(("OBTW", "Multiline Comment Identifier"))
            comment=re.sub("^OBTW","",line).strip()
            lexemeList.append((comment, "Multiline comment"))
            multiLine=True

        elif re.search("^VISIBLE ",line):#Printing
            lexemeList.append(("VISIBLE","Print in Terminal"))
            possibleVar = re.sub("^VISIBLE ","",line) 
            possibleVar = str(possibleVar)

            visibleStatement(possibleVar)

        elif checkifAnyExpression(line):#Expression
                value=evaluateAnyExpression(line,"IT")



        elif re.search("^WTF?", line):#Switch Start
            lexemeList.append(("GIMMEH","User Input"))


        elif re.search("OMG .+",line):#Switch Condition
            print("Condition")
            lexemeList.append(("OMG","Switch Condition"))
            value = re.sub("OMG ","",line)
            if value in symbolList:
                value=symbolList[value]
            print("Value: ",value)
            if int(value)==int(symbolList["IT"]):
                print("Condition is True")
                falseFlag=False
            else:
                print("Condition is False")
                falseFlag=True
        elif re.search("OMGWTF",line):#Default Switch Case
            lexemeList.append(("OMGWTF","Default Switch Case"))
            falseFlag=False
        elif re.search("GTFO",line):#Condition Break
            lexemeList.append(("GTFO","Condition Break"))
         
        elif re.search("OIC",line):#Switch Ending Statement
            lexemeList.append(("OIC","Switch Ending Statement"))
            falseFlag=False

        elif re.search("GIMMEH ",line):#User INput
            possibleVar = re.sub("GIMMEH ","",line)
            lexemeList.append(("GIMMEH","User Input"))
            lexemeList.append((possibleVar,"Variable"))
            print("Possible Input Var: <",possibleVar,">")


            label_widget = tk.Label(window, text="User Input Here:")#Input text window will pop up
            terminal_input = tk.Entry(window)
            terminal_input.grid(column=1,row=4,columnspan=2,rowspan=1,sticky="nsew")
            label_widget.grid(column=0,row=4,columnspan=1,rowspan=1,sticky="nsew")

            terminal_input.insert(tk.END,'')
            terminal_input.bind('<Return>',sendInput)#Input window will send variable if the user presses ENTER
          

            window.wait_variable(buttonPress)#GUI loop will wait for input of user

            data = terminal_input.get()
            print("terminal_input: ",data)

            lexemeList.append((str(data),"Variable"))

            if re.search("^(-?[0-9]+.[0-9]+)|(-?[0-9]+)$",str(data)):#number
                symbolList[possibleVar]=str(data)
                print("NUMBER")
            else:
                symbolList[possibleVar]="\""+str(data)+"\""
            
            label_widget.grid_forget()#Input window disappears
            terminal_input.grid_forget()
 

            return haiFlag, baiFlag, multiLine, False, falseFlag
            
        elif re.search("O RLY?",line):#If Else
            lexemeList.append(("O RLY?","Condition Statement"))
            if symbolList["IT"]=="WIN":
                print("True")
                falseFlag=False
            else:
                print("False")
                falseFlag=True

        elif re.search("YA RLY",line):#If Else
            lexemeList.append(("YA RLY","True Condition Statement"))


  
        else:
            print("Last line", line)
            window_output.insert(tk.INSERT,"ERROR\n")#Add things here
            print("STOPPU")
            return haiFlag, baiFlag, multiLine, True, falseFlag
            

    return haiFlag, baiFlag, multiLine, False, falseFlag



def sendInput(line):
    buttonPress.set("meow")



def interpret(): #Add all the functions for interpeting here
    deleteTable()

    inputLines=window_input.get("1.0","end")#Add code to the symbol and lexemes table
    inputList= re.split('\n', inputLines)
    inputList = list(map(str.strip,inputList))

    haiFlag=False
    baiFlag=False
    falseFlag = False
    multiLine=False#so it knows next lines are comments
    stoppu=False


    
    for line in inputList:#Interpret line by line
        haiFlag, baiFlag, multiLine,stoppu, falseFlag=identify(line,haiFlag,baiFlag, multiLine,stoppu,falseFlag)
        if(stoppu):
            break

    
    # print("LEXEMES")
    # print(lexemeList)

    print("SYMBOLS")
    print(symbolList)


    for i in range(len(lexemeList)):#insert symbols and lexeme into the tables
        treeLex.insert(parent='',index='end',iid=i,values=(wrap(lexemeList[i][0]), wrap(lexemeList[i][1])))


    i=0
    for key,value in symbolList.items():
        if value==None:
            treeSymbol.insert(parent='',index='end',iid=i,values=(wrap(key), wrap("NOOB")))
        else:
            treeSymbol.insert(parent='',index='end',iid=i,values=(wrap(key), wrap(value)))
        i+=1


    window_output.configure(state="normal")#unlock window for output
    
    # window_output.insert(tk.INSERT,"THE BIG GAY\n")#Add things here
    
    window_output.configure(state="disabled")#lock window for output
    # deleteTable()





def gimmehInput():
    
    var = buttonPress.set("button pressed")
    
#EVERYTHING GUI RELATED 



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