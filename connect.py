import cx_Oracle, pymysql, pickle
from datetime import datetime

def start_mysql_connection():
	try:
		cnx = pymysql.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='employees')
	except Exception as e:
		print ('An error occured while connecting to MySQL:', e)

	cursor = cnx.cursor()
	return cnx, cursor

def start_oracle_connection():
	try:
		con = cx_Oracle.connect('hr/oracle@127.0.0.1/orcl')
	except Exception as e:
		print ('An error occured while connecting to Oracle:', e)
	cur = con.cursor()
	return con, cur

def close_connection(con, cur):
	cur.close()
	con.close()

# fonction se chargeant de l'insertion dans le fragment Shipping(Oracle database)
# employee_infos prend les valeurs employee_id, firt_name, last_name, email, phone_number, hire_date, salary
# Function for insert employee in Shipping database (Oracle database)
def insert_employee_shipping(employee_infos):
	employee_infos[5] = datetime.strptime(employee_infos[5] , '%d-%b-%Y')
	con, cur = start_oracle_connection()
	statement = 'insert into employees_shipping(employee_id, first_name, last_name, email, phone_number, hire_date, salary) ' + \
		'values (:1, :2, :3, :4, :5, :6, :7)'
	cur.execute(statement, employee_infos)
	con.commit()
	close_connection(con, cur)
	update_list_employeesID('simple_update', 'shipping.txt', employee_infos[0])

# fonction se chargeant de l'insertion dans le fragment autres(MySQL database)
# employee_infos prend les valeurs employee_id, firt_name, last_name, email, phone_number, hire_date, salary
def insert_employee_others(employee_infos):
	employee_infos[5] = datetime.strptime(employee_infos[5] , '%d-%b-%Y')
	cnx, cursor = start_mysql_connection()
	statement = 'insert into employees_autres(employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id) ' + \
		'values (%s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(statement, employee_infos)
	cnx.commit();
	close_connection(cnx, cursor)
	update_list_employeesID('simple_update', 'others.txt', employee_infos[0])

def delete_employee(employee_id):
	ls1 = list_employeesID('shipping.txt')
	ls2 = list_employeesID('others.txt')
	employee_id = int(employee_id)
	if employee_id in ls1:
		con, cur = start_oracle_connection()
		statement = 'delete from employees_shipping where employee_id = {}'.format(employee_id)
		cur.execute(statement)
		con.commit()
		close_connection(con, cur)
		#on va supprimer l'id de l'employé dans ls1
		#we will drop employee_id in ls1
		update_list_employeesID('simple_update', 'shipping.txt', employee_id, remove=True)
		print("Employee dropped")
	elif employee_id in ls2:
		cnx, cursor = start_mysql_connection()
		statement = 'delete from employees_autres where employee_id = {}'.format(employee_id)
		cursor.execute(statement)
		cnx.commit()
		close_connection(cnx, cursor)
		#on va supprimer l'id de l'employé dans ls2
		#we will drop employee_id in ls2
		update_list_employeesID('simple_update', 'others.txt', employee_id, remove=True)
		print("Employee dropped")
	else:
		print('Employee with ID =', employee_id, ' does not exist')

def list_employeesID(file):
	with open (file, 'rb') as sh:
		unpickler = pickle.Unpickler(sh)
		list_id = unpickler.load()
		return list_id
def update_list_employeesID(update_type, file, id_value=0, remove=False):
	if update_type == 'advanced_update':
		with open(file, "rb+") as sh:
			if file == 'shipping.txt':
				con, cur = start_oracle_connection()
				statement = 'select employee_id from employees_shipping'
				cur.execute(statement)
				itemlist = cur.fetchall()
				close_connection(con, cur)
			if file == 'others.txt':
				cnx, cursor = start_mysql_connection()
				statement = 'select employee_id from employees_autres'
				cursor.execute(statement)
				itemlist = cursor.fetchall()
				close_connection(cnx, cursor)
			list_id = list()
			for i in itemlist:
				list_id.append(i[0])
			pickler = pickle.Pickler(sh)
			pickler.dump(list_id)
			
	if update_type == 'simple_update':
		if id_value != 0:
			list_id = list_employeesID(file)
			if remove == False:
				list_id.append(id_value)
			else:
				list_id.remove(id_value)
			with open(file, "rb+") as sh:
				pickler = pickle.Pickler(sh)
				pickler.dump(list_id)

