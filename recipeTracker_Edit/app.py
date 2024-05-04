from tkinter import *
from tkinter import ttk
import tkinter as tk

from customtkinter import *
import customtkinter as ctk

from PIL import Image, ImageTk
from CTkListbox import *

from controllers.IngredientPageController import * 
from controllers.DBUtil import *
from controllers.AddRecipeController import * 
from controllers.CategoryPageController import * 
from controllers.AppliancePageController import *
from controllers.individualRecipePageController import * 

cursor = getCursor()
connection = getConnection()

#Setting up the GUI window & Frames
ctk.set_appearance_mode("light")
"""
Make sure you set your json.file path right
"""
ctk.set_default_color_theme("new.json")
#ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("1440x780")
root.title("Recipe Tracker")

#Two Frames
base_font = ctk.CTkFont(family="Poplar Std")
# Tall Left Frame
leftFrame = ctk.CTkFrame(root, height = 700, width = 500, fg_color = '#129575', bg_color = '#129575')
leftFrame.pack(anchor = 'w', side = LEFT,fill = Y, expand = FALSE)
# Right Frame
rightFrame = ctk.CTkFrame(root, height=700, width=200, fg_color= '#129575', bg_color= '#129575')
rightFrame.pack(anchor='e', side=RIGHT, fill=Y, expand=FALSE)
# Group Window
groupWindow = ctk.CTkFrame(root, height = 700, width = 500, fg_color = 'transparent', bg_color = 'transparent')
groupWindow.pack(anchor = 'n', fill = BOTH, expand = TRUE)

# Main Window
mainFrame = ctk.CTkFrame(groupWindow, height = 700, width = 300, fg_color = 'transparent', bg_color = 'transparent')
mainFrame.pack(anchor = 's', side = BOTTOM, fill = BOTH, expand = TRUE)

# Header Frame
headerFrame = ctk.CTkFrame(groupWindow, height = 150, width = 300, fg_color = 'transparent', bg_color = 'transparent')
headerFrame.pack(anchor = 'n', side = TOP, fill = BOTH, expand = FALSE)

# Label for the Tall Left Frame 'Main Menu'
leftTitle = ctk.CTkLabel(master = leftFrame, text = "ReciPedia", font = ctk.CTkFont(family="Noto Sans MS", size = 40, weight = 'normal')
                         ,text_color='white')
leftTitle.pack(padx = 20, pady = 20)

# Fonts

pageFont = ctk.CTkFont(family = "Noto Sans MS", size = 20, weight = 'normal')

feedbackFont = ctk.CTkFont(family = "Noto Sans MS", size = 10, weight = "bold")


# Button Icons

#saveImage = Image.open('save.png')

# Add Recipe Frames
#topLeftFrame = ctk.CTkFrame(mainFrame, width = 100, height = 300, fg_color = 'red', bg_color='red')
#topRightFrame = ctk.CTkFrame(groupWindow, width = 150, height = 300, fg_color = 'transparent', bg_color = 'transparent')

#addRecipeFrame = ctk.CTkFrame(mainFrame, height = 700, width = 300, fg_color = 'red', bg_color = 'red')
#addRecipeFrame.pack(fill = BOTH, expand = TRUE)

def newWindow(even, parent_frame, image_path):
    newWindow = ctk.CTkToplevel(parent_frame, fg_color = 'gray')
    
    cursor.execute("SELECT * FROM Recipes WHERE imagePath = %s", (image_path,))
    recipe_info = cursor.fetchone()
    
    newWindow.title(recipe_info[1])

    newWindow.geometry("700x450")

    newWindow.resizable(True, True)

    winFrame = ctk.CTkFrame(newWindow, height = 700, width = 450, fg_color='#d3d3d3', bg_color='#d3d3d3')
    winFrame.pack(fill = BOTH, expand = TRUE)

    frame_left = ctk.CTkFrame(winFrame, fg_color = 'white', bg_color = 'white')
    frame_left.grid(row = 0, column = 0, padx = 10, pady = 10)
    #frame_left.pack(padx = 20, pady = 20)

    frame_image = LabelFrame(frame_left, padx = 20, pady = 20, background = '#d3d3d3')
    frame_image.grid(row = 0, column = 0, padx = 10, pady = 10)

    
    image = Image.open(image_path)
    image.load()
    image.thumbnail((300, 300))
    image_one = ImageTk.PhotoImage(image)

    image_label = tk.Label(frame_image, image=image_one, background= 'gray')
    #image_label = ctk.CTkLabel(frame_image, image = image_one)
    image_label.image = image_one
    image_label.pack(padx=20,pady=20)

    
    frame_bottominfo = LabelFrame(frame_left,padx=20,pady=20, background='#d3d3d3')
    frame_bottominfo.grid(row = 1, column=0,rowspan=3, padx=10,pady=10)

    frame_info = LabelFrame(winFrame,padx=20,pady=20, background='#d3d3d3')
    frame_info.grid(row = 0, column=1,rowspan=3, padx=10,pady=10)

    
    try:
        # Fetch recipe information from the database based on the image path
        #cursor.execute("SELECT * FROM Recipes WHERE imagePath = %s", (image_path,))
        #recipe_info = cursor.fetchone()
        if recipe_info:
            # Extract recipe information
            recipeID = recipe_info[0]
            recipe_name = ctk.CTkLabel(frame_info, text = recipe_info[1],font = ctk.CTkFont(size = 30, weight = 'normal'))
            recipe_name.grid(row = 0, column=0)

            d_label = ctk.CTkLabel(frame_info, text = "Description", width = 40,font=("Helvetica", 15))
            d_label.grid(row = 1, column=0)
            description = tk.Text(frame_info, wrap=tk.WORD, height=5, width=60, font=("Helvetica", 15), background= '#d3d3d3', fg = 'black')
            description.insert(tk.END,recipe_info[6])
            description.configure(state="disabled")
            description.grid(row = 2, column=0, columnspan = 3,rowspan = 4)

            prep_time = recipe_info[3]
            p_label = ctk.CTkLabel(frame_info, text = "Prep Time:     " + str(prep_time),font=("Helvetica", 15))
            p_label.grid(row = 7, column=0)

            cook_time = recipe_info[4]
            c_label = ctk.CTkLabel(frame_info, text = "Cook Time:     " + str(cook_time),font=("Helvetica", 15))
            c_label.grid(row = 8, column=0)
            
            Total_Time = prep_time + cook_time
            t_label = ctk.CTkLabel(frame_info, text = "Total Time:     " + str(Total_Time),font=("Helvetica", 15))
            t_label.grid(row = 9, column=0)
            
            s_label = ctk.CTkLabel(frame_info, text = "Serving Size:     " + str(recipe_info[5]),font=("Helvetica", 15))
            s_label.grid(row = 10, column=0)
            
            instr_label = ctk.CTkLabel(frame_info, text = "Instruction",font=("Helvetica", 15))
            instr_label.grid(row=11,column = 0)
            instruction = tk.Text(frame_info, wrap=tk.WORD,height=20,width=60,font=("Helvetica", 15), background= '#d3d3d3', fg= 'black')           
            instruction.insert(tk.END,recipe_info[7])
            instruction.configure(state="disabled")
            instruction.grid(row=12,column = 0, rowspan = 9)

            categories = getRecipeCategories(recipeID)
            category_text = ", ".join([getCategoryName(c) for c in categories])
            categorylabel = ctk.CTkLabel(frame_bottominfo, text="Categories: " + category_text)
            categorylabel.grid(row=0, column=0, padx=5, pady=5)

            appliances = getRecipeAppliances(recipeID)
            appliance_text = ", ".join([getApplianceName(a) for a in appliances])
            appliancelabel = ctk.CTkLabel(frame_bottominfo, text="Appliances Needed: " + appliance_text)
            appliancelabel.grid(row=1, column=0, padx=5, pady=5)

            ingredients = getRecipeIngredients(recipeID)
            listbox_label = ctk.CTkLabel(frame_bottominfo, text="Ingredients:")
            listbox_label.grid(row=2, column=0, padx=5, pady=5)
            ingredient_listbox = CTkListbox(frame_bottominfo, height=250, width=200)
            for ingredient, quantity, unit in ingredients:
                ingredient_listbox.insert(tk.END, f"{ingredient} - {quantity} {unit}")
            ingredient_listbox.grid(row=3, column=0, padx=5, pady=5)
        else:
            print("Recipe not found")
    except Exception as e:
        print(f"Error fetching recipe information: {e}")
    



