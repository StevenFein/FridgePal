#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import ndb

class RecipeCache(ndb.Model):
    spoonacular_id = ndb.StringProperty(required=True)
    link = ndb.StringProperty(required=True)
    

class Food(ndb.Model):
    food_name = ndb.StringProperty(required=True)
    expiration_date = ndb.DateProperty(required=True)
    user_id = ndb.StringProperty(required=True)

#not totally sure
class Recipe(ndb.Model):
    recipe_title = ndb.StringProperty(required=True)
    recipe_ingredients = ndb.StringProperty(required=True)
