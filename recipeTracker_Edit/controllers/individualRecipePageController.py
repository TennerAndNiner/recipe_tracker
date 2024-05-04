from controllers.DBUtil import * 
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import shutil
import os

def getRecipeCategories(recipeID):
    query = "SELECT categoryID FROM RecipeCategories where recipeID= '" +  str(recipeID) + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    results = [row[0] for row in result]
    return results

def getCategoryName(categoryID):
    query = "SELECT categoryName FROM Categories where categoryID = '" + str(categoryID) + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result
    
def getRecipeAppliances(recipeID):
    query = "SELECT applianceID FROM RecipeAppliances where recipeID= '" +  str(recipeID)  + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    results = [row[0] for row in result]
    return results

def getApplianceName(applianceID):
    query = "SELECT applianceName FROM Appliances where applianceID = '" + str(applianceID) + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result

def getRecipeIngredients(recipeID):
    query = (
        "SELECT Ingredients.ingName, RecipeIngredients.quantity, Units.unitName "
        + "FROM RecipeIngredients "
        + "INNER JOIN Ingredients ON RecipeIngredients.ingID = Ingredients.ingID "
        + "INNER JOIN Units ON RecipeIngredients.unitID = Units.unitID "
        + "WHERE RecipeIngredients.recipeID = %s"
    )
    cursor.execute(query, (recipeID,))
    ingredients = cursor.fetchall()
    
    return [(ingredient[0], ingredient[1], ingredient[2]) for ingredient in ingredients]