def image_click(even,image_path):
    clearPage()
    frame_left = ctk.CTkFrame(mainFrame, fg_color = 'red', bg_color = 'red')
    frame_left.grid(row = 0, column=0,padx=10,pady=10)

    frame_image = LabelFrame(frame_left, padx=20,pady=20, background = '#d3d3d3')
    frame_image.grid(row = 0, column=0,padx=10,pady=10)

    image = Image.open(image_path)
    image.thumbnail((300, 300))
    image_one = ImageTk.PhotoImage(image)

    image_label = tk.Label(frame_image, image=image_one, background= 'gray')
    #image_label = ctk.CTkLabel(frame_image, image = image_one)
    image_label.image = image_one
    image_label.pack(padx=20,pady=20)

    frame_bottominfo = LabelFrame(frame_left,padx=20,pady=20, background='#d3d3d3')
    frame_bottominfo.grid(row = 1, column=0,rowspan=3, padx=10,pady=10)

    frame_info = LabelFrame(mainFrame,padx=20,pady=20, background='#d3d3d3')
    frame_info.grid(row = 0, column=1,rowspan=3, padx=10,pady=10)

    try:
        # Fetch recipe information from the database based on the image path
        cursor.execute("SELECT * FROM Recipes WHERE imagePath = %s", (image_path,))
        recipe_info = cursor.fetchone()
        if recipe_info:
            # Extract recipe information
            recipeID = recipe_info[0]
            recipe_name = ctk.CTkLabel(frame_info, text = recipe_info[1],font = ctk.CTkFont(size = 30, weight = 'normal'))
            recipe_name.grid(row = 0, column=0)

            d_label = ctk.CTkLabel(frame_info, text = "Description", width = 40,font=("Helvetica", 15))
            d_label.grid(row = 1, column=0)
            description = tk.Text(frame_info, wrap=tk.WORD, height=5, width=60, font=("Helvetica", 15), background= '#d3d3d3', fg = 'black')
            description.insert(tk.END,recipe_info[6])
            description.configure(state="disabled")
            description.grid(row = 2, column=0, columnspan = 3,rowspan = 4)

            prep_time = recipe_info[3]
            p_label = ctk.CTkLabel(frame_info, text = "Prep Time:     " + str(prep_time),font=("Helvetica", 15))
            p_label.grid(row = 7, column=0)

            cook_time = recipe_info[4]
            c_label = ctk.CTkLabel(frame_info, text = "Cook Time:     " + str(cook_time),font=("Helvetica", 15))
            c_label.grid(row = 8, column=0)
            
            Total_Time = prep_time + cook_time
            t_label = ctk.CTkLabel(frame_info, text = "Total Time:     " + str(Total_Time),font=("Helvetica", 15))
            t_label.grid(row = 9, column=0)
            
            s_label = ctk.CTkLabel(frame_info, text = "Serving Size:     " + str(recipe_info[5]),font=("Helvetica", 15))
            s_label.grid(row = 10, column=0)
            
            instr_label = ctk.CTkLabel(frame_info, text = "Instruction",font=("Helvetica", 15))
            instr_label.grid(row=11,column = 0)
            instruction = tk.Text(frame_info, wrap=tk.WORD,height=20,width=60,font=("Helvetica", 15), background= '#d3d3d3', fg= 'black')           
            instruction.insert(tk.END,recipe_info[7])
            instruction.configure(state="disabled")
            instruction.grid(row=12,column = 0, rowspan = 9)

            categories = getRecipeCategories(recipeID)
            category_text = ", ".join([getCategoryName(c) for c in categories])
            categorylabel = ctk.CTkLabel(frame_bottominfo, text="Categories: " + category_text)
            categorylabel.grid(row=0, column=0, padx=5, pady=5)

            appliances = getRecipeAppliances(recipeID)
            appliance_text = ", ".join([getApplianceName(a) for a in appliances])
            appliancelabel = ctk.CTkLabel(frame_bottominfo, text="Appliances Needed: " + appliance_text)
            appliancelabel.grid(row=1, column=0, padx=5, pady=5)

            ingredients = getRecipeIngredients(recipeID)
            listbox_label = ctk.CTkLabel(frame_bottominfo, text="Ingredients:")
            listbox_label.grid(row=2, column=0, padx=5, pady=5)
            ingredient_listbox = CTkListbox(frame_bottominfo, height=250, width=200)
            for ingredient, quantity, unit in ingredients:
                ingredient_listbox.insert(tk.END, f"{ingredient} - {quantity} {unit}")
            ingredient_listbox.grid(row=3, column=0, padx=5, pady=5)
        else:
            print("Recipe not found")
    except Exception as e:
        print(f"Error fetching recipe information: {e}")

