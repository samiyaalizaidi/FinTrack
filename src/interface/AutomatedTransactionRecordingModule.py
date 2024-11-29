from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView , QMessageBox
import sys
import pyodbc


# Replace these with your own database connection details
server = 'DESKTOP-6M55HJA\\SQLSERVER1'
database = 'Fintrack'  # Name of your Fintrack database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = '1234'  # Specify a password if not using Windows Authentication

#  Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


class Transaction(QtWidgets.QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(Transaction, self).__init__() 
        # Load the .ui file
        uic.loadUi('../../screens/AutomatedTransactionRecordingModule.ui', self) 
        
        self.connection_string = connection_string

        # Set Window Title
        self.setWindowTitle('Transaction Recording Module')

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID""")

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

        
        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.transactions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # Connect the search function with the search button.
        self.search_button.clicked.connect(self.search)
        
        # Connect the reset function with the reset button.
        self.reset_button.clicked.connect(self.reset)
        
        # Connect the view function with the view button.
        self.view_button.clicked.connect(self.view)

        # Connect the delete function with the delete button.
        self.delete_button.clicked.connect(self.delete)
        
        # Connect the add function with the add button.
        self.add_button.clicked.connect(self.add)

        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

    def end(self):
        self.close()

    def update(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID""")

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

        
        # Close the database connection
        connection.close()
        
    def reset(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID""")

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

    
    def search(self):
        # Clear only the table contents, preserving headers
        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)  # Reset the row count to zero
        
        # Get search input values
        category = self.category_input.currentText().strip()
        sub_category = self.sub_category_input_2.currentText().strip()

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        query = """select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID
                        where 
                        C.CATEGORY_NAME = ? and S.SUB_CATEGORY_NAME = ?
                        """
        
        cursor.execute(query, (category, sub_category,))

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
               
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()
        
        # Adjust content display
        header = self.transactions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)      
      
    def add(self):
        # Pass all the data to view form as parameters
        self.add_form = AddTransaction(self, self.connection_string)
        self.add_form.show()     

        # # Collect data from the input fields
        # category = self.category_input.currentText()
        # sub_category = self.sub_category_input_2.currentText()
        # amount = self.amount_input.text()
        # payment_method = self.payment_method_input.text()
        # expense_type = self.expense_type_input.text()
        # account_number = self.account_number_input.text()
        # date = self.date_input.date().toString("yyyy-MM-dd")  # Convert QDate to string

        # # Validate the input to ensure no field is empty (You can adjust this validation as needed)
        # if not category or not sub_category or not amount or not payment_method or not expense_type or not account_number or not date:
        #     QMessageBox.warning(self, "Input Error", "Please fill in all fields to add a transaction.")
        #     return
        
        # connection = pyodbc.connect(connection_string)
        # cursor = connection.cursor()
        # query = """select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
        #                 FROM [TRANSACTION] T
        #                 inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
        #                 inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
        #                 inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
        #                 inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
        #                 inner join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID
        #                 where 
        #                 C.CATEGORY_NAME = ? and S.SUB_CATEGORY_NAME = ?
        #                 """
        
        # cursor.execute(query, (category, sub_category,))

        # # Get the last inserted row ID (for display purposes, optional)
        # transaction_id = cursor.lastrowid

        # # Close the database connection
        # connection.close()


        # # Create a new transaction (all data is treated as strings)
        # new_transaction = [
        #     str(len(transactions) + 1),  # Generate a new transaction ID (assuming IDs are sequential)
        #     category,
        #     date,
        #     payment_method,
        #     sub_category,
        #     account_number,  # Account number remains a string
        #     amount,  # Amount is a string
        #     expense_type
        # ]

        # # Add the new transaction to the list
        # transactions.append(new_transaction)

        # # Update the table to show the new transaction
        # row_position = self.transactions_table.rowCount()
        # self.transactions_table.insertRow(row_position)  # Insert a new row at the end

        # # Fill the new row with the new transaction data
        # for col, value in enumerate(new_transaction):
        #     item = QtWidgets.QTableWidgetItem(str(value))
        #     item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        #     self.transactions_table.setItem(row_position, col, item)

        # # Optionally, reset all input fields after adding the transaction
        # self.category_input.setCurrentIndex(0)
        # self.sub_category_input_2.setCurrentIndex(0)
        # self.amount_input.clear()
        # self.payment_method_input.clear()
        # self.expense_type_input.clear()
        # self.account_number_input.clear()
        # self.date_input.setDate(QtCore.QDate.currentDate())
      
    def delete(self):
        # dig = QMessageBox(self)
        # dig.setWindowTitle("Confirmation Box")
        # dig.setText ("Are you sure you want to delete this transaction?")
        # dig.setIcon(QMessageBox.Icon.Warning) 
        # dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        # response = dig.exec()

        # if response == QMessageBox.StandardButton.Yes:
        #     id = self.transaction_table.item(self.transaction_table.currentRow(), 0).text()
        #     connection = pyodbc.connect(self.connection_string)
        #     cursor = connection.cursor()
        #     query = """Delete from [Transaction] where Transaction_ID = ?"""
        #     cursor.execute(query, (id,))           
        #    # Commit the transaction to apply the changes
        #     connection.commit()

        #     # Close the cursor and connection
        #     cursor.close()
        #     connection.close()

        # self.update()

        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText("Are you sure you want to delete this transaction?")
        dig.setIcon(QMessageBox.Icon.Warning)
        dig.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            current_row = self.transactions_table.currentRow()
            if current_row >= 0:  # Check if a valid row is selected
                id = self.transactions_table.item(current_row, 0).text()
                
                try:
                    connection = pyodbc.connect(self.connection_string)
                    cursor = connection.cursor()
                    
                    # Check if the transaction exists
                    cursor.execute("SELECT COUNT(*) FROM [Transaction] WHERE Transaction_ID = ?", (id,))
                    count = cursor.fetchone()[0]
                    if count == 0:
                        QMessageBox.warning(self, "Error", "Transaction not found")
                        return
                    
                    # Proceed with the delete query
                    query = """DELETE FROM [Transaction] WHERE Transaction_ID = ?"""
                    cursor.execute(query, (id,))
                    
                    # Commit the transaction to apply the changes
                    connection.commit()

                except pyodbc.Error as e:
                    print("Database error:", e)
                    QMessageBox.warning(self, "Database Error", "An error occurred while deleting the transaction.")
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()

                self.update()  # Assuming this is a valid method to update the UI
            else:
                QMessageBox.warning(self, "Error", "No transaction selected")

        # # Get the selected row
        # selected_row = self.transactions_table.currentRow()

        # # Check if a row is selected
        # if selected_row >= 0:
        #     # Remove the corresponding transaction from the list
        #     del transactions[selected_row]

        #     # Remove the selected row from the table
        #     self.transactions_table.removeRow(selected_row)

    #     # Optionally, show a confirmation message
    #     QMessageBox.information(self, "Success", "Transaction deleted successfully.")
    # else:
    #     # If no row is selected, show a warning message
    #     QMessageBox.warning(self, "No Selection", "Please select a transaction to delete.")
        

            
    def view(self):
        if(self.transactions_table.selectedIndexes()!=0):
            row = self.transactions_table.currentRow()
            id = self.transactions_table.item(row,0).text()
            category = self.transactions_table.item(row,1).text()
            date = self.transactions_table.item(row,2).text()
            payment_method = self.transactions_table.item(row,3).text()
            sub_category = self.transactions_table.item(row,4).text()
            account_number = self.transactions_table.item(row,5).text()
            amount = self.transactions_table.item(row,6).text()
            expense_type = self.transactions_table.item(row,7).text()
        
        # Pass all the data to view form as parameters
        self.view_form = ViewTransaction(id, category, date, payment_method, sub_category, account_number, amount, expense_type)
        self.view_form.show()     
    

class ViewTransaction(QtWidgets.QMainWindow):  
    def __init__(self, id, category, date, payment_method, sub_category, account_number, amount, expense_type):
        super().__init__()
        uic.loadUi('../../screens/ViewTransaction.ui', self)

        # Receive Data from the Main Form
        self.id = id
        self.category = category
        self.date = date
        self.payment_method = payment_method
        self.sub_category = sub_category
        self.account_number = account_number
        self.amount = amount
        self.expense_type = expense_type

        # Set Window Title
        self.setWindowTitle('View Transaction')

        self.id_input.setText(self.id)
        self.category_input.setText(self.category)
        self.date_input.setDate(QtCore.QDate.fromString(self.date, "yyyy-MM-dd"))
        self.payment_method_input.setText(self.payment_method)
        self.sub_category_input.setText(self.sub_category)
        self.account_number_input.setText(self.account_number)
        self.amount_input.setText(self.amount)
        self.expense_type_input.setText(self.expense_type)
        
        self.id_input.setReadOnly(True)
        self.category_input.setReadOnly(True)
        self.date_input.setReadOnly(True)
        self.payment_method_input.setReadOnly(True)
        self.sub_category_input.setReadOnly(True)
        self.account_number_input.setReadOnly(True)
        self.amount_input.setReadOnly(True)
        self.expense_type_input.setReadOnly(True)
        
        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

    def end(self):
        self.close()

class AddTransaction(QtWidgets.QMainWindow):  
    def __init__(self, parent_window, connection_string):
        super().__init__()
        uic.loadUi('../../screens/AddTransaction.ui', self)

        # Set Window Title
        self.setWindowTitle('Add Transaction')

        self.parent_window = parent_window
        self.connection_string = connection_string

        # # Validate the input to ensure no field is empty (You can adjust this validation as needed)
        # if not amount or not payment_method or not expense_type or not account_number or not date:
        #     QMessageBox.warning(self, "Input Error", "Please fill in all fields to add a transaction.")
        #     return
        
        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

        # self.save_button.clicked.connect(self.save(date, payment_method, account_number, amount, expense_type))
        self.save_button.clicked.connect(self.save)


    def save(self):

        # Collect data from the input fields
        amount = float(self.amount_input.text())
        payment_method = self.payment_method_input.currentText()
        expense_type = self.expense_type_input.currentText()
        account_number = self.account_number_input.text()
        date = self.date_input.date().toPyDate()  # Convert QDate to string

        print(type(amount))
        print(amount, payment_method, expense_type, account_number, date)


        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        
        # # Insert the new transaction into the database
        # cursor.execute("""
        #     INSERT INTO [Transaction] (TRANSACTION_DATE, FK_PAYMENT_METHOD_ID, FK_ACCOUNT_ID, TRANSACTION_AMOUNT, FK_EXPENSE_ID)
        #     VALUES (?, (SELECT P.PAYMENT_METHOD_ID FROM PaymentMethod P WHERE PAYMENT_METHOD_NAME = ?), 
        #                (SELECT A.ACCOUNT_ID FROM ACCOUNT A WHERE ACCOUNT_NUM = ?), ?, 
        #                (SELECT E.EXPENSE_ID FROM EXPENSETYPE E WHERE EXPENSE_TITLE = ?))
        # """, (date, payment_method, account_number, amount, expense_type))

        try:
            cursor.execute("""
                INSERT INTO [Transaction] (TRANSACTION_DATE, FK_PAYMENT_METHOD_ID, FK_ACCOUNT_ID, TRANSACTION_AMOUNT, FK_EXPENSE_ID)
                VALUES (?, 
                        (SELECT P.PAYMENT_METHOD_ID FROM PaymentMethod P WHERE PAYMENT_METHOD_NAME = ?), 
                        (SELECT A.ACCOUNT_ID FROM ACCOUNT A WHERE ACCOUNT_NUM = ?), ?, 
                        (SELECT E.EXPENSE_ID FROM EXPENSETYPE E WHERE EXPENSE_TITLE = ?))
            """, (date, payment_method, account_number, amount, expense_type))
            connection.commit()  # Commit if the insert was successful
        except Exception as e:
            print("Error executing insert:", e)
            connection.rollback()  # Rollback in case of error

                # Close the database connection
        connection.close()

        # Update the table in the parent window
        self.parent_window.update()
        # Show a success message and close the window
        QtWidgets.QMessageBox.information(self, "Success", "Transaction Updated Successfully")
        self.close()

    def end(self):
        self.close()

# app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
# window = Transaction(connection_string) # Create an instance of our 
# window.show()
# app.exec() # Start the application