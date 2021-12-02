import json
import sys
import re
from typing import Dict

data = []

"""
reads in data_file line by line and removes adjacent recipes, writing to new_file
"""
def time() -> None:
    json_name = "./mit_5_recipes"
    recipes = None
    with open(json_name + '.json') as recp:
        recipes = json.load(recp)
        for i in recipes:
            idle_time = 0
            for j in i['instructions']:
                line = j['text'].split()
                for k in range(len(line)):
                    word = re.sub(r'[^\w\s]','', line[k]).lower()
                    if word == "hour" or word == "hours":
                        try:
                            idle_time+=int(line[k-1]) * 60
                        except:
                            break;
                    elif word == "minutes" or word == "minute":
                        try:
                            idle_time+=int(line[k-1])
                        except:
                            break;
            
            i['idle_time'] = idle_time
            data.append(i)


            # if recipes are equal, keep last data the same
    with open("new_file.json", 'w') as f_new:
        f_new.write(json.dumps(data))

time()

