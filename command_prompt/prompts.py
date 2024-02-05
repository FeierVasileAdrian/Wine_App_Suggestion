"""
LLM prompts and used functions
"""

# IMPORTS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from Utility import get_wine_folly_data, get_wine_cat_from_main,\
                    get_wine_cat_from_side, pair_wine_with_sides

################################################################################

def get_first_meal_info(meal_description, chat):
  '''
  INPUTS:   * description of the meal
            * chat object

  OUTPUTS:  * list of ingredients contained in the meal
            * list of aromatics contained in the meal
            * list of non-aromatics contained in the meal
            * word 'main' or 'side' defining wether the main tastes of the
              meal come from main ingredients or from side ingredients

  This function uses Langchain chaining prompts to get several infos regarding
  the tastes of the meal given as input.
  '''

  ##############################################################################
  prompt_1_1 = ChatPromptTemplate.from_template(
  """
  You are given a meal description.

  Do not output your reasoning.

  Does the meal description explicitely mentions the ingredients contained in the meal ?

  If the meal description does explicitely mentions the ingredients contained \
  in the meal, store the mentionned ingredients in a python list.

  If the meal description does not explicitely mentions the ingredients contained \
  in the meal, search for the recipe of the meal get the ingredients that are \
  cited in the recipe, store the ingredients in a python list.
  Compare several recipes to make sure you have all the needed ingredients for the meal.

  Use the following format:
     Meal: meal_description
     List_of_ingredients: python list containing the ingredients of the meal

  Here is the meal description: {meal_description}.
  """)

  # chain 1_1:
  chain_1_1 = LLMChain(llm=chat,
                       prompt=prompt_1_1,
                       output_key="List_of_Ingredients")

  ##############################################################################
  prompt_1_2 = ChatPromptTemplate.from_template(
  """
  You are given a meal descripiton.
  You are given a string containing the meal description and a list of all the \
  ingredients contained in the meal.

  You are asked to output a python list containing all the condiments and aromatics \
  of the meal.
  To do so, go through the list of ingredients given as input and perform the 3 \
  following steps:

      1- select every ingredient that is considered as an aromatic and store it in a list. \
         Aromatics refer to vegetables, herbs, spices, leaves that add flavor and aroma to a dish.

      2- select every ingredient that is considered as a condiment and store it in a list. \
         A condiment is a preparation that is added to food, typically after cooking, \
         to impart a specific flavor, to enhance the flavor, or to complement the dish. \
         Salt, pepper, sugar, are condiments.

      3- select all the ingredients from step 1, from step 2 and store \
         them in a list.

  If no ingredient selected, output a python empty list.

  Use the following output:
     Meal: meal_description
     List_Aromatics: list obtained at step 1
     List_Condiments: list obtained at step 2
     List_Side_Ingredients: list obtained at step 3

  Here is the meal description: {meal_description}.
  Here is the string with meal description and list of all ingredients contained in the meal: {List_of_Ingredients}.
  """)

  # chain 1_2:
  chain_1_2 = LLMChain(llm=chat,
                       prompt=prompt_1_2,
                       output_key="List_of_Sides")
  ##############################################################################
  prompt_1_2bis = ChatPromptTemplate.from_template(
  """
  You are given a meal descripiton.
  You are given a string containing the meal description and a list of all the \
  ingredients contained in the meal.
  You are given a string containing the meal description and 3 lists respectively \
  describing:
          1- the aromatics in the meal
          2- the condiments in the meal
          3- all the side ingredients in the meal

  You are asked to output a python list containing every ingredient that is a main \
  ingredient of the meal.

  To do so, go through the list of ingredients, go through the list of side ingredients, \
  create a python list containing the items that are contained in the list of \
  ingredients but not in the list of side ingredients.

  Use the following output:
     Meal: meal_description
     List_of_Main_Ingredients: python list created

  Here is the meal description: {meal_description}.
  Here is the string with meal description and list of all ingredients contained in the meal: {List_of_Ingredients}.
  Here is the string with meal description and the lists of side ingredients: {List_of_Sides}.
  """)

  # chain 1_2bis:
  chain_1_2bis = LLMChain(llm=chat,
                          prompt=prompt_1_2bis,
                          output_key="List_of_Main_Ingredients")

  ##############################################################################

  taste_origin_schema = ResponseSchema(name="taste_origin",
                                       description="""
  You are given a meal descripiton.
  You are given a string containing the meal description and a list of all the \
  ingredients contained in the meal.
  You are given a string containing the meal description and 3 lists respectively \
  describing:
          1- the aromatics in the meal
          2- the condiments in the meal
          3- all the side ingredients in the meal
  You are given a string containing the meal description and a list of the main \
  ingredients contained in the meal.

  You are asked to output a python dictionary.
  To do so, perform the 2 following steps:

          1. Determine the most dominating tastes and aroms of the meal based on the \
             main ingredients and on the side ingredients.\
             Output a python list containing the most dominating tastes of the meal.\
             This list may contain several elements but should contain at least one element.

          2. Determine if the dominating tastes of the meal are mostly due to the side ingredients \
             or mostly due to the main ingredients. If the dominating tastes of the meal are mostly due \
             to the side ingredients, output the word 'side'. If the dominating tastes of the meal are \
             mostly due to the main ingredients, output the word 'main'.

  Use the following format for taste_origin:
     Meal: meal_description
     Dominating_taste: python list from step 1
     Origin_of_Taste: word from step 2

  Here is the meal description: {meal_description}.
  Here is the string with meal description and list of all ingredients contained in the meal: {List_of_Ingredients}.
  Here is the string with meal description and the lists of side ingredients: {List_of_Sides}.
  Here is the string with meal description and list of the main ingredients contained in the meal: {List_of_Main_Ingredients}.
  """)

  response_schemas = [taste_origin_schema]

  output_parser_1_3 = StructuredOutputParser.from_response_schemas(response_schemas)

  format_instructions_1_3 = output_parser_1_3.get_format_instructions()

  review_template_1_3 = """
  You are given a meal descripiton.
  You are given a string containing the meal description and a list of all the \
  ingredients contained in the meal.
  You are given a string containing the meal description and 3 lists respectively \
  describing:
          1- the aromatics in the meal
          2- the condiments in the meal
          3- all the side ingredients in the meal
  You are given a string containing the meal description and a list of the main \
  ingredients contained in the meal.

  You are asked to extract the following information:

  taste_origin:     You are asked to output a python dictionary.
  To do so, perform the 2 following steps:

          1. Determine the most dominating tastes and aroms of the meal based on the \
             main ingredients and on the side ingredients.\
             Output a python list containing the most dominating tastes of the meal.\
             This list may contain several elements but should contain at least one element.

          2. Determine if the dominating tastes of the meal are mostly due to the side ingredients \
             or mostly due to the main ingredients. If the dominating tastes of the meal are mostly due \
             to the side ingredients, output the word 'side'. If the dominating tastes of the meal are \
             mostly due to the main ingredients, output the word 'main'.


  Use the following format for taste_origin:
     Meal: meal_description
     Dominating_taste: python list  from step 1
     Origin_of_Taste: word from step 2

  Here is the meal description: {meal_description}.
  Here is the string with meal description and list of all ingredients contained in the meal: {List_of_Ingredients}.
  Here is the string with meal description and the lists of side ingredients: {List_of_Sides}.
  Here is the string with meal description and list of the main ingredients contained in the meal: {List_of_Main_Ingredients}.

  {format_instructions_1_3}
  """

  prompt_1_3 = ChatPromptTemplate.from_template(template=review_template_1_3)


  # chain_1_3: input= ... and output= ...
  chain_1_3 = LLMChain(llm=chat,
                        prompt=prompt_1_3,
                        output_key="taste_origin_AI")
  ##############################################################################

  overall_chain = SequentialChain(
      chains=[chain_1_1, chain_1_2, chain_1_2bis, chain_1_3],
      input_variables=["meal_description", "format_instructions_1_3"],
      output_variables=["List_of_Ingredients", "List_of_Sides", "List_of_Main_Ingredients", "taste_origin_AI"],
      verbose=False)

  simple_df = overall_chain({'meal_description':meal_description, 'format_instructions_1_3':format_instructions_1_3})
  output_ing_list = simple_df['List_of_Ingredients']
  output_arom_list = simple_df['List_of_Sides']
  output_non_arom_list = simple_df['List_of_Main_Ingredients']
  output_origin = output_parser_1_3.parse(simple_df['taste_origin_AI'])

  return (output_ing_list, output_arom_list, output_non_arom_list, output_origin)

