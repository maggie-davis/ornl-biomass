# Stand alone instructions with python

### Before running the app, you will need to run the etl script using python. To do so, you will first create a new virual environment. Open a terminal and enter the following: 

```
# On Unix/macOS
python3 -m venv .venv

# On Windows
python -m venv .venv
```

### Next, activate the environment:

```
# On Unix/macOS
source .venv/bin/activate

# On Windows
venv\Scripts\activate
```

### Install dependencies:
```
pip install -r requirements.txt
```

### Run ETL script
Before running the etl script, open the .py file and update the file paths and database table names, as well as database connection information based on your environment. You will need a copy of the scenario data, which can be found here: https://bioenergykdf.ornl.gov/document/shortrotationwoodycrops-biocharco-productscenario as well as https://bioenergykdf.ornl.gov/document/switchgrasssoccarbonpaymentscenario. The script will save data in the static/data directory, where it can be seen by the web app. In the future, the copy step will be replaced by an api request, which is a feature planned in the near future.

### To run the web app locally using a simple python server, open a terminal in this directory and enter:

```
python -m http.server
```

Open a browser and navigate to the url listed in the terminal (default: localhost:8000)

This hosts the contents of the index.html. This file is the current version of the application.

# Methods

The values shown on the map are calculated as follows:

- For each FIPS, compute the sum of prod per sqmi

This version of the tool uses weighted scoring prioritization as follows:

1. Criteria: 7 total metrics (energy potential, air quality, etc)
2. Score criteria: these are the county-level data from the model. To compare between differing scales, these are normalized between 0-1 using min-max normalization.
3. Assign weights: these are determined by the user's priorities using the drag/drop functionality. Rankings correspond to the following weights:
   - 1: 0.25
   - 2: 0.21
   - 3: 0.18
   - 4: 0.14
   - 5: 0.11
   - 6: 0.07
   - 7: 0.04
4. Weighted criterion score: multiplied the score for each option against each criterion by the corresponding weight.
5. Overall weighted score: summed the weighted scores for each option.

The values shown on the radar plot are calculated as follows:

- Data are summed to the subclass and region level.
- Data are normalized based on the subclass and region with the highest and lowest values.
- Since low water quality and resiliency metrics are associated with preferable outcomes, these scales are reversed.
- Calculate the weighted scoring priorization as outlined above, omitting step 5. These values are what is shown in the radar plot, where each axis ranges from 0-1 with 0 being the minimum value and 1 being the maximum.
  Since the energy crops have an equally high resiliency, their min and max are same, so they do not appear on the map or the radar plot. This will change when other subclasses are included.
  The data are plotted along each axis relative to the maximum value for any metric. As a result, if the user adjusts the priority of a given metric to a level higher than others, the colored polygon’s intersections with those axes may appear to decrease.

The values shown on the bar plot are calculated as follows:

- Compute the sum of each metric at the subclass and region level.
- Since each metric has a different scale and unit, we normalize each metric based on the region and subclass with the highest value and the lowest value. The normalized metrics are on a scale from 0-1.
- Since low water quality and resiliency metrics are associated with preferable outcomes, these scales are reversed.
- Calculate the weighted scoring priorization as outlined above.
- The overall weighted score is the multiplied by the production per SQMI to arrive at the weighted production per SQMI, which is shown next to the production per SQMI in the bar chart.

# Contact Us

For questions, please contact Maggie Davis (davismr@ornl.gov) or Erik Schmidt (schmidteh@ornl.gov)