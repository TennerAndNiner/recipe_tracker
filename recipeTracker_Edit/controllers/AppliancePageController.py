from controllers.DBUtil import * 
import tkinter as tk

def saveAppliance(nameentry, feedbackLabel):
    name = nameentry.get().capitalize()
    valid = checkValidApplianceEntry(name)
    if valid == False:
        feedbackLabel.configure(text="")
        feedbackLabel.configure(text="Please fill out all required fields.")
    else: 
        exists = checkExisting(name)
        if  exists == False:
            category = (name)
            query = "INSERT INTO Appliances (applianceName) VALUES ('" + name + "')"
            # Using parameterized execution with a tuple
            cursor.execute(query)
            connection.commit()
            query = "SELECT * FROM Appliances"
            cursor.execute(query)
            result = cursor.fetchall()
            fieldsClear(nameentry, feedbackLabel)
            feedbackLabel.configure(text="Appliance Successfully Added!")
        else:
            feedbackLabel.configure(text="Appliance already exists.")

def fieldsClear(nameentry, feedbackLabel):
    nameentry.delete(0, tk.END)
    feedbackLabel.configure(text="")

def checkValidApplianceEntry(name):
    if len(name) == 0:
        return False
    else:
        return True

def checkExisting(name):
    query = "SELECT applianceName FROM Appliances where applianceName = '" + name + "'"
    cursor.execute(query)
    results = cursor.fetchone()
    if results == None:
        return False
    else:
        return True

