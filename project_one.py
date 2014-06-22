#!/usr/bin/env python
# encoding: utf-8
"""
project_one.py

Created by Benjamin M. Gross 6.20.2014

from `Zillow`<http://www.zillow.com/howto/api/GetRegionChart.htm>

GetRegionChart API

The GetRegionChart API generates a URL for an image file that displays 
the historical Zestimates for a specific geographic region. The API 
accepts as input the name of the region as well as a chart type: either 
percentage or dollar value change. Optionally, the API accepts width 
and height parameters that constrain the size of the image. The 
historical data can be for the past 1 year, 5 years or 10 years.

General thought process:

Retrieve Region information from the `Get Region Children API`
_<http://www.zillow.com/howto/api/GetRegionChildren.htm>, and then, for 
each ofthose regions, get a region chart displaying historical data for 
the past 10 years

Also go to `Get Demographics API
_<http://www.zillow.com/howto/api/GetDemographics.htm>` and get certain 
demographic information about the area as well.

"""

import argparse
import pandas
import numpy
import requests
import yaml
import state_dict
import bs4
from collections import Counter

def demographics_from_id(regionid, zwsid):
    """
    Given a region id (which was extracted using the 
    :meth:`regional_data` or :meth:`aggregate_city_data` functions) and
    a Zillow OAthToken, return all of the demographic data for that 
    ``region-id``

    :ARGS:

        regionid: :class:`string` of the region id

        zwsid: :class:`string` of the Zillow OAthToken

    :RETURNS:

        :class:`pandas.Series` with all pertinent demographic 
        information for that regionid


    .. note:: findChildren parameter, attribute
    
        In the demographics API call, the 'attribute' tag is where 
        all of the pertinent data is housed, so that tag is used
        below for the :meth:`BeautifulSoup.findChildren()` below
    """
    def clean_val(tag):
        #Helper function for empty tags
        if tag == None:
            return None
        else:
            return tag.text

    params = {'zws-id':zwsid, 'regionid': regionid}
    url = 'http://www.zillow.com/webservice/GetDemographics.htm'
    socket = requests.get(url, params = params)
    soup = bs4.BeautifulSoup(socket.content)
    data = soup.findChild('attribute')
    d = {}
    for item in data:
        try:
            s = item.findChild('name').text
            d[s + ' neighborhood'] = clean_val(item.findChild('neighborhood'))
            d[s + ' city'] = clean_val(item.findChild('city'))
            d[s + ' nation'] = clean_val(item.findChild('nation'))
        except Exception:
            pass

    return pandas.Series(d, name = regionid)


def extract_tags(tag_list):
    """
    Take in a list of :class:`bs4.element.Tag` and returns the
    Union of the majority of tag.names as a dictionary to then
    iterate over

    :ARGS:
    
        tag_list: :class:`list` of `bs4.element.Tag`

    :RETURNS:
    
        key: :class:`string` the name of the tag that should be 
        used as the "key" (ie appears in all of the list values)

        tags: :class:`list` the remaining tags that should be used to
        to append to the dictionary
    """
    master = []
    agg = []
    for tag in tag_list:
        tmp = map(lambda x: x.name, tag.findChildren())
        agg.extend(tmp)
        if len(tmp) > len(master):
            master = tmp

    #get the occurrences and make sure 'id' is an approprate hash key
    counts = Counter(agg)
    max_val = max(counts.values())
    max_keys = [key if value == max_val else "" for key, value in counts.iteritems()]
    if 'id' not in max_keys:
        print "id was not an appropriate hash key"
        return
    else:
        return counts

