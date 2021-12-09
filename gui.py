from pandas import Series


def present(x: Series):
    """
    Presents a recipe
    """
    print('Here is a recipe. Let me know what you think? Type "yes/1" if you like it and "no/0" do not like.')
    print("Title: " + x['_title'])
    print("URL: " + x['_url'])
    x = input('My thoughts: ').lower().strip()
    if x == 'yes' or x == '1':
        return True
    else:
        return False
