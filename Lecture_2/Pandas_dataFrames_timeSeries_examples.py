# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 10:31:30 2016

@author: noel
"""
import pandas as pd
import datetime as dt
import numpy as np
from Super_Pandas import *
#import Super_Pandas as spd

## TUTORIAL on using Pandas in QSTK
ldt_timestamps = []
for i in range(1, 6):
    ldt_timestamps.append(dt.datetime(2011, 1, i, 16))

print("The index we created has the following dates : ")
ldt_timestamps

## TimeSeries
ts_single_value = pd.TimeSeries(0.0, index=ldt_timestamps)
print("A timeseries initialized to one single value : ")

na_vals = np.arange(len(ldt_timestamps))
print("Dummy initialized array : ")
na_vals

ts_array = pd.TimeSeries(na_vals, index=ldt_timestamps)
print("A timeseries initialized using a numpy array : ")
ts_array

print("Reading the timeseries for a particular date")
print("Date :  ", ldt_timestamps[1])
print("Value : ", ts_array[ldt_timestamps[1]])

## DataFrames
print("Initializing a list of symbols : ")
ls_symbols = ['AAPL', 'GOOG', 'MSFT', 'IBM']
ls_symbols

print("Initializing a dataframe with two lists and zero values : ")
#init_panda(ldt_timestamps,ls_symbols)
df = pd.DataFrame(index=indx, columns=clmns)
df = df.fillna(0.0)

print("Initializing a dataframe with a random numpy array and two lists: ")
#init_panda_np(np.random.randn(len(ldt_timestamps), len(ls_symbols)),ldt_timestamps,ls_symbols)
df_vals = pd.DataFrame(na_vals_2, index=ldt_timestamps, columns=ls_symbols)
df_vals

print "Access the timeseries of a particular symbol : "
df_vals[ls_symbols[1]]

print "Access the timeseries of a particular date : "
df_vals.ix[ldt_timestamps[1]]

print "Access the value for a specific symbol on a specific date: "
df_vals[ls_symbols[1]].ix[ldt_timestamps[1]]

print "Reindexing the dataframe"
ldt_new_dates = [dt.datetime(2011, 1, 3, 16), 
                 dt.datetime(2011, 1, 5, 16),
                 dt.datetime(2011, 1, 7, 16)]
ls_new_symbols = ['AAPL', 'IBM', 'XOM']
df_new = df_vals.reindex(index=ldt_new_dates, columns=ls_new_symbols)
df_new
print "Observe that reindex carried over whatever values it could find and set the rest to NAN"

print "For pandas rolling statistics please refer : http://pandas.pydata.org/pandas-docs/dev/computation.html#moving-rolling-statistics-moments"
###################################################################################################
'''
CLASS: Pandas for Data Exploration, Analysis, and Visualization

WHO alcohol consumption data:
    article: http://fivethirtyeight.com/datalab/dear-mona-followup-where-do-people-drink-the-most-beer-wine-and-spirits/    
    original data: https://github.com/fivethirtyeight/data/tree/master/alcohol-consumption
    files: drinks.csv (with additional 'continent' column)

Pandas Basics: Reading Files, Summarizing, Handling Missing Values, Filtering, Sorting
'''
drinks = pd.read_csv('/home/noel/Code/Python/data/drinks.csv')
type(drinks)            # Use the type method to check python type
# examine the data
drinks                  # print the first 30 and last 30 rows
drinks.head()           # print the first 5 rows
drinks.tail()           # print the last 5 rows
drinks.describe()       # describe any numeric columns
drinks.info()           # concise summary
drinks.columns          # get series of column names
drinks.shape            # tuple of (#rows, #cols)

# find missing values in a DataFrame
drinks.isnull()         # DataFrame of booleans
drinks.isnull().sum()   # convert booleans to integers and add

# handling missing values
drinks.dropna()             # drop a row if ANY values are missing
drinks.fillna(value='NA')   # fill in missing values

# fix the original import with filter
drinks = pd.read_csv('/home/noel/Code/Python/data/drinks.csv', na_filter=False)
drinks.isnull().sum()

# selecting a column ('Series')
drinks['continent']
drinks.continent            # equivalent
type(drinks.continent)      # Series if pandas equivalent to list

# summarizing a non-numeric column
drinks.continent.describe()
#Count the number of countries in each continent
drinks.continent.value_counts()

# selecting multiple columns
drinks[['country', 'beer_servings']]
'''
note the double square bracket the outer pair is used like in a python 
dictionary to select the inner pair is a list!
so in all, the double use of square brackets is telling
the dataframe to select a list!
'''
my_cols = ['country', 'beer_servings']
drinks[my_cols]

# add a new column as a function of existing columns
drinks['total_servings'] = drinks.beer_servings +   drinks.spirit_servings + drinks.wine_servings
drinks.head()
# logical filtering and sorting
drinks[drinks.continent=='EU'] 
'''
How it works: drinks.continent=='EU' by itself returns a bunch
of Trues and Falses drinks.continent=='EU' 
See?

when you wrap drinks around it with square brackets
you're telling the drinks dataframe to select
only those that are True, and not the False ones

drinks[drinks.continent=='EU']
'''
# North American countries with total servings
drinks[['country', 'total_servings']][drinks.continent=='NA']
# same thing, sorted by total_servings
drinks[['country', 'total_servings']][drinks.continent=='NA'].sort_index(by='total_servings')
# contries with wine servings over 300 and total liters over 12
drinks[drinks.wine_servings > 300][drinks.total_litres_of_pure_alcohol > 12]
# contries with more wine servings than beer servings
drinks[drinks.wine_servings > drinks.beer_servings]
# last 5 elements of the dataframe sorted by beer servings
drinks.sort_index(by='beer_servings').tail()
# average North American beer consumption
drinks.beer_servings[drinks.continent=='NA'].mean()
'''
Note the procedure:
drinks                                          Dataframe
drinks.beer_servings                            one column (Series)
drinks.beer_servings[drinks.continent=='NA']    logical filtering
drinks.beer_servings[drinks.continent=='NA'].mean() mean of that filtered column
'''
# average European beer consumption
drinks.beer_servings[drinks.continent=='EU'].mean()
'''
Split-Apply-Combine
'''
# for each continent, calculate mean beer servings
drinks.groupby('continent').beer_servings.mean()
# for each continent, count number of occurrences
drinks.groupby('continent').continent.count()
drinks.continent.value_counts()
# for each continent, calculate the min, max, and range for total servings
drinks.groupby('continent').total_servings.min()
drinks.groupby('continent').total_servings.max()
# We can apply any function using .apply
drinks.groupby('continent').total_servings.apply(lambda x: x.mean())    # mean
# note x here is an entire series
drinks.groupby('continent').total_servings.apply(lambda x: x.std())     # standard deviation
# What does this do?
drinks.groupby('continent').total_servings.apply(lambda x: x.max() - x.min())
'''
Plotting
'''
# bar plot of number of countries in each continent
drinks.continent.value_counts().plot(kind='bar', title='Countries per Continent')
plt.xlabel('Continent')
plt.ylabel('Count')
plt.show()
# bar plot of average number of beer servings by continent
drinks.groupby('continent').beer_servings.mean().plot(kind='bar')
# histogram of beer servings
drinks.beer_servings.hist(bins=20)
# grouped histogram of beer servings
drinks.beer_servings.hist(by=drinks.continent)
# stop and think, does this make sense
# same charts with the same scale for x and y axis
drinks.beer_servings.hist(by=drinks.continent, sharex=True, sharey=True)
# density plot of beer servings
drinks.beer_servings.plot(kind='density')
# same chart, with new x limit
drinks.beer_servings.plot(kind='density', xlim=(0,500))
# boxplot of beer servings by continent
drinks.boxplot(column='beer_servings', by='continent')
# scatterplot of beer servings versus wine servings
drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', alpha=0.3)
# same scatterplot, except all European countries are colored red
colors = np.where(drinks.continent=='EU', 'r', 'b')
colors      # is a series of 'r' and 'b' that 
            # correspond to countries
'''
np.where is like a condensed if statement, it's like a list comprehension for pandas!

it will loop through drinks.continent which is a series
for each element:
    if it is "EU":
        make it 'r'
    else:
        make it 'b'

More in depth:
    drinks.continent=='EU' is a logical statement
        It will return a bunch of Trues and Falses
        and np.where makes the True ones 'r' and
        the False ones 'b'

        Recall logical filtering!
'''
# Side quest
np.where([True, False, False], 'a', 'b')
# 10 gold coins earned
drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', c=colors)
# passing colors into the chart makes the european dots, red!
##############
#### LAB #####
##############
# read in the CSV file from a URL
drinks = pd.read_csv('/home/noel/Code/Python/data/drinks.csv', na_filter=False)
# 1. Show the first 17 rows of drinks
drinks.head(17)
# 2. create a variable called beer_servings and use it to store the beer_servings column
beer_servings = drinks['beer_servings']
# 3. Display a dataframe where the only rows are those with continent North America
drinks[drinks['continent'] == 'NA']
# 4. Create a new dataframe called north_america that holds your answer in 1.
# drinks (the dataframe) should remain unchanged
north_america = drinks[drinks['continent'] == 'NA']
# 5. What is the average wine consumption per person per year in Africa?
drinks['wine_servings'][drinks['continent'] == 'AF'].mean()
# 6. Create a scatter plot between spirit servings and wine servings of all countries
drinks.plot(x='spirit_servings', y='wine_servings', kind='scatter', alpha=0.3)
# 7. Show a list of the top 10 spirit drinking countries 
# (show only country names and spirit servings)
drinks[['country', 'spirit_servings']].sort_index(by='spirit_servings', ascending = False).head(10)
# 8. Plot 6 histograms of wine servings by continent, 
# remember to share x and share y axis scales!
drinks.wine_servings.hist(by=drinks.continent, sharex = True, sharey = True)
# 9. What is the average wine consumption in South America?
drinks['wine_servings'][drinks['continent'] == 'SA'].mean()
# 10. Which continent has the highest on average wine consumption?
drinks.groupby('continent', as_index=False).wine_servings.mean().sort_index(by='wine_servings', ascending = False).head(1)
# Europe
###############################################################################
'''
Joining Data (INNER JOIN)

MovieLens 100k data:
    main page: http://grouplens.org/datasets/movielens/
    data dictionary: http://files.grouplens.org/datasets/movielens/ml-100k-README.txt
    files: u.user, u.data, u.item
'''
# read 'u.data' into 'ratings'
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_table('/home/noel/Code/Python/data/u.data', header=None, names=r_cols, sep='\t')
# read 'u.item' into 'movies'
m_cols = ['movie_id', 'title']
movies = pd.read_table('/home/noel/Code/Python/data/u.item', header=None, names=m_cols, sep='|', usecols=[0,1])
# PANDAS INNER JOIN
# merge 'movies' and 'ratings' (inner join on 'movie_id')
movies.head()
ratings.head()
movie_ratings = pd.merge(movies, ratings)
movie_ratings.head()
'''
Further Exploration
'''
# for each movie, count number of ratings
movie_ratings.title.value_counts()
# for each movie, calculate mean rating
movie_ratings.groupby('title').rating.mean().order(ascending=False)
###############################################################################
'''
----UFO data----
Dealing with nulll values
Scraped from: http://www.nuforc.org/webreports.html
'''
ufo = pd.read_csv('/home/noel/Code/Python/data/ufo.csv')   
ufo.head()              # Look at the top 5 observations
ufo.tail()              # Look at the bottom 5 observations
ufo.describe()          # describe any numeric columns (unless all columns are non-numeric)
ufo.columns             # column names (which is "an index")

ufo['Location'] = ufo['City'] + ', ' + ufo['State']
ufo.head()
# Pandas Column rename
ufo.rename(columns={'Colors Reported':'Colors', 'Shape Reported':'Shape'}, inplace=True)
ufo.head()
del ufo['City']                  # delete a column (permanently)
del ufo['State']                 # delete a column (permanently)
ufo.Shape.value_counts()                # excludes missing values
ufo.Shape.value_counts(dropna=False)    # includes missing values

ufo.Shape.isnull().sum() # count the missing values in the shape column
ufo.isnull().sum()       # returns a count of missing values in all columns
# Shows how many rows has a not null shape AND a not null color
ufo[(ufo.Shape.notnull()) & (ufo.Colors.notnull())]
ufo.dropna()             # drop a row if ANY values are missing
ufo.dropna(how='all')    # drop a row only if ALL values are missing

ufo                      # Without an inplace=True, the dataframe is unaffected!
ufo.Colors.fillna(value='Unknown', inplace=True)
ufo.fillna(value = 'Unknown')   # Temporary
ufo
ufo.fillna(value = 'Unknown', inplace = True)   # Permanent

############# 04 More Pandas  ########################
############# Load UFOs again ########################
ufo = pd.read_csv('/home/noel/Code/Python/data/ufo.csv')   # can also read csvs directly from the web!

ufo                 
ufo.head(5)          # Look at the top x observations
ufo.tail()            # Bottom x observations (defaults to 5)
ufo.describe()        # describe any numeric columns (unless all columns are non-numeric)
ufo.index             # "the index" (aka "the labels")
ufo.columns           # column names (which is "an index")
ufo.shape 		    # gives us a tuple of (# rows, # cols)

# DataFrame vs Series, selecting a column
type(ufo)
ufo['State']
ufo.State            # equivalent
ufo['Shape Reported']	# Must use the [''] notation if column name has a space
type(ufo.State)

# summarizing a non-numeric column
ufo.State.describe()        # Only works for non-numeric if you don't have any numeric data 
ufo.State.value_counts()    # Valuable if you have numeric columns, which you often will
# You can add in a sort optional arguement
ufo.State.value_counts(sort = True)
ufo.shape[0]                # number of rows

ufo.State.value_counts() / ufo.shape[0] # Values divided by number of records
# Shows percentages of sightings for each state
'''Slicing / Filtering / Sorting'''
ufo 					# Sanity check, nothing has changed!
# selecting multiple columns
ufo[['State', 'City','Shape Reported']]
my_cols = ['State', 'City']
ufo[my_cols]
type(ufo[my_cols])
'''
Notation

[row_start_index:row_end_index , col_start_index:col_end_index]
rows row_start_index through row_end_index and columns col_start_index through col_end_index
OR
[row_index , col_start_index:col_end_index]
only row row index and columns col_start_index through col_end_index
OR
[row_start_index:row_end_index , col_index]
rows row_start_index through row_end_index and only column col_index
OR
[[row1, row2], col_index]
only rows row1 and row2 and column col_index
'''
# logical filtering
ufo.State == 'TX'  # the == will compare 'TX' with every element in the column
# if we put the series of Trues and Falses in the dataframe, we will
# only get the rows where it is True, otherwise we won't see it!    
ufo[ufo.State == 'TX']
# only TX sightings

# not TX sightings
ufo[~(ufo.State == 'TX')]   
ufo[(ufo.State == 'TX') == False]
ufo[(ufo.State != 'TX')]                # All the same!

ufo.City[ufo.State == 'TX']
# only cities of texas sightings
ufo[ufo.State == 'TX'].City             # Same thing

ufo[(ufo.State == 'CA') | (ufo.State =='TX')] # CA OR  TX
ufo[(ufo.State == 'CA') & (ufo.State =='TX')] # CA AND TX

ufo_dallas = ufo[(ufo.City == 'Dallas') & (ufo.State =='TX')]
ufo[ufo.City.isin(['Austin','Dallas', 'Houston'])]

# sorting
ufo.State.order()                               # only works for a Series
ufo.sort_index(by='State')                      # sort rows by specific column
ufo.sort_index(by=['State', 'Shape Reported'])  # sort by multiple columns
ufo.sort_index(by=['State', 'Shape Reported'], ascending=[False, True])  # specify sort order
ufo                                             # sort_index won't change the dataframe!

# unless we tell it to with inplace = True
ufo.sort_index(by='State', inplace = True)      # sort rows by specific column
ufo
# Now it's changed!

# detecting duplicate rows
ufo.duplicated()                                # Series of logicals
ufo.duplicated().sum()                          # count of duplicates
ufo[ufo.duplicated(['State','Time'])]           # only show duplicates
ufo[ufo.duplicated()==False]                    # only show unique rows
ufo_unique = ufo[~ufo.duplicated()]             # only show unique rows
ufo.duplicated(['State','Time']).sum()          # columns for identifying duplicates

''' EXERCISE '''
# from before: this gives us the percentage of sightings by state
ufo.State.value_counts() / ufo.shape[0] # Values divided by number of records

# this dataframe is only sightings in texas
ufo_texas = ufo[ufo.State == 'TX']

# Use value counts to display the 
# BONUS, sort the dataframe so the city with the highest frequency is at the top
# Select the shape reported of all sightings in Connectucut
ufo_texas.City.value_counts(sort = True) / ufo_texas.shape[0]
ufo['Shape Reported'][ufo.State=='CT']
'''Modifying Columns'''
# add a new column as a function of existing columns
ufo['Location'] = ufo['City'] + ', ' + ufo['State']
ufo.head()
# rename columns inplace
ufo.rename(columns={'Colors Reported':'Colors', 'Shape Reported':'Shape'}, inplace=True)
ufo.head()
# hide a column (temporarily)
ufo.drop(['Location'], axis=1)
# axis = 1 means column as opposed to axis = 0 (row)
ufo                 # not changed!
# delete a column (permanently)
del ufo['Location']
ufo                 # changed!

'''Handling Missing Values'''
# missing values are often just excluded
ufo.describe()                          # excludes missing values
ufo.Shape.value_counts()                # excludes missing values
ufo.Shape.value_counts(dropna=False)    # includes missing values (new in pandas 0.14.1)

# find missing values in a Series
ufo.Shape.isnull()       # True if NaN, False otherwise
ufo.Shape.isnull().sum() # count the missing values

ufo.Shape.notnull()      # False if NaN, True otherwise

# Shows which rows do not have a shape designation
ufo[ufo.Shape.isnull()]
# Shows how many rows has a not null shape AND a not null color
ufo[(ufo.Shape.notnull()) & (ufo.Colors.notnull())]

# Makes a new dataframe with not null shape designations
ufo_shape_not_null = ufo[ufo.Shape.notnull()]

# drop missing values
ufo.dropna()             # drop a row if ANY values are missing
ufo.dropna(how='all')    # drop a row only if ALL values are missing
ufo                      # Remember, without an inplace=True, the dataframe is unaffected!
# fill in missing values to Colors only
ufo.Colors.fillna(value='Unknown', inplace=True)

# calling fillna on a dataframe will replace ALL null values
ufo.fillna('Unknown')                   # Temporary
ufo.fillna('Unknown', inplace = True)   # Permanent

ufo[ufo.Shape=='TRIANGLE'].shape[0]

ufo.Shape.replace('DELTA', 'TRIANGLE', inplace = True)   # replace values in a Series
ufo.replace('PYRAMID', 'TRIANGLE', inplace = True)       # replace values throughout a DataFrame

ufo[ufo.Shape=='TRIANGLE'].shape[0]
''' Fun Stuff '''
# Make a new month column
ufo['Month'] = ufo['Time'].apply(lambda x:int(x.split('/')[0]))
'''
the apply function applys the lambda funciton to every element in the Series
lambda x:x.split('/')[0] will take in x and split it by '/' and return the first element
so if we pass in say 9/3/2014 01:22 into the function we would get:
9                i.e. the month
'''
# similar for day
ufo['Day'] = ufo['Time'].apply(lambda x:int(x.split('/')[1]))

# for year, I need the [:4] at the end to remove the time
ufo['Year'] = ufo['Time'].apply(lambda x:int(x.split('/')[2][:4]))

# Plot of sightings per day in 2013
ufo[ufo.Year==2013].Day.value_counts().sort_index().plot()

# Plot the number of sightings over time
sightings_per_year = ufo.groupby('Year').City.count()

sightings_per_year.plot(kind='line', 
                        color='r', 
                        linewidth=1, 
                        title='UFO Sightings by year')
# -----Analysis-----
# Clearly, Aliens love the X-Files (which came out in 1993).
# Aliens are a natural extension of the target demographic so it makes sense.

# Well hold on Sinan, the US population is always increasing
# So maybe there's a jump in population which would make sense!
# US Population data from 1930 as taken from the Census
us_population = pd.read_csv('../data/us_population.csv')
us_population.plot(x = 'Date', y = 'Population', legend = False)

# Seems like a steady increase to me..
# Plot the sightings in in July 
ufo[(ufo.Year==2014) & (ufo.Month == 7)].groupby('Day').City.count().plot(  kind='bar', color='b', title='UFO Sightings in July 2014')                                                        
# -----Analysis-----
# Aliens are love the 4th of July. The White House is still standing. Therefore
# it follows that Aliens are just here for the party.

# Well maybe it's just 2014?

# Plot multiple plots on the same plot (plots neeed to be in column format)
ufo_fourth = ufo[(ufo.Year.isin([2011, 2012, 2013, 2014])) & (ufo.Month == 7)]
ufo_fourth.groupby(['Year', 'Day']).City.count().unstack(0).plot(   kind = 'bar', figsize=(7,9))

# unstack will take a groupby of multiple indices and split it by column (mainly great for sub plotting)
# Hmm let's make that prettier by making it 4 seperate charts
ufo_fourth.groupby(['Year', 'Day']).City.count().unstack(0).plot(
                                        kind = 'bar',
                                        subplots=True, 
                                        figsize = (7,9))
'''
Writing Data
'''
ufo.to_csv('ufo_new.csv')               # First column is an index
ufo.to_csv('ufo_new.csv', index=False)  # First column is no longer index
#### LAB ###################
ufo = pd.read_csv('/home/noel/Code/Python/data/ufo.csv')
ufo.rename(columns=lambda x: x.lower().replace(' ',''), inplace=True)

# 2. Show a bar chart of all shapes reported
ufo.groupby('shapereported').city.count().plot(kind='bar', title='UFO Shapes Reported')

# 3. Show a dataframe that only displays the reportings from Utah
ut_ufo = ufo[ufo.state=='UT']
# 4. Show a dataframe that only displays the reportings from Texas
tx_ufo = ufo[ufo.state=='TX']
# 5. Show a dataframe that only displays the reportings from Utah OR Texas
ut_tx_ufo = ufo[(ufo.state =='UT') | (ufo.state == 'TX')]
# 6. Which shape is reported most often?
shape_count = ufo.groupby('shapereported').shapereported.count()
max_shape_seen = max(ufo.groupby('shapereported').shapereported.count())
shpae_most_reported = shape_count.index[shape_count.isin([max_shape_seen]) == True][0]
# OR in one line
shape_most_seen = ufo.groupby('shapereported').shapereported.count().index[ufo.groupby('shapereported').shapereported.count().isin([max(ufo.groupby('shapereported').shapereported.count())]) == True][0]
# 7. Plot number of sightings per day in 2014 (days should be in order!)
ufo['day'] = ufo['time'].apply(lambda x:int(x.split('/')[1]))
ufo['month'] = ufo['time'].apply(lambda x:int(x.split('/')[0]))
ufo['year'] = ufo['time'].apply(lambda x:x.split('/')[2])
ufo['year'] = ufo['year'].apply(lambda x:int(x.split(' ')[0]))
ufo['date'] = ufo['time'].apply(lambda x:x.split(' ')[0])

# This whole relabeling could be avoided
ufo.sort_index(by=['year','month', 'day'], inplace = True)
ufo['time'] = pd.to_datetime(ufo['time'])
sighting_2014 = ufo[ufo.year == 2014]
sighting_2014.set_index([list(range(0,len(sighting_2014)))], inplace=True)
#Initializing a dataframe with everyday of the 2014 year:
ldt_timestamps = pd.date_range('1/1/2014', periods=365, freq='D') 
df_2014_ufo_sightings = pd.DataFrame(index=ldt_timestamps, columns=['sightings'])
df_2014_ufo_sightings = df_2014_ufo_sightings.fillna(0)
#df_2014_ufo_sightings.ix[sighting_2014['date'][80542]]
index = 1
for i in range(0,len(sighting_2014)):
    df_2014_ufo_sightings.ix[sighting_2014['date'][i]][0] = df_2014_ufo_sightings.ix[sighting_2014['date'][i]][0] + 1

#    sigthings_per_day_2014 = sighting_2014[sighting_2014.month == i].groupby('day').time.count()
#    for j in range(1,len(sigthings_per_day_2014)+1):
#        df_2014_ufo_sightings['sightings'][index+j] = sigthings_per_day_2014[j]
#        index = index + len(sigthings_per_day_2014)

df_2014_ufo_sightings['sightings'].plot(kind='bar', title='2014 Sightings per day')
plt.xlabel('day')
plt.ylabel('Count')
plt.xticks([1,31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],['Jan','Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.show()

#for i in range(2,13):
#    sigthings_per_day_2014 = sigthings_per_day_2014.append(sighting_2014[sighting_2014.month == i].groupby('day').day.count())
################################################################################################################################
'''
The IRIS dataset. Taken from the Machine Learning Repository from UCI
https://archive.ics.uci.edu/ml/datasets/Iris

'''
# load the famous iris data
iris = pd.read_csv('/home/noel/Code/Python/data/iris.csv')   # can also read csvs directly from the web!
# Read data into pandas and explore

# explore data numerically, looking for differences between species
iris.describe()
iris.groupby('species').sepal_length.mean()
iris.groupby('species')['sepal_length', 'sepal_width', 'petal_length', 'petal_width'].mean()
iris.groupby('species').describe()

# explore data by sorting, looking for differences between species
iris.sort_index(by='sepal_length')
iris.sort_index(by='sepal_width')
iris.sort_index(by='petal_length')
iris.sort_index(by='petal_width')

# explore data visually, looking for differences between species
iris.petal_width.hist(by=iris.species, sharex=True)
iris.boxplot(column='petal_width', by='species')
iris.boxplot(by='species')
################
### EXERCISE ###
################
'''
create a function called color_flower that takes in a string

if the string inputed is "Iris-setosa":
    return "b"
else if the string inputted is "Iris-virginica":
    return "r"
else:
    return "g"
Solution is below so no peeking!
'''
def color_flower(flower_name):
    if flower_name == 'Iris-setosa':
        return 'b'
    elif flower_name == 'Iris-virginica':
        return 'r'
    else:
        return 'g'

# apply this function to the species column to give us 
# designated colors!
colors = iris.species.apply(color_flower)
colors

iris.plot(x='petal_length', y='petal_width', kind='scatter', c=colors)

pd.scatter_matrix(iris, c=colors, figsize = (10,10))
# look at petal length vs petal width
