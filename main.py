import webapp2
import os
import urllib
import jinja2
import time
from models import Food, Recipe, RecipeCache
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json



#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Mainpage(webapp2.RequestHandler):
    def get(self):

        start_template = jinja_current_dir.get_template("templates/Mainpage.html")
        self.response.write(start_template.render())

class InputPage(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/InputPage.html")
        self.response.write(start_template.render())
    def post(self):
        expiration_string = self.request.get('expirationdate')
        expiration_date = datetime.datetime.strptime(expiration_string, "%Y-%m-%d").date()

        # calendar_url = "http://www.google.com/calendar/event?action=TEMPLATE&text=%s&dates=%s/%s"
        # calendar_link = calendar_url % ("TestEvent", 7, 12) #calendar_start, calendar_end)
        # calendar_html = "<HTML><BODY><A href='%s' target='_blank'>Test Event Link</A></BODY></HTML>"
        # self.response.write(calendar_html % calendar_link)
        user = users.get_current_user()
        food_input = self.request.get('addfooditem')
            #put into database (optional)
        food_record = Food(food_name = food_input, user_id = user.user_id(), expiration_date = expiration_date)
        food_record.put()
        self.redirect('/input')

class Inventory(webapp2.RequestHandler):
    def get(self):
        food_template = jinja_current_dir.get_template("templates/Inventory.html")
        user_foods = Food.query().order(Food.expiration_date).fetch()
        dict_for_template = {'all_user_foods': user_foods}
        self.response.write(food_template.render(dict_for_template))




class Recipes(webapp2.RequestHandler):
    def get(self):
        print(os.environ.get("FOOD_API_KEY"))
        start_template = jinja_current_dir.get_template("templates/Recipes.html")
        user_foods = Food.query().order(Food.expiration_date).fetch()
        user_food_names = ",".join([ food.food_name for food in user_foods ])
        query_params = {
            'ingredients': user_food_names,
            'apiKey': os.environ.get("FOOD_API_KEY"),
        }

        #not totally sure
        # recipe = Recipe.query().fetch()
        # self.response.write(start_template.render(recipe))
        url = 'https://api.spoonacular.com/recipes/findByIngredients?%s' % (urllib.urlencode(query_params))
        # self.response.write(url)
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                result_data = json.loads(result.content)
            else:
                result_data = []
                self.response.status_int = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
        self.response.write(start_template.render(
            {"recipes": result_data}
        ))


class DeleteHandler(webapp2.RequestHandler):
    def post(self):
        food_id = self.request.get('food_id')
        food_key = ndb.Key(urlsafe = food_id)
        food_key.delete()
        time.sleep(0.1)
        self.redirect('/inventory')

class RecipeRedirect(webapp2.RequestHandler):
    def get(self):
        recipe_id = self.request.get('id')
        recipe = RecipeCache.query().filter(RecipeCache.spoonacular_id==recipe_id).get()
        if not recipe:
            query_params = {
                'apiKey': os.environ.get("FOOD_API_KEY"),
            }
            url = 'https://api.spoonacular.com/recipes/%s/information?%s' % (recipe_id,urllib.urlencode(query_params))
            # self.response.write(url)
            try:
                result = urlfetch.fetch(url)
                if result.status_code == 200:
                    result_data = json.loads(result.content)
                else:
                    result_data = None
                    self.response.status_int = result.status_code
            except urlfetch.Error:
                logging.exception('Caught exception fetching url')

            if result_data:
                recipe = RecipeCache(spoonacular_id=recipe_id, link=result_data['sourceUrl'])
                recipe.put()
            else:
                self.response.status = "404 Recipe Not Found"
                return
        self.redirect(recipe.link.encode("utf-8"))



#
#   def post(self):
#         user = users.get_current_user()
#         food_input = self.request.get('user_food_input')
#
#         #put into database (optional)
#         food_record = Food(food_name = food_input)
#         food_record.user_id = user.user_id()
#         food_record.put()
#
#         #pass to the template via a dictionary
#         variable_dict = {'fav_food_for_view': the_fav_food}
#         end_template = jinja_current_dir.get_template("templates/results.html")
#         self.response.write(end_template.render(variable_dict))


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
    ('/', Mainpage),
    ('/input', InputPage),
    ('/inventory', Inventory),
    ('/recipes', Recipes),
    ('/delete', DeleteHandler),
    ('/recipe_redirect',RecipeRedirect),
], debug=True)
