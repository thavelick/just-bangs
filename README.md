# Just Bangs

A clone of duck duck go, but with no index. Just the bangs!

## Installation and Usage

1. Install and start the server
    ```
    git clone https://github.com/thavelick/just-bangs
    cd just-bangs
    curl -fLO https://duckduckgo.com/bang.js
    ./just_bangs
    ```
2. Open your browser to http://localhost:8484/
3. Append your search query to the url, with a bang: 
  http://localhost:8484/gh!+just+bangs

## Dependencies
* Python 3.10
  * That's it
  * It probably works with most any Python 3.x but I didn't test it.

## Created By
* @Sandra@idiomdrottning.org - idea, inspiration, finding the bangs data file
* Tristan Havelick (@Natris1979@social.linux.pizza) - programming

## TODO
* Add environment variables for:
  * Location of bangs file
  * Port
* Add a homepage with a simple seach box
* Commission an artist to make a cute logo and put it on the homepage
