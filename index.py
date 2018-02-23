import connect
import time

while 1:
	choice = input("What do you want to do ? \n\
		1- Add new employee\n\
		2- Delete an employee\n\
		3- View list employees from a table\n\
		4- View an employee by id\n\
		5- Update an employee data\n\
		You can anytime type 'Q' to quit\n")
	if choice.upper() == "Q":
		break
	elif choice == '1':
		print("Your choice is 1")
		employee_infos = ()
		while len(employee_infos) != 8:
			print("Enter employee's information separated by ', ' ")
			# employee_infos prend les valeurs employee_id, firt_name, last_name, email, phone_number, hire_date, salary, department_id
			employee_infos = input()
			if employee_infos.upper() == "Q":
				break
			employee_infos = employee_infos.split(', ')
			if len(employee_infos) == 8:
				if employee_infos[7] == '50':
					del employee_infos[-1]
					connect.insert_employee_shipping(employee_infos)
					print("Employee added")
					break
				if employee_infos[7] != '50':
					connect.insert_employee_others(employee_infos)
					print("Employee added")
					break
			else:
				print('Wrong format. Try again!!')
	elif choice == '2':
		print("Your choice is 2")
		employee_id = input("Enter ID of employee you want to delete : ")
		if employee_id.upper() == "Q":
			break
		connect.delete_employee(employee_id)
	elif choice == '3':
		print("Your choice is 3")
		table = input('Which section of employees would you like to consult: ')
		if table.upper() == 'Q':
			break
		if table.upper() in ('SHIPPING', 'OTHERS'):
			ls = connect.select_employees(table)
			print(ls)
		else:
			print('That section does not exist')
	elif choice == '4':
		print("Your choice is 4")
		employee_id = input('Enter employee id : ')
		if employee_id.upper() == 'Q':
			break
		employee_infos = connect.select_employees('', employee_id)
		print(employee_infos)
	elif choice == '5':
		print("Your choice is 5")
		print('Enter employee ID, new email, new phone number and new salary')
		data = input()
		data = data.split(', ')
		print(data)
		connect.update_employee(data[0], data[1], data[2], data[3])
	else:
		print("Wrong Choice. Note that you can anytime type 'Q' to quit.")
		time.sleep(3)

print('Good Bye!!')
