import xlrd
import xlwt
import random

"""helper functions"""
def listify(worksheet,col_num):
    list = []
    for rows in range(1,worksheet.nrows):
        data = worksheet.cell(rows,col_num)
        list.append(str(data)[5:].strip('\'').lower())
    return list
def random_choice(list_,k):
    arr = []
    for i in range(k):
        choice = random.choice(list(set(list_)))
        arr.append(choice)
    return arr
#------------------------------------------#

workbook = xlrd.open_workbook('restaurantData.xls')
worksheet = workbook.sheet_by_name('Sheet1')

"""Listify restaurants, genre, price, location, sit vs drive"""
rest_list = listify(worksheet,0)
genre_list = listify(worksheet,1)
price_list = listify(worksheet,2)
location_list = listify(worksheet,3)
sitdown_vs_drivethru = listify(worksheet,4)
#------------------------------------------#

"""
    Creates a dictionary to put resturants in their own lists based on price.
"""
dictionary = {"$":[],"$$":[],"$$$":[]}
num_of_genres = len(set(genre_list))
num_of_rests  = len(set(rest_list))

for i in range(num_of_rests):
    name = rest_list[i]
    price = price_list[i]
    dictionary[price].append(name)

low_rest = dictionary['$']
mid_rest = dictionary['$$']
high_rest = dictionary['$$$']

#------------------------------------------#

"""
From here on out, this program creates an excel file and populates the fields
randomly based on a big excel file with data that rachel created..
"""
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sheet1')

row = sheet.row(0)
row.write(0,'Name')
row.write(1,'Genre Likes')
row.write(2,'sit vs driveThru')
row.write(3,'Location')
row.write(4,'Price')
row.write(5,'Place Liked')
row.write(6,'Place Not Liked')
row.write(7,'Ate Recently')
row.write(8,'Ate Longest Ago')

#Loop to populate fields
for i in range(1,101):
#--------------First Field (Member's numbers)----------------------------#
    row = sheet.row(i)
    row.write(0,'member'+str(i))
    list_ = random_choice(list(set(genre_list)),random.randint(1,num_of_genres))
    list_ = list(set(list_))
    fmt = ", ".join(f"{genre}" for genre in list_)
    row.write(1,fmt)
#--------------Second field (Sit vs driveThru)----------------------------#
    row.write(2,random.choice(sitdown_vs_drivethru))
#--------------Third field (Location pref)----------------------------#
    row.write(3,random.choice(location_list))
#--------------Fourth field (Prices pref)----------------------------#
    price = random.choice(price_list)
    row.write(4,price)
#--------------Fifth field (Liked List)----------------------------#
    if price == '$':
        rest_list = low_rest
    elif price == '$$':
        rest_list = mid_rest
    elif price == '$$$':
        rest_list = high_rest
    likedList = random_choice(list(set(rest_list)),random.randint(1,5))
    likedList = list(set(likedList))
    fmt = ", ".join(f"{rest}" for rest in likedList)
    row.write(5,fmt)
#--------------Sixth field (NotLiked List)----------------------------#
    notLikedList = []
    for item in rest_list:
        if item in likedList:
            continue
        notLikedList.append(item)
    try:
        notLikedList = random_choice(list(set(notLikedList)),random.randint(1,5))
    except:
        pass
    print(notLikedList)
    fmt = ", ".join(f"{rest}" for rest in list(set(notLikedList)))
    row.write(6,fmt)
#---------------Seventh field (Ate Recently)---------------------------#
    list_ = random.choice(likedList)
    row.write(7,list_)
#---------------Eighth field (Ate longest ago)---------------------------#
    list_ = random.choice(likedList)
    row.write(8,list_)

#Saves the file...
workbook.save('memebrsData.xls')
