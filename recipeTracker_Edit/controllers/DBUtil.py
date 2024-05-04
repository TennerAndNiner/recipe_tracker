import mysql.connector
from mysql.connector import connect, Error
global connection, cursor


connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DRAJetEb1_h4tuJE",
        database="recipedata",
        port=3306,

    )
cursor = connection.cursor()
# testing cursor connectivity
cursor.execute("SELECT * FROM IngredientTypes")
for row in cursor:
    print(row)

def getConnection():
    return connection

def getCursor():
    return cursor



    


