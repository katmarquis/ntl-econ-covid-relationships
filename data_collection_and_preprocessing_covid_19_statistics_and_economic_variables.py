# -*- coding: utf-8 -*-
"""Data Collection and Preprocessing - Covid-19 Statistics and Economic Variables.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LVoDUImVhWbNj9_WKOIkvcF6hYPlISf_
"""

import numpy as np
import pandas as pd

from google.colab import drive
from google.colab import files
drive.mount('/content/drive')

path = "/content/drive/MyDrive/Undergrad/Junior Summer/SURF/data/"

"""## Counties

https://towardsdatascience.com/the-ultimate-state-county-fips-tool-1e4c54dc9dff
"""

df = pd.read_csv(path + "fips2county.csv")
df.head()

df = df.drop(columns=["STATE_COUNTY"])
print(df.shape)
df.head()

df = df[(df["StateAbbr"] != "HI") & (df["StateAbbr"] != "AK")]
df.shape

df.to_csv(path + "counties_to_use.csv")

"""## Covid Cases and Deaths"""

counties_df = pd.read_csv(path + "counties_to_use.csv", index_col=0)
print(counties_df.shape)
counties_df.head()

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

def days_in_month(month, year):
  if month == 1:
    return 31
  if month == 2:
    if year == 2020:
      return 29
    if year != 2020:
      return 28
  if month == 3:
    return 31
  if month == 4:
    return 30
  if month == 5:
    return 31
  if month == 6:
    return 30
  if month == 7:
    return 31
  if month == 8:
    return 31
  if month == 9:
    return 30
  if month == 10:
    return 31
  if month == 11:
    return 30
  if month == 12:
    return 31

def date_to_string(day, month, year):
  day_string = str(day)
  if day < 10:
    day_string = "0" + day_string
  month_string = str(month)
  if month < 10:
    month_string = "0" + month_string
  year_string = str(year)
  return(month_string + "-" + day_string + "-" + year_string)

def date_to_string_no_day(month, year):
  month_string = str(month)
  if month < 10:
    month_string = "0" + month_string
  year_string = str(year)
  return(year_string + month_string)

def find_last(fips, lst):
  places = lst.copy()
  places.reverse()
  index = places.index(fips)
  return (len(places) - index - 1)

"""https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data"""

file = pd.read_csv(path + "csse_covid_19_daily_reports/01-01-2021.csv")
file = file[(file["Country_Region"] == "US") & (file["Province_State"] == "Connecticut") & (file["Admin2"] == "Fairfield")]
print(file["Confirmed"].tolist()[0])
file.head()

# make df of all combinations of counties and dates with Covid cases and deaths stats

counties_lst = counties_df["CountyName"].tolist()
states_lst = counties_df["StateAbbr"].tolist()
fips_lst = counties_df["CountyFIPS"].tolist()

df_dates = []
df_counties = []
df_states = []
df_fips = []
df_cases_total = []
df_deaths_total = []
df_cases_new = []
df_deaths_new = []

month = 3
year = 2020

for i in range(len(fips_lst)):
   county = counties_lst[i]
   state = states_lst[i]
   fips = fips_lst[i]
   year = 2020
   month = 3
   last_month_total_deaths = 0
   last_month_total_cases = 0
   while year <= 2023:
    while month <= 12:
      if year == 2023 and month > 2:
        break
      day = days_in_month(month, year)
      file = pd.read_csv(path + "csse_covid_19_daily_reports/{}.csv".format(date_to_string(day, month, year)))
      file = file[(file["FIPS"] == fips)]
      if file.empty == True:
        print(month, year, county, state)
      elif file.empty == False:
        num_cases_total = file["Confirmed"].tolist()[0]
        num_deaths_total = file["Deaths"].tolist()[0]
        df_dates.append(date_to_string_no_day(month, year))
        df_counties.append(county)
        df_states.append(state)
        df_fips.append(fips)
        df_cases_total.append(num_cases_total)
        df_deaths_total.append(num_deaths_total)
        new_cases = num_cases_total - last_month_total_cases
        new_deaths = num_deaths_total - last_month_total_deaths
        df_cases_new.append(new_cases)
        df_deaths_new.append(new_deaths)
        last_month_total_cases = num_cases_total
        last_month_total_deaths = num_deaths_total
      month += 1
    month = 1
    year += 1