# def display_recipes():
#     clearPage()
#     def init():
#         cursor.execute("SELECT * FROM Recipes")
#         result = cursor.fetchall()
#         displayResult(result)
    
#     def displayHeader():
#         headerFrame.pack()
#         searchBar = ctk.CTkEntry(headerFrame, width = 300, height = 30, bg_color = 'transparent',
#                                 fg_color = 'transparent', placeholder_text = "Search")
#         searchBar.grid(row=0, column=0, padx = 20, pady = 20)
#         #searchBar.pack(padx = 10, pady = 20, side = tk.LEFT)
#         #searchButton = ttk.Button(headerFrame, text="Search", command=lambda: getNameSearch(searchBar))
#         searchButton = ctk.CTkButton(headerFrame, text = "Search", command = lambda: getNameSearch(searchBar))
#         searchButton.grid(row=0, column=1,padx=5, pady=5)
#         #searchButton.pack(padx = 20, pady = 20)

#     def displayRight():
#         rightFrame.configure(height=700, width=200, fg_color='light gray', bg_color='light gray')

#         spacer = ctk.CTkLabel(rightFrame, text="More Search Options:")
        
#         spacer.grid(row=0, column=0, padx=5, pady=20)

#         category_label = ctk.CTkLabel(rightFrame, text="Category:")
#         category_label.grid(row=1, column=0, padx=5, pady=5)

#         category_options = getCategories()
#         category_combo = ctk.CTkComboBox(rightFrame, values=category_options, state="readonly")
#         category_combo.grid(row=2, column=0, padx=5, pady=5)

#        #categorySelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getCategorySearch(category_combo))
#         categorySelect_button = ctk.CTkButton(rightFrame, text = "Search", command=lambda: getCategorySearch(category_combo))
#         categorySelect_button.grid(row=2, column=1, padx=5, pady=5)
    
#         #Appliance Selection
#         appliance_label = ctk.CTkLabel(rightFrame, text="Appliance:")
#         appliance_label.grid(row=3, column=0, padx=5, pady=5)

#         appliance_options = getAppliances()
#         appliance_combo = ctk.CTkComboBox(rightFrame, values=appliance_options, state="readonly")
#         appliance_combo.grid(row=4, column=0, padx=5, pady=5)

#         #applianceSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getApplianceSearch(appliance_combo))
#         applianceSelect_button = ctk.CTkButton(rightFrame, text = "Search", command = lambda: getApplianceSearch(appliance_combo))
#         applianceSelect_button.grid(row=4, column=1, padx=5, pady=5)
        
#         duration_label = ctk.CTkLabel(rightFrame, text = "Duration (mins):")
#         duration_text = ctk.CTkEntry(rightFrame)
#         duration_label.grid(row=5, column=0,padx=5, pady=5)
#         duration_text.grid(row=6, column=0,padx=5, pady=5)
#         #durationSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getDurationSearch(duration_text))
#         durationSelect_button = ctk.CTkButton(rightFrame, text = "Search", command = lambda: getDurationSearch(duration_text))
#         durationSelect_button.grid(row=6, column=1, padx=5, pady=5)


#         # Ingredient Category Selection
#         ingcategory_label = ctk.CTkLabel(rightFrame, text="Ingredient Type:")
#         ingcategory_label.grid(row=7, column=0, padx=5, pady=5)

#         ingredientcategory_options = getIngredientCategories()
#         ingcategory_combo = ctk.CTkComboBox(rightFrame, values=ingredientcategory_options, state="readonly")
#         ingcategory_combo.grid(row=8, column=0, padx=5, pady=5)
 
#         #ingredientSelectionDisplay_button = ttk.Button(rightFrame, text="Select", command=lambda: displayIngSelection(ingcategory_combo))
#         ingredientSelectionDisplay_button = ctk.CTkButton(rightFrame, text="Select", command=lambda: displayIngSelection(ingcategory_combo))
#         ingredientSelectionDisplay_button.grid(row=8, column=1, padx=5, pady=5)

#     def displayIngSelection(combobox):
#             category = combobox.get()
#             if len(category) > 0:
#                 icID = str(getIngCatID(category))
#                 # Ingredient selection
#                 ingredient_label = ctk.CTkLabel(rightFrame, text="Ingredient:")
#                 ingredient_label.grid(row=9, column=0, padx=5, pady=5)

#                 ingredient_options = getIngredients(icID)
#                 ingredient_combo = ctk.CTkComboBox(rightFrame, values=ingredient_options, state="readonly")
#                 ingredient_combo.grid(row=10, column=0, padx=5, pady=5)
#                 ingredientSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getIngredientSearch(ingredient_combo))
#                 ingredientSelect_button.grid(row=10, column=1, padx=5, pady=5)

#     def getNameSearch(searchBar):
#         answer = searchBar.get()
#         if answer == "":
#             cursor.execute("SELECT * FROM Recipes")
#             result = cursor.fetchall()
#             displayResult(result)

#         else:
#             sqlStatement = "SELECT * FROM Recipes WHERE recipeName LIKE '%" + answer + "%'"
#             cursor.execute(sqlStatement)
#             result = cursor.fetchall()
#             clearPage()
#             displayResult(result)

#     def getCategorySearch(combo):
#         category = combo.get()
#         categoryID = getCategoryID(category)
#         query = (
#             "SELECT Recipes.* FROM Recipes "
#             + "INNER JOIN RecipeCategories ON Recipes.recipeID = RecipeCategories.recipeID "
#             + "INNER JOIN Categories ON RecipeCategories.categoryID = Categories.categoryID "
#             + "WHERE Categories.categoryID = %s"
#         )
#         cursor.execute(query, (categoryID,))
#         result = cursor.fetchall()
#         displayResult(result)

#     def getApplianceSearch(combo):
#         appliance = combo.get()
#         applianceID = getApplianceID(appliance)
#         query = (
#             "SELECT Recipes.* FROM Recipes "
#             + "INNER JOIN RecipeAppliances ON Recipes.recipeID = RecipeAppliances.recipeID "
#             + "INNER JOIN Appliances ON RecipeAppliances.applianceID = Appliances.applianceID "
#             + "WHERE Appliances.applianceID = %s"
#         )
#         cursor.execute(query, (applianceID,))
#         result = cursor.fetchall()
#         displayResult(result)

#     def getIngredientSearch(combo):
#         ingredient = combo.get()
#         ingID = getIngredientID(ingredient)
#         query = (
#             "SELECT Recipes.* FROM Recipes "
#             + "INNER JOIN RecipeIngredients ON Recipes.recipeID = RecipeIngredients.recipeID "
#             + "INNER JOIN Ingredients ON RecipeIngredients.ingID = Ingredients.ingID "
#             + "WHERE Ingredients.ingID = %s"
#         )
#         cursor.execute(query, (ingID,))
#         result = cursor.fetchall()
#         displayResult(result)

#     def getDurationSearch(entry):
#         duration = entry.get()
#         if duration.isdigit():
#             query = "SELECT * FROM Recipes WHERE (prepTime + cookTime) <= %s"
#             cursor.execute(query, (duration,))
#             result = cursor.fetchall()
#             clearPage()
#             displayResult(result)
#         else:
#             messagebox.showerror("Error", f"Please input time in minutes.")

#     def displayResult(result):

#         clearPage()
#         displayHeader()
#         displayRight()
#         row_even_num = 0 # for display the image of each recipe
#         row_odd_num = 1  # for display the name of the each recipe
#         column_num = 0
#         gap_size = 15
#         if result:
#             for x in result:
#                 if column_num <= 2:
#                     image_path = x[2]
#                     try:
#                         image = Image.open(image_path)
#                         image.thumbnail((200, 200))
#                         image_one = ImageTk.PhotoImage(image)

#                         image_label = tk.Label(mainFrame, image=image_one, background='gray')
#                         image_label.image = image_one
#                         image_label.grid(row=row_even_num, column=column_num, padx=gap_size,pady=gap_size)

#                         image_label.bind("<Button-1>", lambda event, path=image_path: image_click(event, path))

#                         name_label = tk.Label(mainFrame,text=x[1], background='#d3d3d3', fg= '#129575')
#                         name_label.grid(row=row_odd_num, column=column_num)

#                     except Exception as e:
#                         print(f"Error opening image: {e}")
#                 else:
#                     column_num = 0
#                     row_even_num += 2
#                     row_odd_num +=2
#                     image_path = x[2]
#                     try:
#                         image = Image.open(image_path)
#                         image.thumbnail((200, 200))
#                         image_one = ImageTk.PhotoImage(image)

#                         image_label = tk.Label(mainFrame, image=image_one, background='gray')
#                         image_label.image = image_one
#                         image_label.grid(row=row_even_num, column=column_num)

#                         image_label.bind("<Button-1>", lambda event, path=image_path: image_click(event, path))

#                         name_label = tk.Label(mainFrame,text=x[1], background='#d3d3d3', fg='#129575')
#                         name_label.grid(row=row_odd_num, column=column_num)
#                     except Exception as e:
#                         print(f"Error opening image: {e}")
                
#                 column_num += 1
#         else:
#             label = tk.Label(mainFrame,text="No results")
#             # label.pack()
#             label.pack()  # Use grid() instead of pack()

#     init()
#     displayHeader()
#     displayRight()

