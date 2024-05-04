CREATE DATABASE IF NOT EXISTS recipedata;
use recipedata;

DROP TABLE IF EXISTS RecipeIngredients;
DROP TABLE IF EXISTS RecipeAppliances;
DROP TABLE IF EXISTS RecipeCategories;
DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Appliances;
DROP TABLE IF EXISTS Ingredients;
DROP TABLE IF EXISTS IngredientTypes;
DROP TABLE IF EXISTS Units;

CREATE TABLE Recipes (
	recipeID INT NOT NULL AUTO_INCREMENT,
    recipeName VARCHAR(100) NOT NULL,
    imagePath VARCHAR(300),
    prepTime INT,
    cookTime INT,
    servingSize INT,
    descriptions VARCHAR(1000),
    instructions VARCHAR(3000),
    PRIMARY KEY (recipeID)
);

CREATE TABLE Categories (
	 categoryID INT NOT NULL AUTO_INCREMENT,
     categoryName VARCHAR(50),
     PRIMARY KEY (categoryID)
);

CREATE TABLE Appliances (
	 applianceID INT NOT NULL AUTO_INCREMENT,
     applianceName VARCHAR(50),
     PRIMARY KEY (applianceID)
);

CREATE TABLE IngredientTypes (
	 ingtypeID INT NOT NULL AUTO_INCREMENT,
     ingtypeName VARCHAR(50),
     PRIMARY KEY (ingtypeID)
);
CREATE TABLE Ingredients (
  ingID INT NOT NULL AUTO_INCREMENT,
  ingtypeID INT,
  ingName VARCHAR(50),
  PRIMARY KEY (ingID),
  FOREIGN KEY (ingtypeID) REFERENCES IngredientTypes(ingtypeID)
);

CREATE TABLE Units (
  unitID INT NOT NULL AUTO_INCREMENT,
  unitName VARCHAR(50),
  PRIMARY KEY (unitID)
);

CREATE TABLE RecipeIngredients (
	recipeID INT NOT NULL,
    ingID INT NOT NULL,
    unitID INT,
    quantity VARCHAR(5),
    PRIMARY KEY (recipeID, ingID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (ingID) REFERENCES Ingredients(ingID),
    FOREIGN KEY (unitID) REFERENCES Units(unitID)
);

CREATE TABLE RecipeAppliances (
	recipeID INT NOT NULL,
    applianceID INT NOT NULL,
    PRIMARY KEY (recipeID, applianceID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (applianceID) REFERENCES Appliances(applianceID)
);

CREATE TABLE RecipeCategories (
	recipeID INT NOT NULL,
    categoryID INT NOT NULL,
    PRIMARY KEY (recipeID, categoryID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID)
);

#Populate DB with default values
INSERT INTO IngredientTypes (ingtypeName) VALUES ('Vegetables & Greens'), ('Fruits'), ('Spices'), ('Dairy & Eggs'), ('Dairy & Meat Substitutes'),
('Meats'), ('Poultry'), ('Herbs & Spices'), ('Seafood'), ('Baking Products, Grain, & Nuts'), ('Fats & Oils'),('Pastas');

INSERT INTO Ingredients (ingtypeID, ingName) VALUES (1, 'Carrot'),(10, 'Flour'),(10, 'Baking Powder'),(10, 'Cream of Tartar'),(11, 'Butter'),(11, 'Vegetable Oil'),(10, 'Vanilla Extract'),
(10, 'Sugar'),(4, 'Cheese'),(3,'Salt'),(3,'Black Pepper'),(12,'Macaroni'),(4, 'Milk');

INSERT INTO Categories (categoryName) VALUES ('Vegetarian'),('Vegan'),('Dinner'),('Mexican'),('Thai'),('Mediterranean'); 

INSERT INTO Appliances (applianceName) VALUES ('Stove'),('Oven'),('Microwave'),('Air Fryer'),('Blender'),('Pasta Maker'),('Toaster');

INSERT INTO	Units (unitName) VALUES ('Cup'),('Teaspoon'),('Tablespoon'),('Milliliter'),('Fluid Ounce'),('Pound'),('Ounce');

SELECT * FROM Units;
SELECT * FROM Categories;

SELECT * FROM RecipeCategories;
SELECT * FROM RecipeAppliances;
SELECT * FROM RecipeIngredients;

SELECT * FROM Recipes;
