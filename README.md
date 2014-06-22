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

###Step 2: Install the Package

###Step 3: Let 'er Rip

###Step 4: Do some cool analysis

###Step 5: Write [me an email](mailto@benjaminmgross@gmail.com) and tell me you love me

##To Do:

- Complete package installation so package can be installed
- Finish `README.md`
- Generate documentation with Sphynx

