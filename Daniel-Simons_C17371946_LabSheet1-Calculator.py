#!/usr/bin/env python
# coding: utf-8

# In[9]:


#Import statement, tkinter is a module which allows us to create a gui
from tkinter import *
#The expression variable is what the calculator will use to get the answer
expression = "" 


# In[22]:


#This function is called when a button with a value is pressed, this value is then added to the expression variable and displayed
def press(num):
    global expression
    expression = expression + str(num)
    #This shows the user the expression
    equation.set(expression)
    
    


# In[18]:


#This function is called when the equals sign is pressed
def equals():
    #It attempts to take the expression created and solve it
    try:
        global expression 
        total = str(eval(expression))
        #After it is evaluated, it sets the output to the answer and then the expression is now just the total
        equation.set(total)
        expression = total
        
    except: 
        #This except is called if an error occurs in the evaluating or in any part of it, it sets the expression to empty
        equation.set(" error ") 
        expression = "" 


# In[19]:


#This function is to allow the user to remove the last character of the expression
def bspace():
    global expression
    lenofexpr = (len(expression))
    #It uses a slice to take the last character away from the expression
    x = slice(0,len(expression)-1)
    expression = expression[x]
    equation.set(expression)


# In[20]:


#This function clears the output of the calculator and the expression
def AC():
    global expression 
    expression = ""
    equation.set("")


# In[23]:


#This function is where the buttons are defined and the gui is created
if __name__ == "__main__":
    #This is the configuration of the gui
    gui = Tk()
    gui.configure(background="grey")
    gui.title("Calculator")
    gui.geometry("545x335")
    
    #This is the creation of the input field or where the expression is shown on the calculator
    equation = StringVar()
    expression_field = Entry(gui,font = "Helvetica 32 bold", textvariable=equation)
    expression_field.grid(columnspan=14)
    equation.set('0') 
  
    #These are the configurations of the number buttons on the calculator
    #Each button is given the gui object, the text it will display, the colour of the text, the colour of the background
    #the function the button will have, the height and the width of the button
    #The buttons are also given their grid placement within the calculator 
    button1 = Button(gui, text=' 1 ', fg='black', bg='white',
                     command=lambda: press(1), height=3, width=18) 
    button1.grid(row=3, column=0) 
  
    button2 = Button(gui, text=' 2 ', fg='black', bg='white', 
                     command=lambda: press(2), height=3, width=18) 
    button2.grid(row=3, column=1) 
  
    button3 = Button(gui, text=' 3 ', fg='black', bg='white', 
                     command=lambda: press(3), height=3, width=18) 
    button3.grid(row=3, column=2) 
  
    button4 = Button(gui, text=' 4 ', fg='black', bg='white', 
                     command=lambda: press(4), height=3, width=18) 
    button4.grid(row=4, column=0) 
  
    button5 = Button(gui, text=' 5 ', fg='black', bg='white', 
                     command=lambda: press(5), height=3, width=18) 
    button5.grid(row=4, column=1) 

    button6 = Button(gui, text=' 6 ', fg='black', bg='white', 
                     command=lambda: press(6), height=3, width=18) 
    button6.grid(row=4, column=2) 
  
    button7 = Button(gui, text=' 7 ', fg='black', bg='white', 
                     command=lambda: press(7), height=3, width=18) 
    button7.grid(row=5, column=0) 
  
    button8 = Button(gui, text=' 8 ', fg='black', bg='white', 
                     command=lambda: press(8), height=3, width=18) 
    button8.grid(row=5, column=1) 
  
    button9 = Button(gui, text=' 9 ', fg='black', bg='white', 
                     command=lambda: press(9), height=3, width=18) 
    button9.grid(row=5, column=2) 
  
    button0 = Button(gui, text=' 0 ', fg='black', bg='white', 
                     command=lambda: press(0), height=3, width=18) 
    button0.grid(row=6, column=0) 
    
    
  
    #These are the functionality buttons, these buttons add, subtract, multiply and divide 
    # They have the same setup as the previous buttons
    
    plus = Button(gui, text=' + ', fg='black', bg='white', 
                  command=lambda: press("+"), height=3, width=18) 
    plus.grid(row=3, column=3) 
  
    minus = Button(gui, text=' - ', fg='black', bg='white', 
                   command=lambda: press("-"), height=3, width=18) 
    minus.grid(row=4, column=3) 
  
    multiply = Button(gui, text=' * ', fg='black', bg='white', 
                      command=lambda: press("*"), height=3, width=18) 
    multiply.grid(row=5, column=3) 
  
    divide = Button(gui, text=' / ', fg='black', bg='white', 
                    command=lambda: press("/"), height=3, width=18) 
    divide.grid(row=6, column=3) 
        
    Decimal= Button(gui, text='.', fg='black', bg='white', 
                    command=lambda: press('.'), height=3, width=18) 
    Decimal.grid(row=6, column=1) 
    
    
    
    #These buttons are more functionality buttons but have commands that are linked the the functions defined above
    equal = Button(gui, text=' = ', fg='black', bg='light grey', 
                   command=equals, height=3, width=18) 
    equal.grid(row=6, column=2) 
  
    clear = Button(gui, text='AC', fg='black', bg='light grey', 
                   command=AC, height=3, width=18) 
    clear.grid(row=2, column=0) 
  
    backspace = Button(gui, text='<--', fg='black', bg='light grey',
                      command=bspace, height=3, width=18)
    backspace.grid(row=2, column=3)
    
    # This starts the GUI 
    gui.mainloop() 
    


# In[ ]:




