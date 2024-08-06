"""Primer ejemplo real de uso de python con una base de datos utilizando una base de datos publica sin alterar (Northwind.db)"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

path = r"D:\Programacion\Python\DataBase\Northwind.db"
colorplot = ['steelblue', 'orange', 'green', 'red',
             'purple', 'blue', 'yellow', 'pink', 'brown', 'gray']
# Obteniendo los 10 productos mas rentables
with sqlite3.connect(path) as conn:
    query = '''
        Select ProductName,SUM(Price*Quantity) as Revenue 
        From OrderDetails as od
        JOIN Products as p ON p.ProductID = od.ProductID
        Group By od.ProductID
        Order By Revenue DESC
        Limit 10
    '''
    top_products = pd.read_sql_query(query, conn)
    # we save the table
    top_products.to_csv("Top_Products.csv")
    top_products.plot(x="ProductName", y="Revenue", kind="bar",
                      figsize=(10, 10), legend=False, color=colorplot)
    plt.title("10 Productos mas rentables")
    plt.xlabel("Productos")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.gca().invert_xaxis()  # Invert x-axis
    fig = plt.savefig("Top_Products.png")
    plt.show()

    # Obteniendo los 10 empleados mas rentables

    query2 = '''
        SELECT FirstName || " " || LastName as Employee,COUNT(*) as TOTAL
        FROM Orders o
        JOIN Employees e
        ON e.EmployeeID = o.EmployeeID
        GROUP BY o.EmployeeID
        ORDER BY TOTAL DESC
        Limit 10
        '''

    top_Sellers = pd.read_sql_query(query2, conn)
    top_Sellers.to_csv("Top_Employees.csv")
    top_Sellers.plot(x="Employee", y="TOTAL", kind="bar",
                     figsize=(10, 10), legend=False, color=colorplot)

    plt.title("10 Empleados mas rentables")
    plt.xlabel("Empleados")
    plt.ylabel("Ordenes")
    plt.xticks(rotation=30)
    plt.gca().invert_xaxis()
    fig = plt.savefig("Top_Employees.png")
    plt.show()

    # Mostrando las ganancias de c/u
    query3 = '''SELECT FirstName || " " || LastName as Employee,
                (
                    SELECT SUM(p.Price * od.Quantity)
                    FROM OrderDetails AS od
                    JOIN Products AS p ON p.ProductID = od.ProductID
                    JOIN Orders AS o ON o.OrderID = od.OrderID
                    WHERE o.EmployeeID = e.EmployeeID
                )AS Ganancias
                FROM 
                Employees AS e
                Limit 9;
            '''
    top_Sellers_Act = pd.read_sql_query(query3, conn)
    top_Sellers_Act.plot(x="Employee", y="Ganancias", kind="bar",
                         figsize=(10, 10), legend=False, color=colorplot)
    top_Sellers_Act.to_csv("Top_Employees_Sells.csv")
    plt.title("10 Empleados mas Exitosos")
    plt.xlabel("Empleados")
    plt.ylabel("Ganancias")
    plt.xticks(rotation=30)
    fig = plt.savefig("Top_Employees_Sells.png")
    plt.show()

    # Aplicando un Update
    query4 = '''Update Employees SET FirstName = 'Diego',LastName = 'Impriglio' '''

    conn.execute(query4)

    # Creando Tabla
    query5 = '''
                CREATE TABLE IF NOT EXISTS Interns (
                    ID INTEGER PRIMARY KEY,
                    FirstName TEXT,
                    LastName TEXT,
                    Age INTEGER,
                    Hours INTEGER
                )
                '''
    query6 = '''INSERT INTO Interns (FirstName,LastName,Age,Hours) 
              VALUES
              ('Pedro','Caballero',24,6),
              ('Juan','Piña',19,5),
              ('Robert','Julians',45,9),
              ('Ana','Sevilla',33,2);
              
            '''
    conn.execute(query5)
    conn.execute(query6)
    conn.commit()
