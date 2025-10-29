import  pandas as pd
#import matplotlib.pyplot
from prettytable import PrettyTable

df = pd.read_csv("county_economic_status_2024.csv", skiprows = 4, 
skipfooter = 2, engine = "python", thousands = ",")

df.columns = ['fips','state','county','arc_county', 'Economic Status', 'Average Unemployment Rate', 'Market Income', 'Poverty Rate', 'Average Unemp. Rate', 'PCMI Percent of US', 'Percent of US Inversed', 'Poverty Rate Percent', 'Composite Index Value', 'Index Value Rank', 'Quartile']
df = df.iloc[1:]


def poverty_stats():
    poverty_average = df['Poverty Rate'].mean()
    poverty_std = df['Poverty Rate'].std()
    poverty_min = df['Poverty Rate'].min()
    poverty_max = df['Poverty Rate'].max()
    print(f"The mean Poverty Rate is: {poverty_average}")
    print(f"The standard deviation Poverty Rate is: {poverty_std}")
    print(f"The minimum Poverty Rate is: {poverty_min}")
    print(f"The maximum Poverty Rate is: {poverty_max}")

def top_states():
    county_counts = df['state'].value_counts()

    table_top = PrettyTable()
    table_top.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]
    table_top.align["State"] = "l"
    for state, count in county_counts.head(10).items():
        state_data = df[df["state"] == state]
        mean_pci = state_data["Market Income"].mean()
        median_pci = state_data["Market Income"].median()
        poverty = state_data["Poverty Rate"].mean()
        table_top.add_row([state,count,f"{mean_pci:.2f}",f"{median_pci:.2f}",f"{poverty:.2f}"])
    print(table_top)

def bottom_states():
    county_counts = df['state'].value_counts()
    table_bottom = PrettyTable()
    table_bottom.field_names = ["State", "# counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]
    table_bottom.align["State"] = "l"
    for state, count in county_counts.tail(10).items():
        state_data = df[df["state"] == state]
        mean_pci = state_data["Market Income"].mean()
        median_pci = state_data["Market Income"].median()
        poverty = state_data["Poverty Rate"].mean()
        table_bottom.add_row([state,count,f"{mean_pci:.2f}",f"{median_pci:.2f}",f"{poverty:.2f}"])
        if state == "District of Columbia":
            del table_bottom._rows[9]
    print(table_bottom)


'''
Now include code to print a PrettyTable displaying information of the top ten counties (regardless of state) by
decreasing poverty rate. Include the state, county, per capita income, poverty rate, and average unemployment.
Your table should look like:
'''

def county_poverty_rates():
    count_10_poverty = df.sort_values(by='Poverty Rate', ascending=False).head(10)
    table_county = PrettyTable()
    table_county.field_names = ["State", "County", "PCI", "Poverty Rate", "Avg Unemployment"]
    table_county.align["State"] = "l"
    for county, row in count_10_poverty.iterrows():
        table_county.add_row([row["state"], row["county"], f"{row['Market Income']:.2f}", f"{row['Poverty Rate']:.2f}", f"{row['Average Unemployment Rate']:.2f}"])
    print(table_county)





def main():
    top_states()
    bottom_states()
    county_poverty_rates()

main()
