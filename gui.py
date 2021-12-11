from pandas import Series


def present(x):
    """
    see if we can learn a linear rule
    """


def present2(x: Series):
    """
    Presents a recipe
    """
    print()
    print('RECIPE: ')

    print("Title:\t" + x['_title'])

    print()

    print("Calories (per 100g):\t\t\t", ' ' + str(int(x['calories'])))
    print('Fat (per 100g):\t\t\t\t', ' ' + str(int(x['fat'])))
    print('Saturated fat (per 100g): \t\t', ' ' + str(int(x['satfat'])))
    print('Protein (per 100g):\t\t\t', ' ' + str(int(x['protein'])))
    print('Salt (per 100g):\t\t\t', '',  str(int(x['salt'])))
    print('Sugar (per 100g):\t\t\t', '', str(int(x['sugar'])))
    print()
    print('Price (USD):\t\t', int(x['price']))
    print('Est time to cook:\t', int(x['time']))
    print()

    steps = x['_steps'].split('#')

    print('Instructions: ')
    for i in range(len(steps)):
        print(str(i + 1) + ': ' + steps[i])
    print()
    print("URL:\t", x['_url'])
    print()

    x = input('My thoughts: ').lower().strip()
    print()
    if x == 'q' or x == 'quit':
        raise StopIteration('User quit')
    if x == 'yes' or x == '1' or x == 'y':
        return True
    return False