def get_meal_body_from_main(meal_description, list_of_ingredients, chat):
  '''
  INPUTS:   * description of the meal
            * list of ingredients contained in the meal
            * chat object

  OUTPUTS:  * Types_of_Ingredients: list defining the type of ever ingredient
                                    contained in the list of ingredients given
                                    as input
            * Ingredient_taste: list defining the taste of ever ingredient
                                contained in the list of ingredients given
                                as input
            * meal_taste: list describing all the tastes of the meal given as
                          input

  This function uses Langchain chaining prompts to get several infos regarding
  the main ingredients contained in the meal.
  '''

  # Get the data from the WineFolly website
  (taste_table, taste_df) = get_wine_folly_data()

  # prompt template 1:
  type_of_ingredient_schema = ResponseSchema(name = "type_of_ingredient",
                                             description =
  """You are given a list of ingredients.
  Here is a list describing all the types of ingredient:
                                                           - Red Meat
                                                           - Cured Meat
                                                           - Pork
                                                           - Poultry
                                                           - Mollusk
                                                           - Fish
                                                           - Lobster & Shellfish
                                                           - Soft Cheese & Cream
                                                           - Pungent Cheese
                                                           - Hard Cheese
                                                           - Alliums
                                                           - Green Vegetables
                                                           - Root Vegetables & Squash
                                                           - Nightshades
                                                           - Funghi
                                                           - Nuts & Seeds
                                                           - Beans & Peas
                                                           - White Starches
                                                           - Whole Wheat Grains
                                                           - Sweet Starchy Vegetables
                                                           - Potato
                                                           - Fruit & Berries
                                                           - Vanilla & Caramel
                                                           - Chocolate & Coffee

  Determine the type of every ingredient and the specified cooking.
  If there is no specified cooking, the value is 0.
  Output a python dictionary describing the ingredient types of every ingredient.

  The dictionary should contain every ingredient type:
                                  - key: name of ingredient
                                  - value: comma separated python list containing:
                                                  * 1 type of ingredient
                                                  * cooking

  Here is the description of the meal: {meal_description}.
  Here is the list of ingredients: {list_of_ingredients}.""")

  response_schemas_2A_1 = [type_of_ingredient_schema]

  output_parser_2A_1 = StructuredOutputParser.from_response_schemas(response_schemas_2A_1)

  format_instructions_2A_1 = output_parser_2A_1.get_format_instructions()

  review_template_2A_1 = """You are given a list of ingredients.
  Here is a list describing all the types of ingredient:
           - Red Meat
           - Cured Meat
           - Pork
           - Poultry
           - Mollusk
           - Fish
           - Lobster & Shellfish
           - Soft Cheese & Cream
           - Pungent Cheese
           - Hard Cheese
           - Alliums
           - Green Vegetables
           - Root Vegetables & Squash
           - Nightshades
           - Funghi
           - Nuts & Seeds
           - Beans & Peas
           - White Starches
           - Whole Wheat Grains
           - Sweet Starchy Vegetables
           - Potato
           - Fruit & Berries
           - Vanilla & Caramel
           - Chocolate & Coffee

  You are asked to extract the following information:

  type_of_ingredient: Determine the type of every ingredient and the specified cooking.
                      If there is no specified cooking, the value is 0.
                      Output a python dictionary describing the ingredient types of \
                      every ingredient.

                      The dictionary should contain every ingredient type:
                                  - key: name of ingredient
                                  - value: comma separated python list containing:
                                               * 1 type of ingredient
                                               * cooking

  Here is the description of the meal: {meal_description}.
  Here is the list of ingredients: {list_of_ingredients}.
  {format_instructions_2A_1} """

  prompt_2A_1 = ChatPromptTemplate.from_template(template=review_template_2A_1)


  # chain 2A_1: input= ... and output= ...
  chain_2A_1 = LLMChain(llm=chat,
                        prompt=prompt_2A_1,
                        output_key="Types_of_Ingredients")
  ##############################################################################
  prompt_2A_2 = ChatPromptTemplate.from_template("""
  You are given:
      * a meal description.
      * a list of the ingredients contained in the meal.
      * a python dictionary describing the ingredient types and the specified \
        cooking.

  You are asked to extract the tastes of every ingredient. There are 5 different \
  basic tastes: sweet, sour, bitter, salty, savoury.
  Only output a python dictionary. This dictionary should contain:
                              - key: name of ingredient
                              - value: comma separated python list containing:
                                                   * type of ingredient
                                                   * cooking
                                                   * taste of ingredient
  Here is the meal description: {meal_description}.
  Here is the list of the ingredients contained in the meal: {list_of_ingredients}.
  Here is the dictionary describing the ingredient types and the specified \
  cooking: {Types_of_Ingredients}.
  """)

  # chain 2A_2: input= ... and output= ...
  chain_2A_2 = LLMChain(llm=chat,
                         prompt=prompt_2A_2,
                         output_key="Ingredient_taste")
  ##############################################################################
  # prompt template 2A_3:
  dominant_taste_schema = ResponseSchema(name="dominant_taste",
                                         description=
  """You are given:
               * a meal description.
               * a list of the ingredients contained in the meal.
               * a python dictionary describing the ingredient types and the specified \
                 cooking.
               * a python dictionary describing the ingredient types, the specified \
                 cooking and the taste of the ingredients.

  Based on the description of the meal, the list of ingredients, the dictionary describing \
  the types of ingredients, the dictionary describing the tastes of ingredient, identify \
  all the tastes of the meal. There are 5 different basic tastes: sweet, sour, bitter, \
  salty, savoury. Keep only the most dominant tastes. The most dominant tastes are the \
  tastes that give its main flavour to the meal.

  Output a python dictionary describing the more dominant tastes.
  If the dominant tastes can not be determined, output 0.

  The dictionary should contain every dominant taste:
           * key: dominant taste
           * value: comma separated python list containing only the name of ingredients
                    that contribute to the taste going from the more contributing
                    ingredient to the less contributing ingredient.

  Here is the meal description: {meal_description}
  Here is the list of ingredients: {list_of_ingredients}
  Here is the dictionary containing the type of ingredients: {Types_of_Ingredients}
  Here is the dictionary containing the taste of ingredients: {Ingredient_taste}""")

  response_schemas_2A_3 = [dominant_taste_schema]

  output_parser_2A_3 = StructuredOutputParser.from_response_schemas(response_schemas_2A_3)

  format_instructions_2A_3 = output_parser_2A_3.get_format_instructions()
  review_template_2A_3 = """You are given:
               * a meal description.
               * a list of the ingredients contained in the meal.
               * a python dictionary describing the ingredient types and the specified \
                 cooking.
               * a python dictionary describing the ingredient types, the specified \
                 cooking and the taste of the ingredients.

  Based on the description of the meal, the list of ingredients, the dictionary describing \
  the types of ingredients, the dictionary describing the tastes of ingredient, you are \
  asked to extract the following information:

  dominant_taste:  identify all the tastes of the meal. There are 5 different basic tastes: \
  sweet, sour, bitter, salty, savoury. Keep only the most dominant tastes. The most dominant \
  tastes are the tastes that give its main flavour to the meal.

  Output a python dictionary describing the more dominant tastes.
  If the dominant tastes can not be determined, output 0.

  The dictionary should contain every dominant taste:
           * key: dominant taste
           * value: comma separated python list containing only the name of ingredients
                    that contribute to the taste going from the more contributing
                    ingredient to the less contributing ingredient.

  Here is the meal description: {meal_description}
  Here is the list of ingredients: {list_of_ingredients}
  Here is the dictionary containing the type of ingredients: {Types_of_Ingredients}
  Here is the dictionary containing the taste of ingredients: {Ingredient_taste}

  {format_instructions_2A_3}"""

  prompt_2A_3 = ChatPromptTemplate.from_template(template=review_template_2A_3)


  # chain 2A_3: input= ... and output= ...
  chain_2A_3 = LLMChain(llm=chat,
                            prompt=prompt_2A_3,
                            output_key="meal_taste")


  ##############################################################################
  # overall_chain: input= ... and output= ...

  overall_chain = SequentialChain(
      chains=[chain_2A_1, chain_2A_2, chain_2A_3],
      input_variables=["meal_description", "list_of_ingredients", "format_instructions_2A_1", "format_instructions_2A_3"],
      output_variables=["Types_of_Ingredients", "Ingredient_taste", "meal_taste"],
      verbose=False)

  simple_df = overall_chain({'meal_description':meal_description, 'list_of_ingredients':list_of_ingredients, 'format_instructions_2A_1':format_instructions_2A_1, 'format_instructions_2A_3':format_instructions_2A_3})
  output_dict_2A_1 = output_parser_2A_1.parse(simple_df['Types_of_Ingredients'])
  output_dict_2A_2 = simple_df['Ingredient_taste']
  output_dict_2A_3 = output_parser_2A_3.parse(simple_df['meal_taste'])

  return (output_dict_2A_1, output_dict_2A_2, output_dict_2A_3)