def aggregate_city_data(n, zwsid):
    """
    Return joined dataframes from the 'n' biggest cities in the 
    United States
    
    :ARGS:
     
        n: :class:`int` of the number of cities you would like to 
        return aggregated data for
    
    :RETURNS:

        a :class:`pandas.DataFrame` with all of the neighborhoods,
        median housing prices, longitude & latitude, etc.
    """
    #DataFrame of the n largest cities
    n_df = largest_cities(n)
    df_list = []
    for ind in n_df.index:
        city, state = n_df.loc[ind, ['City', 'State']]
        params = {'zws-id':zwsid, 
                  'state': state_abreviation(state), 
                  'city':city}
        df_list.append(regional_data(params))
    
    region_df = pandas.concat(df_list, axis = 0)
    
    d = {}
    for regionid in region_df.index:
        d[regionid] = demographics_from_id(regionid, zwsid)
    
    import pdb
    pdb.set_trace()
    dg_df = pandas.DataFrame(d).transpose()
    return region_df.join(dg_df)

def regional_data(param_dict):
    """
    Calls the `GetRegionChildren API_
    <http://www.zillow.com/howto/api/GetRegionChildren.htm>`

    :ARGS:

        param_dict: :class:`dictionary` with the following parameters

             {'zws-id', 'state', 'city'}
    """
    param_dict['childtype'] = 'neighborhood'
    s = requests.get('http://www.zillow.com/webservice/GetRegionChildren.htm?',
                        params = param_dict)

    #now use BeautifulSoup to parse the xml
    soup = bs4.BeautifulSoup(s.content, ['lxml', 'xml'])
    
    #extract into a list of "regions"
    soup_list = soup.findChildren('region')
    tag_dict = extract_tags(soup_list)
    d = {}
    for line in soup_list:
        key = line.findChild('id').text
        vals = map(lambda x: x.text, line.findChildren())
        vals.extend([param_dict['city'] + ' ' + param_dict['state']])
        ind = map(lambda x: x.name, line.findChildren())
        ind.extend(['city-state'])
        d[key] = pandas.Series(vals, index = ind)
    return pandas.DataFrame(d).transpose()

def state_abreviation(state_name):
    """
    The state dictionary has pairings ('abreviatio', 'state'), this
    returs the abreviation for a given value
    """
    for key, value in state_dict.states.iteritems():
        if value == state_name:
            return key
    return "Unable to find that State"

def largest_cities(n = 15):
    """
    Access the wikipedia page `List of US Cities by Population_
    <http://en.wikipedia.org/wiki/List_of_United_States_cities_by_population>`
    and pull in the n largest into :class:`pandas.DataFrame`
    """
    url = 'http://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    table_list = pandas.read_html(url)

    #anonymous function to 'remove footnotes'
    rem_fn = lambda arr: map(lambda x: x.split('[')[0], arr)
    
    #by inspection, the 2nd table is the one we're after
    us_cities = table_list[1]
    
    #remove the 
    us_cities.columns = rem_fn(us_cities.iloc[0, :])
    us_cities = us_cities.iloc[1:, :]

    #format the population and City
    us_cities['2013 estimate'] = map(
        lambda x: float(x.split()[1].replace(',' , '')),
        us_cities['2013 estimate'])

    us_cities['City'] = rem_fn(us_cities['City'])
    
    cols = ['2013 rank', 'City', 'State', '2013 estimate']
    return us_cities.ix[:n, cols]

def config_dict(path):
    """
    Load your configuration file to do the API calls into a dictionary.
    The remainder of the functions assume a{'website':{'username': ,
    'OAthToken': }} pairing
    """
    f = open(path)
    return yaml.load(f)
        

def scipt_function(arg_1, arg_2):
	return None

if __name__ == '__main__':
	
	usage = sys.argv[0] + "usage instructions"
	description = "describe the function"
	parser = argparse.ArgumentParser(description = description, usage = usage)
	parser.add_argument('name_1', nargs = 1, type = str, help = 'describe input 1')
	parser.add_argument('name_2', nargs = '+', type = int, help = "describe input 2")

	args = parser.parse_args()
	
	script_function(input_1 = args.name_1[0], input_2 = args.name_2)
