# SOEN-691-PROJECT BIG DATA ANALYTICS PROJECT

## Team Composition

| Name  | Student id | Email Ids |
| --- | --- | ---|
| 40087977 | Sai Krishna | saich94@gmail.com |
| 40083289 | Dhaval Modi | dhavalmodi556@gmail.com |
| 40082236 | Manushree Mallaraju | NA |

## Project Type
Dataset Analysis (Recommender System)

## Abstract
In the given dataset we have almost 10000 restaurants scattered across different metro cities. It is obviously difficult to find the best restaurant in the city. So for a user, who is new to the city, we want to build a <b>recommender system</b> which can give him/her options of various restaurants based on the different parameters. The parameters that we are going to consider are reviews given by others, similar restaurant to his/her personal preference and location. The recommender systems will be content based as well as colloberative filtering based.

## I. Introduction
### Context

There are many options avalable to a particular user. But it would be more helpful, if we could get personalized preferences. This user might review the restaurant. ANd adding his/her rating, we can improvise the recommedation for the next user. So, with each increased rating we can make our recommender system more efficient with increasing amount of data. That is exactly our goal, to make best use of the avalable dataset and to make the best matching restaurant to user's need.

### Objectives

* The main objective of this project is to recommend a restaurant to a user, based on ratings and number of votes using two most popular algorithms.
* The second objective is to evaluate the result obtained using Mean Absolute Error (MAE) and Root mean squared error (RMSE) metrics. And then comparing the evaluation results of these algorithms.

### Presentation of the problem to solve

<b>Problem : </b> To find a recommedation of a restaurant based on the reviews/preference and location.

<b>Solution: </b> First we will analyse the exisitng data, transform the data. And then we will recommend the restaurant to users based on Content Based recommnedation and ALS recommender. At the end, we will also compare the result of these two recommnder algorithms.

<b>Problem : </b> Out of these two algorithms, which algorithm performs better.
<b>Solution: </b> We will evaluate the each algorithms results using RMSE and MEA metrics. Then we can compare these results to find out the best performing algorithm.

### Related work 

There are many data analysis papers on this datataset. <br />
* https://www.kaggle.com/parthsharma5795/finding-the-best-restaurants-in-bangalore <br />
* https://www.kaggle.com/chirag9073/zomato-restaurants-analysis-and-prediction <br />

But most of these work are limited to analysis of the data. We want to go one extra step ahead and want to implement ALS and Content based recommender system for the user base.

## II. Materials and Methods : the dataset(s), technologies and algorithms that will be used.

### Dataset

This dataset is not officially provided by the Data Owner. It is collected using the web scrapper. It is publicly available on Keggle and uploader by the user who has colllected and updated the data over the period of time. 

The dataset has 10000 rows where each row represents the restaurant and it's attributes. Though it's unofficial dataset, the datset is  cleaned but definitely not ideal. This dataset has been collected over two phases. This may be the reason for the noise in the data.

This dataset has mainly underlying problems

* Sacttered Data <br />

It has total 21 columns but we are not going to focus on all of them. The main columns we have considered are given below.

* <b>Restaurant Id :</b> Unique Id <br />
* <b>Restaurant Name :</b> contains the name of the restaurant <br />
* <b>Country Code :</b> contains thecountry code where it is located <br />
* <b>Aggregate rating :</b> Average rating of the restaurant <br />
* <b>Votes :</b> Number of votes given to particular restaurant <br />
* <b>Average Cost for two :</b> contains the approximate cost for meal for two people <br />

#### Sample Data

![](Sample_Data.PNG)

### Technologies

We are going to use Python, Pandas and Matplotlib. We are going to use Python libraries for general computation on data. Pandas will be useful analysing data and also transforming the data at the same time. Using Matplotlib, we will be able to generate graphs for visulization of huge data.

### Algorithms

<b>Exploratory Data Analysis (EDA) :</b> is an approach to analyzing data sets to summarize their main characteristics, often with visual methods. A statistical model can be used or not, but primarily EDA is for seeing what the data can tell us beyond the formal modeling or hypothesis testing task.

<b>Long short-term memory (LSTM) :</b> We are going to use LSTM for binary classification of reviews provided by users as negative or positive,means the model predicts whether the review provided by user is negative review or positive.

<b>KNN (k-nearest neighbors) :</b> In our dataset, there are many restaurants which are not rated. And we certainely can not ignore large number of restaurants. So we are going to use this algorithm to predict the missing value.

<b>ALS (Alternating Least Squares) :</b> After analysing the data, we are going to generate the recommender system which can recommend used the restaurants based on the parameters.

### Metrics

<b>Mean Absolute Error (MAE) :</b> This metric will be used to average over the test sample of the absolute differences between prediction and actual observation where all individual differences have equal weight. <br />

<b>Root mean squared error (RMSE) :</b> We will use this metric to measure of the differences between sample values and predicted by a recommender model.