def update_employee(employee_id, email=None, phone_number=None, salary=None):
	ls1 = list_employeesID('shipping.txt')
	ls2 = list_employeesID('others.txt')
	employee_id = int(employee_id)
	if employee_id in ls1:
		cn, cur = start_oracle_connection()
		if email != None and phone_number != None and salary != None:
			statement = "update employees_shipping set email = %s, phone_number = %s, salary = %s where employee_id = %s"
			infos = (email, phone_number, salary, employee_id)
		elif phone_number != None and (email == None and salary == None):
			statement = "update employees_shipping set phone_number = %s where employee_id = %s"
			infos = (phone_number, employee_id)
		elif email != None and (phone_number == None and salary == None):
			statement = "update employees_shipping set email = %s where employee_id = %s"
			infos = (email, employee_id)
		elif salary != None and (phone_number == None and email == None):
			statement = "update employees_shipping set salary = %s where employee_id = %s"
			infos = (salary, employee_id)
		cur.execute(statement, infos)
		cn.commit()
		close_connection(cn, cur)
		print("Employee updated")
	elif employee_id in ls2:
		cnx, cursor = start_mysql_connection()
		if email != None and phone_number != None and salary != None:
			statement = "update employees_autres set email = %s, phone_number = %s, salary = %s where employee_id = %s"
			infos = (email, phone_number, salary, employee_id)
		elif phone_number != None and (email == None and salary == None):
			statement = "update employees_autres set email = %s where employee_id = %s"
			infos = (phone_number, employee_id)
		elif email != None and (phone_number == None and salary == None):
			statement = "update employees_autres set email = %s where employee_id = %s"
			infos = (email, employee_id)
		elif salary != None and (phone_number == None and email == None):
			statement = "update employees_autres set email = %s where employee_id = %s"
			infos = (salary, employee_id)
		cursor.execute(statement, infos)
		cnx.commit()
		close_connection(cnx, cursor)
		print("Employee updated")
	else:
		print('Employee with ID =', employee_id, 'does not exist')

def select_employees(section, employee_id=0):
	if employee_id == 0:
		if section.upper() == 'SHIPPING':
			con, cur = start_oracle_connection()
			statement = "select * from employees_shipping"
			cur.execute(statement)
			result = cur.fetchall()
			close_connection(con, cur)
			return result
		if section.upper() == 'OTHERS':
			cnx, cursor = start_mysql_connection()
			statement = "select * from employees_autres"
			cursor.execute(statement)
			result = cursor.fetchall()
			close_connection(cnx, cursor)
			return result
	else:
		ls1 = list_employeesID('shipping.txt')
		ls2 = list_employeesID('others.txt')
		employee_id = int(employee_id)
		if employee_id in ls1:
			con, cur = start_oracle_connection()
			statement = "select * from employees_shipping where employee_id = {}".format(employee_id)
			cur.execute(statement)
			result = cur.fetchone()
			close_connection(con, cur)
			return result
		elif employee_id in ls2:
			cnx, cursor = start_mysql_connection()
			statement = "select * from employees_autres where employee_id = %s"#don't know why it does not accept .format()
			#maybe it's because of MySQL cursor
			cursor.execute(statement, (employee_id))
			result = cursor.fetchone()
			close_connection(cnx, cursor)
			return result
		else:
			print('nothing')
			return employee_id

if __name__ == "__main__":
	update_list_employeesID('advanced_update', 'shipping.txt')
	update_list_employeesID('advanced_update', 'others.txt')
