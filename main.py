import webapp2
import os
import jinja2
from models import Food
from datetime import datetime
from datetime import timedelta

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/MainPage.html")
        self.response.write(start_template.render())

class InputPage(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/InputPage.html")
        self.response.write(start_template.render())

class InventoryPage(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/Inventory.html")
        self.response.write(start_template.render())

class RecipePage(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/Recipes.html")
        self.response.write(start_template.render())

#
#     def post(self):
#         user = users.get_current_user()
#         the_fav_food = self.request.get('user-fav-food')
#
#         #put into database (optional)
#         food_record = Food(food_name = the_fav_food)
#         food_record.user_id = user.user_id()
#         food_record.put()
#
#         #pass to the template via a dictionary
#         variable_dict = {'fav_food_for_view': the_fav_food}
#         end_template = jinja_current_dir.get_template("templates/results.html")
#         self.response.write(end_template.render(variable_dict))
#
# class ShowFoodHandler(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         food_list_template = jinja_current_dir.get_template("templates/foodlist.html")
#         your_foods = Food.query().filter(Food.user_id == user.user_id()).order(-Food.food_name).fetch(3)
#         fav_foods = Food.query().order(-Food.food_name).fetch(3)
#         dict_for_template = {
#             'top_fav_foods': fav_foods,
#             'your_fav_foods': your_foods,
#         }
#         self.response.write(food_list_template.render(dict_for_template))
#
# app = webapp2.WSGIApplication([
#     ('/', FoodHandler),
#     ('/showfavs', ShowFoodHandler)
# ], debug=True)
# #
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/input', InputPage),
    ('/inventory', InventoryPage),
    ('/recipes', RecipePage)
], debug=True)
