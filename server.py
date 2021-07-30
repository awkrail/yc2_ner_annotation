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
        self.render("ner_annotation.html", recipe_id=recipe_id, sentences=sentences, ingredients=ingredients)

class SaveAnnotationHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        with open("./simulator_annotation.json", "r") as f:
            data = json.load(f)

        params = self.request.uri
        _, recipe_id = params.split("?")
        recipe_id = recipe_id.split("=")[-1]
        sentences = data[recipe_id]
        results = json.loads(self.get_argument("results"))
        result_str = json.dumps(results)

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
