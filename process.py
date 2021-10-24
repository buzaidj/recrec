import json

data = []


def recipes_eq(last_data, curr_data):
    return (last_data and curr_data
            and last_data['title'] == curr_data['title']
            and last_data['author'] == curr_data['author']
            )


last_data = None
# smae author, same ingredients, same photo ==> same recipe
with open('allrecipes.json') as f:
    for line in f:
        curr_data = json.loads(line)
        if not recipes_eq(last_data, curr_data):
            data.append(curr_data)
            last_data = curr_data
        # if recipes are equal keep last data the same

print(len(data))

with open('processed_recipes.json', 'w') as f_new:
    f_new.write(json.dumps(data))
