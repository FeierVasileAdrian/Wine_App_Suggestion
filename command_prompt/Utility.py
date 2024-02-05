# IMPORTS
import numpy as np
import pandas as pd
import openai
import os
from langchain.chat_models import ChatOpenAI

################################################################################

def get_LLM():
  '''
  This function creates and returns the OPENAI LLM
  '''
  from dotenv import load_dotenv, find_dotenv
  _ = load_dotenv(find_dotenv())

  openai.api_key  = os.getenv('OPENAI_API_KEY')

  llm_model = "gpt-3.5-turbo"
  chat = ChatOpenAI(temperature=0.0, model=llm_model)

  return chat

def get_wine_folly_data():
  '''
  This function returns the data for pairing wine with food.
  '''
  taste_table = np.array([[2, 1, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 2, 1, 0, 0, 1, 2, 1],
                          [1, 2, 0, 1, 0, 0, 1, 0, 0],
                          [0, 1, 2, 1, 2, 1, 1, 0, 0],
                          [0, 0, 0, 0, 0, 1, 2, 0, 0],
                          [0, 0, 0, 0, 1, 2, 1, 0, 0],
                          [0, 0, 0, 1, 2, 1, 0, 1, 0],
                          [0, 1, 2, 1, 2, 1, 1, 1, 1],
                          [1, 2, 0, 1, 0, 1, 1, 1, 2],
                          [2, 1, 0, 1, 1, 0, 1, 0, 0],
                          [1, 2, 1, 1, 1, 1, 1, 1, 0],
                          [0, 0, 0, 0, 0, 2, 1, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 1, 0],
                          [1, 2, 0, 1, 0, 0, 0, 1, 0],
                          [1, 2, 2, 0, 2, 0, 0, 0, 0],
                          [0, 0, 1, 1, 1, 1, 1, 2, 0],
                          [0, 1, 0, 1, 0, 2, 1, 0, 0],
                          [2, 1, 0, 0, 0, 0, 0, 0, 0],
                          [1, 2, 0, 1, 0, 1, 1, 1, 0],
                          [0, 0, 0, 0, 0, 1, 1, 2, 0],
                          [0, 1, 1, 1, 1, 2, 0, 0, 0],
                          [0, 1, 0, 1, 0, 0, 0, 1, 2],
                          [0, 2, 1, 1, 0, 0, 1, 2, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 1, 1, 1, 0, 0, 2, 0],
                          [0, 0, 0, 1, 0, 0, 0, 2, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 0],
                          [0, 0, 0, 0, 0, 0, 1, 2, 1],
                          [0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 2]])
  taste_df = pd.DataFrame(data = taste_table,
                          columns = ['Bold Red', 'Medium Red', 'Light Red', 'Rosé', 'Rich White', 'Light White', 'Sparkling', 'Sweet White', 'Dessert'],
                          index = ['Red Meat', 'Cured Meat', 'Pork', 'Poultry', 'Mollusk', 'Fish', 'Lobster & Shellfish', 'Soft Cheese & Cream',
                                   'Pungent Cheese', 'Hard Cheese', 'Alliums', 'Green Vegetables', 'Root Vegetables & Squash', 'Nightshades', 'Funghi', 'Nuts & Seeds',
                                   'Beans & Peas','Black Pepper','Red Pepper','Hot & Spicy', 'Herbs', 'Baking Spices', 'Exotic & Aromatic Spices', 'White Starches',
                                   'Whole Wheat Grains', 'Sweet Starchy Vegetables', 'Potato', 'Fruit & Berries', 'Vanilla & Caramel', 'Chocolate & Coffee'])

  return(taste_table, taste_df)

def get_wine_folly_data_herbs_and_spices():
  '''
  This function returns the data for pairing wine with food in terms of
  herbs ans spices.
  '''
  taste_table = np.array([[0, 1, 0, 1, 1, 1, 0, 1, 0],
                          [0, 1, 1, 0, 0, 1, 1, 0, 0],
                          [0, 0, 1, 1, 1, 0, 1, 1, 1],
                          [0, 1, 1, 0, 1, 1, 1, 0, 0],
                          [1, 0, 0, 1, 0, 0, 1, 1, 0],
                          [0, 1, 0, 1, 0, 1, 0, 0, 0],
                          [0, 0, 1, 1, 0, 0, 1, 0, 1],
                          [1, 0, 0, 1, 1, 0, 1, 0, 1],
                          [1, 1, 0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 1, 0, 0, 1, 1, 1],
                          [0, 0, 0, 1, 0, 0, 0, 1, 1]])
  taste_df = pd.DataFrame(data = taste_table,
                          columns = ['Sparkling','Light White','Rich White','Sweet White','Rosé','Light Red','Medium Red','Bold Red','Dessert'],
                          index = ['cat_1','cat_2','cat_3','cat_4','cat_5','cat_6','cat_7','cat_8','cat_9','cat_10', 'cat_11'])
  categories_dict = {'cat_1':['basil', 'mint', 'cilantro','shiso','chervil'],
                     'cat_2':['oregano','thyme','dill','marjoram','tarragon','parsley'],
                     'cat_3':['sage','rosemary','fir','lavender','bay leaf'],
                     'cat_4':['garlic','shallot','chive','leek','onion'],
                     'cat_5':['coriander','cumin','caraway'],
                     'cat_6':['mustard','horseradish','szechuan','wasabi'],
                     'cat_7':['ginger','galangal','green cardamon','turmeric'],
                     'cat_8':['paprika','cayenne', 'ancho', 'aleppo'],
                     'cat_9':['red pepper','white pepper','pink pepper', 'black pepper'],
                     'cat_10':['cinnamon', 'allspice', 'mace', 'vanilla', 'clove', 'fenugreek', 'nutmeg'],
                     'cat_11':['anise','licorice','black cardamom','fennel','star anise']}

  return(taste_table, taste_df, categories_dict)

