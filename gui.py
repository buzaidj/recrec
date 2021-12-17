from numpy import False_
from pandas import Series
import PySimpleGUI as sg


def yes(i):
    return 'yes' if i != 0 else 'no'


def get_name():
    sg.theme('DarkAmber')
    layout = [ [sg.Text("What is your name? \n"), sg.Input(default_text = "name", key='-IN-')],
                [sg.Button("All good!")] ]
    window = sg.Window("Give your name", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "All good!":
            window.close()
            return values['-IN-']
        else:
            break
    window.close()
        

def model_types():
    sg.theme('DarkAmber')
    layout = [ [sg.Text('Which recommender model would you like to use? ')], 
                [sg.Button("Random"), sg.Button("K-NN"), sg.Button("DST"), sg.Button("CF")] ]

    # Create the window
    window = sg.Window("Recipe", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
       
        if event == sg.WIN_CLOSED:
            break
        elif event == "Random":
            window.close()
            return 'rand'
        elif event == "DST": 
            window.close()
            return 'dtree'
        elif event == "K-NN": 
            window.close()
            return 'knn'
        elif event == "CF": 
            window.close()
            return 'cf'
        else:
            break

    window.close()
    

def present(x: Series):
    """
    Presents a recipe
    """

    sg.theme('DarkAmber')

    layout = [  [sg.Text('RECIPE: ')], 
                [sg.Text('Lactose free: ' + str(yes(1 - int(x['lactose']))))], 
                [sg.Text('Vegetarian: ' + str(yes(x['vegetarian'])))],
                [sg.Text("Calories (per 100g):\t"+ ' ' + str(int(x['calories'])))],
                [sg.Text('Fat (per 100g):\t\t'+ ' ' + str(int(x['fat'])))],
                [sg.Text('Saturated fat (per 100g): \t'+ ' ' + str(int(x['satfat'])))],
                [sg.Text('Protein (per 100g):\t\t'+ ' ' + str(int(x['protein'])))],
                [sg.Text('Salt (per 100g):\t\t' + str(int(x['salt'])))], 
                [sg.Text('Sugar (per 100g):\t\t' + str(int(x['sugar'])))],
                [sg.Text('Price (USD):\t\t' + str(int(x['price'])))], 
                [sg.Text("Est time to cook (min):\t" + str(int(x['time'])))], 
                [sg.Text("Would you cook this recipe?")], 
                [sg.Button("Yes"), sg.Button("No")] ]  

    # Create the window
    window = sg.Window("Recipe", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
       
        if event == sg.WIN_CLOSED:
            raise StopIteration('User quit')
        elif event == "No":
            window.close()
            return False
        elif event == "Yes": 
            window.close()
            return True
        else:
            break

    window.close()


def recipe_steps(x: Series):

    sg.theme('DarkAmber')

    steps = x['_steps'].split('#')
    s = ''
    for i in range(len(steps)):
        s += str(i + 1) + ': ' + steps[i] + "\n"

    layout = [  [sg.Text("Title:\t" + x['_title'])],
                [sg.Text('Instructions: ')],
                [sg.Text(s)],
                [sg.Text("URL:\t" + x['_url'])] ]

     # Create the window
    window = sg.Window("Recipe Details", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
       
        if event == sg.WIN_CLOSED:
            break
    
    window.close()

    
