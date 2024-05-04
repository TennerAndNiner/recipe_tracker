from controllers.DBUtil import * 
import tkinter as tk

def saveCategory(nameentry, feedbackLabel):
    name = nameentry.get().capitalize()
    valid = checkValidCategoryEntry(name)
    if valid == False:
        feedbackLabel.configure(text="")
        feedbackLabel.configure(text="Please fill out all required fields.")
    else: 
        exists = checkExisting(name)
        if  exists == False:
            category = (name)
            query = "INSERT INTO Categories (categoryName) VALUES ('" + name + "')"
            # Using parameterized execution with a tuple
            cursor.execute(query)
            connection.commit()
            query = "SELECT * FROM Categories"
            cursor.execute(query)
            result = cursor.fetchall()
            fieldsClear(nameentry, feedbackLabel)
            feedbackLabel.configure(text="Category Successfully Added!")
        else:
            feedbackLabel.configure(text="Category already exists.")

def fieldsClear(nameentry, feedbackLabel):
    nameentry.delete(0, tk.END)
    feedbackLabel.configure(text="")

def checkValidCategoryEntry(name):
    if len(name) == 0:
        return False
    else:
        return True

def checkExisting(name):
    query = "SELECT categoryName FROM Categories where categoryName = '" + name + "'"
    cursor.execute(query)
    results = cursor.fetchone()
    if results == None:
        return False
    else:
        return True

