#!/usr/bin/python
# -*- coding: utf-8 -*-

### gln/data/cultural_production/generate_cultural_exports.py

"""
Convert per-country data to per-language data (e.g., GDP, cultural exports, etc.)
Usage: python convert_country_data_to_lang infile outfiley

Uses the conversion table in ../lang_tools/country_to_lang/,
which lists for each country (2-letter code) its languages (by 3-letter code)
their shares
"""

import os
import sys
import simplejson
import codecs
from collections import Counter
import operator # for dict sorting
# sys.path.append('../lang_tools/country_to_lang')

# 
COUNTRY_TO_LANGS_CONVERSION_FILE = "country_to_lang_mapping.json"
COUNTRY_TO_LANGS = \
    simplejson.load(open(COUNTRY_TO_LANGS_CONVERSION_FILE, "rU"))


COUNTRY_INPUT_PATH = "../../cultural_production/wikipedia/wiki_observ_langs26_{0}_country_exports.tsv".format("1800_1950")
LANG_OUTPUT_PATH = "../../cultural_production/wikipedia/wiki_observ_langs26_{0}_language_exports.tsv".format("1800_1950")

FILTER_CODE = 99999 # Use this number as start year and end year to avoid year filtering


def convert_country_data(country_data):
    'Converting country data to language data'
    language_data = dict()

    for country_name, country_value in country_data.iteritems():
        #for country_code, vals in COUNTRY_TO_LANGS.iteritems():
            langs_proportions = COUNTRY_TO_LANGS[country_name]['langs']
            print country_name, country_value, langs_proportions
            for lang, proportion in langs_proportions.iteritems():
                if lang in language_data:
                    language_data[lang] += (proportion / 100.) * country_value
                else:
                    language_data[lang] = (proportion / 100.) * country_value        
                print "{0}-->{1}: {2}-->{3}".format(country_name, lang, country_value,language_data[lang])
            print
    return language_data



def write_lang_exports_table(infile, outfile):
    country_data = Counter()
    
    input_dataset = codecs.open(infile, "rU")
    input_dataset.readline() # skip header

    # Aggregating country exports for legit years
    for line in input_dataset:
        country_name, total_exports = line.strip().split('\t')
        print country_name, total_exports
        country_data[country_name] = float(total_exports)

    print "Total people:", sum(country_data.values())


    # Convert
    language_data = convert_country_data(country_data)
    
    # Sort dictionary by values: returns a list of tuples
    language_data_sorted = sorted(language_data.iteritems(), 
        key=operator.itemgetter(1),
        reverse=True)
    
    # Write sorted table
    output_dataset = codecs.open(outfile, "w")
    output_dataset.write("lagnuage\tvals\n")

    for lang, total_exports in language_data_sorted:
        output_dataset.write('{0}\t{1}\n'.format(lang, total_exports))
    output_dataset.close()


if __name__ == '__main__':
    # Convert countries to languages:
    write_lang_exports_table(COUNTRY_INPUT_PATH, LANG_OUTPUT_PATH)