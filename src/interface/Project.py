# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView , QMessageBox
import sys
import pyodbc


class USER(QtWidgets.QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(USER, self).__init__() 

        self.connection_string = connection_string
        self.User_DataTable()
    

    def User_DataTable(self):
        # Load the .ui file
        uic.loadUi('../../screens/Project_UserAccessControl.ui', self)
        self.setWindowTitle("User Acess Control")

        self.populate_users()
        
        self.Search_Button.clicked.connect(self.search)        # Connect the search function with the search button.
        self.Delete_Button.clicked.connect(self.delete)        # Connect the delete function with the delete button.
        self.Close_Button.clicked.connect(self.end)         # Connect the close function with the close button.
        self.Add_Button.clicked.connect(self.add)
        self.Edit_Button.clicked.connect(self.edit)
        self.EditRoleSettings_Button.clicked.connect(self.editRoleSettings)

    def end(self):
        self.close()

    def populate_users(self):         

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select U.USER_ID, U.USER_NAME, CONVERT(DATE, U.USER_DOB) as 'Birth_Date', JR.JOB_TITLE, U.USER_EMAIL, U.USER_PASSWORD 
                        from [User] U
                        inner join JobRole JR on JR.JOB_ROLE_ID = U.FK_JOB_ROLE_ID
                        Order by JR.JOB_ROLE_ID""")
        
        self.UserTable.clearContents()
        self.UserTable.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.UserTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.UserTable.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.UserTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    def search(self):
        search_txt = self.Search_Input.text()
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        query = """
            SELECT U.USER_ID, U.USER_NAME, CONVERT(DATE, U.USER_DOB) AS 'Birth_Date', 
                JR.JOB_TITLE, U.USER_EMAIL, U.USER_PASSWORD 
            FROM [User] U
            INNER JOIN JobRole JR ON JR.JOB_ROLE_ID = U.FK_JOB_ROLE_ID
            WHERE LOWER(U.USER_NAME) LIKE ?
        """
        # Add wildcards around the search text for partial matching
        cursor.execute(query, ('%' + search_txt.lower() + '%',))
                
        self.UserTable.clearContents()
        self.UserTable.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.UserTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.UserTable.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.UserTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    def populate_combobox_job_roles(self):
        # Connect to the database
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # Execute the query to fetch job roles
        query = "SELECT JOB_TITLE FROM JobRole ORDER BY JOB_TITLE"
        cursor.execute(query)

        # Fetch all job roles
        job_roles = [row[0] for row in cursor.fetchall()]

        # Add job roles to the QComboBox
        self.JobRoleComboBox.addItems(job_roles)

        cursor.close()
        connection.close()

    def Insert_User(self):
         
        UserName = self.UserName.text()
        UserDOB = self.UserDOB.date().toPyDate()  # Convert to Python's datetime.date
        JobRoleComboBox = self.JobRoleComboBox.currentText()  # Get the selected text
        UserEmail = self.UserEmail.text()
        UserPassword = self.UserPassword.text()

        # SQL query to get JOB_ROLE_ID based on JOB_TITLE
        job_role_query = "SELECT JOB_ROLE_ID FROM JobRole WHERE JOB_TITLE = ?"

        # SQL query to insert into [User] table
        query = """
        INSERT INTO [User] (USER_NAME, USER_DOB, FK_JOB_ROLE_ID, USER_EMAIL, USER_PASSWORD)
        VALUES (?, ?, ?, ?, ?)
        """

        # Connect to the database
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # Get JOB_ROLE_ID for the given job title
        cursor.execute(job_role_query, (JobRoleComboBox,))
        job_role_id = cursor.fetchone()

        # insert query execute
        cursor.execute(query, (UserName,UserDOB, job_role_id[0], UserEmail, UserPassword,))

        # Commit the changes
        connection.commit()
        print("Data inserted successfully!")

        self.User_DataTable()

    def add(self):

        uic.loadUi('../../screens/Project_NewUser.ui', self)
        # Clear previous content if needed
        self.populate_combobox_job_roles()
        self.Done_Button.clicked.connect(self.Insert_User)
        self.Cancel_Button.clicked.connect(self.User_DataTable)

    def Update_User(self, userid):
         
        UserName = self.UserName.text()
        UserDOB = self.UserDOB.date().toPyDate()  # Convert to Python's datetime.date
        JobRoleComboBox = self.JobRoleComboBox.currentText()  # Get the selected text
        UserEmail = self.UserEmail.text()
        UserPassword = self.UserPassword.text()

        # SQL query to get JOB_ROLE_ID based on JOB_TITLE
        job_role_query = "SELECT JOB_ROLE_ID FROM JobRole WHERE JOB_TITLE = ?"

        # SQL query to update the [User] table
        query = """
        UPDATE [User]
        SET 
            USER_NAME = ?,
            USER_DOB = ?,
            FK_JOB_ROLE_ID = ?,
            USER_EMAIL = ?,
            USER_PASSWORD = ?
        WHERE USER_ID = ?
        """

        # Connect to the database
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # Get JOB_ROLE_ID for the given job title
        cursor.execute(job_role_query, (JobRoleComboBox,))
        job_role_id = cursor.fetchone()

        # insert query execute
        cursor.execute(query, (UserName,UserDOB, job_role_id[0], UserEmail, UserPassword, userid,))

        # Commit the changes
        connection.commit()
        print("Data inserted successfully!")

        self.User_DataTable()

    def edit(self):
        
        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText ("Are you sure you want to edit this User?")
        dig.setIcon(QMessageBox.Icon.Warning) 
        dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            userid = self.UserTable.item(self.UserTable.currentRow(), 0).text()
            print(userid)
            uic.loadUi('../../screens/Project_NewUser.ui', self)
            # Clear previous content if needed
            self.populate_combobox_job_roles()
            self.Done_Button.clicked.connect(lambda: self.Update_User(userid))
            self.Cancel_Button.clicked.connect(self.User_DataTable)

    def delete(self):
        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText ("Are you sure you want to delete this user?")
        dig.setIcon(QMessageBox.Icon.Warning) 
        dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            useridvalue = self.UserTable.item(self.UserTable.currentRow(), 0).text()
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()
            query = """Delete from [User] where User_id = ?"""
            cursor.execute(query, (useridvalue,))           
           # Commit the transaction to apply the changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            self.populate_users()

    def deleteRole(self):
            dig = QMessageBox(self)
            dig.setWindowTitle("Confirmation Box")
            dig.setText ("Are you sure you want to delete this Role?")
            dig.setIcon(QMessageBox.Icon.Warning) 
            dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
            response = dig.exec()

            if response == QMessageBox.StandardButton.Yes:
                JobTitlevalue = self.JobTable.item(self.JobTable.currentRow(), 0).text()
                connection = pyodbc.connect(self.connection_string)
                cursor = connection.cursor()
                query = """Delete from [JobRole] where lower(JOB_TITLE) = ?"""
                cursor.execute(query, (JobTitlevalue.lower(),))     
                # Commit the transaction to apply the changes
                connection.commit()

                # Close the cursor and connection
                cursor.close()
                connection.close()

                self.editRoleSettings()

    def addjobtitle(self):
        # Get the text from the input field
        JobTitleValue = self.JobTitleValue.text().title().strip()

        print(JobTitleValue)
        # Check if the input is empty
        if JobTitleValue != "":
            # Connect to the database
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # Define the INSERT query
            query = """
            INSERT INTO JobRole (JOB_TITLE)
            VALUES (?)
            """

            # Execute the query with the parameterized value
            cursor.execute(query, (JobTitleValue,))
            
            # Commit the changes
            connection.commit()

            # Provide feedback
            print(f"Job Title '{JobTitleValue}' added successfully!")

            # Clean up resources
            cursor.close()
            connection.close()

            self.editRoleSettings()
        else:
            print("Job Title cannot be empty!")
            self.editRoleSettings()  # return to the function again

    def editjobtitle(self, JobTitlevalue):
        # Get the text from the input field
        prev_val = JobTitlevalue
        JobTitleValue = self.JobTitleValue.text().title().strip()

        print(JobTitleValue)
        # Check if the input is empty
        if JobTitleValue != "":
            # Connect to the database
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # Define the update query
            query = """
            UPDATE [JobRole]
            SET JOB_TITLE = ?
            WHERE LOWER(JOB_TITLE) = LOWER(?)
            """

            # Execute the update query with parameters
            cursor.execute(query, (JobTitleValue.strip(), prev_val.strip()))
            connection.commit()

            print(f"Job title '{prev_val}' successfully updated to '{JobTitleValue}'!")

            self.editRoleSettings()
        else:
            print("Job Title cannot be empty!")
            self.editRoleSettings()  # return to the function again

    def addRole(self):
        uic.loadUi('../../screens/Project_NewJobRole.ui', self)
        # Clear previous content if needed
        self.JobTitleValue.clear()
        self.Done_Button.clicked.connect(self.addjobtitle)
        self.Cancel_Button.clicked.connect(self.editRoleSettings)

    def editRole(self):
        # Clear previous content if needed

        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText ("Are you sure you want to edit this Role?")
        dig.setIcon(QMessageBox.Icon.Warning) 
        dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            current_val = self.JobTable.item(self.JobTable.currentRow(), 0).text()
            # print(current_val)
            uic.loadUi('../../screens/Project_NewJobRole.ui', self)
            self.JobTitleValue.clear()
            self.Done_Button.clicked.connect(lambda: self.editjobtitle(current_val))
            self.Cancel_Button.clicked.connect(self.editRoleSettings)

    def editRoleSettings(self):
        #Load the .ui file
        uic.loadUi('../../screens/Project_EditRoleSettings.ui', self)

        self.setWindowTitle("Edit Role Settings")

        # Connect to the database
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # Execute the query to fetch job titles
        cursor.execute("""
            SELECT JR.JOB_Title
            FROM [JobRole] JR
            ORDER BY JR.JOB_ROLE_ID
        """)

        # Clear the table and reset its contents
        self.JobTable.clearContents()
        self.JobTable.setRowCount(0)

        # Set the column count to match the query result (1 column: JOB_Title)
        self.JobTable.setColumnCount(1)  # Explicitly set to 1 column

        # Optional: Set the column header
        self.JobTable.setHorizontalHeaderLabels(["Job Title"])


        self.JobTable.clearContents()
        self.JobTable.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.JobTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.JobTable.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        # JobTitlevalue = self.JobTable.item(self.JobTable.currentRow(), 0).text()

        self.DeleteRole_Button.clicked.connect(self.deleteRole)        # Connect the delete function with the delete button.
        self.Close_Button.clicked.connect(self.User_DataTable)         # Connect the close function with the close button.
        self.AddRole_Button.clicked.connect(self.addRole)
        self.EditRole_Button.clicked.connect(self.editRole)

        # Adjust content display
        header = self.JobTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)


def main():
    app = QApplication(sys.argv)
    window = USER()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
