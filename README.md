# STA-2453-Project-2

<img src="https://i.imgur.com/E5v5ZFw.png " data-canonical-src="https://i.imgur.com/E5v5ZFw.png " width="2160" />

**Installation Instructions:** 
1. Ensure you have a Python 3 environment that has the packages listed in requirements.txt 
2. Run app.py to start the local server ('python app.py' should be sufficient)
3. The dashboard should be accessible at http://127.0.0.1:8050/

**Technical Explanation**

This is a dashboard aimed at showing daily Ontario COVID-19 information to the general public, and was developed using Python using the Dash platform with the Bootstrap add-on and a data pipeline developed using the Pandas Python package. It pulls in information from the Ontario Data Catalogue, transforms them using the Pandas Python Package, and then passes it to the front-end Dash application for display.

The data pull and intial transforms are performed in the 'data_handler.py' file. Our primary data source is the Ontario Data Catalogue, which is directly maintained by the Ontario government and associated sub-provincial governments. Some secondary data, such as the shapefiles used for the map and population figures, are taken from Statistics Canada. The dashboard pulls data from the API once per day and stores them as CSV files in the 'data' folder for all future runs that day, significantly increasing performance. We also load in a number of pre-saved shapefiles and PHU population statistics that are present in the 'shapefiles' folder. After fetching the data, we clean and transform them so that they can be used for our visualizations and save them in a dictionary file for later use. 

The creation of the various Plotly graphs and figures are done in the 'fig_creator.py' file. We pass our data dictionary into the figure creation function held in this file - data transformations that are only useful for a single graph or figure (such as getting a DataFrame into a specific format) are done during this phase right before we create the Plotly figures. We save these Plotly files into a dictionary so that they can be easily accessed by the front-end.

The main Dash application is held in the 'app.py' file. Here the code specifying the format of the dashboard and the responsive elements like the sidebar and tabs selections are held. The figure dictionary from the previous file is used to populate the dashboard with various graphs and figures. The data dictionary is also read in here - used to calculate and display certain daily statistics. These statistics are displayed on panel elements generated and formate via helper functions held in the 'utils.py' folder. Some miscellaneous sprites such as the application icon and up and down arrows used in the panel elements are held in the 'assets' folder.

The application is run by executing the 'app.py' Python file which initializes the test server that holds the application. Then the dashboard should be accessible at http://127.0.0.1:8050/ on any web browser. Infrequently if the application is pulling data (which happens once per day on the first run) the Ontario Data Catalogue API can fail and will trigger an error. If this happens, rerunning it until the pull is successful should solve the issue.