def get_meal_body_from_sides(meal_description, list_of_sides, chat):
  '''
  INPUTS:   * description of the meal
            * list of side ingredients contained in the meal
            * chat object

  OUTPUTS:  * Types_of_Ingredients: list defining the type of ever ingredient
                                    contained in the list of ingredients given
                                    as input
            * Ingredient_taste: list defining the taste of ever side ingredient
                                contained in the list of ingredients given
                                as input
            * meal_taste: list describing all the tastes of the meal given as
                          input

  This function uses Langchain chaining prompts to get several infos regarding
  the side ingredients contained in the meal.
  '''

  # Get the data from the WineFolly website
  (taste_table, taste_df) = get_wine_folly_data()

  # prompt template 1:
  type_of_ingredient_schema = ResponseSchema(name = "type_of_side_ingredient",
                                             description ="""
  You are given:    * a meal description
                    * a string that describes side ingredients contained in a meal. \
  The string contains:
                     * Meal: a meal description
                     * List_Aromatics: a list containing the aromatics in the meal
                     * List_Condiments: a list containing the condiments in the meal
                     * List_Side_Ingredients: a list containing all the side ingredients in the meal

  Here is a list describing all the types of side ingredient:
                                                           - Red Meat
                                                           - Cured Meat
                                                           - Pork
                                                           - Poultry
                                                           - Mollusk
                                                           - Fish
                                                           - Lobster & Shellfish
                                                           - Soft Cheese & Cream
                                                           - Pungent Cheese
                                                           - Hard Cheese
                                                           - Alliums
                                                           - Green Vegetables
                                                           - Root Vegetables & Squash
                                                           - Nightshades
                                                           - Funghi
                                                           - Nuts & Seeds
                                                           - Beans & Peas
                                                           - White Starches
                                                           - Whole Wheat Grains
                                                           - Sweet Starchy Vegetables
                                                           - Potato
                                                           - Fruit & Berries
                                                           - Vanilla & Caramel
                                                           - Chocolate & Coffee

  Determine the type of every side ingredient based on the list describing all \
  the types of side ingredient.
  If there is no specified cooking, the value is 0.
  Output a python dictionary describing the ingredient types of every side ingredient.

  The dictionary should contain every ingredient type:
                                  - key: name of side ingredient
                                  - value: comma separated python list containing:
                                                  * 1 type of side ingredient. This type should be contained\
                                                    in the list describing all the types of side ingredient.
                                                  * cooking

  Here is the description of the meal: {meal_description}.
  Here is the string describing the side ingredients in the meal: {list_of_sides}.""")

  response_schemas_2A_1 = [type_of_ingredient_schema]

  output_parser_2A_1 = StructuredOutputParser.from_response_schemas(response_schemas_2A_1)

  format_instructions_2A_1 = output_parser_2A_1.get_format_instructions()

  review_template_2A_1 = """
  You are given:    * a meal description
                    * a string that describes side ingredients contained in a meal. \
  The string contains:
                     * Meal: a meal description
                     * List_Aromatics: a list containing the aromatics in the meal
                     * List_Condiments: a list containing the condiments in the meal
                     * List_Side_Ingredients: a list containing all the side ingredients in the meal

  Here is a list describing all the types of ingredient:
           - Red Meat
           - Cured Meat
           - Pork
           - Poultry
           - Mollusk
           - Fish
           - Lobster & Shellfish
           - Soft Cheese & Cream
           - Pungent Cheese
           - Hard Cheese
           - Alliums
           - Green Vegetables
           - Root Vegetables & Squash
           - Nightshades
           - Funghi
           - Nuts & Seeds
           - Beans & Peas
           - White Starches
           - Whole Wheat Grains
           - Sweet Starchy Vegetables
           - Potato
           - Fruit & Berries
           - Vanilla & Caramel
           - Chocolate & Coffee

  You are asked to extract the following information:

  type_of_side_ingredient:     Determine the type of every side ingredient based on the list describing all \
  the types of side ingredient.
  If there is no specified cooking, the value is 0.
  Output a python dictionary describing the ingredient types of \
  every side ingredient.

  The dictionary should contain every ingredient type:
                                  - key: name of side ingredient
                                  - value: comma separated python list containing:
                                               * 1 type of side ingredient. This type should be contained\
                                                 in the list describing all the types of side ingredient.
                                               * cooking

  Here is the description of the meal: {meal_description}.
  Here is the string describing the side ingredients in the meal: {list_of_sides}.
  {format_instructions_2A_1} """

  prompt_2A_1 = ChatPromptTemplate.from_template(template=review_template_2A_1)


  # chain 2A_1: input= ... and output= ...
  chain_2A_1 = LLMChain(llm=chat,
                        prompt=prompt_2A_1,
                        output_key="Type_Side_Ingredients")
  ##############################################################################
  prompt_2A_2 = ChatPromptTemplate.from_template("""
  You are given:    * a meal description
                    * a string that describes side ingredients contained in a meal. \
  The string contains:
                     ** Meal: a meal description
                     ** List_Aromatics: a list containing the aromatics in the meal
                     ** List_Condiments: a list containing the condiments in the meal
                     ** List_Side_Ingredients: a list containing all the side ingredients in the meal

                    * a python dictionary describing the ingredient types and the specified cooking.

  You are asked to extract the tastes of every side ingredient. There are 5 different \
  basic tastes: sweet, sour, bitter, salty, savoury.
  Only output a python dictionary. This dictionary should contain:
                              - key: name of side ingredient
                              - value: comma separated python list containing:
                                                   * type of ingredient
                                                   * cooking
                                                   * taste of ingredient
  Here is the description of the meal: {meal_description}.
  Here is the string describing the side ingredients in the meal: {list_of_sides}.
  Here is the dictionary describing the ingredient types and the specified \
  cooking: {Type_Side_Ingredients}.
  """)

  # chain 2A_2: input= ... and output= ...
  chain_2A_2 = LLMChain(llm=chat,
                         prompt=prompt_2A_2,
                         output_key="Ingredient_taste")
  ##############################################################################
  # prompt template 2A_3:
  dominant_taste_schema = ResponseSchema(name="dominant_taste",
                                         description="""
  You are given:    * a meal description
                    * a string that describes side ingredients contained in a meal. \
  The string contains:
                     ** Meal: a meal description
                     ** List_Aromatics: a list containing the aromatics in the meal
                     ** List_Condiments: a list containing the condiments in the meal
                     ** List_Side_Ingredients: a list containing all the side ingredients in the meal

                    * a python dictionary describing the ingredient types and the specified cooking.
                    * a python dictionary describing the tastes of ingredients.

  Based on the description of the meal, the list of side ingredients, the dictionary describing \
  the types of side ingredients, the dictionary describing the tastes of side ingredient, identify \
  all the tastes of the meal. There are 5 different basic tastes: sweet, sour, bitter, \
  salty, savoury. Keep only the most dominant tastes. The most dominant tastes are the \
  tastes that give its main flavour to the meal.

  Output a python dictionary describing the more dominant tastes.
  If the dominant tastes can not be determined, output 0.

  The dictionary should contain every dominant taste:
           * key: dominant taste
           * value: comma separated python list containing only the name of side ingredients
                    that contribute to the taste going from the more contributing
                    ingredient to the less contributing ingredient.

  Here is the description of the meal: {meal_description}.
  Here is the string describing the side ingredients in the meal: {list_of_sides}.
  Here is the dictionary describing the ingredient types and the specified cooking: {Type_Side_Ingredients}.
  Here is the dictionary containing the taste of ingredients: {Ingredient_taste}.""")

  response_schemas_2A_3 = [dominant_taste_schema]

  output_parser_2A_3 = StructuredOutputParser.from_response_schemas(response_schemas_2A_3)

  format_instructions_2A_3 = output_parser_2A_3.get_format_instructions()
  review_template_2A_3 = """
  You are given:    * a meal description
                    * a string that describes side ingredients contained in a meal. \
  The string contains:
                     ** Meal: a meal description
                     ** List_Aromatics: a list containing the aromatics in the meal
                     ** List_Condiments: a list containing the condiments in the meal
                     ** List_Side_Ingredients: a list containing all the side ingredients in the meal

                    * a python dictionary describing the ingredient types and the specified cooking
                    * a python dictionary describing the tastes of ingredients.

  Based on the description of the meal, the list of side ingredients, the dictionary describing \
  the types of side ingredients, the dictionary describing the tastes of side ingredient, you are \
  asked to extract the following information:

  dominant_taste:  identify all the tastes of the meal. There are 5 different basic tastes: \
  sweet, sour, bitter, salty, savoury. Keep only the most dominant tastes. The most dominant \
  tastes are the tastes that give its main flavour to the meal.

  Output a python dictionary describing the more dominant tastes.
  If the dominant tastes can not be determined, output 0.

  The dictionary should contain every dominant taste:
           * key: dominant taste
           * value: comma separated python list containing only the name of ingredients
                    that contribute to the taste going from the more contributing
                    ingredient to the less contributing ingredient.

  Here is the description of the meal: {meal_description}.
  Here is the string describing the side ingredients in the meal: {list_of_sides}.
  Here is the dictionary describing the ingredient types and the specified cooking: {Type_Side_Ingredients}.
  Here is the dictionary containing the taste of ingredients: {Ingredient_taste}.

  {format_instructions_2A_3}"""

  prompt_2A_3 = ChatPromptTemplate.from_template(template=review_template_2A_3)


  # chain 2A_3: input= ... and output= ...
  chain_2A_3 = LLMChain(llm=chat,
                            prompt=prompt_2A_3,
                            output_key="meal_taste")


  ##############################################################################
  # overall_chain: input= ... and output= ...

  overall_chain = SequentialChain(
      chains=[chain_2A_1, chain_2A_2, chain_2A_3],
      input_variables=["meal_description", "list_of_sides", "format_instructions_2A_1", "format_instructions_2A_3"],
      output_variables=["Type_Side_Ingredients", "Ingredient_taste", "meal_taste"],
      verbose=False)

  simple_df = overall_chain({'meal_description':meal_description, 'list_of_sides':list_of_sides, 'format_instructions_2A_1':format_instructions_2A_1, 'format_instructions_2A_3':format_instructions_2A_3})
  output_dict_2A_1 = output_parser_2A_1.parse(simple_df['Type_Side_Ingredients'])
  output_dict_2A_2 = simple_df['Ingredient_taste']
  output_dict_2A_3 = output_parser_2A_3.parse(simple_df['meal_taste'])

  return (output_dict_2A_1, output_dict_2A_2, output_dict_2A_3)

