# SOEN-691-PROJECT BIG DATA ANALYTICS PROJECT

## Team Composition

| Name  | Student id |
| --- | --- |
| 40087977 | Sai Krishna |
| 40083289 | Dhaval Modi |
| 40082236 | Manushree Mallaraju |

## Project Type
Dataset Analysis

## Abstract
We have always been fascinated by the variety of restaurants in Bangalore. And each restaurant offers unique signature dishes. Currently there has been more than 12000 registered restaurants. And many more entrepreneurs are standing just around the corner to fill the night with more bars and restaurants. Keeping the new entrepreneurs in mind, with the available data (Zomato website data), we want to analyze which factor can be added to the success or failure of the newly opened restaurant. Some of the factors from the data includes theme, menus, cuisine, cost etc for a particular location. Our main goal is to analyze the existing data, convert them into graphs for simplification so that it can help new entrepreneurs to decide how, when and where they should open the restaurant to hit the success on first attempt.

## I. Introduction
### Context

The basic idea of analysing the Zomato dataset is to get a fair idea of the factors affecting the establishment of different types of restaurants in different places in Bengaluru. The market has not yet been saturated with the opening of new restaurants every day and the demand is increasing day by day. Nevertheless, it has become difficult for new restaurants to compete with existing restaurants despite increasing competition.

### Objectives

The objectives is to answer questions regarding the restaurants based on the different chosen parameters. 
The other objective is to help the new enterauprenaurs help deciding different paramteers to consider before opening the new restaurants and also to determine the probability of the success of the restaurants.
Recommend the restaurantbased on user's needs.
We will also try to find if there is a relation between restaurant type,location and the cost?

### Presentation of the problem to solve

Problem : For the new enterprenaurs, it's very essential to get success in the first shot due to high realty cost. 
They are also confused about locality, cuisine, rates and many more things.

Solution: First we will analyse the exisitng data, transform the data into graphs for better representation. 
On top of that we will generate a recommender system based on that.  

### Related work 

There are many data analysis papers on this datataset. <br />
https://www.kaggle.com/shahules/zomato-complete-eda-and-lstm-model <br />
https://www.kaggle.com/parthsharma5795/finding-the-best-restaurants-in-bangalore <br />
https://www.kaggle.com/chirag9073/zomato-restaurants-analysis-and-prediction <br />

But most of these work are limited to analysis of the data. We want to go one extra step ahead and wantg to implement 
recommender system for the user based on the user's needs.

## II. Materials and Methods : the dataset(s), technologies and algorithms that will be used.

### Dataset : 

The dataset size is 89 Mbs with 60800 rows. It has total 17 columns but we are not going to focus on all of them. The main columns we have considered are given below.

<b>name :</b> contains the name of the restaurant <br />
<b>address :</b> contains the address of the restaurant in Bengaluru <br />
<b>online_order :</b> whether online ordering is available in the restaurant or not <br />
<b>book_table :</b> table book option available or not <br />
<b>rate :</b> contains the overall rating of the restaurant out of 5 <br />
<b>votes :</b> contains total number of rating for the restaurant as of the above mentioned date <br />
<b>rest_type :</b> restaurant type <br />
<b>cuisines :</b> food styles, separated by comma <br />
<b>approx_cost(for two people) :</b> contains the approximate cost for meal for two people <br />
<b>reviews_listlist of tuples :</b>  containing reviews for the restaurant, each tuple consists of two values, rating and review by the customer <br />
<b>listed_in(city) :</b> contains the neighborhood in which the restaurant is listed <br />

### Technologies

Python, Spark, Panda

### Algorithms

<b>Exploratory Data Analysis (EDA) :</b> is an approach to analyzing data sets to summarize their main characteristics, often with visual methods. A statistical model can be used or not, but primarily EDA is for seeing what the data can tell us beyond the formal modeling or hypothesis testing task.

<b>Long short-term memory (LSTM) :</b> We are going to use LSTM for binary classification of reviews provided by users as negative or positive,means the model predicts whether the review provided by user is negative review or positive.

<b>KNN (k-nearest neighbors) :</b> In our dataset, there are many restaurants which are not rated. And we certainely can not ignore large number of restaurants. So we are going to use this algorithm to predict the missing value.

<b>ALS (Alternating Least Squares) :</b> After analysing the data, we are going to generate the recommender system which can recommend used the restaurants based on the parameters.
