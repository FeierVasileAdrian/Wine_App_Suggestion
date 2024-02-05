# IMPORTS
import sys
import numpy as np

from Utility import get_LLM
from get_messages import put_in_format, create_wine_cat_string_choice, create_wine_cat_string_imposed, \
                         create_wine_grape_string, create_wine_string, create_bottle_string, get_introduction_text,\
                         get_exit_message, get_meal_input_text, get_wine_cat_num_error_message, \
                         get_wait_message_2, get_wait_message_3, get_wait_message_4, get_option_error_message, \
                         get_option_1_message, get_option_2_message, get_option_3_message

from prompts import get_AI_grape_proposition, get_AI_wine_proposition, get_AI_bottle_proposition, \
                    get_wine_categories

########################################################################################################################

def MAIN_INTERACTION():
  """
  INPUTS: /
  OUTPUTS: /

  This function defines the interaction with the user. It asks inputs and
  displays the messages to the user.
  """
  formated_introduction_text = put_in_format(get_introduction_text())
  user_start = input(formated_introduction_text)

  if user_start == 'q':
    formated_exit_message = put_in_format(get_exit_message())
    sys.exit(formated_exit_message)


  # define the LLM model
  chat = get_LLM()

  #########
  # step 1: get the meal description and propose the corresponding wine categories
  formated_input_meal_text = put_in_format(get_meal_input_text())
  user_meal = input(formated_input_meal_text)

  if user_meal == 'q':
    formated_exit_message = put_in_format(get_exit_message())
    sys.exit(formated_exit_message)

  (wine_categories, meal_dominating_taste)  = get_wine_categories(user_meal, chat)

  if len(wine_categories) > 1:
    wine_cat_string_choice = create_wine_cat_string_choice(wine_categories)
    formated_wine_cat_string_choice = put_in_format(wine_cat_string_choice)
    number_wine_cat = input(formated_wine_cat_string_choice)

  else:
    wine_cat_string_imposed = create_wine_cat_string_imposed(wine_categories)
    formated_wine_cat_string_imposed = put_in_format(wine_cat_string_imposed)
    print(formated_wine_cat_string_imposed)
    number_wine_cat = '1'


  if number_wine_cat == 'q':
    formated_exit_message = put_in_format(get_exit_message())
    sys.exit(formated_exit_message)

  while int(number_wine_cat) > len(wine_categories):
    formated_wine_cat_num_error = put_in_format(get_wine_cat_num_error_message(len(wine_categories)))
    number_wine_cat = input(formated_wine_cat_num_error)

  # step 1bis: keep only the slected wine category for the rest of the analysis
  selected_wine_cat = np.array([wine_categories[int(number_wine_cat)-1]])

  # Display "Please wait" message no.2
  formated_wait_message_2 = put_in_format(get_wait_message_2())
  print(formated_wait_message_2)

  #########
  # step 2: get the wine grape
  wine_grapes = get_AI_grape_proposition(chat, wine_categories, user_meal, meal_dominating_taste)
  wine_grape_string = create_wine_grape_string(wine_grapes.get(selected_wine_cat[0]))
  # Display the message about the wine grape
  formated_wine_grape_string = put_in_format(wine_grape_string)
  print(formated_wine_grape_string)

  # Display "Please wait" message no.3
  formated_wait_message_3 = put_in_format(get_wait_message_3())
  print(formated_wait_message_3)

  #########
  # step 3: get the wine
  current_wine_cat = selected_wine_cat[0]
  current_wine_grape = wine_grapes.get(current_wine_cat).get('suggestion')
  wine_suggestion_output = get_AI_wine_proposition(chat, user_meal, meal_dominating_taste, current_wine_cat, current_wine_grape)

  item_acc = 0
  for key, value in wine_suggestion_output.items():
    if item_acc == 1:
        wine_dict = {key: value}
    item_acc += 1

  # Display the message about the wine
  wine_string = create_wine_string(wine_dict, wine_grapes)
  formated_wine_string = put_in_format(wine_string)
  print(formated_wine_string)

  # step 3bis: drop the key 'explanation' from wine_dict
  wine_dict_pop = wine_dict.get(current_wine_grape)[0]
  wine_dict_pop.pop('explanation')

  #########
  # step 4: get the bottles

  # display the message
  wine_bottle_string = create_bottle_string(current_wine_grape, wine_dict_pop.get('appellation'))
  bottle_option_input = input(wine_bottle_string)

  if bottle_option_input == 'q':
    formated_exit_message = put_in_format(get_exit_message())
    sys.exit(formated_exit_message)

  while int(bottle_option_input)!= 1 and int(bottle_option_input)!= 2 and int(bottle_option_input)!= 3:
    bottle_option_input = input(get_option_error_message())

  # Display "Please wait" message no.4
  formated_wait_message_4 = put_in_format(get_wait_message_4())
  print(formated_wait_message_4)

  bottle_AI = get_AI_bottle_proposition(chat, current_wine_cat, current_wine_grape, wine_dict_pop)

  # Display wine bottle suggestion
  if int(bottle_option_input) == 1:
    formated_option_1_message = put_in_format(get_option_1_message(current_wine_grape, wine_dict_pop, bottle_AI))
    print(formated_option_1_message)

  elif int(bottle_option_input) == 2:
    formated_option_2_message = put_in_format(get_option_2_message(current_wine_grape, wine_dict_pop, bottle_AI))
    print(formated_option_2_message)

  elif int(bottle_option_input) == 3:
    formated_option_3_message = put_in_format(get_option_3_message(current_wine_grape, wine_dict_pop, bottle_AI))
    print(formated_option_3_message)
