def shop(name,quantity,unit,grocery_list):
    grocery_list.append('{0}{1}{2}'.format(name,quantity,unit))
    return grocery_list
store1=[]
store2=[]
shop('banana',2,'units',store1)
shop('milk',1,'liters',store2)
print(store1)
print(store2)
