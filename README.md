# Soccer Match Recommender

### What is this?
This is a collection of python scripts that connect to a REST API
that serves world cup results in JSON format. The purpose of these scripts is
to grade the quality of a given world cup match using an arbitrary
scoring metric that doesn't reveal any match scores. After running the program
it should be easy to choose a full match to watch with a spoiler-free experience.

### Installation instructions
You must have python installed to run these programs.

1. Clone this repository, or download the zip file
2. Install pipenv
```
pip install pipenv
```
3. Sync the dependencies
```
pipenv sync --dev
```
4. Run the script of choice
```
pipenv run <script-name>
```

### Script Descriptions
Each script is unique, so here is a brief overview of each

* daily script: shows matches from the current day ranked against each other with no quality score.
This script only ranks the matches against each other.
* daily_relative script: shows matches from the current day ranked with arbitrary quality score
This makes it easy to tell if any given match is way better than the others (or way worse)
* overall cup: ranks every game played so far against each other and shows the quality scores.
