import re

import Levenshtein
import numpy as np
import pandas as pd
from src.preferences import Preferences

def key_word_matching(string):
    x = Preferences()
    (area_patterns,
    food_patterns,
    price_patterns) = get_patterns()
    (x.area, bool1) = matcher(area_patterns,string)
    (x.food_type, bool2) = matcher(food_patterns,string)
    (x.price, bool3) = matcher(price_patterns,string)
             
    return(x, bool1 & bool2 & bool3)

def get_patterns():
    table = pd.read_csv('restaurant_info.csv')

    area = table.area.unique()[:-1]
    extra_area = ['((?<=in\sthe\s)\w+)','(\w+(?= (part)?\s+of\s+(the)?(town|city)))']
    area_patterns = np.concatenate([area,extra_area])

    food = table.food.unique()
    extra_food = ['((?<=serves\s)\w+)','(\w+(?= restaurant))']
    food_patterns = np.concatenate([food,extra_food])

    price = table.pricerange.unique()
    extra_price = ['(\w+(?= price(d)?))','(\w+(?= cost(ing)?))']
    price_patterns = np.concatenate([price,extra_price])

    rules=(area_patterns,food_patterns,price_patterns)
    return rules

def matcher(patterns, string):
    matcher = re.compile('|'.join(patterns))
    item=""
    try:
        item = matcher.search(string).group()
    except:
        return (None,False)
    if item in patterns:
        return (item, False)
    else:
        return (levenshtein(item, patterns), True)
    

def levenshtein(item, table):
    distances = [(x , Levenshtein.distance(item, x)) for x in table]
    distances.sort(key= lambda x : x[1])
    if distances[0][1] > 3:
        return "random"
    return distances[0][0]