def get_AI_grape_proposition(chat, wine_types, meal_description, meal_taste):
  '''
  INPUTS:   * a chat object
            * a list containing wine categories
            * a description of the meal
            * a dictionary describing the tastes of the meal

  OUTPUTS:  * proposition of wine grape pairing well with the meal
              given as input

  This function suggests a  wine grape that would pair best with the meal given
  as input.
  This function uses gpt-3.5-turbo model and Langchain chaining prompts.
  '''

  # prompt template 5:
  # Create prompt using ResponseSchema
  proposition_schema = ResponseSchema(name="grape_proposition",
                                      description="""
                                      You are given: \

                                         * {wine_types}: a first python list containing the wine categories \

                                         * {meal_description}: the description of a meal \

                                         * {meal_taste}: a python dictionary describing the main \
                                           tastes of the meal and the ingredients \
                                           of the meal associated to that taste \

                                      Suppose you are a wine specialist that knows almost \
                                      everything about pairing meals and wines. \
                                      Based on the wine categories, the description of the meal, \
                                      the main tastes of the meal, you are asked to suggest a wine grape \
                                      corresponding to the wine category and that would pair best with \
                                      the meal. \
                                      Give also a short explanation why you chose that particular wine grape\
                                      to pair with the meal in terms of aroms and tastes. \

                                      Output a python dictionary. The dictionary should contain: \
                                          * key: type of wine \
                                          * value: a python list containing:
                                                ** suggestion of wine grape corresponding to the type of wine and \
                                                 that would pair with the meal. \
                                                ** a short explanation why you chose that particular wine grape\
                                                 to pair with the meal in terms of aroms and tastes. \

                                          """)

  response_schemas = [proposition_schema]

  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

  format_instructions = output_parser.get_format_instructions()

  review_template = """
  You are given: \
                  * {wine_types}: a first python list containing the wine categories \

                  * {meal_description}: the description of a meal \

                  * {meal_taste}: a python dictionary describing the main  tastes of the meal \
                  and the ingredients of the meal associated to that taste \


  Suppose you are a wine specialist that knows almost everything about pairing \
  meals and wines. \
  Based on the wine categories, the description of the meal, the main tastes of \
  the meal, you are asked to extract the following information: \

  grape_proposition:        for every wine category contained in the python list \
                            {wine_types}, suggest a wine grape  and that would pair best with the meal. \
                            Give also a short explanation why you chose that particular wine grape\
                            to pair with the meal in terms of aroms and tastes. \
                            Output a python dictionary. The dictionary should contain: \
                                 * key : type of wine
                                 * value: a python dictionary. The dictionary should contain: \
                                       ** key no.1 named "suggestion" \
                                       ** value no.1: suggestion of wine grape corresponding to the type \
                                                      of wine and that would pair with the meal. \
                                       ** key no.2 named "description" \
                                       ** value no.2:  short explanation why you chose that particular wine grape\
                                                       to pair with the meal in terms of aroms and tastes. \

  {format_instructions}
    """

  prompt = ChatPromptTemplate.from_template(template=review_template)


  # chain: input= ... and output= ...
  chain = LLMChain(llm=chat,
                   prompt=prompt,
                   output_key="proposition_AI")

  # overall_chain: input= ...
  # and output= ...
  overall_chain_proposition = SequentialChain(
        chains=[chain],
        input_variables=["wine_types", "meal_description", "meal_taste", "format_instructions"],
        output_variables=["proposition_AI"],
        verbose=False)

  simple_df_proposition = overall_chain_proposition({'wine_types': wine_types, 'meal_description':meal_description, 'meal_taste':meal_taste, 'format_instructions':format_instructions})
  output_dict = output_parser.parse(simple_df_proposition['proposition_AI'])

  return(output_dict.get('grape_proposition'))

  '''

  This function takes as input:
  * a first python list containing the wine categories
  * a description of the meal
  * a dictionary describing the taste of the meal
  * a second python list containing wines that you can not suggest.

  This function outputs a proposition of wine grape using GPT AI model.
  '''

  # prompt template 5:
  # Create prompt using ResponseSchema
  proposition_schema = ResponseSchema(name="grape_proposition",
                                      description="""
                                      You are given: \

                                         * {wine_types}: a first python list containing the wine categories \

                                         * {meal_description}: the description of a meal \

                                         * {meal_taste}: a python dictionary describing the main \
                                           tastes of the meal and the ingredients \
                                           of the meal associated to that taste \

                                      Suppose you are a wine specialist that knows almost \
                                      everything about pairing meals and wines. \
                                      Based on the wine categories, the description of the meal, \
                                      the main tastes of the meal, you are asked to suggest a wine grape \
                                      corresponding to the wine category and that would pair best with \
                                      the meal. \
                                      Give also a short explanation why you chose that particular wine grape\
                                      to pair with the meal in terms of aroms and tastes. \

                                      Output a python dictionary. The dictionary should contain: \
                                          * key: type of wine \
                                          * value: a python list containing:
                                                ** suggestion of wine grape corresponding to the type of wine and \
                                                 that would pair with the meal. \
                                                ** a short explanation why you chose that particular wine grape\
                                                 to pair with the meal in terms of aroms and tastes. \

                                          """)

  response_schemas = [proposition_schema]

  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

  format_instructions = output_parser.get_format_instructions()

  review_template = """
  You are given: \
                  * {wine_types}: a first python list containing the wine categories \

                  * {meal_description}: the description of a meal \

                  * {meal_taste}: a python dictionary describing the main  tastes of the meal \
                  and the ingredients of the meal associated to that taste \


  Suppose you are a wine specialist that knows almost everything about pairing \
  meals and wines. \
  Based on the wine categories, the description of the meal, the main tastes of \
  the meal, you are asked to extract the following information: \

  grape_proposition:        for every wine category contained in the python list \
                            {wine_types}, suggest a wine grape  and that would pair best with the meal. \
                            Give also a short explanation why you chose that particular wine grape\
                            to pair with the meal in terms of aroms and tastes. \
                            Output a python dictionary. The dictionary should contain: \
                                 * key : type of wine
                                 * value: a python dictionary. The dictionary should contain: \
                                       ** key no.1 named "suggestion" \
                                       ** value no.1: suggestion of wine grape corresponding to the type \
                                                      of wine and that would pair with the meal. \
                                       ** key no.2 named "description" \
                                       ** value no.2:  short explanation why you chose that particular wine grape\
                                                       to pair with the meal in terms of aroms and tastes. \

  {format_instructions}
    """

  prompt = ChatPromptTemplate.from_template(template=review_template)


  # chain: input= ... and output= ...
  chain = LLMChain(llm=chat,
                   prompt=prompt,
                   output_key="proposition_AI")

  # overall_chain: input= ...
  # and output= ...
  overall_chain_proposition = SequentialChain(
        chains=[chain],
        input_variables=["wine_types", "meal_description", "meal_taste", "format_instructions"],
        output_variables=["proposition_AI"],
        verbose=False)

  simple_df_proposition = overall_chain_proposition({'wine_types': wine_types, 'meal_description':meal_description, 'meal_taste':meal_taste, 'format_instructions':format_instructions})
  output_dict = output_parser.parse(simple_df_proposition['proposition_AI'])

  return(output_dict.get('grape_proposition'))

