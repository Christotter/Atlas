import datetime
from urllib import request
import flask
import re
app = flask.Flask("PROJECT")

# ---- Methods
# Reseting country list to delete all countries created by this specific user
def delete_c_list():
    # Declaring the c_list variable globally so it's effectively updated outside of the function
    global c_list

    # Iterate trough the countries list and delete all the ones created by this specific user
    for i, o in enumerate(c_list):
        if str(o.username).lower() == username.lower():
            # Delete in the country list
            del c_list[i]
            # Delete in the Class
            del o
    # Return below was not necessary
    # return c_list

# Create or open a text file and store the total number of countries in it
def write_stat():
    # Reset variable storing the total of countries
    total = 0

    # Count all the default countries and the ones created by this specific user
    for obj in c_list:
        if str(obj.username).lower() == username.lower() or str(obj.username).lower() == "default":
            total += 1
    stat = str(total)
    file = open("stat.txt", "a")
    file.seek(0)
    file.truncate()
    file.write("Total number of countries in your Atlas : " + stat + "\n")
    file.close()

# Get the html page OR the total number of countries from the text file and return it to a variable
def get(request):
    requested_file = open(request)
    content = requested_file.read()
    requested_file.close()
    return content

# ---- End of methods

# ---- Class definition
class Country:

    # Initialize the class
    def __init__(self, cname, continent, capital, population, size, username):
        self.cname = cname
        self.continent = continent
        self.capital = capital
        self.population = population
        self.size = size
        self.username = username

    # Method to display a specific country and modify it
    def country_display(country, request):

        # html_page = get("country.html")

        # Select the original version of the modified country and delete it from the country list
        # (the modified country with new details will be later added to the list)
        for i, o in enumerate(c_list):
            if o.cname == country.cname:
                del c_list[i]
                break

        # Return the Country html page with original data for the chosen country
        return request.replace("$$cname$$", country.cname).replace("$$continent$$", country.continent).replace("$$capital$$", country.capital).replace("$$population$$", country.population).replace("$$size$$", country.size)

    # Method to display all the countries
    def all_countries_display(c_list, request, stat):

        # Display all the countries and the total number of countries in the html page
        actual_values = ""
        # Only select the default countries and the ones created by the active user
        for obj in c_list:
            if str(obj.username).lower() == username.lower() or str(obj.username).lower() == "default":
                actual_values += "<p>Country name : " + obj.cname + "<br>Continent : " + obj.continent + "<br>Capital : " + obj.capital + "<br>Population : " + obj.population + "<br>Size (km2) : " + obj.size + "<br>" + "-----------"

        return request.replace("$$allcountries$$", actual_values).replace("$$stat$$", stat)
# ---- End of Class Country

# Creating an empty username variable
# username = ""

# Creating empty country list array (used to display all countries)
c_list = []

# Creating pre defined default countries objects - Feel free to add more
switzerland = Country("Switzerland", "Europe", "Bern", "8,717,105", "41,285", "default")
china = Country("China", "Asia", "Beijing", "1,411,778,724", "9,596,961", "default")

# Appending objects to list
c_list.append(switzerland)
c_list.append(china)


# ---- Routes part
# Login page
@app.route("/",methods=['GET','POST'])
def home():
    return get("index.html")

# Homepage
@app.route("/welcome", methods=['POST', 'GET'])
def welcome():
    global username
    # Get the current username (important for new countries ownership)

    # Necessary when returning on the welcome page from another page
    # If not done it execute username = flask.request.form.get("username")
    # and crash because Nonetype is returned and failed can't pass the next if
    if flask.request.form.get("username") != None:
        username = flask.request.form.get("username")

    if re.match('^[a-zA-Z]+$', username):
        html_page = get("welcome.html")

        # Return the current local time on the page
        now = datetime.datetime.now()
        actual_time = now.strftime("%d-%m-%Y - %H:%M:%S")
        return html_page.replace("$$TIME$$", actual_time)
    else:
        return get("index.html")

# Add Country page
@app.route("/add_country")
def add_country():
    return get("add_country.html")

# Delete account page
@app.route("/deleted_account")
def deleted_account():
    delete_c_list()
    return get("deleted_account.html")

# Adding country page
@app.route("/adding_country",methods=['GET','POST'])
def adding_country():

    # To get the country data enter by the user in the form
    cname = flask.request.form.get("cname")
    continent = flask.request.form.get("continent")
    capital = flask.request.form.get("capital")
    population = flask.request.form.get("population")
    size = flask.request.form.get("size")

    global username

    # Create a new Country instance with the data entered by the user, store it in a variable
    new_country = Country(str(cname), str(continent), str(capital), str(population), str(size), str(username))

    # Add the new country to the countries list
    c_list.append(new_country)

    return get("adding_country.html")

# All countries page
@app.route("/all_countries")
def all_countries():

    request = get("all_countries.html")

    # Create or open a text file and store the total number of countries in it
    write_stat()
    # Get the the total number of countries from the text file and return it to a variable
    stat = get("stat.txt")
    #Call the all_countries_display method with country list in parameter
    return Country.all_countries_display(c_list, request, stat)

# Modifing country page
@app.route("/country",methods=['GET','POST'])
def country():
    html_page = get("modify_country.html")

    # Get the data entered by the user (name of the country to be modified)
    choice = flask.request.form.get("mc")

    country = []
    # Go trough countries list
    for i, o in enumerate(c_list):
        # Set the country entered by the user and all the existing
        # countries names to lowercase and check if there is a match
        # Also check if the country has been created by this specific user
        if str(o.cname).lower() == choice.lower() and str(o.username).lower() == username.lower():
            # If there is a match store the data in an array
            country = c_list[i]
            break

    # If no corresponding country has be returned in the previous test return an error
    if country == []:
        return html_page.replace("Enter the name of the country you want to modify:", "Please enter a valid country name (only one of those you created):")

    request = get("country.html")
    # If the previous test has been passed, call the class method
    # to display the chosen country with its original data
    return Country.country_display(country, request)

# Modify country page
@app.route("/modify_country",methods=['GET','POST'])
def modify_country():

    # To get the country data enter by the user in the form
    cname = flask.request.form.get("cname")
    continent = flask.request.form.get("continent")
    capital = flask.request.form.get("capital")
    population = flask.request.form.get("population")
    size = flask.request.form.get("size")

    global username

    # Necessary because otherwise a "None" country is created along with the modification
    # of the current country. This "None" country will later displayed in the Display all countries list
    # If the data entered by the user is valid it creates a Country instance and add it to the countries list
    if cname is not None:
        new_country = Country(str(cname), str(continent), str(capital), str(population), str(size), str(username))
        c_list.append(new_country)
    return get("modify_country.html")
# ---- End of routes part
