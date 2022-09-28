# Housing Prediction

## Problem Statement

Build a model of housing prices in California using the California census data. This data has metrics such as the population, median income, median housing price, and so on for each block group(district) in California. Block groups are the smallest geographical unit for which the US Census Bureau publishes sample data (a block group typically has a population of 600 to 3,000 people). The model learns from this data and will be able to predict the median housing price in any district, given all the other metrics.

## Business Goal

Investment Analysis for a particular area. 

## Model Design

* Supervised 
* Polynomial
* Univariate 
* Batch Learning

## Performance Measure

* R<sup>2
* RMSE

## Salient Features

* Follows CICD pipeline.
* Uses GridSearchCv to find the best model.
* Maintains entity and artifact folder.
* Use seperate thread for training purpose.
* Integrated UI.

### Pipeline Components

Data Ingestion
Data Validation
Data Transformation
Model Training
Model Evaluation
Model Push


### Exception
Housing Exception: Custom exception for the project



