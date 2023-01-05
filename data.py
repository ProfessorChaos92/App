import pymongo
import csv

# Converts CSV list to insert values
def CsvToDict():
    global mydict
    mydict = []
    csv_filename = r'C:\Users\IqbalDev2\Documents\Groceries.csv'
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Price'] = float(row['Price']) # Converts Price to float
            row['Quantity'] = int(row['Quantity']) #Converst price to int
            mydict.append(row)
        print(mydict)

#Connects to Mongo Atlas
def ConnectToMongo():
    client = pymongo.MongoClient('mongodb+srv://dbuser:barium22@iqbalcluster.cic7y.mongodb.net/?retryWrites=true&w=majority')
    mydb =client["InventoryDB"]
    global mycol, UserCol
    mycol = mydb["CurrentInventory"]
    UserCol = mydb["Users"]

def InsertRecord(item,price,quantity,username):
    mydict = { "Item": item, "Price": price, "Quantity": quantity, "UserName" : username }
    x = mycol.insert_one(mydict)

def RegisterUser(username,password,email):
    ListOfUsers = []
    for x in UserCol.find():
        ListOfUsers.append(x['UserName'])
    if username in ListOfUsers:
        return 'UserName Taken'
    else:
        mydict = {"UserName" :username, "PassWord": password, "Email": email}
        x = UserCol.insert_one(mydict)
        return 'Success'

def QueryUser():
    list = []
    for i in UserCol.find():
        print(i)
        list.append(i)
    return list
    
def InsertManyRecords(): 
    mylist = mydict
    x = mycol.insert_many(mylist)

def QueryAll(username):
    myquery = {"UserName": username}
    list = []
    for i in mycol.find(myquery):
        print(i)
        list.append(i)
    return list

def QueryAllRecords():
    list = []
    for i in mycol.find():
        print(i)
        list.append(i)

def Query(item):
    myquery = { "Item": item}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x["Item"] + ' quanity has been updated to ' + str(x["Quantity"]) )

def UpdateQuantity(item,quantity):
    myquery = { "Item": item }
    newvalues = { "$set": { "Quantity": quantity } }
    mycol.update_one(myquery, newvalues)
    global updateditem
    updateditem = (mycol.find_one({ "Item": item })["Item"])
     
   

def Test1():
    x= input('What item quantity would you like to update: ')
    y= input('What quantity: ')
    y = int(y)
    UpdateQuantity(x,y)

def Drop():
    mycol.drop()
    UserCol.drop()


def Intro():
    print("""
    Welcome to the Inventory Management System

    What would like to do? Please enter what you would like to do:

    1. View Current Inventory
    2. Update Inventory
    3. Exit

    """)

    command = input('Please select and option : ')
    command = int(command)
    if (command) == 1:
        QueryAll()
    elif (command) == 2:
        Test1()
        print(' ')
        Query(updateditem)
    else:
        exit()

def LoginValidate(username,password):
    myquery = { "UserName": username , "PassWord": password }
    mydoc = UserCol.find_one(myquery)
    print(mydoc)
    if mydoc is None:
        return False 
    elif username == mydoc['UserName'] and password == mydoc['PassWord']:
        return True  
    else:
        return False

def LowInventory():
    myquery = { "Quantity": 0}
    mydoc = mycol.find(myquery)
    list = []
    for i in mydoc:
        print(i['Item'])
        list.append(i['Item'])
    return list

def ItemQuery():
    list = []
    mydoc = mycol.find()
    for x in mydoc:
        list.append(x['Item'])
    return list

class Sku: #Add Items
    def __init__(self, Item, Price, Quantity,Username):
        self.Item = Item
        self.Price = Price
        self.Quantity = Quantity
        self.Username = Username
    
    #Post
    def AddRecord(self):
        mydict = { "Item": self.Item, "Price": self.Price, "Quantity": self.Quantity, "UserName" : self.Username}
        mycol.insert_one(mydict)
        return '{} Added'.format(self.Item)
    
    #Put
    def UpdateRecord():
        pass
    #Get

    def GetRecord():
        pass

    #Del
    def DelRecord():
        pass


ConnectToMongo()
# print(ItemQuery())
# Reccord1 =Sku('ToothPase', 3.99, 1, "miqguel55")
# Reccord1.AddRecord()



# LowInventory()
# RegisterUser('Pablo98','Barium88','Pablo@yahoo.com')
# QueryUser()
# Intro()
# Query()
# Drop()
# CsvToDict()
# InsertManyRecords()
# QueryAll()
# QueryAllRecords()
# InsertRecord('chips',3.22,4,'miguel22')
# Query()
# QueryAll('miguel978')
# RegisterUser()