def get_AI_wine_proposition(chat, meal_description, meal_taste, wine_category, wine_grape):
  '''
  INPUTS:   * a chat object
            * the description of a meal
            * a dictionary describing the tastes of the meal
            * a string describing 1 wine category
            * a string describing 1 wine grape corresponding to the wine category

  OUTPUTS:  * a dictionary describing 1 wine corresponding to the wine category
              and wine grape given as input

  This function suggests a  wine  that would pair best with the meal given
  as input and that corresponds to the wine grape given as input.
  This function uses gpt-3.5-turbo model and Langchain chaining prompts.
  '''

  # prompt template 5:
  # Create prompt using ResponseSchema
  proposition_schema = ResponseSchema(name="wine_proposition",
                                            description="""
                                            You are given: \
                                               * {meal_description}: the description of a meal \

                                               * {meal_taste}: a python dictionary describing the main \
                                                  tastes of the meal and the ingredients \
                                                  of the meal associated to that taste \

                                              * {wine_category}: a string describing a wine category \

                                              * {wine_grape}: a string describing a wine grape corresponding to \
                                                 the wine category defined by {wine_category} \

                                            Suppose you are a wine specialist that knows almost \
                                            everything about pairing meals and wines. \
                                            Based on the description of the meal, the main tastes of the meal, the\
                                            wine category and the wine grape corresponding to that wine category, you \
                                            are asked to suggest the wine that would pair best with the meal and that \
                                            corresponds the wine category defined by {wine_category} and the wine grape \
                                            defined by {wine_grape}.  \

                                            Give also a short explanation why you chose that particular wine \
                                            to pair with the meal in terms of aroms and tastes. \

                                            Output a python dictionary. The dictionary should contain: \

                                               * name of wine grape \

                                               * python list. This list should contain the 4 following items: \

                                                   1: python dictionary. This dictionary should contain: \

                                                           *** key: "appellation" \
                                                           *** value: appellation of the wine. The appellation of a wine is \
                                                                      a legally defined geographical location used to identify where \
                                                                      and how grapes are grown and made into wine. \

                                                   2: python dictionary. This dictionary should contain: \

                                                           *** key: "year of production" \
                                                           *** value: the year of production of the wine. \

                                                   3: python dictionary. This dictionary should contain: \

                                                           *** key: "origins" \
                                                           *** value: country of origin of the wine. If possible, precise the region or \
                                                                      city of origin. \

                                                   4: python dictionary. This dictionary should contain: \

                                                           *** key: "explanation" \

                                                           *** value: Do not mention the price of the wine, \
                                                                      do not mention any website and \
                                                                      explain why you chose that particular wine \
                                                                      to pair with the meal in terms of aroms and tastes without \
                                                                      mentionning the price of the bottle or any url.


                                          """)

  response_schemas = [proposition_schema]

  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

  format_instructions = output_parser.get_format_instructions()

  review_template = """
  You are given: \
                  * {meal_description}: the description of a meal \

                  * {meal_taste}: a python dictionary describing the main \
                    tastes of the meal and the ingredients \
                    of the meal associated to that taste \

                  * {wine_category}: a string describing a wine category \

                  * {wine_grape}: a string describing a wine grape corresponding to \
                    the wine category defined by {wine_category} \

  Suppose you are a wine specialist that knows almost everything about pairing \
  meals and wines. Based on the description of the meal, the main tastes of the \
  meal, the wine category and the wine grape corresponding to that wine category, \
  you are asked to extract the following information: \

  wine_proposition:               the wine that would pair best with the meal and that \
                                  corresponds to the wine category defined by \
                                  {wine_category} and to the wine grape defined by \
                                  {wine_grape}. \

                                  Give also a short explanation why you chose that \
                                  particular wine to pair with the meal in terms of \
                                  aroms and tastes. \

                                  Output a python dictionary. The dictionary should contain: \

                                               * name of wine grape\

                                               * python list. This list should contain the 4 following items: \

                                                   1: python dictionary. This dictionary should contain: \

                                                           *** key: "appellation" \
                                                           *** value: appellation of the wine. The appellation of a wine is \
                                                                      a legally defined geographical location used to identify where \
                                                                      and how grapes are grown and made into wine. \

                                                   2: python dictionary. This dictionary should contain: \

                                                           *** key: "year of production" \
                                                           *** value: the year of production of the wine. \

                                                   3: python dictionary. This dictionary should contain: \

                                                           *** key: "origins" \
                                                           *** value: country of origin of the wine. If possible, precise the region or \
                                                                      city of origin. \

                                                   4: python dictionary. This dictionary should contain: \

                                                           *** key: "explanation" \

                                                           *** value: Do not mention the price of the wine, \
                                                                      do not mention any website and \
                                                                      explain why you chose that particular wine \
                                                                      to pair with the meal in terms of aroms and tastes without \
                                                                      mentionning the price of the bottle or any url. \

  {format_instructions}
    """

  prompt = ChatPromptTemplate.from_template(template=review_template)


  # chain: input= ... and output= ...
  chain = LLMChain(llm=chat,
                   prompt=prompt,
                   output_key="proposition_AI")

  # overall_chain: input= ...
  # and output= ...
  overall_chain_proposition = SequentialChain(
        chains=[chain],
        input_variables=["meal_description", "meal_taste", "wine_category", "wine_grape", "format_instructions"],
        output_variables=["proposition_AI"],
        verbose=False)

  simple_df_proposition = overall_chain_proposition({'meal_description':meal_description, 'meal_taste':meal_taste, 'wine_grape':wine_grape, 'wine_category':wine_category, 'format_instructions':format_instructions})
  output_dict = output_parser.parse(simple_df_proposition['proposition_AI'])

  return(output_dict)

