#print el menu
def print_menu():
    print("---------menu---------")
    print("1 add stock")
    print("2 remove stock")
    print("3 show stock's contents")
    print("4 exit the program")
# print el content    
def print_stock():
    for id, (key , value) in enumerate(d.items() , 1):
         print(f"{id}. {key}:{value}")    
#enter the stock
def enter_stock():
                print("enter the stock name or its ID")
                stock=input() #string or int
                if stock.isdigit():
                    id_stock = int(stock)
                    if 1 <= id_stock <=len(d): 
                        name = list(d.keys())[id_stock-1]
                        print("exist")
                    else:
                        print("not exist") 
                        return None   
                else:
                    name = stock.lower()
                    if name in d:
                        print("exist")
                    else:
                        print("new stock")  
                return name  
#add stock
def add_stock(name):
                print("enter how much you want to add the stock : ")
                val1 = input()
                if val1.isdigit():
                    val1 = int(val1)
                else:
                    print("invalid") 
                    return   
                if name in d :
                    d[name] = d[name] + val1
                else:
                    d[name] = val1
#remove stock
def remove_stock(name):
                print("enter how much you want to remove from the stock :") 
                val2 = input()
                if val2.isdigit():
                    val2 = int(val2)
                else:
                    print("invaild") 
                    return
                if d[name] - val2 >= 0:
                    d[name] = d[name] - val2
                else:
                    print("invalid")                    

#-------------------------------------------------------------------------------------------    
d={}
try:
    file = open("stock.txt","r")
    for i in file: # i as lines 
        key , value = i.split(",")
        d[key] = int(value)
except FileNotFoundError:
    print("the file is not exist")
except ValueError:
    print("invalid file format")   
          
#print(d)    
#----------------------------------------------------------------------------------------------
while(True):
    print_menu()
    output = input("enter your choice : ")
    if (output == "1" or output == "2" or output == "3" or output == "4"): #34an string
        match output:
            case "1":#add stock
                print_stock()
                name = enter_stock()
                if name is not None:
                    add_stock(name)
                #print(d)    
            case "2": #remove stock
                print_stock()
                name = enter_stock()
                if name not in d:
                    print("invalid")
                    continue
                if name is not None:
                    remove_stock(name)

                #print(d)    
            case "3":
                print_stock()
            case "4":
                file = open("stock.txt","w")
                for key , value in d.items():
                    file.write(f"{key},{value} \n")
                file.close() 
                break       

    else:
        print("invaild choice")



