#!/usr/bin/env python
# encoding: utf-8
"""
project_one.py

Created by Benjamin M. Gross 6.20.2014

from `Zillow`<http://www.zillow.com/howto/api/GetRegionChart.htm>

GetRegionChart API

The GetRegionChart API generates a URL for an image file that displays the historical Zestimates for a specific geographic region. The API accepts as input the name of the region as well as a chart type: either percentage or dollar value change. Optionally, the API accepts width and height parameters that constrain the size of the image. The historical data can be for the past 1 year, 5 years or 10 years.

General thought process:

Retrieve Region information from the `Get Region Children API`_<http://www.zillow.com/howto/api/GetRegionChildren.htm>, and then, for each of
those regions, get a region chart displaying historical data for the past 10 years

Also go to `Get Demographics API_<http://www.zillow.com/howto/api/GetDemographics.htm>` and get certain demographic information about the area as well.

"""

import argparse
import pandas
import numpy
import requests
import yaml


def config_dict(path):
    """
    Load your configuration file to do the API calls into a dictionary.  The
    remainder of the functions assume a{'website':{'username': , 'OAthToken'}}
    pairing
    """
    f = open(path)
    return yaml.load(f)

def get_regions(states = None):
    if states:
        

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