data = pd.DataFrame()
data["Date"] = df_dates
data["County"] = df_counties
data["State"] = df_states
data["FIPS"] = df_fips
data["Total_Cases"] = df_cases_total
data["Total_Deaths"] = df_deaths_total
data["New_Cases"] = df_cases_new
data["New_Deaths"] = df_deaths_new

data.to_csv(path + "covid_cases_and_deaths_by_county.csv")
data.head()

# note that the above county/date combinations were dropped
# the only notably missing ones are those from Utah and two from MA

"""## Vaccinations

https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh

### Reduce Data Frame to Needed Entries
"""

vax_data = pd.read_csv(path + "COVID-19_Vaccinations_in_the_United_States_County.csv")
vax_data.sample(n=5)

dates_lst = vax_data["Date"].tolist()
years = []
months = []
days = []
for date in dates_lst:
  new_date = date.split("/")
  years.append(int(new_date[2]))
  months.append(int(new_date[0]))
  days.append(int(new_date[1]))

vax_data["Date_Year"] = years
vax_data["Date_Month"] = months
vax_data["Date_Day"] = days
vax_data.sample(n=5)

# drop unknown counties and convert fips codes to integers instead of lists

vax_data = vax_data[vax_data["FIPS"] != "UNK"]
vax_data.reset_index(drop=True)
new_fips = []
old_fips = vax_data["FIPS"].tolist()
for code in old_fips:
  new_fips.append(int(code))
vax_data["FIPS"] = new_fips
vax_data.head(n=5)

# adjust to only contiguous US

vax_data = vax_data[(vax_data["Recip_State"] != "HI") & (vax_data["Recip_State"] != "AK")]

# drop extra columns from vax data
vax_data = vax_data[["Date","Date_Year","Date_Month","Date_Day","FIPS","Recip_County","Recip_State",
                    "Census2019","Series_Complete_Yes","Series_Complete_Pop_Pct","Booster_Doses",
                    "Booster_Doses_Vax_Pct","SVI_CTGY","Series_Complete_Pop_Pct_SVI","Booster_Doses_Vax_Pct_SVI"]]

vax_data.sample(n=5)

# only keep last row entry of each month for each county

vax_set = set(vax_data["FIPS"].tolist())
counties = vax_set

date_lst = [[12,2020]]
for y in range(2021,2023):
  for m in range(1,13):
    date_lst.append([m,y])
for m in range(1,6):
  date_lst.append([m,2023])

df = pd.DataFrame(columns = ["Date","Date_Year","Date_Month","Date_Day","FIPS","Recip_County","Recip_State",
                    "Census2019","Series_Complete_Yes","Series_Complete_Pop_Pct","Booster_Doses",
                    "Booster_Doses_Vax_Pct","SVI_CTGY","Series_Complete_Pop_Pct_SVI","Booster_Doses_Vax_Pct_SVI"])

for fips in counties:
  temp_data = vax_data[vax_data["FIPS"] == fips]
  temp_data.sort_values(["Date_Year","Date_Month","Date_Day"])
  for date in date_lst:
    temp = temp_data[(temp_data["Date_Year"] == date[1]) & (temp_data["Date_Month"] == date[0])]
    row = temp.head(1)
    df = pd.concat([df, row], axis=0, ignore_index = True)

df.to_csv(path + "vax_data_to_use.csv")
df.head()

"""### Combine Vaccination Information with County Cases and Deaths Data Frame"""

vax_data = pd.read_csv(path + "vax_data_to_use.csv", index_col=0)
vax_data.sample(n=5)

vax_set = set(vax_data["FIPS"].tolist())
len(vax_set) # number of counties that are included in vax data

data = pd.read_csv(path + "covid_cases_and_deaths_by_county.csv", index_col=0)
data.sample(n=5)

dates = data["Date"].tolist()
years = []
months = []
for d in dates:
  y = np.floor(d/100)
  m = d - y*100
  years.append(y)
  months.append(m)
data["Month"] = months
data["Year"] = years

data.head()

data_set = set(data["FIPS"].tolist())
len(data_set) # number of counties that are included in cases and deaths data

# show that vaccination data covers all cases data

not_in = 0
for county in data_set:
  if county not in vax_set:
    not_in += 1
print(not_in)

# append vax data to cases/deaths df

