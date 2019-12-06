
from KB import *

load_restaurant_data()
load_members_data()


class Memoize:
    def __init__(self, func):
        self.func = func
        self.table = dict()
    
    def __call__(self, *args, **kwargs):
        key = dict((k, v) for k, v in enumerate(args))
        key.update(kwargs)
        fs = frozenset(key.items())  # For hashing
        if fs in self.table:
            return self.table[fs]
        val = self.func(*args, **kwargs)
        self.table[fs] = val
        return val
    
    def clearTable(self):
        self.table.clear()


class NotEnoughRestaurantsError(Exception):
    pass


class NotEnoughPeopleError(Exception):
    pass


def bayesian_classifier(person, features):
    likesset = set(person.objects(likes))
    n = len(features) - 1
    T = len(restaurants)
    L = len(likesset)
    tot = (T ** n) / (L ** n)
    for f in features:
        s = f()
        tot *= len(s & likesset) / len(s)
    return tot


def std_features(genre, price, location, svd):
    gf = lambda: set(genre.objects(examplesOf))
    pf = lambda: set(price.objects(examplesOfPrice))
    lf = lambda: set(location.objects(examplesOfAt))
    sf = lambda: set(svd.objects(examplesOfSVD))
    return [gf, pf, lf, sf]


def restaurant_genre(restaurant):
    return restaurant.objects(isA)[0]


def restaurant_price(restaurant):
    return restaurant.objects(isPrice)[0]


def restaurant_location(restaurant):
    return restaurant.objects(isAt)[0]


def restaurant_svd(restaurant):
    return restaurant.objects(isSVD)[0]


def features_from_restaurant(restaurant):
    return [
        restaurant_genre(restaurants[restaurant]),
        restaurant_price(restaurants[restaurant]),
        restaurant_location(restaurants[restaurant]),
        restaurant_svd(restaurants[restaurant])
    ]


def classify(person, genre, price, location, first=0, last=None):
    return bayesian_classifier(person,
                               std_features(genre, price, location)[first:last])


@Memoize
def classify_restaurant(person, restaurant, first=0, last=None):
    f = features_from_restaurant(restaurant)
    f = std_features(f[0], f[1], f[2], f[3])
    return bayesian_classifier(person, f[first:last])


def sort_by_nth_item(tuple_arr, n=0):
    return list(sorted(tuple_arr, key=lambda x: x[n]))


def find_top_N_restaurants(person, N, first=0, last=None):
    if last == first:
        raise NotEnoughRestaurantsError()
    scores = []
    for restaurant in restaurants:
        score = classify_restaurant(person, restaurant, first=first, last=last)
        scores.append((restaurant, score))
    nonzero = list(filter(lambda x: x[1] != 0, scores))
    if len(nonzero) >= N:
        s = sort_by_nth_item(nonzero, n=1) # nonzero[i][1] is score
        r = list(map(lambda x: x[0], s))   # restaurants
        return r[-N:][::-1]
    if last is None:
        last = 0
    return find_top_N_restaurants(person, N, last=last-1)


def user_likes_restaurant(user, restaurant: str, priority=1):
    [genre, price, location, svd] = features_from_restaurant(restaurant)
    for i in range(priority):
        new_restaurant = Entity(restaurant)
        facts.append(Fact(new_restaurant, isA,     genre))
        facts.append(Fact(new_restaurant, isPrice, price))
        facts.append(Fact(new_restaurant, isAt,    location))
        facts.append(Fact(new_restaurant, isSVD,   svd))
        facts.append(Fact(user, likes, new_restaurant))
    classify_restaurant.clearTable()


def find_group_top_N_restaurants(person_arr, N, increment=0):
    """
    Find Group Top N Restaurants
  
    Params:
     - person_arr: Array of person objects
     - N: integer > 0
    """
    # Internal docs:
    # increment is used when recursing to increase the number
    # of items from find_top_N_restaurants for each person
    
    # Too few people to handle reasonably
    if len(person_arr) == 0: raise NotEnoughPeopleError()
    
    # Find the intersect of the top N+increment items for each person
    intersect = None
    for i, person in enumerate(person_arr):
        s = set(find_top_N_restaurants(person, N + increment))
        if i == 0:
            intersect = s
        else:
            intersect &= s
    
    # Recurse, but take more items per person by increasing increment
    if len(intersect) < N:
        return find_group_top_N_restaurants(person_arr, N, increment=increment+1)
    
    # Construct (restaurant, score) tuples for use by sort_by_nth_item
    tuples = []
    for restaurant in intersect:
        S = 0 # sum
        for person in person_arr:
            S += classify_restaurant(person, restaurant)
        tuples.append((restaurant, S))
    s = sort_by_nth_item(tuples, 1)  # scores in tuples[i][1]
    r = list(map(lambda x: x[0], s)) # restaurants
    return r[-N:][::-1]


def easy_classify(person, genre, price, location):
    return classify(
        people[person],
        genres[genre],
        prices[price],
        locations[location]
    )


def print_classifications(person):
    for restaurant in restaurants:
        score = classify_restaurant(people[person], restaurant)
        print(f"Restaurant {restaurant}: P = {score}")


def print_top_N(person, N):
    top = find_top_N_restaurants(people[person], N)
    print(f"Top {N} restaurants for {person}: {top}")

