## Abstract
In 3-4 sentences, concisely describe:

What problem your project addresses.
The overall approach you will use to solve the problem.
How you propose to evaluate your success against your stated goals.

We are hoping to create a algorithm that looks at NFL players performance and predicts their performance for the following year. By doing so, we will be able to create a ranking that can be used to predict Fantasy Football Performance. We will evaluate the effectiveness of our model by running it against previous years and seeing how it performed predicting player performance vs how they actually performed that year.

## Motivation and Question
Describe your motivation for your project idea.

We are all very interested in the intersection between sports and statistics. Football is a sport where statistics are tracked frequently and there are many available. We are hoping to find which statistics and variables are more significant in determining a players performance year to year. Fantasy Football is played by millions of people all over the world and an effective algorithm would be helpful to all players.

## Planned Deliverables
Concisely state what you are aiming to create and what capabilities it will have.

We are hoping to deliver a Python package containing all code we will use for our algorithm and a Jupyter notebook where analysis and performance is examined. We will need to extensively clean our data and ensure the data set we are looking at has all variables we are hoping to look at. If our model proves to be ineffective, at least we will be able to determine which statistics are not helpful in predicting performance year to year.

## Written Deliverables
You’ll also write a blog post on your project; you don’t have to discuss this post in your proposal though.

## Resources Required
What resources do you need in order to complete your project? Data? Computing power? An account with a specific service?

Please pay special attention to the question of data. If your project idea involves data, include at least one link to a data set you can use. If you can’t find data for your original idea, that’s ok! Think of something related to your group’s interests for which you can find data.

Most projects should involve data in some way, but certain projects may not require data. Ask me if you’re not sure.

We will be working with numerous data sources. We are hoping to take the basic stats that all Fantasy Football users look at and add several additional statistics we think might be helpful in predicting performance. We are hoping to create a master dataset that we can use to run learning methods and make conclusions on. Once we have a functioning dataset, we will need to run learning models that will give us a ranking for the players in our dataset.

## What You Will Learn
Each group member should return to their stated goals from the reflective goal-setting assignment at the beginning of the course. Then, in this section, please state what each group member intends to learn through working on the project, relating your intentions to your stated goals. You might be thinking of certain algorithms, software packages, version control, project management, effective teamwork, etc.

Johnny:  
-Data collection, web scraping, working with API's  
-Implementation of ML algorithm  
-Theory (math related) on whichever algorithm we choose to employ  

Ethan:  
-Data collection and exploring how to combine different data sources.  
-Implementing a ML algorithm to a topic we are passionate about.  
-Exploring different algorithms we could potentially implement on our data.

Dean:  
-Data collection and integration.  
-Creating and implementing a ML algorithm to a real world topic.  
-Understanding, on a mathematical level, why one algorithm would be better than another.


## Risk Statement

1. It is possible that we cannot get all the data we need to accurately predict performance. There is no guarantee that we can get all of ESPN's data set, but I am hopeful through enough effort we will put together a good data set. We are also at risk of not having certain data which affects performance like opposing match-ups (individually), change of coaches and how this affects the player, team acquisitions, injuries, etc.
2. Finding the correct algorithm and feature selection will be tricky and could prevent optimal performance. We (hopefully) will have many features to choose from, so narrowing down these columns will be risky. Additionally, algorithm choice / implementation will be tricky. We are outputting a ranking, which will most likely depend on a quantitative metric. As a result, we need to figure out some sort of regression model that will optimally rank our players.

## Ethics Statement

#### What groups of people have the potential to benefit from our project?

Primarily, fantasy football players. Those who use our algorithm will (hopefully) receive insight into future player performance and can therefore edit their decision making to maximize their season.

#### What groups of people have the potential to be excluded from benefit or even harmed from our project?

The other members of the league who do not use the algorithm will not have the insight and therefore might be at a disadvantage. At the very least they will be excluded from the benefit.

#### Will the world become an overall better place because we made our project? Describe at least 2 assumptions behind your answer. For example, if your project aims to make it easier to predict crime, your assumptions might include:

Not necessarily. It might aid some fantasy football owners, but I do not think there are any large scale benefits or harms. 

## Tentative Timeline

In the first three weeks, we will primarily focus on data collection, exploration, and wrangling. We believe a large component to this project will be scraping data off the web and through various API's. We also expect us to have to imput our own data, much of which will be calculated using various statistical techniques. As a result, we hope to spend the first three weeks in this data collection/wrangling phase. By the end of week 3, hopefully we have a working data set.

In the next three weeks, we will create our algorithm. During this time period, we will implement our own algorithm to rank players based on performance. By the end of week 6, we hope to have a working algorithm (not necessarily optimal yet).