Welcome to RecRec, a recipe recommender:

Here's a brief overview of different files and what they do.

graphing.py: creates graphs based on recorded preferences by a user of how given models do when compared to a random reccomender.
gui.py: presents the user a recipe
inf_scroll.py: the main startup script that handles the user entering their name and selecting a model
data.csv: the CSV that stores all reipe data used by our program from 4382 recipes.
knn.py: a model that uses a KNN classifier to recommend recipes
make_dataframe.py: creates a CSV from the JSON input file with all recipes in the MIT dataset (with time and cost data added)
pricing.ipynb: adds cost data to recipes and puts it back in the recipes JSON
cf.py: a model that uses Collaboritve Filtering to recommend to users recipes based on what similar users like
dtree.py: a model that uses a Decision Tree to recommend users recipes and uses the multi-armed bandit as seen in CS-4700 to intersperse getting new IID data of a users preferences with reccomending them recipes
rand_recommender.py: a model that just continually randomly selects recipes to present to a user
recommender.py: an abstract class that gives some methods that recommenders are expected to implement
time.py: adds time data to recipes by parsing their ingredients

The entire recipes JSON from the MIT dataset was too big to add to our GitHub repo and is not licensed for everyone to use, only licensed for academic use, so we refrained from including it in the repository.


Here's an overview of some directories:
graphs: stores some scatter plots that analyze perfrmance
recs: store previous recommendations from a recommender (i.e. KNN, Dtree, CF) to a user
users: store each users preferences over recipes selected IID from the data and presented to them