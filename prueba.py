#import datetime
# """fruits = []

# fruits.append({'id': 0, 'nombre': "cherry"})
# fruits.append({'id': 1, 'nombre': "banana"})
# fruits.append({'id': 2, 'nombre': "apple"})

# #fruits.sort()

# for fruit in fruits:
#     print(fruit['id'])
#     print(fruit['nombre'])"""

def orden(dict):
    return dict['id']

fruits = []

fruits.sort()

fruits.append({'id': 1, 'nombre': "cherry"})
fruits.append({'id': 2, 'nombre': "banana"})
fruits.append({'id': 3, 'nombre': "apple"})

#fruits.sort()
print("---")
for fruit in fruits:
    print(fruit)

fruits.sort(key=orden)

print("---")
for fruit in fruits:
    print(fruit)

# fruits.append({'id': 1, 'nombre': "anana"})

# print("---")
# for fruit in fruits:
#     print(fruit)
# #datetime.datetime(1, 1, 1, 0, 0, 0, 0)
# objeto = {}

# date = datetime.datetime.now()
# date2 = datetime.datetime(2024, 6, 17, 17, 20, 0, 0)

# date3 = date - date2

# print(date3)
# millis = date3.total_seconds() * 1000
# print(millis)

#objeto['date'] = date

#print(objeto)
#print(objeto['date'])

