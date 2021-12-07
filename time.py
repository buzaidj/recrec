import json
import sys
import re
from typing import Dict
import sys

data = []


def add_time_data(data_file) -> None:
    """
    reads in data_file line by line and removes adjacent recipes, writing to new_file
    """

    recipes = None
    with open(data_file + '.json') as recp:
        recipes = json.load(recp)
        for i in recipes:
            idle_time = 0
            for j in i['instructions']:
                line = j['text'].split()
                idle_time_pre_upd = idle_time
                for k in range(len(line)):
                    word = re.sub(r'[^\w\s]', '', line[k]).lower()
                    if word == "hour" or word == "hours":
                        try:
                            idle_time += int(line[k-1]) * 60
                        except:
                            pass
                    elif word == "minutes" or word == "minute":
                        try:
                            idle_time += int(line[k-1].split('-')[0])
                        except:
                            pass

                # if no time for instruction given, assume 2 minutes
                if idle_time_pre_upd == idle_time:
                    idle_time += 2

            i['idle_time'] = idle_time
            data.append(i)

            # if recipes are equal, keep last data the same
    with open(data_file + '_time' + ".json", 'w') as f_new:
        f_new.write(json.dumps(data))


if __name__ == '__main__':
    filename = sys.argv[1]
    add_time_data(filename)
