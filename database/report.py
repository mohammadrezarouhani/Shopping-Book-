from .models import *


def total_sale_for_each_category() -> List[CategoryLastMonth]:
    query = """
        SELECT 
        Categoreis.title,
        SUM(Products.price * OrderItems.quantity) AS total_value
        FROM OrderItems
        INNER JOIN Products ON OrderItems.product_id = Products.id
        INNER JOIN Categoreis ON Categoreis.id = Products.category_id
        INNER JOIN Orders ON OrderItems.order_id = Orders.id
        where strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')) > datetime('now','-1 month')
        GROUP BY Categoreis.title   
        ORDER BY CAST(total_value AS FLOAT) DESC
        """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [CategoryLastMonth(*item) for item in reports]


def total_number_of_category_book() -> List[CategoryRecordsNumber]:
    query = """
            SELECT Categoreis.title,
            Count(Products.id) as book_number
            FROM Products JOIN Categoreis ON Categoreis.id=Products.category_id  
            GROUP BY Categoreis.title
            ORDER BY CAST(book_number AS INT) DESC
        """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [CategoryRecordsNumber(*item) for item in reports]


def top_ten_best_seller() -> List[TopSellers]:
    query = """
        SELECT 
        Products.publisher,
        SUM(Products.price * OrderItems.quantity) AS total_value
        FROM OrderItems
        INNER JOIN Products ON OrderItems.product_id = Products.id
        INNER JOIN Categoreis ON Categoreis.id = Products.category_id
        INNER JOIN Orders ON OrderItems.order_id = Orders.id
        where strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')) > datetime('now','-3 month')
        GROUP BY Products.publisher
        ORDER BY CAST(total_value AS INT) DESC  LIMIT 10
        """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [TopSellers(*item) for item in reports]


def most_expecive_books() -> List[ExpensiveBook]:
    query = """
            SELECT 
            Categoreis.title ,MAX(CAST(Products.price AS FLOAT)) as price,Products.title  from Products 
            INNER JOIN Categoreis ON Categoreis.id=Products.category_id 
            GROUP BY Categoreis.title
            ORDER BY CAST(price AS INT) DESC
        """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [ExpensiveBook(*item) for item in reports]


def category_distinct_buyers() -> List[CategoryRecordsNumber]:
    query = """SELECT 
            Categoreis.title,
            COUNT(DISTINCT Users.id) as user_count
            FROM OrderItems
            INNER JOIN Products ON OrderItems.product_id=Products.id
            INNER JOIN Categoreis ON Categoreis.id = Products.category_id
            INNER JOIN Orders ON OrderItems.order_id = Orders.id
            INNER JOIN Users on Users.id=Orders.user_id
            where strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')) > datetime('now','-1 month')
            GROUP BY Categoreis.title 
            ORDER BY CAST(user_count AS INT) DESC LIMIT 10
            """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [CategoryRecordsNumber(*item) for item in reports]


def avg_sale_per_customer() -> List[SaleCustomerAvg]:
    query = """SELECT 
            Users.username,
            AVG(Orders.amount) as sale_avg
            FROM Orders
            INNER JOIN Users on Users.id=Orders.user_id
            where strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')) > datetime('now','-1 month')
            GROUP BY Users.id 
            ORDER BY CAST(sale_avg AS FLOAT) DESC
            """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [SaleCustomerAvg(*item) for item in reports]


def avg_number_of_book_per_sale() -> List[ProductNumPerSale]:
    query = """
            SELECT 
            Products.title,
            CAST(AVG(OrderItems.quantity) as INT) as product_number
            FROM Orders
            INNER JOIN OrderItems on OrderItems.order_id=Orders.id
            INNER JOIN Products on Products.id=OrderItems.product_id
            where strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')) > datetime('now','-1 month')
            GROUP BY Products.id 
            ORDER BY CAST(product_number AS INT) DESC
        """

    res = cursor.execute(query)
    reports = res.fetchall()

    return [ProductNumPerSale(*item) for item in reports]


def daily_customer_number_avg() -> int:
    query = """
    SELECT CAST(AVG(users_number) as INT) as users_avg from 
            (SELECT 
            strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')),
            COUNT(Users.id) as users_number
            FROM Orders
            INNER JOIN Users on Users.id=Orders.user_id
            where strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')) > datetime('now','-1 month')
            GROUP BY strftime('%d-%m-%Y', datetime(Orders.purchase_date, 'unixepoch')))
        """

    res = cursor.execute(query)
    report = res.fetchone()
    if report:
        return report[0]
    return None



def sale_per_month_of_year():
    query="""
        SELECT 
        strftime("%m-%Y",datetime(Orders.purchase_date,'unixepoch')) as month,
        CAST(SUM(Products.price*OrderItems.quantity) AS INT)
        FROM Orders 
        INNER JOIN OrderItems on OrderItems.order_id=Orders.id
        INNER JOIN Products on Products.id=OrderItems.product_id
        INNER JOIN  Categoreis on Categoreis.id=Products.category_id
        GROUP BY strftime("%m-%Y",datetime(Orders.purchase_date,'unixepoch'))
        ORDER BY strftime("%m-%Y",datetime(Orders.purchase_date,'unixepoch'))
        """
    res=cursor.execute(query)
    items=res.fetchall()
    
    return [(SalePerMonth(*item))for item in items]
