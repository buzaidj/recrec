import json
from typing import List
from collections import Counter
from urllib.parse import urlparse
import pandas as pd
import re
import sys

# foods for which we want to include the descriptor after the comma in the ingredients
INCLUDE_EXTRA_INFO = 'spices', 'flour', 'vinegar', 'oil', 'sauce', 'rice', 'syrups', 'alcoholic beverage', 'fish'
JSON_NAME = 'mit_5_recipes_prices_time'
NUM_TITLE_WORDS = 1000
NUM_INGREDIENT_WORDS = 1000
BIGRAMS = False
WEBSITES_TO_KEEP = 'delish.com', 'cooking.nytimes.com', 'epicurious.com', 'foodnetwork.com', 'chowhound.com'


def ingr_name_parse(ingr: str):
    parts = list(map(lambda x: x.strip(), ingr.split(',')))
    if parts[0] in INCLUDE_EXTRA_INFO:
        # include second part
        return parts[0] + ((', ' + parts[1]) if 1 < len(parts) else '')
    else:
        return parts[0]


def get_ingredients_in_recipe(single_rec):
    """
    Get all the ingredients in one recipe
    """
    ingrs = []
    for d in single_rec['ingredients']:
        ingr = d['text']
        ingr_name = ingr_name_parse(ingr)
        ingrs.append(ingr_name)
    return ingrs


def get_all_ingredients(recipes: json):
    """
    Get all ingredients in recipes json
    """
    ingredients = []
    for recipe in recipes:
        for d in recipe['ingredients']:
            ingr = d['text']
            ingr_name = ingr_name_parse(ingr)
            ingredients.append(ingr_name)
    return ingredients


def get_n_top_things(ingredients: List[str], n: int):
    """
    Get n top ingredients
    """
    return Counter(ingredients).most_common(n)


def top_ingredients(recipes: json):
    """
    get top ingredients for use in bag of words
    """
    ingrs = get_all_ingredients(recipes)
    top_ingr = get_n_top_things(ingrs, NUM_INGREDIENT_WORDS)
    return list(map(lambda x: x[0], top_ingr)), list(map(lambda x: x[1], top_ingr))


def bigrams(text: str):
    words = text.strip().split(' ')
    if (len(words)):
        return [(t1, t2) for (t1, t2) in zip(words[:-1], words[1:])]
    else:
        return None


def unigrams(title: str):
    return title.strip().split(' ')


def get_all_titles(recipes: json):
    titles = []
    for recipe in recipes:
        title = recipe['title'].lower()
        title = re.sub(r'\W+ ', '', title)
        if BIGRAMS:
            titles.append(bigrams(title))
        else:
            titles.append(unigrams(title))
    return titles


def top_titles(recipes: json):
    titles = get_all_titles(recipes)
    flat_titles = [item for sublist in titles for item in sublist]
    top_titles = get_n_top_things(flat_titles, NUM_TITLE_WORDS)
    return list(map(lambda x: x[0], top_titles)), list(map(lambda x: x[1], top_titles))


def get_website(rec):
    website = urlparse(rec['url']).netloc
    if website[:4] == 'www.':
        website = website[4:]
    return website


def create_dataframe(all_recipes: json):
    rows = []

    recipes = []
    # drop all recipes with url not in WEBSITES_TO_KEEP
    for rec in all_recipes:
        website = get_website(rec)
        if website in WEBSITES_TO_KEEP:
            recipes.append(rec)

    titles, _ = top_titles(recipes)
    ingredients, _ = top_ingredients(recipes)

    for rec in recipes:
        d = {}

        ntr = rec['nutr_values_per100g']

        # all nutrition info is normalized per 100g
        d['calories'] = ntr['energy']
        d['fat'] = ntr['fat']
        d['protein'] = ntr['protein']
        d['salt'] = ntr['salt']
        d['satfat'] = ntr['saturates']
        d['sugar'] = ntr['sugars']

        # price and time (estiamted per recipe by us)
        d['price'] = rec['cost']
        d['time'] = rec['idle_time']
        d['numsteps'] = len(rec['instructions']) 

        website = get_website(rec)

        d['website'] = website

        # list of all titles in this recipe
        if BIGRAMS:
            curr_title = rec['title'].lower()
            curr_title = re.sub(r'\W+ ', ' ', curr_title)
            curr_title = bigrams(curr_title)
            for word in titles:
                if word in curr_title:
                    d['title::' + str(word[0] + '_' + word[1])] = 1
                else:
                    d['title::' + str(word[0] + '_' + word[1])] = 0
        else:
            curr_title = rec['title'].lower().strip().split(' ')
            for word in titles:
                d['title::' + str(word)] = 1 if word in curr_title else 0

        curr_ingrs = get_ingredients_in_recipe(rec)
        # print(curr_ingrs)
        for ingr in ingredients:
            d['ingr::' + str(ingr)] = 1 if ingr in curr_ingrs else 0

        # not used for learning
        d['_id'] = rec['id']
        d['_url'] = rec['url']
        d['_title'] = rec['title']
        d['_steps'] = '#'.join(
            list(map(lambda x: x['text'], rec['instructions']))
        )

        rows.append(d)

    return pd.DataFrame(rows)


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open('../../' + file_name + '.json') as recp:
        recipes = json.load(recp)
        df = create_dataframe(recipes)
        df.to_csv('data' + '.csv', index=False)
