# api

This is my RESTful api. The underlying model is just for show and has not been optimized. I have utilized FastAPI. The /home route accepts dynamic text input from the user. The text will be sent to a POST request which will search the root file for a dataset of that name. This can be reconfigured to pull queried data from a SQL server or anywhere else data might be stored. It pulls in the data, preprocesses it, runs the model over it to make predictions, and returns a mailing list with the names and addresses of predicted buyers. This mailing list is also saved in the root folder. 
