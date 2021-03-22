# Simple web application

This application was created as an exercise in creating an architecture to communicate
with a data base.

**app.py** file is main application that manage three servers (**b_1.py, b_2.py, b_3.py).

When we enter url http://127.0.0.1:7000/base with all four **.py** files running
we send a request for checking data base (in postresql). All rows have "flag" 
variable. Flag 1 = row to process, 2 = in progress, 3 = done, 4 = error.  
App search for first row with flag 1 or 4 and take it ID.  
Then ask servers if they are free. If at least one of them is, then send a 
request to one of them. Next server connect to the DB take row with specified ID
and do calculation (in this case it is just adding 2 values). 