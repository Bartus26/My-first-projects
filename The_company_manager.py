
import pickle

class Employee:
    def __init__(self,name=None, position=None, salary=None, id=None):
        self.name = name
        self.position = position
        self.salary = salary
        self.id = id    

    def input_data(self):
        self.id = input("Insert employee ID: ")
        self.name = input("Insert employee name: ")
        self.position = input("Insert employee position: ")
        self.salary = input("Insert employee salary: ")

    def output_for_check(self):
        print(f"Employee {self.name}, ID {self.id} is on position {self.position} with salary {self.salary}")

    def writing_on_file(self):
        return f"[{self.name}, {self.position}, {self.salary}]"
    
    
           
class Manager(Employee):
    def __init__(self, name=None, position=None, salary=None,id=None, managed_staff=None):
        super().__init__(name, position, salary, id)
        self.managed_staff = managed_staff

    def output_for_check(self):
        print(f"Manager {self.name}, ID {self.id} is manager of {self.position} with salary {self.salary}, manaded {self.managed_staff} employee/s")

    def input_data(self):
        super().input_data()
        self.managed_staff = input("Insert how many employees he managed?: ")
   
    def writing_on_file(self):
        return f"[{self.name}, {self.position}, {self.salary},{self.managed_staff}]"


class FileManager:
    def __init__(self,adress):
        self.adress = adress

    def try_open_data(self):
        try:
            with open(self.adress, "r"):
                pass
        except FileNotFoundError:
            with open(self.adress, "w"):
                pass

    def add_data(self, id, obj):
        self.id=id
        self.obj = obj
        with open(self.adress, "ab") as data:
            pickle.dump({self.id : self.obj}, data)        
            print("Saved")

    def clear_data(self,confirm):
        self.confirm = confirm
        if self.confirm.upper() == "Y":
            with open(self.adress, "w"):
                pass
            print("Cleared")
        elif self.confirm.upper() == "N":
            print("OK")
        else:
            print("Wrong input")

    def read_data(self):
        counter = 0
        with open(self.adress, "rb") as data:
            try:
            
                while True:
                    print("== ID : [NAME, POSITION, SALARRY, MANAGED EMPLOYEE] ==") if counter == 0 else None
                    print(pickle.load(data))
                    counter+=1
            except EOFError:
                if counter == 0:
                    print("No data for read")
                else:
                    print("="*20)

    

#MAIN

# basic data:



file = FileManager("Vzdelavanie\Exercises with gemini\employees_data.pkl") #create object with file path
employee = Employee() #create employee object
manager = Manager() # create manager object

#Greeting
print("="*30)
print("Hello. Welcome in your company Managment System\n") #Greeting 

#body of software:
while True: 
    
    #Basic menu:
    user_input = input("Insert (L)ist all, (A)dd employee, (C)lear stored file or (E)xit: ")
    
    if user_input.upper() == "E": #Immediately stop program
        break 

    elif user_input.upper() == "A": #Go to "add" loop      
        while True: #Loop for add data to file
            is_manager = input("Employee is manager? (Y/N): ")

            if is_manager.upper() == "N": 
                employee.input_data()
                employee.output_for_check()
                while True:
                    
                    user_aproval = input("Confirm employee data (Y/N): ")
                    if user_aproval.upper() == "Y":
                        file.try_open_data()
                        file.add_data(employee.id, employee.writing_on_file())
                        break
                    
                    elif user_aproval.upper() == "N":
                        print("Memory erased. Input a data again")
                        break
                    
                    else:
                        print("Invalid input!")
                break                  
                             
            elif is_manager.upper() == "Y":
                manager.input_data()
                manager.output_for_check()
                while True:                    
                    user_aproval = input("Confirm employee data (Y/N): ")
                    if user_aproval.upper() == "Y":
                        file.try_open_data()
                        file.add_data(manager.id, manager.writing_on_file())
                        break
                    
                    elif user_aproval.upper() == "N":
                        print("Memory erased. Input a data again")
                        break
                    
                    else:
                        print("Invalid input!")
                break                  

            else:
                print("Wrong input. Enter (Y/N)")    
    elif user_input.upper() == "C":  # Clear stored file
        confirm_for_erase = input("Realy you can erase all data? (Y/N): ")
        file.try_open_data()
        file.clear_data(confirm_for_erase)
    elif user_input.upper() == "L": # List file
        file.try_open_data()
        file.read_data()
    else:
        print("Invalid input!")
            



