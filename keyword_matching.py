import numpy as np
import pandas as pd
import re
import Levenshtein

def key_word_matching(rules, string):
    (area_patterns,
    food_patterns,
    price_patterns) = rules
    area=""
    food=""
    price=""

    if area == "":
        area = area_matching(area_patterns,string)
    if food == "":
        food = food_matching(food_patterns,string)
    if price == "":
        price = price_matching(price_patterns,string)

    print(area,food,price)             
    return(area,food,price)

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

def area_matching(patterns, string):
    matcher = re.compile('|'.join(patterns))
    area=""
    try:
        area = matcher.search(string).group()
        print(area)
    except:
        print("no area found")
    if area in patterns:
        return area
    else:
        return levenshtein(area, patterns)
    
def food_matching(patterns, string):
    matcher = re.compile('|'.join(patterns))
    food=""
    try:
        food = matcher.search(string).group()
        print(food)
    except:
        print("no food type found")
    if food in patterns:
        return food
    else:
        return levenshtein(food, patterns)

def price_matching(patterns, string):
    matcher = re.compile('|'.join(patterns))
    try:
        price = matcher.search(string).group()
        print(price)
    except:
        print("no pricerange found")
    if price in patterns:
        return price
    else:
        return levenshtein(price, patterns)

def levenshtein(item, table):
    distances = [(x , Levenshtein.distance(item, x)) for x in table]
    distances.sort(key= lambda x : x[1])
    if distances[0][1] > 3:
        return "no keyword matching"
    return distances[0][0]