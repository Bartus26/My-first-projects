

import sqlite3
from time import sleep

       
class DatabaseManager():
    def __init__(self, db_file="company_emp.db"):
        self.db_file = db_file
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        self.create_table()     # every call to class create table if isn't exists
        

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS employees_data (
                         id TEXT PRIMARY KEY,
                         name TEXT,
                         surname TEXT,
                         position TEXT,
                         salary REAL,
                         managed_staff INTEGER DEFAULT 0 )
                         ''')
        self.con.commit()
    def close_connect(self):
        self.con.close()
        sleep(0.5)
        print("Have a nice day!")
        sleep(0.5)
        print("Bye!")

    def add_employee(self):
        id = input("Insert employee ID: ")# string
        name = input("Insert employee first name: ") # string
        surname = input("Insert employee surname: ") # string
        position = input("Insert employee position: ") # string
        while True:
            try:
                salary = float(input(f"Insert  {name}  salary: "))
                break
            except Exception as e_1:
                print(e_1)
                print("Salary must be number")
                print()
                sleep(0.5)
        while True:
            try:
                managed_staff = int(input(f"How many employees {name} managing? \n(when {name} {surname} is not manager input 0): "))
                break
            except Exception as e_2:
                print(e_2)
                print("Employee quantity must be number")
                print()
                sleep(0.5)  
        while True:
            check = input(f"Check insert data:\n\tID: {id}\n\tname: {name}\n\tsurname: {surname}\n\tposition: {position}\n\tsalary: {salary}\n\t{f'Employee managing {managed_staff} ' if managed_staff!=0 else 'Employee is not a manager'}\n\tAre data correct? (y/n): ")
            if check.upper() == "Y":
                try:
                    self.cur.execute('''INSERT INTO employees_data 
                                 (id,name,surname,position,salary,managed_staff)
                                 VALUES (?,?,?,?,?,?)''', (id, name, surname, position,salary, managed_staff))
                    self.con.commit()
                    sleep(0.5)
                    print("Done")
                    print(f"Data saved to {self.db_file}")                    
                    print()
                    input("Press Enter to continue...")
                                        
                except Exception as e_3:
                    print("Error writing data to file:")
                    print(e_3)
                    print("Data not saved")
                    print()

                break
                    
               
            elif check.upper() == "N":
                print("Data not saved")
                print()
                sleep(0.5)
                break
            else:
                print()
                print("Wrong! Insert (y/n)")
                print()                

    def list_table(self):
        temp =self.cur.execute("SELECT * FROM employees_data")
        if temp.fetchone() == None:
            print("Table is empty. Insert employee first.")
            print()
            sleep(0.5)

        else:
            temp =self.cur.execute("SELECT * FROM employees_data")
            print("-id-,-name-,-surname-,-position-,-salary-,-managed_staff-")
            for i in temp:
                print(i)
                sleep(0.15)
            print("----------End----------")
            input("Press Enter to continue...")
            
    def update_data(self):
        id = input("Insert Employee ID to be updated: ")
        try:
            temp = self.cur.execute("SELECT * FROM employees_data WHERE id = ?",(id,))
            
            if temp.fetchone() == None:
                print(f"\nID '{id}' is not in storage data")
                input("Press Enter to continue...")
            else:
                temp = self.cur.execute("SELECT * FROM employees_data WHERE id = ?",(id,))
                print("Select a field to update: ")
                print(temp.fetchone())
                print(f"'I(d)', '(n)ame', '(s)urname', '(p)osition', 'sala(r)y' or '(m)anage status' ?")
                while True:
                    user_input = input("Your input: ")
                    if user_input in ["d","n","s","p","r","m"]:
                        if user_input == "d":
                            parameter = "id"
                        elif user_input == "n":
                            parameter = "name"
                        elif user_input == "s":
                            parameter = "surname"
                        elif user_input == "p":
                            parameter = "position"
                        elif user_input == "r":
                            parameter = "salary"
                        elif user_input == "m":
                            parameter = "managed_staff"
                        break
                    else:
                        print("Wrong input! (d/n/s/p/r/m)")
                while True:
                    new_value = input(f"Insert new value for {parameter}: ")
                    if parameter == "salary" :
                        try:
                            new_value = float(new_value)
                            break
                        except Exception as e:
                            print(f"Wrong input. Must be real number")
                            print(e)
                            print()
                    elif parameter == "managed_staff":
                        try:
                            new_value = int(new_value)
                            break
                        except Exception as e:
                            print(f"Wrong input. Must be integer")
                            print(e)
                            print()
                    else:
                        break

                self.cur.execute(f"""UPDATE employees_data 
                                 SET {parameter} = ? 
                                 WHERE id = ?""",(new_value,id,))
                self.con.commit()
                sleep(0.5)
                print("New value has been saved!")

        except Exception as e:
            print("Error writing data to file:")
            print(e)
            print()


    def erase_table(self):
        approval = input(f"Are you sure that you want to permanently delete all data? (y/n): ")
        while True:
            if approval.upper() == "N":
                break
            if approval.upper() == "Y":
                second_approval = input(f"Are you realy sure that you want to permanently delete all data? (y/n): ")
                if second_approval.upper() == "N":
                    break
                elif second_approval.upper() == "Y":
                    self.cur.execute("DROP TABLE IF EXISTS employees_data")
                    sleep(1)
                    print("All data erased")
                    sleep(0.5)
                    print("The program will now shut down.")
                    return "erased"
                else:
                    print(f"Your input '{second_approval}' is wrong. (y/n)")
            else:
                print(f"Your input '{approval}' is wrong. (y/n)")
        
        
def greeting():
    print("="*50)
    print("Hello. Welcome in your company Management System")
          
def menu():
    print()
    print("""Chose what you can do:
            For list all insert (L)
            For add employee insert (A)
            For update data insert (U)
            For ERASE all data from file (ERASE)
            For exit insert (E)
                """)

#MAIN

file = DatabaseManager("Vzdelavanie\Exercises with gemini\company_emp.db") #create object with file path
loop_counter = 0


#body of software:
greeting()
while True: 
     
    menu()
    user_input = input("Your input: ")       
    user_input = user_input.upper()
    
    #Immediately stop program
    if user_input == "E": 
        file.close_connect()
        break 

    # List whole data
    elif user_input == "L":
        file.list_table()
    
    # Add new employee
    elif user_input == "A":
        file.add_employee()

    # Erase table
    elif user_input == "ERASE":
        erased = file.erase_table()         
        if erased == "erased":
            file.close_connect()
            break
    # Update table row - is can update 1 column in 1 step
    elif user_input == "U":
        file.update_data()
    else:

    #output for wrong user input
        print(f"Your input '{user_input}' is wrong")

        # when user 3 times inserts wrong input, the menu will be displayed again.
        if loop_counter == 3:
            menu()
            loop_counter = 0 
        loop_counter += 1

#END



    

            



