# KC House Rocket - Data Insights
<p align="center">

The business issues and the House Rocket company representing in this project are fictitious.

The application with the visualizations of the results, is here [here](https://analytics-house-rocket-dino.herokuapp.com/)


## 1. **Project description and business issues**

House Rocket is an American digital platform whose business model is the purchase and sale of real estate using technology. Their main strategy is to buy good homes in great locations at low prices and then resell them.
later at higher prices. The greater the difference between buying and selling, the greater the company's profit and therefore the greater its revenue.

However, homes have many attributes that make them more or less attractive to buyers and sellers, and location and time of year can also influence prices.

Based on this context, two business questions were created:

1. Which houses should the House Rocket CEO buy and at what purchase price?
2. Once the house is in the company's possession, when is the best time to sell it and what would the sale price be?
    

## 2. **Business Assumptions**
    
To more accurately determine the answers to business questions after data analysis, it was necessary to perform:
    
- Duplicate IDs have been removed, probably caused by human error.
- It was also observed that the property found in line '15870', has 33 bathrooms, was considered a human typing error and deleted from the dataset.
- Property condition and price were the main considerations in determining whether a property was considered good or bad for purchase.
- The season of the year was defined as a period reference, for sale or not. 


## 3. **Data Dictionary**

Some columns are described as:

- id - unique id
- date - date of sale
- price - Sale price
- rooms - Number of rooms
- Bathrooms - Number of bathrooms, where 0.5 represents a suite.
- sqft_living - Indoor area
- sqft_lot - Square meter of the property
- floors - Number of floors
- waterfront - Whether the property has a sea view or not
- view - Quality of view
- condition - Condition of the apartment,
- grade - Level of construction and quality design.
- sqft_above - Area above ground level
- sqft_basement - Basement area
- yr_built - Year of construction
- yr_renovated - Year of last renovation
- CEP - CEP
- lat - Latitude
- long - longitude
- sqft_living15 - The square footage of the interior living space for the 15 closest neighbors
- sqft_lot15 - The square footage of the 15 nearest neighbors' lots


## 4. **Solution Strategy**

**Step 01.** Determining the business problem

**Step 02.** Load and Inspect the Data

**Step 03.** Clean and Transform the Data 

**Step 04.** Exploratory Data Analysis

**Step 05.** Business Hypothesis Testing 

**Step 06.** Answering the Business Questions 

**Step 07.** App creation 

**Step 08.**  Conclusion and Understanting the Business results

## 5. **Top  10 Insights**

**Hypothesis 1 - Properties that overlook the water are 30% more expensive in the media.**
False. Because properties overlooking the water are 3x more valued than properties without water views. Evidencing that the purchase of properties overlooking the water is profitable

**Hypothesis 2 - Properties with a construction date less than 1955 are 50% cheaper, on average.**
False. Little changes the values ​​of properties that were built before and after 1955

**# Hypothesis 3 - Properties without a basement have a total area of ​​40% larger than properties with a basement**
False. Properties without a basement have a larger area than properties with a basement, but 20% on average

**Hypothesis 4 - YoY property price growth is 10%**
False. From 2014 to 2015, there was a drop in property prices

**Hypothesis 5 - Properties with 3M bathrooms have a Mo price growth of 15%**
False. The graph varies with growths and decays. The months of January, February and November are good months to buy properties with 3 bathrooms and the months of April, May and June are the best for sale.

**Hypothesis 6 - Properties with good conditions (3 or more), are 30% more expensive, on average**
False. Houses in good condition are 62% more expensive. It is profitable to buy houses in dilapidated condition and sell in good condition.

**Hypothesis 7 - Properties that have had at least one renovation are 40% more expensive, on average.**
true. Homes that have already been renovated at least once, have a 40% increase, reaffirming that the business of buying/renovating/selling is profitable

**Hypothesis 8 - Houses with a basement are 30% more expensive than houses without a basement, on average.**
Real. Houses that have a basement are 30% more expensive, invest in a house with a basement below average prices
 
**Hypothesis 9 - Houses with good views are 30% more expensive than houses that do not have them, on average.**
False. Houses with good views are almost double (91%) the price of houses with bad views, investing in houses with good views, below average, are profitable

**Hypothesis 10 - Properties with 3 bedrooms or more are 40% more expensive than properties with less, on average.**
Truth. Investing in houses with more bedrooms and that are below average is profitable


## 6. **Business Results**

After the analysis, 10,435 properties were selected as suitable for purchase.

These properties were in good condition and below the median price.

If all 10,435 homes were purchased, the transaction cost would be $4.053.331.057,00.

For this case, the total profit returned if all properties were sold would be $748.496.293,90.

Considering that a 30% profit margin was considered for properties with a price below the median per season and a margin of 10% for properties with a price greater than the median per season. 

## 7. **Conclusions**
The main objective of this project was to answer two business questions:
1. Which homes should the company buy and at what price?
2. Once purchased, when should these homes be sold and at what profit margin?

In addition to generating sales insights for possible improvements.

To achieve this objective, the dataset was cleaned, analyzed and some hypotheses were tested. To determine the best real estate opportunities, data was pooled based on location, housing condition and whether the price was below average.

These characteristics were determined based on previous analyses, in which it was observed that location plays one of the most important roles in real estate pricing. In addition, for all these situations, the housing condition, especially in the lower classes, had a significant effect on prices, significantly reducing them.

After grouping the houses in the dataset based on these conditions, the average price was calculated and if a house cost less than this average and was in good condition, that house would be classified as suitable for purchase. After separating all suitable houses, the profit was calculated.

This calculation was made by grouping the good real estate opportunities based on all previous characteristics and seasons. Average prices were calculated and if the purchase price was above this median, a 10% profit margin would be added, otherwise the profit margin would be 30%.

At the end of this analysis, the resulting dataset contained 10,435 houses, their characteristics, the purchase and sale prices and the profit margin of each. 

## 8. **Next Steps**

This project was made following the concept of minimum viable product (MVP). The analysis done here is very simple, but it gives a good start to a similar business problem. The next steps would be to improve this analysis by applying more sophisticated methods.

First, the statistical analysis could be done in the business hypothesis test, to verify if the results found were really significant. Then more feature engineering can be done and a machine learning model can be built to determine the best opportunities, times and price to sell these homes.

Machine learning algorithm implementation can start with simple regression models and evolve to use random forest or more complex models.

And also, the use of the CRIPS-DS method, to return more times in the project and bring improvements in the determination of the best properties.
