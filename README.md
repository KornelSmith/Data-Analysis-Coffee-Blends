# Data-Analysis-Coffee-Blends

This project is an analysis of data on coffee blends' quality and price.

The Tableau dashboard can be accessed here: https://public.tableau.com/views/CoffeeBlends/Dashboard1?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

Data source: https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview/versions/2

## Table of Content
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Data Insights](#data-insights)
- [Data Cleansing](#data-cleansing)
- [Analysis](#analysis)  

## Overview

In this project I aimed to give insight into the relationship between quality, price, origin, and roast of different coffee blends. This is one of my first data analytics projects so it also serves as practice. Just kidding, I'm just justifying my caffeine consumption as research.

The data source is not mine. I found it on kaggle.com, and it's originally from coffeereview.com. For my purposes, I was only interested in a few characteristics of coffee blends:
- rating: a number associated with the quality of the coffee, according to a system described by coffeereview.com
- price
- origin: where the coffee was grown
- roast: to what level the particular blend is roasted

If you want to read up on the rating system, visit this page: https://www.coffeereview.com/interpret-coffee/

## Technologies used
- Python Pandas
- Tableau Public

## Data Insights

<img width="1281" alt="Screenshot 2024-11-20 at 19 01 24" src="https://github.com/user-attachments/assets/b25cc616-37af-4006-997a-4d98dd68f90d">

This map shows the countries where the blends in the data were grown. Most of these countries lie in the coffee belt, that is between the Tropic of Cancer and Tropic of Capricorn, but there are a few exceptions.

The darker the colour on the map, the higher the average quality is of blends that come from that region. The highest ratings came from Argentina, but coffees from Panama, Ecuador and East African countries also perform strongly.

<img width="1176" alt="Screenshot 2024-11-20 at 20 52 57" src="https://github.com/user-attachments/assets/561b3893-c29a-4e5b-9337-4f0426c99af6">

If we plot the average quality against the average price per region, we see that most coffees in the data are concentrated at 5-10 USD / 100g and a rating of 92-94. This rating actually corresponds to the mean and median rating for the whole dataset (93). The circle size shows the number of samples taken from the corresponding country. While an increasing trend can be identified here, this is only due to the fact that the data has been aggregated by countries. The R^2 correlation is only 0.14 between price and quality.

<img width="592" alt="Screenshot 2024-11-20 at 21 00 50" src="https://github.com/user-attachments/assets/080c89b5-5871-411b-9dce-e6d9bad6faf4">

To get a better feel of the rating, this histogram shows the ratings for the entire dataset. 30% of the data has rating 93, which brings this to be both the mean and the median of the data.

<img width="1154" alt="Screenshot 2024-11-20 at 21 03 54" src="https://github.com/user-attachments/assets/b09ad286-972e-423e-8b9c-ae03daf17886">

These charts show the average quality, and average price, per roast. Darker roasts seem to have been rated as of inferior quality, which is consistent with general oppinion in coffee  communities. If beans are roasted too dark, the roasting process creates chemicals that overpower the natural flavours of the bean, which is not desirable for high-end coffee. Consqeuenty, light to medium-light roasts also have a higher price. Medium-dark roast is the most popular in Italy and France, which can explain the higher unit price for this roast.

## Data Cleansing

After visually inspecting the data, I decided that the following things had to be fixed:
- the location column showed too much geographical detail, I wanted to keep only the country information
- the origin column had the same problem, but also sometimes showing multiple origin countriess
- the price column gave the price in the local currency of the location column, and in varying units of measurement

The cleansing.py file contains the class that handles this data cleansing.

### Fixing the location column

shfeu
