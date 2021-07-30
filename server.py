import os
import json
import sqlite3

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        with open("./simulator_annotation.json", "r") as f:
            data = json.load(f)
        recipe_ids = list(data.keys())

        connect = sqlite3.connect("yc2_ner_annotation.sqlite3")
        cur = connect.cursor()
        res = cur.execute("select recipe_type from annotation")
        done_recipe_ids = [x[0] for x in res.fetchall()]

        recipe_id_with_done = []

        for recipe_id in recipe_ids:
            data = {"recipe_id" : recipe_id}
            if recipe_id in done_recipe_ids:
                data["done"] = True
            else:
                data["done"] = False
            recipe_id_with_done.append(data)

        self.render("index.html", recipe_ids=recipe_id_with_done)

class NERAnnotationHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        with open("./simulator_annotation.json", "r") as f:
            data = json.load(f)
        params = self.request.uri
        _, recipe_id = params.split("?")
        recipe_id = recipe_id.split("=")[-1]
        sentences = data[recipe_id]["sentences"]
        ingredients = data[recipe_id]["ingredients"]
        timestamps = [x[0] for x in data[recipe_id]["timestamps"]]
        self.render("ner_annotation.html", recipe_id=recipe_id, sentences=sentences, ingredients=ingredients, segment=timestamps)

class SaveAnnotationHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        with open("./simulator_annotation.json", "r") as f:
            data = json.load(f)

        params = self.request.uri
        _, recipe_id = params.split("?")
        recipe_id = recipe_id.split("=")[-1]
        sentences = data[recipe_id]["sentences"]

        # selected action
        action_results = json.loads(self.get_argument("results"))
        
        # selected ingredients
        selected_ingredients = self.get_arguments("checked_ingredient")
        ingredient_list = [[0 for _ in data[recipe_id]["ingredients"]] for _ in sentences]
        ingredient2idx = {y:x for x,y in enumerate(data[recipe_id]["ingredients"])}

        for ingredient in selected_ingredients:
            ingredient, step_num = ingredient.split("_")
            step_num = int(step_num)
            ingredient_list[step_num][ingredient2idx[ingredient]] = 1

        result_dict = {
                "annotation" : {
                    "action" : action_results,
                    "ingredients" : ingredient_list
                    },
                "ingredients" : ingredient2idx,
                "sentences" : data[recipe_id]["sentences"] }
        result_str = json.dumps(result_dict)
        connect = sqlite3.connect("yc2_ner_annotation.sqlite3")
        cur = connect.cursor()
        cur.execute("insert into annotation (recipe_type, annotation) values (?,?)", [recipe_id, result_str])
        connect.commit()
        self.render("save.html")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/ner_annotation.html?(.*)", NERAnnotationHandler),
        (r"/save.html?(.*)", SaveAnnotationHandler)
    ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static")
    )
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
