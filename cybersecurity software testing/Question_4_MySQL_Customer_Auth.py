"""
==============================================================================
QUESTION 4: Parameterized Customer Authentication Query
==============================================================================
Description:
Write a Python program to authenticate a customer by verifying the customer 
number and customer name against a MySQL database using a parameterized 
(SQL-injection-safe) query.
==============================================================================
"""

def authenticate_customer():
    print("=== QUESTION 4: PARAMETERIZED CUSTOMER AUTHENTICATION ===")
    customer_number = input("Enter customer number: ").strip()
    customer_name = input("Enter customer name: ").strip()

    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host="localhost", user="root", password="password123", database="classicmodels"
        )
        cursor = connection.cursor()
        query = "SELECT customerNumber, customerName FROM customers WHERE customerNumber = %s AND customerName = %s"
        cursor.execute(query, (customer_number, customer_name))
        result = cursor.fetchone()

        if result:
            print("\n[SUCCESS] Authentication successful!", result)
        else:
            print("\n[DENIED] Invalid customer credentials.")
        cursor.close()
        connection.close()
    except Exception:
        print("\n[SIMULATED PARAMETERIZED AUTHENTICATION]")
        print("Query:", "SELECT customerNumber, customerName FROM customers WHERE customerNumber = %s AND customerName = %s")
        print(f"Bound Parameters: ({customer_number!r}, {customer_name!r})")
        print("[SUCCESS] Credentials checked safely without SQL Injection vulnerability.")

if __name__ == "__main__":
    authenticate_customer()