svi = []
series_num = []
series_pct = []
series_svi = []
booster_num = []
booster_pct = []
booster_svi = []

for row in data.itertuples():
  fips = row.FIPS
  month = row.Month
  year = row.Year
  vax_info = vax_data[(vax_data["Date_Year"] == year) & (vax_data["Date_Month"] == month) & (vax_data["FIPS"] == fips)]

  if vax_info["SVI_CTGY"].tolist() != []:
    svi.append(vax_info["SVI_CTGY"].tolist()[0])
  elif vax_info["SVI_CTGY"].tolist() == []:
    svi.append(np.NaN)

  if vax_info["Series_Complete_Yes"].tolist() != []:
    series_num.append(vax_info["Series_Complete_Yes"].tolist()[0])
  elif vax_info["Series_Complete_Yes"].tolist() == []:
    series_num.append(np.NaN)

  if vax_info["Series_Complete_Pop_Pct"].tolist() != []:
    series_pct.append(vax_info["Series_Complete_Pop_Pct"].tolist()[0])
  elif vax_info["Series_Complete_Pop_Pct"].tolist() == []:
    series_pct.append(np.NaN)

  if vax_info["Series_Complete_Pop_Pct_SVI"].tolist() != []:
    series_svi.append(vax_info["Series_Complete_Pop_Pct_SVI"].tolist()[0])
  elif vax_info["Series_Complete_Pop_Pct_SVI"].tolist() == []:
    series_svi.append(np.NaN)

  if vax_info["Booster_Doses"].tolist() != []:
    booster_num.append(vax_info["Booster_Doses"].tolist()[0])
  elif vax_info["Booster_Doses"].tolist() == []:
    booster_num.append(np.NaN)

  if vax_info["Booster_Doses_Vax_Pct"].tolist() != []:
    booster_pct.append(vax_info["Booster_Doses_Vax_Pct"].tolist()[0])
  elif vax_info["Booster_Doses_Vax_Pct"].tolist() == []:
    booster_pct.append(np.NaN)

  if vax_info["Booster_Doses_Vax_Pct_SVI"].tolist() != []:
    booster_svi.append(vax_info["Booster_Doses_Vax_Pct_SVI"].tolist()[0])
  elif vax_info["Booster_Doses_Vax_Pct_SVI"].tolist() == []:
    booster_svi.append(np.NaN)

data["SVI"] = svi
data["Series_Complete_Num"] = series_num
data["Series_Complete_Pct"] = series_pct
data["Series_Complete_SVI"] = series_svi
data["Booster_Complete_Num"] = booster_num
data["Booster_Complete_Pct"] = booster_pct
data["Booster_Complete_SVI"] = booster_svi

data.sample(n=5)

# figure out what to do with missing values

# population
pop_lst = []

for row in data.itertuples():
  county = row.FIPS
  vax_info = vax_data[(vax_data["FIPS"] == county)]
  pop = vax_info["Census2019"].tolist()
  pop_lst.append(pop[0])

data["Population"] = pop_lst
data.sample(n=5)

data.to_csv(path + "county_cases_deaths_vax.csv")

"""## Policy and Lockdowns

https://healthdata.gov/dataset/COVID-19-State-and-County-Policy-Orders/gyqz-9u7n
"""

df = pd.read_csv(path + "COVID-19_State_and_County_Policy_Orders.csv")
df.head()

policies = df["policy_type"].tolist()
count = 0
for p in policies:
  if p == 'Shelter in Place':
    count += 1
count/len(policies)

df = df[df["policy_type"] == "Shelter in Place"] # keep track of shelter in place orders
df.head()

def from_date(date_string):
  date_lst = date_string.split("/")
  year = date_lst[0]
  year = int(year)
  month = date_lst[1]
  month = int(month)
  return (month, year)

months = []
years = []

for row in df.itertuples():
  date_str = row.date
  month, year = from_date(date_str)
  months.append(month)
  years.append(year)

df["Date_Month"] = months
df["Date_Year"] = years
df.head()

# make sure all states that had a stay at home order have a shelter in place order

