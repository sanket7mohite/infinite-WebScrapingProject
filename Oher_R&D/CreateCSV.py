import csv

mydict = [{'name': 'Kelvin Gates', 'age': '19', 'country': 'USA'},
          {'name': 'Blessing Iroko', 'age': '25', 'country': 'Nigeria'},
          {'name': 'Idong Essien', 'age': '42', 'country': 'Ghana'}]

fields = ['name', 'age', 'country']

with open('profiles3.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)

    writer.writeheader()
    writer.writerows(mydict)