def showScrollable():
    clearPage()
    
    def myHeader(parent_frame):
        headerFrame = tk.Frame(parent_frame)
        headerFrame.pack()
        searchBar = ctk.CTkEntry(headerFrame, width = 300, height = 30, bg_color = 'transparent',
                                fg_color = 'transparent', placeholder_text = "Search")
        searchBar.grid(row=0, column=0, padx = 20, pady = 20)
        #searchBar.pack(padx = 10, pady = 20, side = tk.LEFT)
        #searchButton = ttk.Button(headerFrame, text="Search", command=lambda: getNameSearch(searchBar))
        #searchButton = ctk.CTkButton(headerFrame, text = "Search", command = lambda: getNameSearch(searchBar))
        searchButton = ctk.CTkButton(headerFrame, text = "Search", command = lambda: getNameSearch(searchBar))
        #searchButton = ctk.CTkButton(headerFrame, text = "Search")
        searchButton.grid(row=0, column=1,padx=5, pady=5)
        #searchButton.pack(padx = 20, pady = 20)

    
    def myRight(parent_frame):
        rightFrame = tk.Frame(parent_frame)
        # rightFrame.configure(height=700, width=200, fg_color='light gray', bg_color='light gray')
        rightFrame.pack(side='right')

        spacer = ctk.CTkLabel(rightFrame, text="More Search Options:")
        
        spacer.grid(row=0, column=0, padx=5, pady=20)

        category_label = ctk.CTkLabel(rightFrame, text="Category:")
        category_label.grid(row=1, column=0, padx=5, pady=5)

        #category_options = getCategories()
        category_combo = ctk.CTkComboBox(rightFrame, values= getCategories(), state="readonly")
        category_combo.grid(row=2, column=0, padx=5, pady=5)

        #categorySelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getCategorySearch(category_combo))
        categorySelect_button = ctk.CTkButton(rightFrame, text = "Search", command=lambda: getCategorySearch(category_combo))
        #categorySelect_button = ctk.CTkButton(rightFrame, text = "Search")
        categorySelect_button.grid(row=2, column=1, padx=5, pady=5)
    
        #Appliance Selection
        appliance_label = ctk.CTkLabel(rightFrame, text="Appliance:")
        appliance_label.grid(row=3, column=0, padx=5, pady=5)

        appliance_options = getAppliances()
        appliance_combo = ctk.CTkComboBox(rightFrame, values=appliance_options, state="readonly")
        appliance_combo.grid(row=4, column=0, padx=5, pady=5)

        #applianceSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getApplianceSearch(appliance_combo))
        applianceSelect_button = ctk.CTkButton(rightFrame, text = "Search", command = lambda: getApplianceSearch(appliance_combo))
        #applianceSelect_button = ctk.CTkButton(rightFrame, text = "Search")
        applianceSelect_button.grid(row=4, column=1, padx=5, pady=5)
        
        duration_label = ctk.CTkLabel(rightFrame, text = "Duration (mins):")
        duration_text = ctk.CTkEntry(rightFrame)
        duration_label.grid(row=5, column=0,padx=5, pady=5)
        duration_text.grid(row=6, column=0,padx=5, pady=5)
        #durationSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getDurationSearch(duration_text))
        durationSelect_button = ctk.CTkButton(rightFrame, text = "Search", command = lambda: getDurationSearch(duration_text))
        #durationSelect_button = ctk.CTkButton(rightFrame, text = "Search")
        durationSelect_button.grid(row=6, column=1, padx=5, pady=5)


        # Ingredient Category Selection
        ingcategory_label = ctk.CTkLabel(rightFrame, text="Ingredient Type:")
        ingcategory_label.grid(row=7, column=0, padx=5, pady=5)

        ingredientcategory_options = getIngredientCategories()
        ingcategory_combo = ctk.CTkComboBox(rightFrame, values=ingredientcategory_options, state="readonly")
        ingcategory_combo.grid(row=8, column=0, padx=5, pady=5)
 
        #ingredientSelectionDisplay_button = ttk.Button(rightFrame, text="Select", command=lambda: displayIngSelection(ingcategory_combo))
        ingredientSelectionDisplay_button = ctk.CTkButton(rightFrame, text="Select", command=lambda: displayIngSelection(ingcategory_combo))
        #ingredientSelectionDisplay_button = ctk.CTkButton(rightFrame, text="Select")
        ingredientSelectionDisplay_button.grid(row=8, column=1, padx=5, pady=5)


    #myHeader(mainFrame)
    #myRight(mainFrame)
    
    def createCanvas(parent_frame):
    # Create a new Frame
        # newFrame = Frame(master = mainFrame, width = 200, height = 200)
        # newFrame.pack(fill = BOTH, expand = True)
        
        # Create a new Canvas
        my_canvas = Canvas(parent_frame, bg = 'light gray')
        my_canvas.pack(side = tk.LEFT, fill = BOTH, expand = TRUE)

        # Create a new Scroll Bar
        myScrollBar = ttk.Scrollbar(parent_frame, orient= VERTICAL, command = my_canvas.yview)
        myScrollBar.pack(side = tk.RIGHT, fill = Y, padx= 10, pady= 10)

        #Configure the canvas 
        my_canvas.configure(yscrollcommand= myScrollBar.set)
        my_canvas.bind('<Configure>', lambda e : my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # Create a second frame
        # The second frame is packed with recipes
        second_frame = ctk.CTkFrame(my_canvas, width = 700, height = 200, bg_color = 'transparent', fg_color='transparent')
        my_canvas.create_window((0, 0), window=second_frame, anchor = 'nw', width = 900)
        return second_frame
    
  
    def init():
        cursor.execute("SELECT * FROM Recipes")
        result = cursor.fetchall()
        displayScrollResult(result)

    def displayIngSelection(combobox):
            category = combobox.get()
            if len(category) > 0:
                icID = str(getIngCatID(category))
                ingredient_label = ctk.CTkLabel(rightFrame, text="Ingredient:")
                ingredient_label.grid(row=9, column=0, padx=5, pady=5)

                ingredient_options = getIngredients(icID)
                ingredient_combo = ctk.CTkComboBox(rightFrame, values=ingredient_options, state="readonly")
                ingredient_combo.grid(row=10, column=0, padx=5, pady=5)
                ingredientSelect_button = ttk.Button(rightFrame, text="Search", command=lambda: getIngredientSearch(ingredient_combo))
                ingredientSelect_button.grid(row=10, column=1, padx=5, pady=5)

    def getIngredientSearch(combo):
            ingredient = combo.get()
            ingID = getIngredientID(ingredient)
            query = (
             "SELECT Recipes.* FROM Recipes "
             + "INNER JOIN RecipeIngredients ON Recipes.recipeID = RecipeIngredients.recipeID "
             + "INNER JOIN Ingredients ON RecipeIngredients.ingID = Ingredients.ingID "
            + "WHERE Ingredients.ingID = %s"
         )
            cursor.execute(query, (ingID,))
            result = cursor.fetchall()
            displayScrollResult(result)


    def getNameSearch(searchBar):
        answer = searchBar.get()
        if answer == "":
            cursor.execute("SELECT * FROM Recipes")
            result = cursor.fetchall()
            displayScrollResult(result)

        else:
            sqlStatement = "SELECT * FROM Recipes WHERE recipeName LIKE '%" + answer + "%'"
            cursor.execute(sqlStatement)
            result = cursor.fetchall()
            #clearPage()
            displayScrollResult(result)

    def getCategorySearch(combo):
            category = combo.get()
            categoryID = getCategoryID(category)
            query = ("SELECT Recipes.* FROM Recipes " + "INNER JOIN RecipeCategories ON Recipes.recipeID = RecipeCategories.recipeID "
                                    + "INNER JOIN Categories ON RecipeCategories.categoryID = Categories.categoryID "
            + "WHERE Categories.categoryID = %s")
            cursor.execute(query, (categoryID,))
            result = cursor.fetchall()
            displayScrollResult(result)

    def getApplianceSearch(combo):
            appliance = combo.get()
            applianceID = getApplianceID(appliance)
            query = ("SELECT Recipes.* FROM Recipes "
             + "INNER JOIN RecipeAppliances ON Recipes.recipeID = RecipeAppliances.recipeID "
             + "INNER JOIN Appliances ON RecipeAppliances.applianceID = Appliances.applianceID "
             + "WHERE Appliances.applianceID = %s"
             )
            cursor.execute(query, (applianceID,))
            result = cursor.fetchall()
            displayScrollResult(result)

        

    def getDurationSearch(entry):
        duration = entry.get()
        if duration.isdigit():
            query = "SELECT * FROM Recipes WHERE (prepTime + cookTime) <= %s"
            cursor.execute(query, (duration,))
            clearPage()
            result = cursor.fetchall()
            displayScrollResult(result)
        else:
            messagebox.showerror("Error", f"Please input time in minutes.")
    #Display the recipes on the scrollable canvas

    myHeader(mainFrame)
    myRight(mainFrame)
    second_frame = createCanvas(mainFrame)


   # def displayScrollRecipes(second_frame, result):
    def displayScrollResult(result):
        clearScrollPage(second_frame)

        row_even_num = 0 # for display the image of each recipe
        row_odd_num = 1  # for display the name of the each recipe
        column_num = 0
        gap_size = 20
            
        if result:
            for x in result:
                if column_num <= 2:
                    image_path = x[2]
                    try:
                        image = Image.open(image_path)
                        image.thumbnail((200, 200))
                        image_one = ImageTk.PhotoImage(image)

                        image_label = tk.Label(second_frame, image=image_one, background='gray')
                        image_label.image = image_one
                        image_label.grid(row=row_even_num, column=column_num, padx=gap_size,pady=gap_size)

                        #image_label.bind("<Button-1>", lambda event, path=image_path: image_click(event, path))
                        image_label.bind("<Button-1>", lambda event, path = image_path: newWindow(event, second_frame, path))

                        name_label = tk.Label(second_frame,text=x[1], background='#d3d3d3', fg= '#129575')
                        name_label.grid(row=row_odd_num, column=column_num)

                    except Exception as e:
                        print(f"Error opening image: {e}")
                else:
                    column_num = 0
                    row_even_num += 2
                    row_odd_num +=2
                    image_path = x[2]
                    try:
                        image = Image.open(image_path)
                        image.thumbnail((200, 200))
                        image_one = ImageTk.PhotoImage(image)

                        image_label = tk.Label(second_frame, image=image_one, background='gray')
                        image_label.image = image_one
                        image_label.grid(row=row_even_num, column=column_num)

                            #image_label.bind("<Button-1>", lambda event, path=image_path: image_click(event, path))
                        image_label.bind("<Button-1>", lambda event, path=image_path: newWindow(event, second_frame, path))

                        name_label = tk.Label(second_frame,text=x[1], background='#d3d3d3', fg='#129575')
                        name_label.grid(row=row_odd_num, column=column_num)
                    except Exception as e:
                        print(f"Error opening image: {e}")
                
                column_num += 1
        else:
            label = tk.Label(second_frame, text="No results")
            label.pack()


    # Displays all the recipes
    #clearScrollPage(second_frame)
    init()

"""
This is the code that clears all the info in the Scroll Page
We don't need to clear out the info
"""
def clearScrollPage(usedFrame):
    for frame in usedFrame.winfo_children():
        frame.destroy()
            
def clearPage():
    for frame in mainFrame.winfo_children():
        frame.destroy()
    for frame in headerFrame.winfo_children():
        frame.pack_forget()
    headerFrame.pack_forget()
    for frame in rightFrame.winfo_children():
        frame.destroy()
    rightFrame.configure(height=0, width=0)

def addRecipePage():
    clearPage()


    """
    Note this code uses a local variable from a different function.
    Therefore, all values should belong in the mainFrame.
    
    Except, for the bottomFrame, which holds the upload image and save button

    """

    """
    3 Frames
    Top Left Frame -- This frame is the frame where input our information --

    Top Right Frame -- This frame is the frame where we select our categories --
    Bottom Frame -- This frame is the frame where we upload our image and save --
    """

    #addRecipeFrame.pack(fill = BOTH, expand = TRUE)

    topLeftFrame = ctk.CTkFrame(mainFrame, width = 100, height = 300, fg_color = 'transparent', bg_color='transparent')
    topLeftFrame.pack(side = tk.LEFT, fill = BOTH, expand = False)

    topRightFrame = ctk.CTkFrame(mainFrame, width = 150, height = 300, fg_color = 'transparent', bg_color = 'transparent')
    topRightFrame.pack(side = tk.LEFT, fill = BOTH, expand = True)
    
    bottomFrame = ctk.CTkFrame(mainFrame, width = 200, height = 100, fg_color = 'gray', bg_color = 'gray')
    bottomFrame.pack(side = tk.BOTTOM, fill = BOTH, expand = FALSE)
    #bottomFrame.grid(row = 10, fill = BOTH, expand = False)
    #bottomFrame.grid(row = 10, column = 5, padx = 20, pady = 20)

    upperRightFrame = ctk.CTkFrame(mainFrame, width = 200, height = 600, fg_color = 'gray', bg_color = 'gray')
    upperRightFrame.pack(side = tk.RIGHT, fill = BOTH, expand = TRUE)

    
    
    
    name_label = ctk.CTkLabel(topLeftFrame, text = "Name Of The Recipe")
    name_text = ctk.CTkEntry(topLeftFrame, placeholder_text= "Name")
   
    name_label.grid(row=0, column=0, padx =5, pady=5)
    name_text.grid(row=0, column=1, padx = 5, pady=5)

    #name_label.pack(padx = 10, pady = 20, side = tk.LEFT)
    #name_text.pack(padx = 10, pady = 20, side = tk.LEFT)

    
    prepTime_label = ctk.CTkLabel(topLeftFrame, text= "Preparation Time")
    prepTime_text = ctk.CTkEntry(topLeftFrame, placeholder_text = "Input Minutes")
    
    prepTime_label.grid(row=1, column=0, padx = 5, pady=5)
    prepTime_text.grid(row=1, column=1, padx = 5, pady=5)


    cookTime_label = ctk.CTkLabel(topLeftFrame, text= "Cook Time")
    cookTime_text = ctk.CTkEntry(topLeftFrame, placeholder_text = "Input Minutes")
    
    cookTime_label.grid(row=2, column=0, padx =5, pady=5)
    cookTime_text.grid(row=2, column=1, padx = 5, pady=5)

    serving_label = ctk.CTkLabel(topLeftFrame, text= "Serving Size")
    serving_text = ctk.CTkEntry(topLeftFrame, placeholder_text = "Number Of People")
    
    serving_label.grid(row=3, column=0, padx =10, pady=20)
    serving_text.grid(row=3, column=1, padx = 10, pady=20)

    
    description_label = ctk.CTkLabel(topLeftFrame, text= "Description")
    description_text = ctk.CTkTextbox(topLeftFrame, width= 300, height= 150)
    description_label.grid(row=4, column=0,padx=5,pady=5,sticky="nsew")
    description_text.grid(row=4, column=1,padx=20,pady=20,sticky="nsew")

    
    instruction_label = ctk.CTkLabel(topLeftFrame, text= "Instruction")
    instruction_text = ctk.CTkTextbox(topLeftFrame, width= 300, height= 150)
    instruction_label.grid(row=6, column=0,padx=5,pady=5,sticky="nsew")
    instruction_text.grid(row=6, column=1,padx=20,pady=20,sticky="nsew")

    # Category Selection
    category_label = ctk.CTkLabel(topRightFrame, text="Category:")
    category_label.grid(row=0, column=2, padx=10, pady=20)

    category_options = getCategories()
    category_combo = ctk.CTkComboBox(topRightFrame, values=category_options, state="readonly")
    category_combo.grid(row=0, column=3, padx=10, pady=20)

    
    cListbox_label = ctk.CTkLabel(topRightFrame, text="Added Categories:")
    #cListbox_label.grid(row=1, column=2, padx=10, pady=20)
    cListbox_label.grid(row = 1, column = 2, padx = 20, pady = 20)
    category_listbox = CTkListbox(topRightFrame, height=60, width=150)
    category_listbox.grid(row=1, column=3, padx= 10, pady=20)
    
    #categorySelect_button = ttk.Button(mainFrame, text="Select", command=lambda: addCategory(category_combo, category_listbox))
    categorySelect_button = ctk.CTkButton(topRightFrame, text = "Select", command = lambda: addCategory(category_combo, category_listbox))
    categorySelect_button.grid(row=0, column=4, padx=5, pady=5)
    
    
    # Ingredient Category Selection
    # ingredientadd_label = ctk.CTkLabel(mainFrame, text="Select an Ingredient Category to begin adding Ingredients.")
    # ingredientadd_label.grid(row=0, column=2, padx=5, pady=5)
    ingcategory_label = ctk.CTkLabel(topRightFrame, text="Ingredient Type:")
    ingcategory_label.grid(row=2, column=2, padx=5, pady=5)
    #ingcategory_label.pack(padx = 20, pady = 20)

    ingredientcategory_options = getIngredientCategories()
    ingcategory_combo = ctk.CTkComboBox(topRightFrame, values=ingredientcategory_options, state="readonly")
    ingcategory_combo.grid(row=2, column=3, padx=5, pady=5)
    
    #ingredientSelectionDisplay_button = ttk.Button(mainFrame, text="Select", command=lambda:displayIngredientSelection(ingcategory_combo, ingredient_listbox))
    ingredientSelectionDisplay_button = ctk.CTkButton(topRightFrame, text = "Select", command = lambda:displayIngredientSelection(ingcategory_combo, ingredient_listbox))
    ingredientSelectionDisplay_button.grid(row=2, column=4, padx=5, pady=5)
    #ingredientSelectionDisplay_button.pack(padx = 20, pady = 20)
    
    listbox_label = ctk.CTkLabel(topRightFrame, text="Added Ingredients:")
    listbox_label.grid(row=3, column=2, padx=5, pady=5)
    ingredient_listbox = CTkListbox(topRightFrame, height=250, width=200)
    ingredient_listbox.grid(row=3, column=3, padx=5, pady=5)

    
    #Appliance Selection
    appliance_label = ctk.CTkLabel(topRightFrame, text="Appliance:")
    appliance_label.grid(row=4, column=2, padx=5, pady=5)

    appliance_options = getAppliances()
    appliance_combo = ctk.CTkComboBox(topRightFrame, values=appliance_options, state="readonly")
    appliance_combo.grid(row=4, column=3, padx=5, pady=5)

    #applianceSelect_button = ttk.Button(topRightFrame, text="Select", command=lambda: addAppliance(appliance_combo,  appliance_listbox))
    applianceSelect_button = ctk.CTkButton(topRightFrame, text="Select", command=lambda: addAppliance(appliance_combo,  appliance_listbox))
    applianceSelect_button.grid(row=4, column=4, padx=5, pady=5)

    appliance_label = ctk.CTkLabel(topRightFrame, text="Added Appliances:")
    appliance_label.grid(row=5, column=2, padx=5, pady=5)
    appliance_listbox = CTkListbox(topRightFrame, height=100, width=200)
    appliance_listbox.grid(row=5, column=3, padx=5, pady=5)

    
    # setImagePath()
    # image_label = ctk.CTkLabel(mainFrame, text ="")
    # upload_button = ctk.CTkButton(mainFrame, text="Upload Image", command=lambda: upload_image(image_label))
    # image_label.grid(row=1, column=2,padx=5,pady=20)
    # upload_button.grid(row=2, column=2,padx=5,pady=20)

    submit_button = ctk.CTkButton(bottomFrame,text="Upload Image & Submit", command=lambda:saveRecipe(name_text, prepTime_text, cookTime_text, serving_text, description_text, instruction_text, category_listbox, ingredient_listbox, appliance_listbox))
    submit_button.pack(padx = 10, pady = 10)

    # clear_button = ctk.CTkButton(mainFrame,text="Clear content", command = clear_fields)
    # clear_button.grid(row=10,column=1)
    

# Perhaps a new window?

    def displayIngredientSelection(combobox, ingredient_listbox):
        #padx = pady = 5
        category = combobox.get()
        if len(category) > 0:
            icID = str(getIngCatID(category))
            # Ingredient selection
            ingredient_label = ctk.CTkLabel(upperRightFrame, text="Ingredient:")
            ingredient_label.grid(row=0, column=0, padx = 5, pady = 5)
            #ingredient_label.pack(padx = 20, pady = 20)

            
            ingredient_options = getIngredients(icID)
            ingredient_combo = ctk.CTkComboBox(upperRightFrame, values=ingredient_options, state="readonly")
            ingredient_combo.grid(row=0, column=1, padx = 20, pady = 20)

            
            # Quantity input
            quantity_label = ctk.CTkLabel(upperRightFrame, text="Quantity:")
            quantity_label.grid(row=1, column=0, padx = 20, pady = 20)

            quantity_entry = ctk.CTkEntry(upperRightFrame)
            quantity_entry.grid(row=1, column=1, padx = 20, pady = 20)

            
            # Unit selection
            unit_label = ctk.CTkLabel(upperRightFrame, text="Unit:")
            unit_label.grid(row=2, column=0, padx = 20, pady = 20)

            unit_options = getUnits()
            unit_combo = ctk.CTkComboBox(upperRightFrame, values=unit_options, state="readonly")
            unit_combo.grid(row=2, column=1, padx = 20, pady = 20)

            
            #add_button = ttk.Button(mainFrame, text="Add", command=lambda: addRecipeIngredient(ingredient_combo, quantity_entry, unit_combo, ingredient_listbox))
            add_button = ctk.CTkButton(upperRightFrame, text="Add", command=lambda: addRecipeIngredient(ingredient_combo, quantity_entry, unit_combo, ingredient_listbox))
            add_button.grid(row=3, column=1, padx = 20, pady = 20)
            
def addIngredientPage():
    clearPage()

    ingredientTitle = ctk.CTkLabel(mainFrame, text = "Add An Ingredient", font = pageFont,
                         text_color='#129575')
    
    ingredientTitle.pack(padx = 20, pady = 20, side = tk.TOP)

    #ingredientTitle.grid(row = 0, column = 0, sticky = 'W', padx = 20, pady = 20)

    nameentry = ctk.CTkEntry(mainFrame, width = 140, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Name")
    nameentry.pack(padx = 20, pady = 20, side=tk.TOP)
    #nameentry.grid(row = 1, column = 0, sticky = 'W', padx = 20, pady = 20)

    # Extend the length of the combo box 
    ingredientcategories = getIngredientCategories()

    combobox = ctk.CTkComboBox(mainFrame, values=ingredientcategories, width = 210, height = 10)



    combobox.set("Select an Ingredient Category")  # set initial value
    combobox.pack(padx=20, pady=10, side=tk.TOP)
    #combobox.grid(row = 1, column = 1)


    feedbackLabel = ctk.CTkLabel(mainFrame, text="")
    savebutton = ctk.CTkButton(mainFrame, text = " Save ", command=lambda: saveIngredient(nameentry, combobox, feedbackLabel))
    savebutton.pack(padx=20, pady=10, side=tk.TOP)
    #savebutton.grid(row = 1, column = 1, padx = 20, pady = 20)
    #feedbackLabel.grid(row = 2, column = 1, padx = 20, pady = 20)
    feedbackLabel.pack(padx = 20, pady = 10, side = tk.TOP)

def addCategoryPage():
    clearPage()

    categoryTitle = ctk.CTkLabel(mainFrame, text = "Add a category", font = pageFont,
                         text_color='#129575')
    categoryTitle.grid(row = 0, column = 0, sticky = 'W', padx = 20, pady = 20)

    nameentry = ctk.CTkEntry(mainFrame, width = 140, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Name")
    feedbackLabel = ctk.CTkLabel(mainFrame, text="", font = feedbackFont)
    savebutton = ctk.CTkButton(mainFrame, text = " Save ", command=lambda: saveCategory(nameentry, feedbackLabel))
    #nameentry.pack(padx = 20, pady = 20, side=tk.LEFT)
    #savebutton.pack(padx=20, pady=10, side=tk.LEFT)
    #feedbackLabel.pack(padx=20, pady=10, side=tk.LEFT)

    nameentry.grid(row = 1, column = 0, padx = 20, pady = 20)
    savebutton.grid(row = 1, column = 1, padx = 20, pady = 20)
    feedbackLabel.grid(row = 2, column = 0, padx = 20, pady = 20)

def addAppliancePage():
    clearPage()

    applianceTitle = ctk.CTkLabel(mainFrame, text = "Add an Appliance", font = pageFont, text_color= '#129575')
    
    applianceTitle.grid(row = 0, column = 0, sticky = 'W', padx = 20, pady = 20)
    #applianceTitle.pack(padx = 20, pady = 20, side = tk.LEFT)
    
    nameentry = ctk.CTkEntry(mainFrame, width = 140, height = 30, bg_color = 'transparent',
                          fg_color = 'transparent', placeholder_text = "Name")
    
    feedbackLabel = ctk.CTkLabel(mainFrame, text="", font = feedbackFont)
    savebutton = ctk.CTkButton(mainFrame, text = " Save ", command=lambda: saveAppliance(nameentry, feedbackLabel))
    
    #nameentry.pack(padx = 20, pady = 20, side=tk.LEFT)
    #savebutton.pack(padx=20, pady=10, side=tk.LEFT)
    #feedbackLabel.pack(padx=20, pady=10, side=tk.LEFT)

    nameentry.grid(row = 1, column = 0, padx = 20, pady = 20)
    savebutton.grid(row = 1, column = 1, padx = 20, pady = 20)
    feedbackLabel.grid(row = 2, column = 0, padx = 20, pady = 20)

# BUTTONS
recipeButton = ctk.CTkButton(master = leftFrame, text = "Home ", command = showScrollable)
addRecipeButton = ctk.CTkButton(master = leftFrame, text = " + Add Recipe ", command = addRecipePage)
addIngredientButton = ctk.CTkButton(master = leftFrame, text = " + Add Ingredient ", command = addIngredientPage)
addCategoryButton = ctk.CTkButton(master = leftFrame, text = " + Add Category ", command = addCategoryPage)
addApplianceButton = ctk.CTkButton(master = leftFrame, text = " + Add Appliance ", command = addAppliancePage)

recipeButton.pack(pady = 20)
addRecipeButton.pack(pady = 20)
addIngredientButton.pack(pady = 20)
addCategoryButton.pack(pady = 20)
addApplianceButton.pack(pady = 20)
#Setting up
showScrollable()
root.mainloop()