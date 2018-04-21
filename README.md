Willem Lucas
SI - 206
3/25/18
Project: Spotify Charting Application

Scraping a new single page → 4
Web API you haven’t used before that requires API key or HTTP Basic authorization ✣ →  4
Total = 8/8 Challenge Score

Revised: Web API you haven’t used that requires API key or HTTP authorization changed to Web API you haven’t used that requires Oauth 6

	My final project will access data from Spotify’s data catalogue, scrape the main Billboard Hot 100 chart, and integrate plotly. Its goal is to take a keyword (artist) from a user, make search requests using the Spotify API, take the same keyword and scrape the Billboard website for any occurrences, and finally use plotly to visually represent some sort of more specific data on the search requests itself. A following search may involve a user making a search like ‘Drake’. The program will return the top ten Drake songs streaming on Spotify, if they are on currently charting on the Billboard Hot 100, and create a scatterplots showing the charting, streaming, and spotify data. A search that doesn’t appear on the Billboard will return ‘Not charting ’. Key terms that aren’t specific songs, say, ‘Butterfly’, will return ten most popular results, which could range in a variety of genres and artists. Interaction will be conducted using an interface that also includes instructions. A sample output may look like:
  
Drake:
Drake - God’s Plan - Scary Hours (2018); Charting at spot #4
Drake - Diplomatic Immunity - Scaring Hours (2018);  Not charting
Drake - Fireworks - Thank Me Later Not (2008); Not charting
Blocboy JB - Look Alive feat. Drake - Look Alive Single (2018); Charting #11
      ……
Graphs will be opened based on an option provided to the user to display a graph based on a handful of topics (listed below)
Users can explore a song more by typing in its number, the program will bring them to the items page on the Spotify website.
And so on, revealing only the top 10 
5 Fields referenced: Artist Name, Song Name, Album Name, Album Year, Charting
4 Potential Graphs: 
Comparing charting data to streaming data
Comparing charting data to other charting data variables
Comparing followers to popularity rating
Comparing trends in charting movement with 
Data Sources: 
API BaseURL: https://api.spotify.com.
API Documentation: https://beta.developer.spotify.com/documentation/general/guides/authorization-guide/
Webpage being scraped: https://www.billboard.com/charts/hot-100
Tools: https://plot.ly/

Additional revisions include creating a list that populates the cache with artist data of some of my favorite artists. Dictionaries are loaded accordingly to update the database. The database relational key will be songs that are both charting and in the cache. 


