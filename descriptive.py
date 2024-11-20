# this class creates the .csv files that are used for visulations in Tableau

import pandas as pd
import matplotlib.pyplot as plt

class CoffeeBlendsDescriptiveAnalysis:
    def __init__(self, file_path):
        # initialise the class

        self.file_path = file_path
        self.df =  None

    def load_data(self):
    # loads .csv data into a dataframe

        try:
            self.df = pd.read_csv(self.file_path)
            print("Data loaded successfully")
        except FileNotFoundError:
            print("Error: the file does not exist.")
        
    def rating_per_price(self, output_file = 'rating_per_price.csv'):

        # this function calculates the average rating and price per blend origin
        # combine all origin columns into a single column

        origin_columns = ['origin1', 'origin2', 'origin3', 'origin4', 'origin5', 'origin6']
        melted = self.df.melt(['rating', 'price_per_100g'], origin_columns, None, 'Origin')
        melted = melted.dropna(subset = ['Origin'])

        # calculate the average rating and price for each origin country

        average = (melted.groupby('Origin')[['rating', 'price_per_100g']].mean().reset_index())

        # count the number of occurance of each origin country to get a sample size for each

        average['num_samples'] = melted.groupby('Origin').size().values

        average[['rating', 'price_per_100g']] = average[['rating', 'price_per_100g']].round(2)
        average.to_csv(output_file, index = False)

    def rating_price_per_roast(self, output_file = 'rating_price_per_roast.csv'):

        # this function calculates the average rating and price per roast level

        output = self.df.groupby('roast').agg(
        price_per_100g = ('price_per_100g', 'mean'),
        rating = ('rating', 'mean'),
        num_samples = ('roast', 'size')  # add count of samples for each group
        ).reset_index()

        output[['price_per_100g', 'rating']] = output[['price_per_100g', 'rating']].round(2)

        output.to_csv(output_file, index = False)

    def ratings_distribution(self, output_file = 'ratings_distribution.csv'):

        # this function converts the origin columns into one, and lists the rating for each blend (but doesn't aggregate)

        origin_columns = ['origin1', 'origin2', 'origin3', 'origin4', 'origin5', 'origin6']
        melted = self.df.melt(['rating', 'price_per_100g'], origin_columns, None, 'origin')
        melted = melted.dropna(subset = ['origin'])

        melted.to_csv(output_file, index = False)