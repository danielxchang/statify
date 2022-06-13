# statify

## Summary
<p>This backend REST API was built with Flask (Python) and MySQL as its database solution. The backend API was deployed with Heroku and the frontend demo using this API was deployed with Netlify.</p> 
<p>This backend API allows users to input roster and play-by-play data into a provided Google Sheet template to send (as CSVs) to the API as a POST request in order to tally the stats in a given game. Using this data, the API, manages the data in various tables using MySQL and allows the user to retrieve various game statistics such as a box score, team stats, and even a formatted play-by-play, similar to how professional sports games (i.e. the NBA) would be presented on sites like ESPN.</p>
<p>Currently, the API only supports basketball; however, I've built this API with extensibility in mind to other sports, if desired.</p>

## Demo
<p><a href="https://statify-sports.netlify.app/" target="__blank">Click to see demo</a> (basic web page demo that utilizes the API to present game stats)</p>
