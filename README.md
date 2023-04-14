# Line Check Compliance Tracker
This project uses BeautifulSoup4 to login to my work account and scrape the rota data for selected management staff in the current week. Then, using openpyxl and a spreadsheet template I created,
it populates all the shifts the managers have worked and the shifts they have off. Using this data I can easily reference who was working when certain tasks have been missed
and provide weekly updates for all tracking compliance. Once populated with all the information scraped from behind my work login, it then emails the spreadsheet to the work email
address so it can be used on Monday morning.

It is very much a funcational but rough and messy implementation. There are places where the code definitely needs to be refactored to make it more readable, especially during the 
openpyxl usage. I could use better variable names and split things like this little gargoyle
-  -"ws[f"{day_colums[(y*2) + 1]}{row_index}"] = "N""

into a more readable format.
Perhaps not the best mindset but maintability was not the most important thing for this project. It currently works perfectly and saves the management team over 30 minutes each 
week!



 
