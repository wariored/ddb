# This middleware is written in python. It allows you to make request in two databases

**In order to realize the middleware I chose the following scenario:**

Firstly I relied on the default Oracle DB with the HR user (this database already contains data). Subsequently I performed a horizontal fragmentation of employees (EMPLOYEE table) according to their departments (DEPARTMENT_ID column). Thus, we have two fragments having on the one hand the employees of the Department of Shipping with the id 50 and on the other hand the employees of the other departments (id = 50). We then get a central database that is in the Oracle DBMS and contains all the employees as well as the Shipping fragment (EMPLOYEE_SHIPPING table) and another MySQL database (named EMPLOYEES) that contains employees from other departments (table EMPLOYEE_AUTRES ).

Thus, thanks to our middleware, we will be able to perform insertion, selection, update and deletion requests. The user will just have to make a request and the middleware will call the corresponding table.

## FONCTIONS

**insert_employee_shipping (employee_infos):**

This function will allow the insertion of an employee into the Oracle DB. It takes an employee_infos parameter that is an array that contains the employee information to add (employee_id, firt_name, last_name, email, phone_number, hire_date, salary). Once the employee is added to the EMPLOYEE_SHIPPING table, the id is then saved to a file called shipping.txt (see THE FILES section).

**insert_employee_others (employee_infos):**

This function does the same thing as the previous one but by inserting the employee in the MySQL database (table EMPLOYEE_AUTRES) and saving the id in others.txt.

**list_employeesID (file):**

This function takes as parameter a txt file (shipping.txt or others.txt) and returns the list of ids that are in this file.

**select_employees (section, employee_id = 0):**

This function will allow the retrieval of one or more employees depending on the requested section (fragment). It takes as parameter the section which designates the fragment where the request will be made and the id of the employee initialized to 0. If employee_id is 0, then we will know that the user wants to visualize all the employees and he will be oriented at the level of the desired section. Otherwise, if the employee_id is not 0, we consider that it wants to select an employee, so the insert_employee_shipping (file) function is called to see which fragment the employee is in.
In the case where id_employee = 0, the function returns a dictionary containing the list of all the employees of the given fragment and in the opposite case, it returns a table containing the information of the employee whose id has been given.

**delete_employee (employee_id):**

This function takes the id of an employee as parameter and then allows it to be deleted. We have two lists ls1 and ls2 which contain the Shipping employees and the other employees respectively. Depending on the id entered, we will move in the concerned DB, perform the deletion and update the list.

**update_employee (employee_id, email = None, phone_number = None, salary = None):**

This function will be used to update employees. It takes as parameter the id of the employee and the information (initialized to None) that can be updated. Depending on where the employee is located, we will be able to update each parameter or all at once.

**update_list_employeesID (update_type, file, id_value = 0, remove = False):**

This one is used to update txt files.

## TXT FILES

Two txt files (shypping.txt and others.txt) exist and record the employee IDs contained in each fragment.
These files allow us not to connect to databases every time to find an employee, which makes the middleware very powerful. The consultation of the files tells us directly in which fragment is an employee.
At first the txt files are empty. Just run the command below to load the ids of each fragment into the corresponding file.
> python connect.py

**Notice:** Files are updated each time there is insertion or deletion.
