#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cx_Oracle #import the Oracle Python library
import getpass 
import pandas as pd
import datetime #This is used for date time objects
from datetime import timedelta  #This is used to add days to dates

#This will combine the date with the time and convert it to a datetime object
def timeselection(screenid,showtime1):

    #date_time_obj = datetime.strptime(showtime, '%Y-%m-%d')
    #print(date_time_obj)
    print("--------------TIME SLOT---------------")
    print("Slots taken in Screen:",screenid,showtime1)
    try:
        #This query selects all showings showing in selected screen
        sqlquery = "select  SLOTID,SHOWTIME,SCREEN_SCREENNO,FILM_FILMID,filmlength from dt2283group_p.showingslot join dt2283group_p.film on filmid = dt2283group_p.showingslot.film_filmid  where screen_screenno = :1 order by showtime"
        cur.execute(sqlquery,(screenid,))#VERY IMPORTANT FOR FUTURE SELF, THIS RIGHT HERE MAKES IT A TUPLE
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        for row in cur: 
            #This for loop gets the vaulues from the rows and prints them to the screen
            slotid,showtime,screenno,filmid,filmlength= row
            
            print("-",slotid,"|------|",showtime.time(),showtime.date(),"|------|",screenno,"|---------|",filmid,"|---------|")
        print("--------------------------------------------------------------------------------------------------------------")
    #Try and catch so user enters correct input
    try:
        print("Please select a time for this showing slot ")
        time = input()
        hmm = showtime1+" "+time
        hmm2 = datetime.datetime.strptime(hmm,'%Y-%m-%d %H:%M:%S')
 
    except (ValueError,TypeError):
        print("Oops!  That was no date.  Try again...")
        timeselection(screenid,showtime1)
        
    #v_datetime >= showtime) and (v_datetime <= showtime + filmlength/(24*60));
     #To make sure the time doesnt overlap with another film   
    if hmm2 >= showtime and hmm2 <= (showtime + timedelta(minutes = filmlength)):
            print("time already taken")
            timeselection(screenid,showtime1)
    else:
        #Returns the datetime object
        print(hmm2)
        return hmm2
            
#This will allow the user to select a screen 
def screenselection():
    print("--------------SCREENS---------------")
    print("Please select the screen number of the screen you want this film to be played in")
    
    try:
        #Query to select all avaiable screens
        cur.execute("select * from dt2283group_p.cinemascreen")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        for row in cur:
            #Takes the values and prints
            #Rows from queries are tuples 
            screenid,theathre = row
            print("Screen Number:",screenid)
            
    try:
        value = int(input())
        if(value>screenid or value <1):
            print("Please enter a valid screen number")
            screenselection()
        else:
            return value
        
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
        screenselection()
        

#User selects a film from a selection displayed            
def filmselection():
    print("--------------FILM---------------")
    print("-FILM ID--------Film Name--------Available from-------Rating")
    
    try:
        cur.execute("select * from dt2283group_p.film")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        print("Please select the ID of the film you want for this slot")
        for row in cur:
            filmid,filmname,filmrating,filmdirector,filmlanguage,filmsubtitles,filmlength,AVAILABLEFROM = row
            print(filmid,"|------|",filmname,"||",AVAILABLEFROM.date().strftime("%Y-%m-%d "),"||",filmrating)
    
    #The last id produced will be the biggest and this if statement makes sure the user cannot select a higher value
    try:
        fid = int(input())
        if(fid>filmid or fid<1):
            print("Please enter a correct ID")
            filmselection()
        else:
        
            print(fid,"Selected")
            return fid
        
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
        filmselection()
    
    