states = [ 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

for s in states:
  temp = df[(df["state_id"] == s) & (df["policy_level"] == "state")]
  if temp.empty == True:
    print(s)

# make dict of start/stop dates by county for those that aren't unknown

counties = set(df["fips_code"].tolist())
counties = [x for x in counties if str(x) != 'nan']

start_and_stop_dict_c = {}
for c in counties:
  entry = []
  temp = df[df["fips_code"] == c]
  start = temp[temp["start_stop"] == "start"]
  if start.empty == True:
    entry.append([0,0])
  elif start.empty == False:
    m = start["Date_Month"].tolist()[0]
    y = start["Date_Year"].tolist()[0]
    entry.append([m,y])
  stop = temp[temp["start_stop"] == "stop"]
  if stop.empty == True:
    entry.append([0,0])
  elif stop.empty == False:
    m = stop["Date_Month"].tolist()[0]
    y = stop["Date_Year"].tolist()[0]
    entry.append([m,y])
  if entry[0] == [0,0]:
    state = temp["state_id"].tolist()[0]
    temp2 = df[(df["state_id"] == state) & (df["policy_level"] == "state") & (df["start_stop"] == "start")]
    m = temp2["Date_Month"].tolist()[0]
    y = temp2["Date_Year"].tolist()[0]
    entry[0] = [m,y]
  if entry[1] == [0,0]:
    state = temp["state_id"].tolist()[0]
    temp2 = df[(df["state_id"] == state) & (df["policy_level"] == "state") & (df["start_stop"] == "stop")]
    m = temp2["Date_Month"].tolist()[0]
    y = temp2["Date_Year"].tolist()[0]
    entry[1] = [m,y]
  start_and_stop_dict_c[c] = entry
print(start_and_stop_dict_c)

# do the same for states

states = set(df["state_id"].tolist())

start_and_stop_dict_s = {}
for s in states:
  entry = []
  temp = df[(df["state_id"] == s) & (df["policy_level"] == "state")]
  start = temp[temp["start_stop"] == "start"]
  m = start["Date_Month"].tolist()[0]
  y = start["Date_Year"].tolist()[0]
  entry.append([m,y])
  stop = temp[temp["start_stop"] == "stop"]
  m = stop["Date_Month"].tolist()[0]
  y = stop["Date_Year"].tolist()[0]
  entry.append([m,y])
  start_and_stop_dict_s[s] = entry
print(start_and_stop_dict_s)

counties_df = pd.read_csv(path + "county_cases_deaths_vax.csv",index_col=0)
counties_df.sort_values(["FIPS","Date"])
counties_df.head()

shelter_in_place = [] # 0 is no, 1 is yes

for row in counties_df.itertuples():
  fips = row.FIPS
  state = row.State
  month = row.Month
  year = row.Year
  date_ind = month + 12*(year - 2020)
  if fips in start_and_stop_dict_c:
    entry = start_and_stop_dict_c[fips]
    start = entry[0]
    start_ind = start[0] + 12*(start[1] - 2020)
    stop = entry[1]
    stop_ind = stop[0] + 12*(stop[1] - 2020)
    if date_ind >= start_ind and date_ind <= stop_ind:
      shelter_in_place.append(1)
    elif date_ind < start_ind or date_ind > stop_ind:
      shelter_in_place.append(0)
  elif fips not in start_and_stop_dict_c:
    if state not in start_and_stop_dict_s:
      shelter_in_place.append(0)
    elif state in start_and_stop_dict_s:
      entry = start_and_stop_dict_s[state]
      start = entry[0]
      start_ind = start[0] + 12*(start[1] - 2020)
      stop = entry[1]
      stop_ind = stop[0] + 12*(stop[1] - 2020)
      if date_ind >= start_ind and date_ind <= stop_ind:
        shelter_in_place.append(1)
      elif date_ind < start_ind or date_ind > stop_ind:
        shelter_in_place.append(0)

counties_df["Stay_at_home_order"] = shelter_in_place
counties_df.head()

counties_df.to_csv(path + "county_cases_deaths_vax_home.csv")

"""## Economic Variables

https://github.com/OpportunityInsights/EconomicTracker/tree/main
"""

data = pd.read_csv(path + "county_cases_deaths_vax_home.csv", index_col = 0)
data.head()

counties = set(data["FIPS"].tolist())
print(len(counties))

"""### Credit/Debit Card Spending"""

spending_df = pd.read_csv(path + "ec_data/Affinity - County - Daily.csv")
spending_df.sample(n=5) # spend_all is consumer spending relative to Jan 2020

counties_incl = set(spending_df["countyfips"].tolist())
print(len(counties_incl))

spending = []

for row in data.itertuples():
  fips = row.FIPS
  if fips in counties_incl:
    temp = spending_df[(spending_df["countyfips"] == fips) & (spending_df["year"] == row.Year) & (spending_df["month"] == row.Month)]
    nums = temp["spend_all"].tolist()
    nums_filtered = [float(i) for i in nums if i != "."]
    if nums_filtered == []:
      spending.append(np.NaN)
    elif nums_filtered != []:
      num = np.mean(nums_filtered)
      spending.append(num)
  elif fips not in counties_incl:
    spending.append(np.NaN)

data["Spending"] = spending

data.to_csv(path + "county_cases_deaths_vax_policy_ec.csv")
data.head()

"""### Job Postings"""

data = pd.read_csv(path + "county_cases_deaths_vax_policy_ec.csv",index_col=0)
data.head()

jobs_df = pd.read_csv(path + "ec_data/Job Postings - County - Weekly.csv")
jobs_df.sample(n=5)

counties_incl = set(jobs_df["countyfips"].tolist())
print(len(counties_incl))

jobs = []

for row in data.itertuples():
  fips = row.FIPS
  if fips in counties_incl:
    temp = jobs_df[(jobs_df["countyfips"] == fips) & (jobs_df["year"] == row.Year) & (jobs_df["month"] == row.Month)]
    nums = temp["bg_posts"].tolist()
    nums_filtered = [float(i) for i in nums if i != "."]
    if nums_filtered == []:
      jobs.append(np.NaN)
    elif nums_filtered != []:
      num = np.mean(nums_filtered)
      jobs.append(num)
  elif fips not in counties_incl:
    jobs.append(np.NaN)

data["Job_Postings"] = jobs

data.to_csv(path + "county_cases_deaths_vax_policy_ec.csv")
data.head()

"""### Employment"""

data = pd.read_csv(path + "county_cases_deaths_vax_policy_ec.csv",index_col=0)
data.head()

employ_df = pd.read_csv(path + "ec_data/Employment - County - Weekly.csv")
employ_df.sample(n=5)

counties_incl = set(employ_df["countyfips"].tolist())
print(len(counties_incl))

emp = []

for row in data.itertuples():
  fips = row.FIPS
  if fips in counties_incl:
    temp = employ_df[(employ_df["countyfips"] == fips) & (employ_df["year"] == row.Year) & (employ_df["month"] == row.Month)]
    nums = temp["emp"].tolist()
    nums_filtered = [float(i) for i in nums if i != "."]
    if nums_filtered == []:
      emp.append(np.NaN)
    elif nums_filtered != []:
      num = np.mean(nums_filtered)
      emp.append(num)
  elif fips not in counties_incl:
    emp.append(np.NaN)

data["Employment_Rate"] = emp

data.to_csv(path + "county_cases_deaths_vax_policy_ec.csv")
data.head()

"""### Unemployment Insurance Claims"""

data = pd.read_csv(path + "county_cases_deaths_vax_policy_ec.csv",index_col=0)
data.head()

ui_df = pd.read_csv(path + "ec_data/UI Claims - County - Weekly.csv")
ui_df.head(n=5)

counties_incl = set(ui_df["countyfips"].tolist())
print(len(counties_incl))

ui = []
ui_rate = []

for row in data.itertuples():
  fips = row.FIPS
  if fips in counties_incl:
    temp = ui_df[(ui_df["countyfips"] == fips) & (ui_df["year"] == row.Year) & (ui_df["month"] == row.Month)]

    nums = temp["initclaims_count_regular"].tolist()
    nums_filtered = [float(i) for i in nums if i != "."]
    if nums_filtered == []:
      ui.append(np.NaN)
    elif nums_filtered != []:
      num = np.mean(nums_filtered)
      ui.append(num)

    nums = temp["initclaims_rate_regular"].tolist()
    nums_filtered = [float(i) for i in nums if i != "."]
    if nums_filtered == []:
      ui_rate.append(np.NaN)
    elif nums_filtered != []:
      num = np.mean(nums_filtered)
      ui_rate.append(num)

  elif fips not in counties_incl:
    ui.append(np.NaN)
    ui_rate.append(np.NaN)

data["UI_Count"] = ui
data["UI_Rate"] = ui_rate

data.to_csv(path + "county_cases_deaths_vax_policy_ec.csv")
data.head()