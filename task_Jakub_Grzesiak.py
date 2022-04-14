'''
Author: Jakub Grzesiak
Date: 14.04.2022r.
'''

'''
READ ME:

    - xlwr - necessary package to save files ("pip install xlwr")
    - xls - format of used excel files
    - "Data_base" - input file (to load data from) - example data file
    - "Out" - output file (to save data)
       necessary libraries: numpy, pandas, datetime, re

Instruction:
    
    1. Open python file in the customized porgram (Visual Studio Code recommended)
    2. Make sure the folder with project is the parent folder 
       (Otherwise, there may be problems with laoding and saving data)
    3. Run python file in terminal
    4. Follow the prompts (Navigating the program consists of entering [proposed] words)
'''

# Imports
import pandas as pd
import numpy as np
import datetime
import re


# class for creating customers
class Customer:

    id = 1
    def __init__(self, name, VAT_id, creation_date, addres):
        self.name = name
        self.VAT_id = VAT_id
        self.creation_date = creation_date 
        self.addres = addres
        self.id = Customer.id
        Customer.id += 1


# class for creating data_base
class Data_base:

    def __init__(self):
        self.customers = list()
        self.customers_df = pd.DataFrame()

    # method for adding customers
    def add_customer(self):
        name = input("Customer name: ")
        VAT_id = input("VAT id: ")
        addres = input("Customer addres: ")
        creation_date = datetime.date.today()
        self.customers.append(Customer(name=name, VAT_id=VAT_id, \
            creation_date=creation_date, addres=addres))

    # method for printing customer
    def list_customers(self):
        ids = list()
        names = list()
        VAT_ids = list()
        creation_dates = list()
        addreses = list()
        for customer in self.customers:
            ids.append(customer.id)
            names.append(customer.name)
            VAT_ids.append(customer.VAT_id)
            creation_dates.append(customer.creation_date)
            addreses.append(customer.addres)      
        self.customers_df = pd.DataFrame({"name": names, "VAT id": VAT_ids, \
            "creation_date": creation_dates, "addres": addreses})
        self.customers_df.index = ids
        print(self.customers_df)
        
    # method for searching customers
    def find_customer(self):
        search = input("Search phrase: ")
        for customer in self.customers:
            if str(customer.id) == search or customer.name == search or customer.VAT_id == search \
                or customer.creation_date == search or customer.addres == search:              
                print("--------------------")
                print("Customer found:\n")
                print(f"Customer id: {customer.id}")
                print(f"Customer name: {customer.name}")
                print(f"VAT id: {customer.VAT_id}")
                print(f"Customer addres: {customer.addres}\n")
                find = input("Is this the client you are looking for? [y/n]: ")               
                if find == "y" or find == "yes":
                    self.decision(customer)
                    break
                elif customer == self.customers[-1]:
                    print("\nNot found")                   
            elif customer == self.customers[-1]:
                print("\nNot found")

    # method for making decision
    def decision(self, customer):
        decision = input("What do you want to do? [edit/delete/back]: ")
        if decision == "edit":
            self.edit_customer(customer)
        elif decision == "delete":
            self.delete_customer(customer)
        else:
            pass

    # method for editing customer
    def edit_customer(self, customer):       
        customer.name = input("Customer name: ")
        customer.VAT_id = input("VAT id: ")
        customer.addres = input("Customer addres: ")
        print("--------------------")

    # method for deleting customer     
    def delete_customer(self, customer):
        decision = input("Do you want to delete this customer? [y/n]: ")
        if decision == "y" or decision == "yes":           
            delete_id = [i for i in range(len(self.customers)) if self.customers[i] == customer]
            del self.customers[delete_id[0]]
            print("Customer deleted succesuflly")
            print("--------------------")
                
    # method to load data from a *.xls file
    def load_data(self):
        data = pd.read_excel(r'Data_base.xls')               
        for row in range(len(data)):
            creation_date = data["creation_date"][row]
            if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", str(creation_date)):  
                creation_date = datetime.date.today()
            self.customers.append(Customer(name=data["name"][row], VAT_id=data["VAT id"][row], \
                creation_date=creation_date, addres=data["addres"][row]))

    # method to save data to a *.xls file    
    def save_data(self):
        # the following problem does not affect the operation of the program
        with pd.ExcelWriter("out.xls") as writer:
            self.customers_df.to_excel(writer)


# interface class
class Interface:

    def __init__(self):

        self.main()

    def main(self):
    
        data = Data_base()
        print("==========================")
        print("= Welcome to the program =")
        print("==========================")
        while(True):          
            print("\n----------------------------------------")
            print("Available options:\n")
            print("- Customers list [list]")
            print("- Add customer [add]")
            print("- Search customer [search]")
            print("- Load file [load]")
            print("- Save file [save]")
            print("- Close program [close]\n")
            decision = input("Choose what you want to do: ")
            if decision == "close":
                print("=========================")
                print("======== Goodbye ========")
                print("=========================")
                break
            elif decision == "list":               
                while(True):
                    data.list_customers()
                    back_decion = input("Back to menu? [y/n]: ")
                    if back_decion == "yes" or back_decion == "y":
                        break
            elif decision == "add":               
                while(True):
                    data.add_customer()
                    back_decion = input("\nAdd another? [y/n]: ")
                    if back_decion == "no" or back_decion == "n":
                        break
            elif decision == "search":
                while(True):
                    data.find_customer()
                    back_decion = input("Search another? [y/n]: ")
                    if back_decion == "no" or back_decion == "n":
                        break
            elif decision == "load":
                data.load_data()
                print('Data from "Data_base.xls" load succesfully\n')
                data.list_customers()
            elif decision == "save":
                data.list_customers()
                back_decision = input("Save data? [y/n]: ")
                if back_decision == "yes" or back_decision == "y":
                    data.save_data()
                    print('Data saved to "out.xls" succesfully')
                else:
                    print("Failed to save")
            else:
                print("Action unavailable!\n")


# Start program
if __name__ == '__main__':
    Interface()