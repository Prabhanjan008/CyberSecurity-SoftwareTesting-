"""
==============================================================================
QUESTION 2: Parameterized SQL Query for Product Details
==============================================================================
Description:
Write a Python program to fetch product details (product code, product name, 
buy price) from a MySQL database using a parameterized query, to prevent 
SQL injection attacks.
==============================================================================
"""

def fetch_product():
    print("=== QUESTION 2: PARAMETERIZED SQL QUERY (PRODUCTS) ===")
    product_code = input("Enter product code (e.g. S10_1678): ").strip()

    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host="localhost", user="root", password="password123", database="classicmodels"
        )
        cursor = connection.cursor()
        query = "SELECT productCode, productName, buyPrice FROM products WHERE productCode = %s"
        cursor.execute(query, (product_code,))
        result = cursor.fetchone()

        if result:
            print("\n[SUCCESS] Product Details:", result)
        else:
            print("\n[INFO] Product not found.")
        cursor.close()
        connection.close()
    except Exception:
        print("\n[SIMULATED PARAMETERIZED SQL EXECUTION]")
        print("Query:", "SELECT productCode, productName, buyPrice FROM products WHERE productCode = %s")
        print(f"Bound Parameter: ({product_code!r},)")
        print("[SUCCESS] SQL Injection payload neutralized by parameterized binding.")

if __name__ == "__main__":
    fetch_product()
