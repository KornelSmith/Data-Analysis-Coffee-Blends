# this class was designed based on visual inspection of the raw data and was later adjusted to bring
# the output to the desirable shape

import pandas as pd
import string
import re
from word2number import w2n
from accessories import conversion_rates, us_states, all_countries

class CoffeeBlendsDataCleansing:
    def __init__(self, file_path):
        # initialise the class

        self.file_path = file_path
        self.df =  None

    def load_data(self):
        # loads a .csv file into a dataframe

        try:
            self.df = pd.read_csv(self.file_path)
            print("Data loaded successfully")
        except FileNotFoundError:
            print("Error: the file does not exist.")

    def assign_country(self):
        # this function extracts the country from the 'location' column and puts this in a new column

        def get_country(location):

            if isinstance(location, str): # checks if the entry in the location column is a string
                location_parts = location.split(',') # splits each entry by commas

                if "Hong Kong" in location_parts: # by visual inspection of the data, Hong Kong has to be treated separately
                    return "Hong Kong"
                
                last_part = location_parts[-1].strip() # takes the last part of each entry, which is either a US state, or a country name

                if last_part in us_states:
                    return "United States" # return US if the last part is a US state
                else:
                    return last_part # if the last part is not a US state, return the last part, which will be a country
            else:
                    return "Unknown"
            

        self.df['country'] = self.df['location'].apply(get_country) # apply the get_country function to the 'location' column and create a new column for country
        self.df.drop('location', axis = 1, inplace = True) # remove the 'location' column
        print("Countries successfully added")

    def clean_origin(self):
        # the origin column contains multiple origin countries per blend, separated by commas or semicolons
        # this function separates the origin countries into separate columns, while also keeping only the country information

        self.df['origin'] = self.df['origin'].apply(lambda x: re.sub(r'[,]', ';', str(x)))  # Replace commas with semicolons

        max_countries = self.df['origin'].apply(lambda x: str(x).count(';')).max() + 1
        # find the maximum number of countries in a cell by counting the semicolons
        # we will create as many new columns - if there are max 5 countries in a cell, we need columns origin1 to origin5

        for i in range(max_countries):
            column_name = f'origin{i + 1}' #create new column name

            # here each cell entry in the origin column is split at semicolons
            # then the extract_country function is called to validate each of these splits as countries
            # then we return the ith content of the string if it exists, as a country, otherwise we return None

            self.df[column_name] = self.df['origin'].apply(lambda x: self.extract_country(str(x).split(';')[i].strip()) if len(str(x).split(';')) > i else None)       

        self.df.drop('origin', axis = 1, inplace = True) # removing the origin column
        print("Origin countries cleaned")

    def extract_country(self, text):
        
        # checks if text contains a valid country
        # this operates on the string pieces that are a result of splitting up the origin column entries at semicolons

        text = text.translate(str.maketrans("", "", string.punctuation)).lower() # remove punctuation and normalise text
        text = text.strip()

        # some country names contain words that are themselves country names, for example:
        # Dominica vs Dominican Republic, or Congo vs Democratic Republic of the Congo
        # to deal with this, first we sort the list of countries and states based on name length in descending order, to first pick up the longer match

        sorted_countries = sorted(all_countries + us_states, key = lambda x: -len(x)) # sort the list of countries and states based on name length in descending order
        countries = []

        # Check for matching country names
        for country in sorted_countries:
            country_lower = country.lower() # set to lower cases

            # ensure country is a whole word match (use word boundaries like spaces or start/end of text)

            if f" {country_lower} " in f" {text} " or text.startswith(country_lower) or text.endswith(country_lower):
                countries.append(country)

            # remove matched country from the text to prevent re-matching shorter country names

            text = re.sub(rf"\b{re.escape(country_lower)}\b", "", text, flags = re.IGNORECASE).strip()

        return ", ".join(countries) if countries else None

    def convert_price(self):

        # in the dataset, the price of each blend is given in a local currency per some unit of measurement
        # the most common units of measurement are grams and ounces
        # this function standardises the price to be in USD per 100g for all blends

        prices = []
        amounts = []
        units = []

        # this is done by iterating through the rows of the dataframe

        for idx, row in self.df.iterrows():

            # extract information from the data
            est_price = row['est_price']
            country = row['country']

            # if the price is null:
            if pd.isnull(est_price):
                prices.append(None)
                amounts.append(None)
                units.append(None)
                continue
        
            # the est_price column contains information as price per quantity
            # split price and quantity
            parts = str(est_price).split('/')

            # if this is not in the expected format, it is discarded

            if len(parts) != 2:
                prices.append(None)
                amounts.append(None)
                units.append(None)
                continue

            price_part = parts[0].strip()
            quantity_part = parts[1].strip()

            # extract unit of measurement
            units_match = re.findall(r'gram|grams|ounce|ounces', quantity_part.lower())
            # if found, keep it
            if units_match:
                unit = units_match[0]
                units.append(unit)
            
            # if not found, discard (a few entries have price given per capsule, but this is not significant)
            else:
                prices.append(None)
                amounts.append(None)
                units.append(None)
                continue

            # Ccean quantity part
            quantity_part = quantity_part.replace("-", " ")
            text = quantity_part.split()

            # the quantity can be given in the following formats:
            # 2 ounce
            # 3 5 gram packets
            # six 10 gram bags
            # the quantity is extracted to accommodate these formats
            try:
                num1 = float(text[0]) # try to take the first part of the string as float
            except ValueError:
                try:
                    num1 = w2n.word_to_num(text[0]) # if  that doesn't work, it's likely a word that means a number, so try that
                except ValueError:
                    num1 = None

            try:
                num2 = float(text[1])  # then take the second part of the text as float
            except ValueError:
                num2 = 1 # if that doesn't work, then there is no second number, so we set it to 1

            if unit == "ounce":
                num3 = 28.3495 # if the unit was ounce, we need to convert to grams
            else:
                num3 = 1

            if num1 is not None:
                amount = num1 * num2 * num3 # we multiply the numbers together to get the total quantity in grams
                amounts.append(amount)
            else:
                amounts.append(None)

            # extract price
            price_match = re.search(r'\d+(\.\d+)?', price_part) # from the price part, take a string section that matches this format
            price = float(price_match.group(0)) if price_match else None # save it as float

            if price is not None:
                price = 100 * price / amount # whatever the currency, we first convert the price to reflect 100g

                # based on the country information of the blend (which is where the blend was purchased) fetch the conversion rate (tabulated in Nov 2024)

                conversion_rate = conversion_rates.get(country, None) 
                if conversion_rate is not None:
                    price = price / conversion_rate # convert to US dollars
                    
                price = round(price, 2)

            prices.append(price)              

        # assign results back to dataframe
        self.df['price_per_100g'] = prices

