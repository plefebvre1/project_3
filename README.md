# project_3
Repository containing files for GWU Fintech Bootcamp Project 3


EXECUTIVE SUMMARY:

  This project aimed to accomplish two things: connect customers to their TD Ameritrade accounts remotely using an API, and then, perform technical analysis on the customers portfolio. The majority of the grunt work is done through our functions.py file, where the data sourcing, cleaning and analysis occurs. Our app.py file extends the project by providing Streamlit code that allows for users to input their information, as well as interact with their results.

Data Source and Collection: 

  TD Ameritrade API: With a TD Ameritrade cash account, we were able to use TD’s api to access our accounts remotely. The API functions through the python    library TD-client. To connect to the server, the customer needs a:
TD Ameritrade  cash account
TD Ameritrade Developer account
TD Ameritrade API key
A consumer iD
A redirect URL
The consumer id, redirect url and client id are to be stored in an environment file located in the same folder as the python file we are producing. 

Data Cleanup:

1. Using the account data from the API, pull portfolio information:
    a. High, Close, datetime, portfolio value
    
2. Produce relevant technical analysis on the portfolio
    a. Output: A dataframe containing financial metrics for the portfolio and the market.
    b. Metrics: Annualized sharpe ratio, average annualized returns, volatility, variance, covariance
    
Results:

Our resulting product is a python file that allows for a user to input their required TD Ameritrade authentications, and run a Streamlit application to calculate and display financial metrics of their portfolio against the market.

<img width="438" alt="Screen Shot 2022-06-02 at 4 52 19 PM" src="https://user-images.githubusercontent.com/95647683/171736124-055dd8df-7f4b-43ef-bf69-1229335243aa.png">




