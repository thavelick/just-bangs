# Just Bangs

A clone of duck duck go, but with no index. Just the bangs!

* [What are bangs?](https://duckduckgo.com/bang)

## Installation and Usage

1. Install and start the server
    ```
    git clone https://github.com/thavelick/just-bangs
    cd just-bangs
    curl -fLO https://duckduckgo.com/bang.js
    ./just_bangs
    ```
2. Optionally, before starting the server, create a `custom-bang.js`
   file that will shadow the downloaded bangs. You only need the `t`
   and `u` fields on the custom bangs.
3. Open your browser to http://localhost:8484/
4. Append your search query to the url, with a bang:
   http://localhost:8484/gh!+just+bangs

### Environment variables

* `JUST_BANGS_DEFAULT_BANG`: The bang to use when none is specified.
  Without this, queries without a bang will show a page with a simple
  usage example.
* `JUST_BANGS_PORT`: The http port on which the server should run. Defaults
  to 8484
* `JUST_BANGS_MAIN_FILE`: The path to the file containing all the normal bangs
  from DDG. Defaults to `./bang.js`
* `JUST_BANGS_CUSTOM_FILE`: The path to the file containing custom bangs.
  Defaults to `./custom-bang.js`
* `JUST_BANGS_BASE_URL_PATH`: Normally, just bangs runs from the root, but
   if you're going to run it from a subfolder, specify that folder here
   to ensure that url parsing works as it should

## Dependencies
* Python 3.10
  * That's it
  * It probably works with most any Python 3.x but I didn't test it.

## Created By
* [Idiomdrottning](https://idiomdrottning.org/about) - idea, finding the bangs
  data file, adding `custom-bang.js`
* [Tristan Havelick](https:/tristanhavelick.com) - initial programming
