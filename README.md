# IMDB database - Search for top rated movies!

# running imdb_top_1000:

Assumes a working Python 3 installation (with python=python3 and pip=pip3).

(1) Run the code below to install the dependencies.
>$ pip install -r requirements.txt

(2) Initialize the database, by running the SQL files (Creating the necessary tables) 
IMPORTANT: In the 'Create Attributes.SQL' change the directory to the full path of the 'modified_imdb_top_1000.csv' file. 

(3) In the app.py-file, set your own database username and password

(4) Run Web-App
>$ python src/app.py


----------------------------------------------------------------------------------------------

# How to use the application:

(1) Create account / You start by pressing the 'Create Account' button, you then get to page where you choose your username and password.

(2) Login / Now you can login on your account by typing in your username and password.

(3) Frontpage / On the frontpage you will see 8 random movies and some different filter options.

(4) Searching / You can search for movies by searching for the name of the movie. A regular expression is utilised to help you find movies with your input in their titles.
		You can combine this with your desired genre, director or rating. Genre and director will match your input as best as possible and rating will give you anything above the input.
		
(5) User page / Each user have their own individual page where they can see their favourite punks.

(6) Contact / At last we have a 'contact' page so you have an option to contact the three founders and thank them for their awesome work!