def get_AI_bottle_proposition(chat, wine_category, wine_grape, wine):
  '''
  INPUTS:   * a chat object
            * a string describing a wine category
            * a string describing a wine grape
            * a dictionary describing a wine (i.e. appellation, year of production,
              origins)

  OUTPUTS:  * best bottle: a dictionary describing a bottle of wine corresponding to
                           the wine given as input. This wine is considered as 'the
                           best bottle one can find'.

            * cheap bottle: a dictionary describing a bottle of wine corresponding to
                            the wine given as input. This wine is considered as 'the
                            cheapest bottle one can find'.

            * easy to find bottle: a dictionary describing a bottle of wine
                                   corresponding to the wine given as input. This wine
                                   is considered as 'the easiest-to-find bottle one
                                   can find'.

  This function suggests a  wine  that would pair best with the meal given
  as input and that corresponds to the wine grape and wine given as input.
  This function uses gpt-3.5-turbo model and Langchain chaining prompts.
  '''

  # prompt template 5:
  # Create prompt using ResponseSchema
  best_proposition_schema = ResponseSchema(name="best_proposition",
                                            description="""
                                            You are given: \

                                               * {wine_category}: a string describing a wine category \

                                               * {wine_grape}: a string describing a wine grape corresponding to \
                                                               the wine category defined by {wine_category} \

                                               * {wine}: a python dictionary describing a wine. This \
                                                         dictionary contains 3 different keys: \
                                                            1- 'appellation': the appellation of the wine. You \
                                                                              should know that the appellation of \
                                                                              a wine is a legally defined geographical \
                                                                              location used to identify where and how \
                                                                              grapes are grown and made into wine.  \
                                                            2- 'year of production': the year of production of the wine. \
                                                            3- 'origins': the geographical origins of the wine. \

                                            Suppose you are a wine specialist that knows everything about wine and particularly about \
                                            wine bottles and their prices. Base your thinking on the description of the meal, the main \
                                            tastes of the meal, the wine category and the wine grape corresponding to that wine category. \
                                            Only consider wine bottle corresponding to the wine category {wine_category} and to the wine \
                                            grape {wine_grape}. You are asked to propose the best wine bottle you know and that corresponds \
                                            to the considered wine. This bottle of wine should be considered as the best in terms of quality, \
                                            reputation and rarety. This wine bottle should be considered as perfect by many specialists. \


                                            Only output a python dictionary, avoid any other text. This dictionary should contain: \

                                                  * key no.1: 'name of the bottle' \
                                                  * value no.1 name of the proposed bottle of wine \

                                                  * key no.2: 'minimum price of a bottle' \
                                                  * value no.2: minimum price of a bottle expressed in euros. Add the symbol '€'\

                                                  * key no.3: 'awards' \
                                                  * value no.3: Briefly explain the awards the bottle received. If there is no \
                                                                award, output '0'. \

                                                  * key no.4: 'bottling' \
                                                  * value no.4: python list with 3 items. If no information, output '0'. These items \
                                                                are: \
                                                                    -1: place of wine bottling. Locate this place in a region and country. \
                                                                    -2: date of wine bottling \

                                                  * key no.5: 'bottler' \
                                                  * value no.5: name of the bottler. \

                                                  * key no.6: 'alcoholic strength' \
                                                  * value no.6: alcoholic strength of the bottle of wine expressed in '% vol'. If no \
                                                                information, output '0'. \

                                                  * key no.7: 'description' \
                                                  * value no.7: short description of the bottle of wine. Also explain why you think that \
                                                                this bottle is the best one can find for the wine grape {wine_grape}.

                                          """)

  ratio_proposition_schema = ResponseSchema(name="ratio_proposition",
                                            description="""
                                            You are given: \

                                               * {wine_category}: a string describing a wine category \

                                               * {wine_grape}: a string describing a wine grape corresponding to \
                                                               the wine category defined by {wine_category} \

                                               * {wine}: a python dictionary describing a wine. This \
                                                         dictionary contains 3 different keys: \
                                                            1- 'appellation': the appellation of the wine. You \
                                                                              should know that the appellation of \
                                                                              a wine is a legally defined geographical \
                                                                              location used to identify where and how \
                                                                              grapes are grown and made into wine.  \
                                                            2- 'year of production': the year of production of the wine. \
                                                            3- 'origins': the geographical origins of the wine. \

                                            Suppose you are a wine specialist that knows everything about wine and particularly about \
                                            wine bottles and their prices. Base your thinking on the description of the meal, the main \
                                            tastes of the meal, the wine category and the wine grape corresponding to that wine category. \
                                            Only consider wine bottle corresponding to the wine category {wine_category} and to the wine \
                                            grape {wine_grape}. You are asked to propose the wine bottle that has the best quality/price \
                                            ratio that you know and that corresponds to the considered wine. The price of this wine bottle \
                                            should be lower than the price of the first wine bottle you proposed.\

                                            Only output a python dictionary, avoid any other text. This dictionary should contain: \

                                                  * key no.1: 'name of the bottle' \
                                                  * value no.1 name of the proposed bottle of wine \

                                                  * key no.2: 'price of a bottle' \
                                                  * value no.2: price of a bottle expressed in euros. Add the symbol '€'\

                                                  * key no.3: 'awards' \
                                                  * value no.3: Briefly explain the awards the bottle received. If there is no \
                                                                award, output '0'. \

                                                  * key no.4: 'bottling' \
                                                  * value no.4: python list with 3 items. If no information, output '0'. These items \
                                                                are: \
                                                                    -1: place of wine bottling. Locate this place in a region and country. \
                                                                    -2: date of wine bottling \

                                                  * key no.5: 'bottler' \
                                                  * value no.5: name of the bottler. \

                                                  * key no.6: 'alcoholic strength' \
                                                  * value no.6: alcoholic strength of the bottle of wine expressed in '% vol'. If no \
                                                                information, output '0'. \

                                                  * key no.7: 'description' \
                                                  * value no.7: short description of the bottle of wine. Also explain why you think that \
                                                                this bottle has the best quality/price ratio for the wine grape {wine_grape}.

                                          """)

  easy_proposition_schema = ResponseSchema(name="easy_proposition",
                                           description="""
                                            You are given: \

                                               * {wine_category}: a string describing a wine category \

                                               * {wine_grape}: a string describing a wine grape corresponding to \
                                                               the wine category defined by {wine_category} \

                                               * {wine}: a python dictionary describing a wine. This \
                                                         dictionary contains 3 different keys: \
                                                            1- 'appellation': the appellation of the wine. You \
                                                                              should know that the appellation of \
                                                                              a wine is a legally defined geographical \
                                                                              location used to identify where and how \
                                                                              grapes are grown and made into wine.  \
                                                            2- 'year of production': the year of production of the wine. \
                                                            3- 'origins': the geographical origins of the wine. \

                                            Suppose you are a wine specialist that knows everything about wine and particularly about \
                                            wine bottles and their prices. Base your thinking on the description of the meal, the main \
                                            tastes of the meal, the wine category and the wine grape corresponding to that wine category. \
                                            Only consider wine bottle corresponding to the wine category {wine_category} and to the wine \
                                            grape {wine_grape}. You are asked to propose a wine bottle that everyone can find easily at \
                                            the supermaket and that corresponds to the considered wine. \

                                            Only output a python dictionary, avoid any other text. This dictionary should contain: \

                                                  * key no.1: 'name of the bottle' \
                                                  * value no.1 name of the proposed bottle of wine \

                                                  * key no.2: 'price of a bottle' \
                                                  * value no.2: price of a bottle expressed in euros. Add the symbol '€'\

                                                  * key no.3: 'awards' \
                                                  * value no.3: Briefly explain the awards the bottle received. If there is no \
                                                                award, output '0'. \

                                                  * key no.4: 'bottling' \
                                                  * value no.4: python list with 3 items. If no information, output '0'. These items \
                                                                are: \
                                                                    -1: place of wine bottling. Locate this place in a region and country. \
                                                                    -2: date of wine bottling \

                                                  * key no.5: 'bottler' \
                                                  * value no.5: name of the bottler. \

                                                  * key no.6: 'alcoholic strength' \
                                                  * value no.6: alcoholic strength of the bottle of wine expressed in '% vol'. If no \
                                                                information, output '0'. \

                                                  * key no.7: 'description' \
                                                  * value no.7: short description of the bottle of wine. Also explain why you think that \
                                                                this bottle has the best quality/price ratio for the wine grape {wine_grape}.

                                          """)

  response_schemas = [best_proposition_schema, ratio_proposition_schema, easy_proposition_schema]

  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

  format_instructions = output_parser.get_format_instructions()

  review_template = """
  You are given: \

                  * {wine_category}: a string describing a wine category \

                  * {wine_grape}: a string describing a wine grape corresponding to \
                                  the wine category defined by {wine_category} \

                  * {wine}: a python dictionary describing a wine. This dictionary contains 3 \
                            different keys: \

                                    1- 'appellation': the appellation of the wine. You should \
                                                      know that the appellation of a wine is a \
                                                      legally defined geographical location used \
                                                      to identify where and how grapes are grown \
                                                      and made into wine.  \
                                    2- 'year of production': the year of production of the wine. \
                                    3- 'origins': the geographical origins of the wine. \

  Suppose you are a wine specialist that knows everything about wine and particularly about \
  wine bottles and their prices. Base your thinking on the description of the meal, the main \
  tastes of the meal, the wine category and the wine grape corresponding to that wine category. \
  Only consider wine bottle corresponding to the wine category {wine_category} and to the wine \
  grape {wine_grape}. You are asked to propose 3 bottles of wine: \


  best_proposition:       the best wine bottle you know that corresponds to the considered wine. This \
                          bottle of wine should be considered as the best in terms of quality, reputation \
                          and rarety. This wine bottle should be considered as perfect by many specialists. \

                          Only output a python dictionary, avoid any other text. This dictionary should contain: \

                                              * key no.1: 'name of the bottle' \
                                              * value no.1 name of the proposed bottle of wine \

                                              * key no.2: 'minimum price of a bottle' \
                                              * value no.2: minimum price of a bottle expressed in euros. Add the symbol '€'\

                                              * key no.3: 'awards' \
                                              * value no.3: Briefly explain the awards the bottle received. If there is no \
                                                            award, output '0'. \

                                              * key no.4: 'bottling' \
                                              * value no.4: python list with 3 items. If no information, output '0'. These items \
                                                            are: \
                                                                -1: place of wine bottling. Locate this place in a region and country. \
                                                                -2: date of wine bottling \

                                              * key no.5: 'bottler' \
                                              * value no.5: name of the bottler. \


                                              * key no.6: 'alcoholic strength' \
                                              * value no.6: alcoholic strength of the bottle of wine expressed in '% vol'. If no \
                                                            information, output '0'. \

                                              * key no.7: 'description' \
                                              * value no.7: short description of the bottle of wine. Also explain why you think that \
                                                            this wine bottle is the best one can find for the wine grape {wine_grape}. \


  ratio_proposition:      the wine bottle that has the best quality/price ratio that you know and that corresponds to the considered \
                          wine. The price of this wine bottle should be lower than the price of the first wine bottle you proposed.\

                          Only output a python dictionary, avoid any other text. This dictionary should contain: \

                                                  * key no.1: 'name of the bottle' \
                                                  * value no.1 name of the proposed bottle of wine \

                                                  * key no.2: 'minimum price of a bottle' \
                                                  * value no.2: minimum price of a bottle expressed in euros. Add the symbol '€'\

                                                  * key no.3: 'awards' \
                                                  * value no.3: Briefly explain the awards the bottle received. If there is no \
                                                                award, output '0'. \

                                                  * key no.4: 'bottling' \
                                                  * value no.4: python list with 3 items. If no information, output '0'. These items \
                                                                are: \
                                                                    -1: place of wine bottling. Locate this place in a region and country. \
                                                                    -2: date of wine bottling \

                                                  * key no.5: 'bottler' \
                                                  * value no.5: name of the bottler. \

                                                  * key no.6: 'alcoholic strength' \
                                                  * value no.6: alcoholic strength of the bottle of wine expressed in '% vol'. If no \
                                                                information, output '0'. \

                                                  * key no.7: 'description' \
                                                  * value no.7: short description of the bottle of wine. Also explain why you think that \
                                                                this wine bottle has the best quality/price ratio for the wine grape {wine_grape}. \

  easy_proposition:       a bottle of wine that everyone can find easily at the supermaket and that corresponds to the considered wine.\

                          Only output a python dictionary, avoid any other text. This dictionary should contain: \

                                                  * key no.1: 'name of the bottle' \
                                                  * value no.1 name of the proposed bottle of wine \

                                                  * key no.2: 'price of a bottle' \
                                                  * value no.2: price of a bottle expressed in euros. Add the symbol '€'\

                                                  * key no.3: 'awards' \
                                                  * value no.3: Briefly explain the awards the bottle received. If there is no \
                                                                award, output '0'. \

                                                  * key no.4: 'bottling' \
                                                  * value no.4: python list with 3 items. If no information, output '0'. These items \
                                                                are: \
                                                                    -1: place of wine bottling. Locate this place in a region and country. \
                                                                    -2: date of wine bottling \

                                                  * key no.5: 'bottler' \
                                                  * value no.5: name of the bottler. \

                                                  * key no.6: 'alcoholic strength' \
                                                  * value no.6: alcoholic strength of the bottle of wine expressed in '% vol'. If no \
                                                                information, output '0'. \

                                                  * key no.7: 'description' \
                                                  * value no.7: short description of the bottle of wine. Also explain why you think that \
                                                                this wine bottle can be easily found at the supermarket. \

  {format_instructions}
    """

  prompt = ChatPromptTemplate.from_template(template=review_template)


  # chain: input= ... and output= ...
  chain = LLMChain(llm=chat,
                   prompt=prompt,
                   output_key="proposition_AI")

  # overall_chain: input= ...
  # and output= ...
  overall_chain_proposition = SequentialChain(
        chains=[chain],
        input_variables=["wine_category", "wine_grape", "wine", "format_instructions"],
        output_variables=["proposition_AI"],
        verbose=False)

  simple_df_proposition = overall_chain_proposition({'wine_category':wine_category, 'wine_grape':wine_grape, 'wine':wine, 'format_instructions':format_instructions})
  output_dict = output_parser.parse(simple_df_proposition['proposition_AI'])

  return(output_dict)

