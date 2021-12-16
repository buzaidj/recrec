from pandas import Series


def yes(i):
    return 'yes' if i != 0 else 'no'


def present(x: Series):
    """
    Presents a recipe
    """
    print()
    print('RECIPE: ')

    print()

    print('Lactose free: ' + str(yes(1 - int(x['lactose']))))
    print('Vegetarian: ' + str(yes(x['vegetarian'])))

    print()

    print("Calories (per 100g):\t\t\t", ' ' + str(int(x['calories'])))
    print('Fat (per 100g):\t\t\t\t', ' ' + str(int(x['fat'])))
    print('Saturated fat (per 100g): \t\t', ' ' + str(int(x['satfat'])))
    print('Protein (per 100g):\t\t\t', ' ' + str(int(x['protein'])))
    print('Salt (per 100g):\t\t\t', '',  str(int(x['salt'])))
    print('Sugar (per 100g):\t\t\t', '', str(int(x['sugar'])))
    print()
    print('Price (USD):\t\t', int(x['price']))
    print('Est time to cook (min):\t', int(x['time']))
    print()

    x = input('Would you cook this? (y/n/q): ').lower().strip()
    print()
    if x == 'q' or x == 'quit':
        raise StopIteration('User quit')
    if x == 'yes' or x == '1' or x == 'y':
        return True
    return False


def recipe_steps(x: Series):

    print("Title:\t" + x['_title'])

    steps = x['_steps'].split('#')

    print('Instructions: ')
    for i in range(len(steps)):
        print(str(i + 1) + ': ' + steps[i])
    print()
    print("URL:\t", x['_url'])
    print()
