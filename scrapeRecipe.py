from bs4 import BeautifulSoup
import requests
import csv
from pandas import DataFrame

#scrapre recipes off of the Simply Recipes website
def SimplyRecipe(link, name):
   name_index = 0
   for i in link:
      response = requests.get(i)
      soup = BeautifulSoup(response.text, "html.parser")
      recipe_name = soup.find(name="h1", class_="heading__title")
      recipe_p = recipe_name.getText()

      #extract the description
      description = soup.find(name="p", class_="heading__subtitle")
      description_p = description.getText().split('.')
      description_p = '\n'.join(description_p)

      #extract the ingredients
      ingredient_list = []
      ingredients = soup.find_all(name="li", class_="structured-ingredients__list-item")
      for tag_i in ingredients:
         tag_i = tag_i.find("p")
         ingredient_list.append(tag_i.getText())
      ingredient_list = '\n'.join(ingredient_list)

      #extract the steps
      steps = soup.find_all(name="p", class_="comp mntl-sc-block mntl-sc-block-html")
      steps1 = []
      for tag in steps:
         steps1.append(tag.getText())
      steps1 = '\n'.join(steps1[1:16])

      #extract cooking times and details
      cook_time = soup.find_all(class_="comp meta-text")
      cook_time1 = []
      for tag in cook_time:
         cook_time1.append(tag.getText())
      cook_time1 = ''.join(cook_time1)

      #make into table
      def pandas_table():
         info = {'Recipe Name': [recipe_p],
               'Description': [description_p],
               'Grocery Item Quantity and Names': [ingredient_list],
               'Steps': [steps1],
               'Time Divisions': [cook_time1]}
         table = DataFrame(info)
         return table
      
      pandas_table().to_csv(name[name_index], index = False)
      name_index += 1

#first argument is a list of the website names
#second argument is a list of the names of the CSV files
SimplyRecipe(["https://www.simplyrecipes.com/recipes/caramelized_onion_dip/", "https://www.simplyrecipes.com/cajun-shrimp-alfredo-recipe-7482727", "https://www.simplyrecipes.com/chocolate-babka-recipe-5206527"], 
             ["Onion Dip.csv", "Shrimp Pasta.csv", "Chocolate Babka.csv"])