def get_wine_cat_from_sides(meal_description, string_of_sides, taste_dict, chat):
  '''
  INPUTS:   * the description of a meal
            * a list of side ingredients contained in the meal
            * a dictionary describing the tastes of the meal
            * a chat object

  OUTPUTS:  * a list of wine categories
            * a list describing the most dominating tastes of the meal

  This function suggests a wine category that would pair well with the meal
  given as input based on the side ingredients in that meal.
  The suggestion is done using a data table.
  '''

  # get side ingredients that appear in dominating taste
  sides_list = taste_dict.get('taste_origin')['Dominating_taste']

  # get the dict with types of ingredient
  # get the dict with types of dominating taste
  (ing_types_side, ing_tastes_side, meal_taste_side) = get_meal_body_from_sides(meal_description, string_of_sides, chat)

  # output the dictionary describing the most dominating side tastes
  meal_dom_taste_side = meal_taste_side.get('dominant_taste')

  ## try to pair wine category with side ingredients using herbs&spices data
  wines_cat_sides = pair_wine_with_sides(sides_list)

  if len(wines_cat_sides)==0:
    ## if not possible to pair wine categories with herbs&spices data, pair side
    ## ingredients with initial pairing data
    wines_cat_sides = get_wine_cat_from_side(meal_description, ing_types_side, meal_taste_side, chat)


  return (wines_cat_sides, meal_dom_taste_side)

def get_wine_categories(meal_description, chat):
  '''
  INPUTS:   * the description of a meal
            * a chat object

  OUTPUTS:  * a list of wine categories
            * a list describing the most dominating tastes of the meal

  This function suggests a wine category that would pair well with the meal
  given as input based on the main ingredients in that meal.
  The suggestion is done using a data table.
  '''

  # get the meal infos
  (ing_list, side_list, main_list, taste_origin) = get_first_meal_info(meal_description, chat)
  word = taste_origin.get('taste_origin')['Origin_of_Taste']

  if(word == 'main'):
    # no need to change the function get_meal_body_from_main when no sauce
    (ing_types_main, ing_tastes_main, meal_taste_main) = get_meal_body_from_main(meal_description, main_list, chat)
    meal_dom_taste = meal_taste_main.get('dominant_taste')
    wine_cat = get_wine_cat_from_main(meal_description, ing_types_main, meal_taste_main, chat)

  elif(word == 'side'):
    (wine_cat, meal_taste_side) = get_wine_cat_from_sides(meal_description, side_list, taste_origin, chat)
    meal_dom_taste = meal_taste_side

  return(wine_cat, meal_dom_taste)
