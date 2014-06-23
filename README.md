#README.md

##Introduction

Zillow aggregates some very interesting data, especially if you're interested
aspects of home prices, demographics (like income, education, etc.) -- not to mention all of this information is provided with latitude and longitude coordinates to boot! This light-weight module gives you the ability to:

1. Take the 'n' largest cities in the US (data scraped from [Wikipedia](http://en.wikipedia.org/wiki/List_of_United_States_cities_by_population)
2. Go to Zillow's API, & extract ``regionid``'s (of which there are several hundred for any metropolitan city) along with some interesting Zillow Index Data
3. Join that data with demographic data, such as median house prices, cost per square foot, median income, etc. **all** provided at a "neighborhood", "city", & "state" level.
4. Put it all into Jesus' favorite data structure... [pandas](http://pandas.pydata.org), to do some serious data analysis

##Dependencies:

- [Requests](http://docs.python-requests.org/en/latest/): Leveraged heavily to hit the Zillow API, as well as pass arguments to API
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/): Specifically `bs4`, for parsing the horrific, sadder-than-baby-tears expunged from the Zillow API
- [PyYaml](http://pyyaml.org/): For parsing configuration files, but it'd be easy to make a few tweaks and not need this library at all


##Installation:

    $ git clone https://github.com/benjaminmgross/api-scrapin
	$ cd api-scrapin
	$ python setup.py install

I know what you're thinking, "why can't I `pip install` it?" Stop whining! ... fine, I haven't figured out how to do that yet with packages, but I'm working on it...

##Up and Running in 5 Steps

###Step 1: Get Yourself a Zillow API Token

1. Go to [Zillow's Registration Page](https://www.zillow.com/webservice/Registration.htm) where you will be prompted to create a login.
2. After you create a login, go to the [Zillow API Overview Page](http://www.zillow.com/howto/api/APIOverview.htm)
3. Click on the [get a ZWSID](http://www.zillow.com/webservice/Registration.htm)
4. Fill out the information, click all of the check boxes of different APIs you might wannt, and then get ready to receive your Zillow API key in your inbox! 

###Step 2: Install the Package

Standard...

###Step 3: Let 'er Rip

The crux of what makes this package special is the ability to merge, what's called "region-id" and cities.  For instance, you probably don't know that there are 267 `region-id`'s around the New York City area.  However, by simply typing "New York, NY" into the "Regional API", you get back all of the different `region-id`'s.  You can then **use that regional-id** as a parameter for your query, and then get back even cooler stuff like, median household income, price per square foot... even average level of education. 

###Step 4: Do some cool analysis

You got this one covered

###Step 5: Write [me an email](mailto@benjaminmgross@gmail.com) and tell me you love me

##To Do:

- Complete package installation so package can be installed
- Finish `README.md`
- Generate documentation with Sphynx

