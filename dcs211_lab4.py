import  pandas as pd
#import matplotlib.pyplot
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


def main():
    #top_states()
    #bottom_states()
    #county_poverty_rates()
    printTableBy(df, 'Poverty Rate', 10, "counties by poverty rate")
    printTableBy(df, 'Market Income', 10, "counties by pci")
    printTableBy(df, 'Average Unemployment Rate', 10, "counties by Average Unemployment Rate")

main()