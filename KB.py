
from xlrd import *
from semanticNetworks import *

# Restaurant Data
restaurants = {}
genres      = {}
prices      = {}
locations   = {}
SVDs        = {}

# Member Data
people = {}

# Misc
facts = []

# Relations used
isA     = GetIsA()
isPrice = Relation('is price')
isAt    = Relation('is at location')
isSVD   = Relation('is of svd')
cheaperThan   = Relation('<', 1)
expensiveThan = Relation('>', 1, cheaperThan)
examplesOf      = Relation('is an example of', 1, isA)
examplesOfPrice = Relation('is an example of price', 1, isPrice)
examplesOfAt    = Relation('is an example of at', 1, isAt)
examplesOfSVD   = Relation('is an example of an SVD', 1, isSVD)

likes    = Relation('likes')
dislikes = Relation('dislikes')
ateRecently   = Relation('ate recently')
ateLongestAgo = Relation('ate longest ago')
examplesOfLikes    = Relation('is a liked restaurant', 1, likes)
examplesOfDislikes = Relation('is a disliked restaurant', 1, dislikes)
examplesOfRecent   = Relation('was recently eaten', 1, ateRecently)
examplesOfLongest  = Relation('was eaten long ago', 1, ateLongestAgo)

# Gather XLS sheets
restaurantWB = open_workbook('restaurantData.xls')
rData = restaurantWB.sheet_by_index(0)

membersWB = open_workbook('membersData.xls')
mData = membersWB.sheet_by_index(0)


# Row-loading functions
def load_restaurant_row(row):
    def col(i): return rData.cell(row, i).value
    [name, genre, price, location, svd] = [ col(i).lower() for i in range(5) ]
    # Load into dictionaries if not yet created
    if name  not in restaurants: restaurants[name] = Entity(name)
    if genre not in genres:      genres[genre]     = Entity(genre)
    if price not in prices:      prices[price]     = Entity(price)
    if svd   not in SVDs:        SVDs[svd]         = Entity(svd)
    if location not in locations: locations[location] = Entity(location)
    # Specify relations
    facts.append(Fact(restaurants[name], isA, genres[genre]))
    facts.append(Fact(restaurants[name], isPrice, prices[price]))
    facts.append(Fact(restaurants[name], isAt, locations[location]))
    facts.append(Fact(restaurants[name], isSVD, SVDs[svd]))


def load_person(row):
    def col(i):       return mData.cell(row, i).value
    
    def csv2lst(csv, sep=','):
        lst = list(map(lambda s: s.strip(), csv.split(sep)))
        if len(lst) == 1 and lst[0] == '': return []
        return lst
    
    def add_csv_relationship(relation, source, csv, sep=','):
        lst = csv2lst(csv, sep=sep)
        for l in lst:
            facts.append(Fact(people[name], relation, source[l]))
            
    [name, genre, svd, location, price, liked, disliked, recently, longest] \
        = [ col(i).lower() for i in range(9) ]
    if name not in people: people[name] = Entity(name)
    # Specify relations
    add_csv_relationship(likes, genres, genre)
    add_csv_relationship(likes, SVDs, svd)
    add_csv_relationship(likes, locations, location)
    add_csv_relationship(likes, prices, price)
    add_csv_relationship(likes, restaurants, liked)
    add_csv_relationship(dislikes, restaurants, disliked)
    add_csv_relationship(ateRecently, restaurants, recently)
    add_csv_relationship(ateLongestAgo, restaurants, longest)


# Load XLS data into KB
def load_restaurant_data():
    for row in range(rData.nrows):
        if row == 0:
            continue
        load_restaurant_row(row)


def load_members_data():
    for row in range(mData.nrows):
        if row == 0:
            continue
        load_person(row)

