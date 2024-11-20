# Data-Analysis-Coffee-Blends

This project is an analysis of data on coffee blends' quality and price.

The Tableau dashboard can be accessed here: https://public.tableau.com/views/CoffeeBlends/Dashboard1?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

Data source: https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview/versions/2

## Table of Content
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Conclusions](#conclusions)
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

## Conclusions

<img width="1281" alt="Screenshot 2024-11-20 at 19 01 24" src="https://github.com/user-attachments/assets/b25cc616-37af-4006-997a-4d98dd68f90d">

This map shows the countries where the blends in the data were grown. Most of these countries lie in the coffee belt, that is between the Tropic of Cancer and Tropic of Capricorn, but there are a few exceptions.

The darker the colour on the map, the higher the average quality is of blends that come from that region. The highest ratings came from Argentina, but coffees from Panama, Ecuador and East African countries also perform strongly.

<img width="1288" alt="Screenshot 2024-11-20 at 19 08 06" src="https://github.com/user-attachments/assets/77d3d017-fd6c-453d-960b-89181bbcb927">

If we plot the average quality against the average price per region, we see that most coffees in the data are concentrated at 5-10 USD / 100g and a rating of 92-94. This 
