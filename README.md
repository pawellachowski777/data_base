# Simple web application


This application was created as an exercise in creating an architecture to communicate with a database.

*app.py* file is the main application that manages three servers (*b_1.py, b_2.py, b_3.py*).

This is a structure of the table *a_b* in the database created in Postgresql

![makra](https://drive.google.com/uc?export=view&id=1p43Q_dXpL_BqRZ9q5F6C5xg-ounZ7Pyu)


When we enter URL http://127.0.0.1:7000/base with all four *.py* files running
we send a request for checking the database. The app is looking for rows with flag = 1 or = 5
where flag 1 means row to process, 2 is in progress, 3 is done, 4 is error.  
 
If there are any rows with flag 1 or 4, app asks servers if they are free. If at least one of them is, then send a 
request. Nextly the server connects to the DB take row with a specified ID
and does the calculation (in this case it is just adding 2 values). I used time.sleep()
method to simulate doing same big calculation. 
If all servers are running or there is nothing to calculate in the base, 
app will not send request
