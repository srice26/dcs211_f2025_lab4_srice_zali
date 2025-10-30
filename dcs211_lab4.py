import  pandas as pd
import matplotlib.pyplot as plt
import requests
from prettytable import PrettyTable

df = pd.read_csv("county_economic_status_2024.csv", skiprows = 4, 
skipfooter = 2, engine = "python", thousands = ",")

df.columns = ['fips','state','county','arc_county', 'Economic Status', 'Average Unemployment Rate', 'Market Income', 'Poverty Rate', 'Average Unemp. Rate', 'PCMI Percent of US', 'Percent of US Inversed', 'Poverty Rate Percent', 'Composite Index Value', 'Index Value Rank', 'Quartile']
df = df.iloc[1:]

def poverty_stats() -> None:
    '''
    prints useful messages to provide data statistics
    args = none
    returns = none
    '''
    poverty_average = df['Poverty Rate'].mean()
    poverty_std = df['Poverty Rate'].std()
    poverty_min = df['Poverty Rate'].min()
    poverty_max = df['Poverty Rate'].max()
    print(f"The mean Poverty Rate is: {poverty_average}")
    print(f"The standard deviation Poverty Rate is: {poverty_std}")
    print(f"The minimum Poverty Rate is: {poverty_min}")
    print(f"The maximum Poverty Rate is: {poverty_max}")

def top_states() -> None:
    '''
    prints table including top 10 states in terms of number of counties 
    args = none
    returns = none
    '''

    county_counts = df['state'].value_counts()

    table_top = PrettyTable()
    table_top.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]
    table_top.align["State"] = "l"
    table_top.align["County"] = "l"
    for state, count in county_counts.head(10).items():
        state_data = df[df["state"] == state]
        mean_pci = state_data["Market Income"].mean()
        median_pci = state_data["Market Income"].median()
        poverty = state_data["Poverty Rate"].mean()
        table_top.add_row([state,count,f"{mean_pci:.2f}",f"{median_pci:.2f}",f"{poverty:.2f}"])
    print(table_top)

def bottom_states() -> None:
    '''
    prints table including bottom 10 states in terms of number of counties, excluding DC
    args = none
    returns = none
    '''
    county_counts = df['state'].value_counts()
    table_bottom = PrettyTable()
    table_bottom.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]
    table_bottom.align["State"] = "l"
    table_bottom.align["County"] = "l"
    for state, count in county_counts.tail(10).items():
        state_data = df[df["state"] == state]
        mean_pci = state_data["Market Income"].mean()
        median_pci = state_data["Market Income"].median()
        poverty = state_data["Poverty Rate"].mean()
        table_bottom.add_row([state,count,f"{mean_pci:.2f}",f"{median_pci:.2f}",f"{poverty:.2f}"])
        if state == "District of Columbia":
            del table_bottom._rows[9]
    print(table_bottom)

def county_poverty_rates() -> None:
    '''
    prints table displaying information of the top ten counties (regardless of state) by
    decreasing poverty rate
    args = none
    returns = none
    '''
    count_10_poverty = df.sort_values(by='Poverty Rate', ascending=False).head(10)
    table_county = PrettyTable()
    table_county.field_names = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]
    table_county.align["State"] = "l"
    table_county.align["County"] = "l"
    for county, row in count_10_poverty.iterrows():
        table_county.add_row([row["state"], row["county"], f"{row['Market Income']:.2f}", f"{row['Poverty Rate']:.2f}", f"{row['Average Unemployment Rate']:.2f}"])
    print(table_county)

def printTableBy(dataframe: pd, field: str, how_many: int, title: str) -> None:   
    '''
    prints table displaying the top ten or bottom ten counties based on poverty rate, per capitaincome, or average unemployment
    args:
        - dataframe: pd, overall pandas dataframe
        - field: str, what is being measured
        - how_many: int, number of rows for top and bottom separately
        - title: str, title of table
    returns = none
    '''
    table_data = PrettyTable()
    sort_by_head = df.sort_values(by=field, ascending=False).head(how_many)
    table_data.field_names = ["State", "County", "PCI", field , "Avg Unemployment"]
    table_data.align["State"] = "l"
    table_data.align["County"] = "l"
    for i, row in sort_by_head.iterrows():
        table_data.add_row([row["state"], row["county"], f"{row['Market Income']:.2f}", f"{row[field]:.2f}", f"{row['Average Unemployment Rate']:.2f}"])
    table_data.add_divider()
    sort_by_tail = df.sort_values(by=field, ascending=False).tail(how_many).iloc[::-1]
    for i, row in sort_by_tail.iterrows():
        table_data.add_row([row["state"], row["county"], f"{row['Market Income']:.2f}", f"{row[field]:.2f}", f"{row['Average Unemployment Rate']:.2f}"])
    print(title.upper())
    print(table_data)


def createByStateBarPlot(df: pd.DataFrame, field: str, filename: str, title: str, ylabel: str) -> None:
    '''
    prints useful messages to provide data statistics
    args:
        - dataframe: pd, overall pandas dataframe
        - field: str, what is being measured
        - filename: str, name of the file that is being created
        - title: str, title of table
        -ylabel: str, title of the y-axis of the graph
    returns = none
    '''

    us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
    }
    
    abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

    grouped_states = df.groupby("state")[field].mean().sort_values(ascending=True)

    abbrev_list = []
    for state in grouped_states.index:
        if state in us_state_to_abbrev:
            abbrev_list.append(us_state_to_abbrev[state])
    grouped_states.index = abbrev_list

    plt.figure(figsize=(12, 6))
    plt.bar(grouped_states.index, grouped_states.values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main() -> None:
    '''
    used to execute each of the functions above
    args = none
    returns = none
    '''
    top_states()
    bottom_states()
    county_poverty_rates()
    printTableBy(df, 'Poverty Rate', 10, "counties by poverty rate")
    printTableBy(df, 'Market Income', 10, "counties by pci")
    printTableBy(df, 'Average Unemployment Rate', 10, "counties by Average Unemployment Rate")
    createByStateBarPlot(df, 'Poverty Rate', "pov_rate.png", "States By Poverty Rate", "Poverty Rate")
    createByStateBarPlot(df, 'Average Unemployment Rate', "unemp_rate.png", "States By Unemployment Rate", "Employment Rate")
    
main()