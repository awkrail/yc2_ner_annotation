import json

def extract_recipes(data):
    recipe_dict = {}
    for recipe_id, dt in data["database"].items():
        recipe_type = dt["recipe_type"]
        sentences = [ann["sentence"] for ann in dt["annotations"]]
        if not recipe_id in recipe_dict:
            recipe_dict[recipe_type] = sentences
    return recipe_dict

if __name__ == "__main__":
    with open("/mnt/LSTA5/data/common/recipe/youcook2/annotations/youcookii_annotations_trainval.json", "r") as f:
        data = json.load(f)
    recipe_dict = extract_recipes(data)
    with open("./data/text_recipes.json", "w") as f:
        json.dump(recipe_dict, f)