#Selects the date for the film, The movies can only be changed within a week    
def dateselection():
    print("--------------DATE---------------")
    print("Please choose a date within the next 7 days")
    print("Selected the labelled number on the side")

    #Displays the next week
    for x in range(7):
        now = datetime.datetime.now()
        now = now + timedelta(days=x)
        print (x,":",now.strftime("%Y-%m-%d "))
    #user input cannot be out of this range   
    try:
        choice = int(input())
        if(choice>=0 and choice <=6):
            print("Selected option:",choice)
            returndate = datetime.datetime.now()
            return (returndate + timedelta(days=choice)).strftime("%Y-%m-%d ")#Time delta used to add days to the current date

        else:
            print("Please select an option from the list")
            dateselection()
        
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
        dateselection()
    
    
 #This function calls the other function and calls the sql function
#It also creates the id value for slot by querying the last id in the table 
def addShowingSlot():
    print("Creating..")
    try:
        cur.execute("select SLOTID from dt2283group_p.showingslot where SLOTID=(select max(SLOTID) from dt2283group_p.showingslot)")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        for row in cur:
            slotmaxid, = row
            slotmaxid+=1
    print("Creation Begun")
    showtime = dateselection()
    print(showtime)
    print("---------------------------------")
    filmid = filmselection()
    print("---------------------------------")
    screenid = screenselection()
    print("---------------------------------")
    timeslot = timeselection(screenid,showtime)
    
    #Function returns a boolean to which the system returns the current showings of films
    success = cur.callfunc('dt2283group_p.c_showingslot', bool, [timeslot,filmid,screenid,slotmaxid])
    
    print(success)
    try:
        print('Showing Slot -----Viewing Time------Screen Number-----Film ID-----------Film Name')
        cur.execute('select SLOTID,SHOWTIME,SCREEN_SCREENNO,FILM_FILMID,FILMNAME from dt2283group_p.showingslot join dt2283group_p.film on filmid = dt2283group_p.showingslot.film_filmid Order by slotid desc')
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        for row in cur:
            slotid,showtime,screenno,filmid,filmname = row
            print("-",slotid,"|------|",showtime.time(),showtime.date(),"|------|",screenno,"|---------|",filmid,"|---------|",filmname)
            print("--------------------------------------------------------------------------------------------------------------")
    
#First choice the user can make         
def userChoice():
        print("Would you like to addd a showing? ")
        userchoice = input()
        if userchoice == 'y' or userchoice == 'Y':
            addShowingSlot()
        else:
            print("Please enter either 'y' or 'Y'")
            userChoice()


p_username = ""# define the login details
p_password = ""
print('Please enter your username')
p_username = input()
print('Please enter your password')
p_password = getpass.getpass()#Accepts a password without showing it.
p_host = ""
p_service = ""
p_port = ""
# create the connection
print('Establishing Connection')
try:
    con = cx_Oracle.connect(user=p_username, 
                        password=p_password, 
                        dsn=p_host+"/"+p_service+":"+p_port)
    
    print("Database version:", con.version)
    print("Oracle Python version:", cx_Oracle.version)
    
    cur = con.cursor()
    
    # execute a query returning the results to the cursor
    try:
        print('Showing Slot -----Viewing Time------Screen Number-----Film ID-----------Film Name')
        cur.execute('select SLOTID,SHOWTIME,SCREEN_SCREENNO,FILM_FILMID,FILMNAME from dt2283group_p.showingslot join dt2283group_p.film on filmid = dt2283group_p.showingslot.film_filmid Order by slotid desc ')
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
    else:
        for row in cur:
            slotid,showtime,screenno,filmid,filmname = row
            #print("Table: ", row)
            print("-",slotid,"|------|",showtime.time(),showtime.date(),"|------|",screenno,"|---------|",filmid,"|---------|",filmname)
        print("--------------------------------------------------------------------------------------------------------------")
    userChoice()
    cur.close()

# close the connection to the database

    con.close()
except (cx_Oracle.OperationalError, cx_Oracle.DatabaseError, cx_Oracle.InterfaceError) as e:
        errorObj, = e.args
        print("There was a database error")
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)

        print('The database connection failed')


# # 

# In[ ]:




