from controllers.DBUtil import * 
import tkinter as tk

connection = getConnection()
cursor = getCursor()

def saveIngredient(nameentry, combobox, feedbackLabel):
    name = nameentry.get().capitalize()
    category = combobox.get()
    valid = checkValidIngredientEntry(name, category)
    if valid == False:
        feedbackLabel.configure(text="")
        feedbackLabel.configure(text="Please fill out all required fields.")
    else: 
        exists = checkExisting(name)
        if  exists == False:
            icID = str(getIngCatID(category))
            ingredient = (icID, name)
            query = "INSERT INTO Ingredients (ingTypeID, ingName) VALUES (%s, '%s')"%ingredient
            # Using parameterized execution with a tuple
            cursor.execute(query)
            connection.commit()
            query = "SELECT * FROM Ingredients"
            cursor.execute(query)
            result = cursor.fetchall()
            ingredientClear(nameentry, combobox, feedbackLabel)
            feedbackLabel.configure(text="Ingredient Successfully Added!")
        else:
            feedbackLabel.configure(text="Ingredient already exists.")
        
def checkValidIngredientEntry(name, category):
    if len(name) == 0 or category == "Select an Ingredient Category":
        return False
    else:
        return True

def ingredientClear(nameentry, combobox, feedbackLabel):
    nameentry.delete(0, tk.END)
    combobox.set("Select an Ingredient Category")
    feedbackLabel.configure(text="")

def getIngredientCategories():
    query = "SELECT ingtypeName FROM IngredientTypes"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def getIngCatID(name):
    query = "SELECT ingtypeID FROM IngredientTypes where ingtypeName= '" + name + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result



def checkExisting(name):
    query = "SELECT ingName FROM Ingredients where ingName = '" + name + "'"
    cursor.execute(query)
    results = cursor.fetchone()
    if results == None:
        return False
    else:
        return True