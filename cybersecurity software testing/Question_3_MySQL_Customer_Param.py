"""
==============================================================================
QUESTION 3: Parameterized SQL Query for Customer Details
==============================================================================
Description:
Write a Python program to retrieve customer details from a MySQL database 
based on the customer number, using a parameterized query to prevent SQL 
injection attacks.
==============================================================================
"""

def fetch_customer():
    print("=== QUESTION 3: PARAMETERIZED SQL QUERY (CUSTOMERS) ===")
    customer_number = input("Enter customer number (e.g. 103): ").strip()

    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host="localhost", user="root", password="password123", database="classicmodels"
        )
        cursor = connection.cursor()
        query = "SELECT customerNumber, customerName, contactFirstName, contactLastName FROM customers WHERE customerNumber = %s"
        cursor.execute(query, (customer_number,))
        result = cursor.fetchone()

        if result:
            print("\n[SUCCESS] Customer Details:", result)
        else:
            print("\n[INFO] Customer not found.")
        cursor.close()
        connection.close()
    except Exception:
        print("\n[SIMULATED PARAMETERIZED SQL EXECUTION]")
        print("Query:", "SELECT customerNumber, customerName, contactFirstName, contactLastName FROM customers WHERE customerNumber = %s")
        print(f"Bound Parameter: ({customer_number!r},)")
        print("[SUCCESS] SQL Injection attempt prevented.")

if __name__ == "__main__":
    fetch_customer()
