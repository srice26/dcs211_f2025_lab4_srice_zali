import  pandas as pd
#import matplotlib.pyplot
#import PrettyTable

'''
useful tools:
pandas to read csv file: skiprows,skipfooter, engine, and thousands
arc_data.columns = [’fips’,’state’,’county’,’arc_county’, ...

Remove rows: (just use slicing,with iloc since slices work with numbers), overwriting the data frame.

print the mean, standard deviation, minimum, and maximum
poverty rate over all data in the CSV. Remember to use pandas methods to easily compute those stats

 Recall that you can grab the states only using arc_data[’state’] (presuming you renamed the associated column
with ’state’ above. Use the Python type function in the interpreter to determine the type of the result from
arc_data[’state’].

Use the pandas method named value_counts (which works on a Pandas Series object) to determine/print the
number of counties per state. (Hint: Texas has 254, while Delaware has 3.)

 Use the PrettyTable library to print a table of the top-ten states (using your approach from the previous item)
in terms of number of counties. Include the state name, number of counties, mean per-capita income, median
per-capita income, and poverty rate. 

 To display numeric data in your table to two decimal places, use f-string formatting. For example, an f-string
to format the contents of a variable number to two decimal places would look like f"{number:.2f}".

Go back in your Python program and remove the thousands option when reading the CSV. What is the result of
running your program, and why is that option needed? Include the answer in your Google Doc.
'''

df = pd.read_csv("county_economic_status_2024.csv", skiprows = 4, 
skipfooter = 2, engine = "python", thousands = ',')

df.columns = ['fips','state','county','arc_county', 'Economic Status', 'Average Unemployment Rate', 'Market Income', 'Poverty Rate', 'Average Unemp. Rate', 'PCMI Percent of US', 'Percent of US Inversed', 'Poverty Rate Percent', 'Composite Index Value', 'Index Value Rank', 'Quartile']
df = df.iloc[1:]


poverty_average = df['Poverty Rate'].mean()
poverty_std = df['Poverty Rate'].std()
poverty_min = df['Poverty Rate'].min()
poverty_max = df['Poverty Rate'].max()

print(f"The mean Poverty Rate is: {poverty_average}")

print(f"The standard deviation Poverty Rate is: {poverty_std}")

print(f"The minimum Poverty Rate is: {poverty_min}")

print(f"The maximum Poverty Rate is: {poverty_max}")


