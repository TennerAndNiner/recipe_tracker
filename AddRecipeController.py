from controllers.DBUtil import * 
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import shutil
import os

def saveRecipe(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text, category_listbox, ingredient_listbox, appliance_listbox): 
        image_path = upload_image()
        name = name_text.get()
        prepTime = prepTime_text.get()
        cookTime = cookTime_text.get()
        servingSize = serving_text.get()
        descriptions = description_text.get("1.0", tk.END)
        instructions = instruction_text.get("1.0", tk.END)

        appliance_listbox.get("All")
        appliances = appliance_listbox.get("All")
        categories = category_listbox.get("All")
        ingredients = ingredient_listbox.get("All")

        notexists = checkRecipeNameExisting(name)

        # Execute the SQL command to insert the recipe into the database
        if notexists == False:
            messagebox.showerror("Error", "A recipe with this name already exists.")
        elif image_path == None:
            messagebox("Error", "No duplicate images!")
        elif name and prepTime and cookTime and servingSize and descriptions and instructions and ingredients and notexists and image_path != None:
            recipetable_vals = (name, image_path, prepTime, cookTime, servingSize, descriptions, instructions)
            saveRecipeTable(recipetable_vals)
            thisID = getRecipeID(name)
            if categories:
                saveRecipeCategories(categories, thisID)
            saveRecipeIngredients(ingredients, thisID)
            if appliances:
                saveRecipeAppliances(appliances, thisID)
            clear_fields(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text)
            messagebox.showinfo("Success", "Recipe uploaded successfully!")
        else:
            messagebox.showerror("Error", "Please fill out all necessary fields before submitting.")

def checkRecipeNameExisting(name):
    query = "SELECT recipeID FROM Recipes where recipeName = '" + name + "'"
    cursor.execute(query)
    results = cursor.fetchone()
    if results == None:
        return True
    else:
        return False

def getRecipeID(name):
    query = "SELECT recipeID FROM Recipes where recipeName = '" + name + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result

def getCategoryID(name):
    query = "SELECT categoryID FROM Categories where categoryName = '" + name + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result

def getApplianceID(name):
    query = "SELECT applianceID FROM Appliances where applianceName = '" + name + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result

def getIngredientID(name):
    query = "SELECT ingID FROM Ingredients where ingName = '" + name + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result

def getUnitID(name):
    query = "SELECT unitID FROM Units where unitName = '" + name + "'"
    cursor.execute(query)
    tuple = cursor.fetchall()
    result = tuple[0][0]
    return result

def saveRecipeTable(recipetable_vals):
    try:
        query = "INSERT INTO Recipes(recipeName,imagePath, prepTime, cookTime, servingSize, descriptions, instructions) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        cursor.execute(query, recipetable_vals)
        connection.commit()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data to Recipes table: {e}")
        connection.rollback()
    
def saveRecipeCategories(categories, recipeID):
    try:
        for category in categories:
            categoryID = getCategoryID(category)
            value = (recipeID, categoryID)
            query = "INSERT INTO RecipeCategories(recipeID, categoryID) VALUES (%s, %s)"
            cursor.execute(query, value)
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data to RecipeCategories table: {e}")
        connection.rollback()
    
def saveRecipeIngredients(ingredients, recipeID):
    try:
        for ingredient in ingredients:
            name, quantity, unit = split_ingredient(ingredient)
            ingID = getIngredientID(name)
            unitID = None
            if unit:
                unitID = getUnitID(unit)
            else:
                unitID = 1
            value = (recipeID, ingID, unitID, quantity)
            query = "INSERT INTO RecipeIngredients(recipeID, ingID, unitID, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, value)
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data to RecipeIngredients table: {e}")
        connection.rollback()

def split_ingredient(ingredient_str):
    # Split the ingredient name from the rest
    parts = ingredient_str.split(" - ")

    if len(parts) < 2:
        raise ValueError("Invalid ingredient format")

    name = parts[0].strip()
    quantity_unit = parts[1].strip()
    unit = None
    quantity = None
    quantity_parts = quantity_unit.split()

    if len(quantity_parts) == 1:
        quantity = quantity_parts[0]  
    elif len(quantity_parts) > 1:
        quantity = quantity_parts[0]  
        unit = quantity_parts[1]

    return name, quantity, unit

def saveRecipeAppliances(appliances, recipeID):
    try:
        for appliance in appliances:
            applianceID = getApplianceID(appliance)
            value = (recipeID, applianceID)
            query = "INSERT INTO RecipeAppliances (recipeID, applianceID) VALUES (%s, %s)"
            cursor.execute(query, value)
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data to RecipeAppliances table: {e}")
        connection.rollback()

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        # image_label.configure(image=photo)
        # image_label.image = photo  # Keep a reference to avoid garbage collection
        dir = save_image(file_path)
        if dir == False:
            messagebox.showinfo("Not Accepted", "No Duplicate Images")
            return None
        else:
            messagebox.showinfo("Success", "Image uploaded successfully!")
            return dir
    else:
        return None

def save_image(file_path):
    save_dir = "saved_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    if os.path.exists(file_path) == True:
        return False
    
    filename = os.path.basename(file_path)
    shutil.copy(file_path, os.path.join(save_dir, filename))
    print("Image saved to:", os.path.join(save_dir, filename))
    return os.path.join(save_dir,filename)
    
# clear out the text content after done with the submision 
def clear_fields(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text):
    name_text.delete(0, tk.END)
    prepTime_text.delete(0, tk.END)
    cookTime_text.delete(0, tk.END)
    serving_text.delete(0, tk.END) 
    description_text.delete(1.0, tk.END) 
    instruction_text.delete(1.0, tk.END)

def getCategories():
    query = "SELECT categoryName FROM Categories"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def getAppliances():
    query = "SELECT applianceName FROM Appliances"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names


def getIngredients(ID):
    query = "SELECT ingName FROM Ingredients WHERE ingtypeID = '" + ID + "'"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def getUnits():
    query = "SELECT unitName FROM Units"
    # Execute the query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Extract the names from the results and store them in a list
    names = [row[0] for row in results]
    return names

def addCategory(category_combo,  category_listbox):
    category = category_combo.get()

    if category:
        entry = f"{category}"
        category_listbox.insert(tk.END, entry)
        # Clear input fields after adding
        category_listbox.set("")
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")


def addRecipeIngredient(ingredient_combo, quantity_entry, unit_combo, ingredient_listbox):
    ingredient = ingredient_combo.get()
    quantity = quantity_entry.get()
    unit = unit_combo.get()
    
    if ingredient and quantity and unit:
        entry = f"{ingredient} - {quantity} {unit}"
        ingredient_listbox.insert(tk.END, entry)
        # Clear input fields after adding
        ingredient_combo.set("")
        quantity_entry.delete(0, tk.END)
        unit_combo.set("")
    elif ingredient and quantity:
        entry = f"{ingredient} - {quantity}"
        ingredient_listbox.insert(tk.END, entry)
        ingredient_combo.set("")
        quantity_entry.delete(0, tk.END)
        unit_combo.set("")
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")

def addAppliance(appliance_combo,  appliance_listbox):
    appliance = appliance_combo.get()

    if appliance:
        entry = f"{appliance}"
        appliance_listbox.insert(tk.END, entry)
        # Clear input fields after adding
        appliance_listbox.set("")
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")