import textwrap

################################################################################

def put_in_format(text_input):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """
  input_lines = text_input.splitlines()

  format_text = """
  """
  for line in input_lines:
    wrapper = textwrap.TextWrapper(width=100)
    word_list = wrapper.wrap(text=line)

    for element_line in word_list:
      format_text += "  {} \n".format(element_line)

    format_text += "\n"


  return format_text

def create_wine_cat_string_choice(wine_cat_array):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  wine_cat_string_choice = """
  Which of the following wine categories would you prefer with your meal?
  """

  item_num = 1
  for item in wine_cat_array:
    wine_cat_string_choice += """
    {}
    """.format(str(item_num) + "- " + item)
    item_num += 1

  wine_cat_string_choice += """
  Type the number corresponding to the wine category you prefer.
  For example, to select the wine category "{}", type 1 and then ENTER.
  """.format(wine_cat_array[0])

  return wine_cat_string_choice

def create_wine_cat_string_imposed(wine_cat_array):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  wine_cat_string_imposed = """
  The tastes and aromas contained in the meal you just described would pair very well with a {} wine.
  """.format(wine_cat_array[0])

  return wine_cat_string_imposed

def create_wine_grape_string(wine_grape_output):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  num_acc = 0
  for key,value in wine_grape_output.items():

    if num_acc == 0:
      selected_grape = value
    elif num_acc == 1:
      description = value

    num_acc += 1

  wine_grape_string = """
  Based on your meal, I propose you to pair your meal with a wine made from {} grape.

  {}
  """.format(selected_grape, description)

  return wine_grape_string

def create_wine_string(wine_output, wine_grapes_output):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  for key, value in wine_output.items():
    selected_grape = key
    wine_infos_dict = value[0]

  wine_string = """
  Based on your meal, I propose you to pair your meal with this wine:
      Grape: {}
      Appelation: {}
      Year Of Production: {}
      Origins: {}

  {}
  """.format(selected_grape,
             wine_infos_dict.get('appellation'),
             wine_infos_dict.get('year of production'),
             wine_infos_dict.get('origins'),
             wine_infos_dict.get('explanation'))

  return wine_string

def create_bottle_string(wine_grape, wine):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  bottle_string = """
  We are almost done!
  I need you to provide me one last information.
  Based on my huge knowledge, I can give you 3 options for the choice of the {}, {} wine bottle:

       - option no.1: BEST WINE BOTTLE
         I will give you the best wine bottle of I know.
         This bottle of wine should be considered as the best in terms of quality, reputation and rarety.
         You should then expect a higher price.

       - option no.2: BEST QUALITY/PRICE RATIO BOTTLE
         I will give you the wine bottle that has the best quality/price ratio that I know.

       - option no.3: EASY TO FIND BOTTLE
         I will give you a wine bottle that everyone can find easily at the supermaket.

  Type 1, 2 or 3  and then ENTER to select an option.
  """.format(wine_grape, wine)

  return bottle_string

def get_introduction_text():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  introduction_text = """
  Hi there!

  I'm a Wine Suggestion Intelligence.
  I have been created to help you choose a bottle of wine that would pair perfectly with your meal.
  I will guide you through several steps and at the end, I will provide you with a bottle of wine.
  At any time, you can type "q" to exit the program.

  Type ENTER to start the adventure!
  """

  return introduction_text

def get_exit_message():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  exit_message="""
  You broke my artifical heart! You chose to quit the program.
  """

  return exit_message

def get_meal_input_text():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  meal_input_text = """
  To begin, give me a description of your meal , then ENTER.
  """

  return meal_input_text

def get_wait_message_1():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  wait_message_1 = """
  I am analyzing your meal description and figuring out what wine category would pair best with...
  Please wait, you will not regret it, trust me!
  """

  return wait_message_1

def get_wine_cat_num_error_message(number):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  wine_cat_error_message = """
  Wrong number!
  The number you enter should be lower or equal to {}.
  """.format(number)

  return wine_cat_error_message

def get_wait_message_2():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  wait_message_2 = """
  Let me take a look at the wine category you have just selected...
  Which wine grape am I going to suggest ?
  Let me think...
  """

  return wait_message_2

def get_wait_message_3():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  wait_message_3 = """
  I will finally suggest you a wine corresponding to that grape.
  There are thousands and thousands of wine in my head!
  I need a moment to go through and select the best wine for your meal!
  """

  return wait_message_3

def get_wait_message_4():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  error_message_4 = """
  Lucky you!
  I will search for that wine bottle, give me a moment please...
  """

  return error_message_4

def get_option_error_message():
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  option_error_message = """
  Wrong input!
  Input should be 1 or 2 or 3.
  """

  return option_error_message

def get_option_1_message(wine_grape, wine_dict, bottle_info):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  option_1_message = """
  Here is the best bottle of "{}, {}" I know:

        - bottle name: {}
        - minimum price: {}
        - awards: {}
        - bottling: -- place: {}
                    -- year: {}
        - bottler: {}
        - alcoholic strength: {}

  {}
  """.format(wine_grape,
             wine_dict.get('appellation'),
             bottle_info.get('best_proposition').get('name of the bottle'),
             bottle_info.get('best_proposition').get('minimum price of a bottle'),
             bottle_info.get('best_proposition').get('awards'),
             bottle_info.get('best_proposition').get('bottling')[0],
             bottle_info.get('best_proposition').get('bottling')[1],
             bottle_info.get('best_proposition').get('bottler'),
             bottle_info.get('best_proposition').get('alcoholic strength'),
             bottle_info.get('best_proposition').get('description'))

  return option_1_message

def get_option_2_message(wine_grape, wine_dict, bottle_info):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  option_2_message = """
  Here is the bottle of "{}, {}" with the best quality/price ratio I know:

        - bottle name: {}
        - minimum price: {}
        - awards: {}
        - bottling: -- place: {}
                    -- year: {}
        - bottler: {}
        - alcoholic strength: {}

  {}
  """.format(wine_grape,
             wine_dict.get('appellation'),
             bottle_info.get('ratio_proposition').get('name of the bottle'),
             bottle_info.get('ratio_proposition').get('minimum price of a bottle'),
             bottle_info.get('ratio_proposition').get('awards'),
             bottle_info.get('ratio_proposition').get('bottling')[0],
             bottle_info.get('ratio_proposition').get('bottling')[1],
             bottle_info.get('ratio_proposition').get('bottler'),
             bottle_info.get('ratio_proposition').get('alcoholic strength'),
             bottle_info.get('ratio_proposition').get('description'))

  return option_2_message

def get_option_3_message(wine_grape, wine_dict, bottle_info):
  """
  INPUTS: unformated text (string)
  OUTPUTS: formatted text

  This function formats the text given as input so that it can be displayed
  to the user in a more comprehensible way.
  """

  option_3_message = """
  Here is the bottle of "{}, {}" that is the easiest to find following my experience and knowledge:

        - bottle name: {}
        - minimum price: {}
        - awards: {}
        - bottling: -- place: {}
                    -- year: {}
        - bottler: {}
        - alcoholic strength: {}

  {}
  """.format(wine_grape,
             wine_dict.get('appellation'),
             bottle_info.get('easy_proposition').get('name of the bottle'),
             bottle_info.get('easy_proposition').get('minimum price of a bottle'),
             bottle_info.get('easy_proposition').get('awards'),
             bottle_info.get('easy_proposition').get('bottling')[0],
             bottle_info.get('easy_proposition').get('bottling')[1],
             bottle_info.get('easy_proposition').get('bottler'),
             bottle_info.get('easy_proposition').get('alcoholic strength'),
             bottle_info.get('easy_proposition').get('description'))

  return option_3_message
