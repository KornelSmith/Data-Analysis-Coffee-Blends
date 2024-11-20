

from Cleansing import CoffeeBlendsDataCleansing
from descriptive import CoffeeBlendsDescriptiveAnalysis

# Step 1: Clean the data
data_cleansing = CoffeeBlendsDataCleansing('combined_coffee_data.csv')
data_cleansing.load_data()  
data_cleansing.assign_country()
data_cleansing.clean_origin()
data_cleansing.convert_price()
data_cleansing.df.to_csv('output.csv', index = False)

# Step 2: Perform descriptive analysis on the cleaned data
data_analysis = CoffeeBlendsDescriptiveAnalysis('output.csv')
data_analysis.load_data()  
data_analysis.rating_per_price()
data_analysis.rating_price_per_roast()
data_analysis.ratings_distribution()