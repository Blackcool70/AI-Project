
from KB import *

load_restaurant_data()
load_members_data()


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


def classify_restaurant(person, restaurant, first=0, last=None):
    f = features_from_restaurant(restaurant)
    f = std_features(f[0], f[1], f[2], f[3])
    return bayesian_classifier(person, f[first:last])


class NotEnoughRestaurantsError(Exception):
    pass


def find_top_N_restaurants(person, N, first=0, last=None):
    if last == first:
        raise NotEnoughRestaurantsError()
    scores = []
    for restaurant in restaurants:
        score = classify_restaurant(person, restaurant, first=first, last=last)
        scores.append((restaurant, score))
    nonzero = list(filter(lambda x: x[1] != 0, scores))
    if len(nonzero) >= N:
        s = sorted(nonzero, key=lambda x: x[1]) # sorted
        r = list(map(lambda x: x[0], s))        # restaurants
        return r[-N:][::-1]
    print(">> LOWERING requirements <<")
    if last is None: last = 0
    return find_top_N_restaurants(person, N, last=last-1)


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
