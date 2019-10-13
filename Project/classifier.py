
def selectRestaurants():
    """
    Select the list of all restaurants.
    
    Equivalent to SELECT * FROM RESTAURANTS;
    
    Usage [there is only one way to use]:
    ```
    selectRestaurants()
    ```
    """
    pass

def selectLiked(base=restaurants()):
    """
    Select the list of all restaurants that have been liked.
    
    Params:
     - [Named] base: list of all restaurants
    
    Equivalent to SELECT * FROM $base WHERE LIKED = True;
    
    Usage:
    ```
    selectLiked()
    
    selectLiked(base=some_array)
    ```
    """
    pass

def selectGenre(genre, base=restaurants()):
    """
    Select the list of all restaurants with a given genre.
    
    Params:
     - genre: Genre to search for
     - [Named] base: list of all restaurants
    
    Equivalent to SELECT * FROM $base WHERE GENRE = $genre;
    
    Usage:
    ```
    selectGenre("Fast Food")
    
    selectGenre("Fast Food", base=some_array)
    ```
    """
    pass

def selectPriceLevel(priceLevel, base=restaurants()):
    """
    Select the list of all restaurants with a given price level.
    
    Params:
     - priceLevel: Price level to search for
     - [Named] base: list of all restaurants
    
    Equivalent to SELECT * FROM $base WHERE PRICE_LEVEL = $priceLevel;
    
    Usage:
    ```
    selectPriceLevel(0)
    
    selectPriceLevel(0, base=some_array)
    ```
    """
    pass

def selectLocation(location, base=restaurants()):
    """
    Select the list of all restaurants in a given location.
    
    Params:
     - location: Location to search in
     - [Named] base: list of all restaurants
    
    Equivalent to SELECT * FROM $base WHERE LOCATION = $location;
    
    Usage:
    ```
    selectLocation("Canyon")
    
    selectLocation("Canyon", base=some_array)
    ```
    """
    pass

def classifyFeatures(genre, priceLevel, location):
    """
    Find the probability that a user will like a restaurant with the
    given features.
    
    Params (alt: features):
     - genre:      Restaurant's genre
     - priceLevel: Restaurant's price level
     - location:   Restaurant's location
    
    Returns a probability (so a number between 0 and 1, inclusive).
    
    Usage:
    ```
    classifyFeatures("Tex Mex", 0, "Amarillo")
    ```
    """

    # Use a Naive-Bayes Classifier to determine
    #  P(Liked | Genre, Price Level, Location)
    rest = restaurants()
    
    L   = selectLiked()
    G   = selectGenre(genre)
    P   = selectPriceLevel(priceLevel)
    Loc = selectLocation(location)
    
    PGL = selectGenre(genre,           base=L)
    PPL = selectPriceLevel(priceLevel, base=L)
    PLL = selectLocation(location,     base=L)

    numerator   = len(rest) * len(PGL) * len(PPL) * len(PLL)
    denominator = len(L) * len(G) * len(P) * len(Loc)
    return numerator / denominator

