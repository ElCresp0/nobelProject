# Intel recruitment task
Write a Python program to query the Nobel Prize API and retrieve information about Nobel Laureates.

# Requirements
Use the Nobel Prize API to retrieve a list of all Nobel Laureates in Physics who won the prize in the year 2000 or later.
For each laureate, print their full name, year they won the prize, and the university/organization they were affiliated with at the time they won the prize.
Allow the user to enter the year of a prize and print the details for laureates of that specific year.
Handle potential errors from the API gracefully.
Use comments to document your code.
You can start from the documentation at https://www.nobelprize.org/about/developer-zone-2/

# How to run the application
Run App.py with python from command line,
input years (2000 - current year) to print the prizes
input 'exit' to exit

# Modules used
 - datetime - to read the current year for the query
 - requests - to send GET requests to nobel API
 - re - to validate user input using regular expressions
