## Features

### Module # 1 - Automated Transaction Recording Module

![Screen](Images/AutomatedTransactionRecordingModule.png)
![Screen](Images/AccountInfo.png)

This module handles the automatic recording, categorization, and updating of financial transactions.

#### Feature 1a: Transaction Entry

##### Description: 

The system automatically records financial transactions such as sales, purchases, payments, and receipts.

##### User Access:

1) Administrator: Can view, edit, and delete all transactions.
2) Accountant: Can create and edit transactions but cannot delete them.
3) Auditor: Can view all transactions.

#### Feature 1b: Transaction Categorization

##### Description: 

Automatically categorizes transactions into predefined categories (e.g., revenue, expenses) based on rules set by the Administrator.

##### User Access:

1) Administrator: Can set and modify categorization rules.
2) Accountant: Can view and apply categorization rules.
3) Auditor: Can view categorized transactions.

#### Feature 1c: Account Balances Update

##### Description: 

The system updates account balances after each transaction is recorded.

##### User Access:

1) Administrator: Can view all account balances and manually adjust them if necessary.
2) Accountant: Can view account balances but cannot adjust them.
3) Auditor: Can view account balances and audit changes.

### Module # 2 - Financial Reporting Module

![Screen](Images/Picture2.png)

This module generates various financial reports for analysis and decision-making.

#### Feature 2a: Cash Flow Statement Generation

##### Description: 

Generates a cash flow statement detailing the inflows and outflows of cash.

##### User Access:

1) Administrator: Can generate, customize, and save cash flow statements.
2) Accountant: Can generate and save cash flow statements.
3) Auditor: Can generate and view cash flow statements for auditing purposes.

### Module # 3 - User Access Control Module

![Screen](Images/Picture3.png)

![Screen](Images/Picture4.png)

This module manages user roles, access levels, and security protocols.

#### Feature 3a: Role-Based Access Control

##### Description: 

The system assigns specific roles (Administrator, Accountant, Auditor) to users, defining their access level and permissions.

##### User Access:

1) Administrator: Can create, modify, and delete user roles and assign permissions.
2) Accountant: No access to role management.
3) Auditor: Can view user roles and permissions for audit purposes.

### Additional Features (Tentative)

#### Feature 4a: Authentication and Authorization

##### Description: 

The system requires users to log in with a username and password. Authorization is based on their role.

##### User Access:

1) Administrator: Can view login activity logs and modify authentication settings.
2) Accountant: Can log in and perform assigned tasks.
3) Auditor: Can log in and view audit logs related to user access.

#### Feature 4b: Income Statement Generation

##### Description: 

Generates an income statement summarizing revenues, costs, and expenses over a specific period.

##### User Access:

1) Administrator: Can generate, customize, and save income statements.
2) Accountant: Can generate and save income statements.
3) Auditor: Can generate and view income statements for auditing purposes.

#### Feature 4c: Balance Sheet Generation

##### Description: 

Generates a balance sheet showing the organization’s assets, liabilities, and equity.

##### User Access:

1) Administrator: Can generate, customize, and save balance sheets.
2) Accountant: Can generate and save balance sheets.
3) Auditor: Can generate and view balance sheets for auditing purposes.
