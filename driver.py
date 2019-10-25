from ToStr import tostr
from semanticNetworks import *
from KB import *

def getRelation(obj, relation):
    return obj.objects(relation)

def print_is(name):
    print(name, end=' ')
    print("is a ", end='')
    print(tostr(getRelation(name, isa)))

def print_price(name):
    print("Price of", end=' ')
    print(name, end=': ')
    print(tostr(name.objects(isprice)))

def print_location(name):
    print(name, end=' ')
    print("is at ", end='')
    print(tostr(name.objects(isat)))

def print_features(name):
    print(f"Printing Features for {name}:\n")
    print_is(name)
    print_price(name)
    print_location(name)


def print_places_at(location):
    print("Places at", end=' ')
    print(location, end=': ')
    print(tostr(location.objects(examplesat)))


print_features(mcdonalds)


# printing all restaurants that are "p" (cheap) that are "american"
print()
print(tostr(list(filter(lambda x: isprice(x, p),
                        getRelation(american, examplesof)))))

print()
print_features(grills_gon_wild)

