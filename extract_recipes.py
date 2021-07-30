import json
import random
random.seed(116)

def extract_recipes():
    with open("new_yc2_data/yc2_test_anet_format.json") as f:
        test_data = json.load(f)

    recipe_keys = list(test_data.keys())
    random.shuffle(recipe_keys)
    test_recipe_keys = recipe_keys[:100]

    recipe_dict = {}
    for recipe_id in test_recipe_keys:
        recipe_dict[recipe_id] = test_data[recipe_id]
    return recipe_dict

if __name__ == "__main__":
    recipe_dict = extract_recipes()
    with open("new_yc2_data/simulator_annotation.json", "w") as f:
        json.dump(recipe_dict, f)
