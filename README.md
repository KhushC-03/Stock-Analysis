# Stock-Analysis
Monitor Stocks, Calculate Stock Prices, Set Notifications, Create Portfolios

Create a folder in the same directory called 'SharePortfolios'.

This will become an exe file soon. 
Right now we curnetly support stock monitoring for one stock, portfolio creation, price checker and a curency calculator.
Im looking into adding support for multiple stock monitoring (up to 9000 differnt stocks).
Unfortunetly you will get rate limited depending on your delay between monitoring (default is 125s can be changed in settings.json), proxy support will be added. 
I use pure python to get current stock price from the yahoo finance website as its more acurate then depending on packages, I also get more scraping control.
The reason the file isnt a .py file is because it currently contains sensitive binary data which will be stored on an api soon.
Also there will be a Ui version along with the cli version.
The News function does not work at this moment, this is something I currently working on, keep posted for updates.
To have 24/7 monitoring I advise you place the application on a server to run around the clock.