def get_wine_cat_from_main(meal_description, output_type_ing, output_dom_taste, chat):
  '''
  INPUTS:   * the description of a meal
            * a list of ingredients contained in the meal
            * a dictionary describing the tastes of the meal
            * a chat object

  OUTPUTS:  * a list of wine categories

  This function suggests a wine category that would pair well with the meal
  given as input based on the ingredients in that meal.
  The suggestion is done using a data table.
  '''

  # Get the data from the WineFolly website
  (taste_table, taste_df) = get_wine_folly_data()

  # dictionary containing dominant tastes
  taste_dict = output_dom_taste.get('dominant_taste')
  num_tastes = len(taste_dict)

  # dictionary containing the ingredients and their corresponding tastes
  ing_dict = output_type_ing.get('type_of_ingredient')


  # get the dominant tastes of the meal and all the ingredients associated to
  # that taste

  dominant_tastes = []
  assoc_ing = []
  for key, value in taste_dict.items():
    dominant_tastes.append(key)
    assoc_ing.append(value)

  # get the ingredient types of all the dominant ingredients
  wine_pair = np.ones((1,9))

  # for every dominant taste
  for taste_id in range(num_tastes):
    for ingr_id in range(len(assoc_ing[taste_id])):
      ing_name = assoc_ing[taste_id][ingr_id]
      ing_cat = ing_dict.get(ing_name)[0]
      wine_pair = np.vstack([wine_pair, taste_df.loc[ing_cat]])

  wine_binar = np.min(wine_pair, axis=0)
  index_selected = wine_binar.nonzero()
  wine_type_selection = np.array(taste_df.columns[index_selected])

  # add an exception if wine_type_selection is empty
  if len(wine_type_selection)==0:

    # remove ingr 1 by 1 until wine_binar is not zero array anymore
    while np.sum(wine_binar)==0:

      wine_pair = wine_pair[:-1,:]
      wine_binar = np.min(wine_pair, axis=0)

  index_selected = wine_binar.nonzero()
  wine_type_selection = np.array(taste_df.columns[index_selected])

  return(wine_type_selection)

def get_wine_cat_from_side(meal_description, output_type_ing, output_dom_taste, chat):
  '''
  INPUTS:   * the description of a meal
            * a list of side ingredients contained in the meal
            * a dictionary describing the tastes of the meal
            * a chat object

  OUTPUTS:  * a list of wine categories

  This function suggests a wine category that would pair well with the meal
  given as input based on the side ingredients in that meal.
  The suggestion is done using a data table.
  '''

  # Get the data from the WineFolly website
  (taste_table, taste_df) = get_wine_folly_data()

  # dictionary containing dominant tastes
  taste_dict = output_dom_taste.get('dominant_taste')
  num_tastes = len(taste_dict)

  # dictionary containing the ingredients and their corresponding tastes
  ing_dict = output_type_ing.get('type_of_side_ingredient')


  # get the dominant tastes of the meal and all the ingredients associated to
  # that taste

  dominant_tastes = []
  assoc_ing = []
  for key, value in taste_dict.items():
    dominant_tastes.append(key)
    assoc_ing.append(value)

  # get the ingredient types of all the dominant ingredients
  wine_pair = np.ones((1,9))

  # for every dominant taste
  for taste_id in range(num_tastes):
    for ingr_id in range(len(assoc_ing[taste_id])):
      ing_name = assoc_ing[taste_id][ingr_id]
      ing_cat = ing_dict.get(ing_name)[0]
      wine_pair = np.vstack([wine_pair, taste_df.loc[ing_cat]])

  wine_binar = np.min(wine_pair, axis=0)
  index_selected = wine_binar.nonzero()
  wine_type_selection = np.array(taste_df.columns[index_selected])

  # add an exception if wine_type_selection is empty
  if len(wine_type_selection)==0:

    # remove ingr 1 by 1 until wine_binar is not zero array anymore
    while np.sum(wine_binar)==0:

      wine_pair = wine_pair[:-1,:]
      wine_binar = np.min(wine_pair, axis=0)

  index_selected = wine_binar.nonzero()
  wine_type_selection = np.array(taste_df.columns[index_selected])

  return(wine_type_selection)

def pair_wine_with_sides(list_of_sides):
  '''
  INPUTS:   * the description of a meal
            * a list of side ingredients contained in the meal
            * a dictionary describing the tastes of the meal
            * a chat object

  OUTPUTS:  * a list of wine categories

  This function suggests a wine category that would pair well with the meal
  given as input based on the side ingredients in that meal.
  The suggestion is done using a data table.
  '''

  # get wine folly data with herbs
  (taste_table_herbs, taste_df_herbs, categories_dict_herbs) = get_wine_folly_data_herbs_and_spices()

  num_sides = len(list_of_sides)
  dict_sides_location = {}
  for ingr in list_of_sides:
    ingr_split = ingr.split()

    for single_ingr in ingr_split:

      for key_cat, value_cat in categories_dict_herbs.items():

        if single_ingr.lower() in value_cat:

          dict_sides_location[single_ingr] = key_cat

  wine_side_pair = np.ones((1,9))
  for key_select, value_select in dict_sides_location.items():
    wine_side_pair = np.vstack([wine_side_pair, taste_df_herbs.loc[value_select]])

  if(wine_side_pair.shape[0] > 1):
    wine_side_binar = np.min(wine_side_pair, axis=0)
    index_selected_side = wine_side_binar.nonzero()
    wine_type_selection_side = np.array(taste_df_herbs.columns[index_selected_side])
  else:
    wine_type_selection_side = []

  return(wine_type_selection_side)
