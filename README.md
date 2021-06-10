# branch_curator

### A simple solution to manage a branch activity.

* This project aims to find a solution for managing project related activity in a branch (ISE/CSE) . 
* This project will help people to create anew project and ask people to join in .
* It also has a option to create blogs and share knowledge .
* It recommends the matching projects and blogs based on your interests.
* It automatically tags topic whenerver you submit a project.
* It gives overall trends such as which field is trending and how much new things are coming to it.

## ML PART 
* This project does recommendations and topic classification
* For recommendation we collects likes of people in past as data and match the items using cosine similarity.
* For topic classification we use naive bayes algorithm on a vector of words also called as bag of words

## backend part 
* We have used Django in the backend and Postgresql as database.
* Django ORM used for interacting with database and Django Template langauge for displaying the contents to user.
* Trends in a particular filed is calculated using z-score

## frontend part
* bootstrap-4 used for design of website and Django Template langauge for displaying the contents to user.

#### This website is diployed on heroku.
https://bcurator.herokuapp.com/

