import json
import sys
from typing import Dict

data = []

"""
recipes_eq(last_data, curr_data) is true iff recipe's author and title are equal
"""
def recipes_eq(fst_recipe: Dict, snd_recipe: Dict) -> bool:
    return (fst_recipe and snd_recipe
            and fst_recipe['title'] == snd_recipe['title']
            and fst_recipe['author'] == snd_recipe['author']
            )

"""
reads in data_file line by line and removes adjacent recipes, writing to new_file
"""
def elim_dups(data_file: str, new_file: str) -> None:
    last_recipe = None
    with open(data_file) as f:
        for line in f:
            curr_recipe = json.loads(line)
            if not recipes_eq(last_recipe, curr_recipe):
                data.append(curr_recipe)
                last_recipe = curr_recipe
            # if recipes are equal, keep last data the same

    with open(new_file, 'w') as f_new:
        f_new.write(json.dumps(data))

    
# if calling process.py, just run with sys args for data file and new file
if __name__ == "__main__":
    data_file, new_file = sys.argv[1], sys.argv[2]
    elim_dups(data_file, new_file)
    
