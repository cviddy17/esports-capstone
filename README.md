# README

Version History:
.9.2018.4.8 Notes about this project.
.9.2017.10.19 Cleaning/Overhaul
.9.2017.10.5 Added webapp functionality

### About this project

This project was a project that I used for my capstone at Galvanize.

The dataset that ultimately drove this site was ineffective at prediction, but I do take pride in having a data pipeline built that I will ultimately extend as a showcase of ETL, Data Visualization, and Machine Learning.

I did most of my visualizations in this project in Bokeh, however, the plan is to move to plot.ly for interactive components and traditional matplotlib for non-interactive components. I also built the original site using Flask and a Bootstrap Theme, however future plans will include using the Flask-Bootstrap package to reduce html code as well as building my own themes for CSS.

### Scope and problem:

eSports is a growing industry. By 2019, total revenue is projected to exceed $1B. Most of this revenue comes from advertising, partnerships, and sponsorships.

Players gain their revenue through streaming sites such as twitch, as well as through team sponsorship and tournament earnings.

I seek to predict the chance that a player reaches the final stage of any given tournament. Finalists have the most media coverage in a tournament, which is great for the player’s pocket and prospective teams, but is also a great for feeding game demand and maximizing ad revenue (since they have the most coverage) and conversion. esportsearnings.com is a site that tracks earnings for players from all tournaments in all video games. My prediction analysis will focus on Starcraft II, a game with longevity that will serve as the stepping stone for analyzing eSports as a whole.

### Visualizations

By visualizing graphs in Bokeh into a web-based interface, I can show some of the interesting analyses in an interactive manner. This is great for explaining data to clients, managers, engineers, and other data scientists alike.

Models used: Logistic Regression (baseline) Gradient Boost, Random Forest

Results/Conclusions: With the dataset given, I was able to predict with 67% accuracy if a player will reach the finals. As more data is added to the site and through other external sources, results should improve over time.


Currently the webapp will be hosted on

capstone.cvdatascience.com

Note that this site will be built out in the future, so expect future updates!
