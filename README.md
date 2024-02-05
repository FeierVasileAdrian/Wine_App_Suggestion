# Wine_Suggestion_App

## 1. Project description
The Wine Suggestion Application does wine suggestions to the user based on the meal description given as input.
Namely, the App suggests:
  * 1 wine grape
  * 1 wine
  * 1 bottle of that wine

Of course, the suggestions of such an App is not worth the advices of a real oenologist but I found it interesting and really funny to compare with.

This App is part of my personal learning and training about LLMs.

This App uses the power of GPT-3.5 Turbo model.

I used LangChain sequential chains to build more advanced prompts and chains of prompts.



## 2. How does the App proceed to suggest wine ?
After the user inputs the meal description, the App performs 4 main steps:

* Step 1
  * Based on meal description given as input, the model determines the main ingredients and the main tastes of the meal.
  * Then, it determines if the taste of the meal is mainly determined by the main ingredients or by the sides ingredients (i.e. sauces and spices).
  * Now the model knows which ingredients contribute the most to the taste of the meal, it uses a simple method to determine what wine category would pair best with the meal. If there are several matching wine categories, the app asks the user what wine category he/she prefers.

* Step 2:
  * Based on wine category and on meal description, the model suggests a wine grape.

* Step 3:
  * Based on wine category, meal description and wine grape, the model suggests a wine.
  * Every wine suggestion is determined by the following informations:
     * appellation
     * year of production
     * origins
     * short description of the wine

* Step 4:
  * Based on wine suggestion, the model proposes 3 options to the user:
    * option 1: ‘best bottle’. In that option, the model will suggests the best wine bottle it knows.
    * option 2: ‘best quality/price ratio bottle’. In that option, the model will suggest the wine bottle that has the best quality/price ratio.
    * option 3: ‘easy to find ratio’. In that option, the model will suggest a bottle of wine that is easy to find, at the supermarket for example.

    Every wine bottle is followed by those informations:
      * name of the bottle
      * price of a bottle
      * awards
      * bottling (place and date)
      * bottler
      * alcoholic strength
      * description of the wine bottle


## 2. How to install and run the project

### 2.0 Required modules
* python - 3.10.6 version
 * cohere
 * tiktoken
 * openai - 0.28.1 version
 * langchain - 0.0.319 version
 * python-dotenv
 * numpy
 * pandas

### 2.1 Using Google Colab (recommended)

  1.  Download Wine_App_Suggestion folder

  2. Go to Google Colab. Here is the link: [Google Colab](https://colab.research.google.com/?utm_source=scs-index)

  3. Click File, then click Upload Notebook and browse the file named Wine_Suggestion_APP_interact_GitHub.ipynb  that is contained in folder  /Wine_App_Suggestion/notebook

  4. In the folder /Wine_App_Suggestion/notebook, create a .env file that contains your OpenAI API secret key.
     This file should contain the following line (filled in with you personal key):   OPENAI_API_KEY = ‘sk-…’
     Make sure you have credentials for using get-3.5-turbo model.

  5. Import the .env file you created into Google Colab Notebook. (If needed check this helpful video: [YouTube Video]()

  6. If you have all modules installed, you can comment the installation lines in Google notebook (see picture here under).
     Otherwise, run the cell and the required modules will be installed.

  7. Click Runtime then click Run All. The WineApp starts running. It may take 30 sec to 1 min before you have the first output from the App.

  8. Enjoy the experience !

</br>
</br>


### 2.2 Using terminal under MacOs

  1. Download Wine_App_Suggestion folder

  2. Make sure you have installed all the required modules

  3. In the folder `/Wine_App_Suggestion/command-prompt`, create a `.env` file that contains your OpenAI API secret key. </br>
     This file should contain the following line (filled in with you personal key):   `OPENAI_API_KEY = ‘sk-…’` </br>
     Make sure you have credentials for using get-3.5-turbo model.

  5. Open your terminal and run the file `wine_suggestion_app_interact_github.py`

  6. Enjoy the experience !

</br>
</br>


## 3. Use case example

Here are some examples of meals that have been used for the development of the App:
  -  Rare beef steak with some smashed potatoes and roasted peppers.
  -  One big plate of freshly opened oysters.
  -  Toasts with foie gras and cranberry jam.
  -  Niçoise salad.
  -  Pasta with Ragù.
  -  Pad Ka Prao.
  -  Coq au vin.

Let us take the first meal:     Rare beef steak with some smashed potatoes and roasted peppers.


Here are the outputs I obtained when using on GoogleColab

</br>

Output  0 - User is asked to input the meal description

<img width="935" alt="Screenshot 2024-01-10 at 14 10 20" src="https://github.com/FeierVasileAdrian/wine_App/assets/140477455/2f5c79a3-15fb-4fdb-a22b-347376d34ef7">

</br>
</br>
</br>

Output 1:  User is asked to choose between 2 wine categories (i.e. Bold Red and Medium Red). It may happen that there is only 1 matching wine category. In that case, the user is not asked to choose.

<img width="873" alt="Screenshot 2024-01-10 at 14 11 16" src="https://github.com/FeierVasileAdrian/wine_App/assets/140477455/07c1f7e7-0e9c-4d70-9b89-ed5c43688931">

</br>

Output 2:  Based on the wine category and on the meal description given as input, the App suggest a wine grape.

<img width="992" alt="Screenshot 2024-01-10 at 14 11 53" src="https://github.com/FeierVasileAdrian/wine_App/assets/140477455/380a7a5d-c049-4429-93cd-36ffc65cfdb5">

</br>
</br>
</br>

Output 3: Based on wine grape, wine category and meal description given as input, the App suggests a wine and outputs several informations about that wine.
<img width="1000" alt="Screenshot 2024-01-10 at 14 12 02" src="https://github.com/FeierVasileAdrian/wine_App/assets/140477455/541dfe77-7196-45c0-81d2-1ce3597189de">

</br>
</br>

Output 4: User is asked to select one of the 3 options proposed by the App for the selection of wine bottle.

<img width="957" alt="Screenshot 2024-01-10 at 14 12 09" src="https://github.com/FeierVasileAdrian/wine_App/assets/140477455/673d951f-6f2b-45e5-abe6-5364960fa8af">

</br>
</br>
</br>

Output 5: Based on wine and on user selection, App suggest a wine bottle and output several informations about that bottle.

<img width="894" alt="Screenshot 2024-01-10 at 14 12 53" src="https://github.com/FeierVasileAdrian/wine_App/assets/140477455/bdb48d82-b07b-4228-a191-598fa0aa9a73">

</br>

Feel free to try it by yourself !

</br>


## 4. Further developments

As further development, it would be useful to link the model to a DB. Indeed, the main issue with such a model is hallucination.
The idea would be to improve the step 3 by feeding the model with a “wine category - wine grape - wine” DB and asking the model to select one wine based on that DB.
Using a large DB would decrease hallucination but also improve the diversity of the wine output at step 3.

</br>
</br>

## 5. License

Distributed under the MIT license.

</br>
</br>

## 6. Contact

Vasile Adrian Feier - adi.feier@hotmail.com - [LinkedIn profile](https://www.linkedin.com/in/vasile-adrian-feier-9907001b7/)

</br>
</br>

## 7. Acknowledgments

* [Choose a license](https://choosealicense.com/)
* [Choose a wine category based on ingredients](https://winefolly.com/tips/getting-started-with-food-and-wine-pairing/)
* [Choose a wine based on herbs and spices](https://winefolly.com/tips/herb-and-spice-pairings-with-wine/)
