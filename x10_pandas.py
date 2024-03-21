import pandas as pd
# import zipfile
import requests


def f01_create_df_from_dict():
    # Creating a basic example dataset
    data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emily'],
    'Age': [25, 30, 22, 35, 28],
    'Salary': [50000, 60000, 45000, 70000, 55000],
    'Department': ['HR', 'Finance', 'IT', 'Marketing', 'HR']
    }

    df = pd.DataFrame(data)
    csv_file = ('employee.csv')
    df.to_csv(csv_file)

    return df


def f01a_save_df_to_csv():
    pass

def f02_create_df_from_list():
    # List of planets
    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # Create a DataFrame from the list
    planets_df = pd.DataFrame(planets, columns=['Planet'])

    # Size of each planet (example values, fictional)
    planet_sizes = [0.383, 0.949, 1.00, 0.532, 11.21, 9.45, 4.01, 3.88]

    # Create a DataFrame from the list
    planets_df = pd.DataFrame(planets, columns=['Planet'])

    # Add a 'Size' column to the DataFrame
    planets_df['Size (Earth = 1)'] = planet_sizes
    # Display the DataFrame

    print(planets_df)
    return planets_df


def f03_create_df_from_csv():
    csv_file = ('employee.csv')
    df.read_csv(csv_file)
    print(df)

def download_from_kaggle():
    #import kaggle

    # Download the dataset (this requires the Kaggle API credentials set up)
    #kaggle.datasets.download('vinicius150987/titanic3', path='./', unzip=True)
    pass

def f04_create_df_from_json():
    url = 'https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json'
    response = requests.get(url)
    json_data = response.json()
    
    # Assuming the JSON structure has a key 'elements' containing the data
    elements_data = json_data['elements']
    df = pd.DataFrame(elements_data)
    
    # Optionally, save the DataFrame to a local file
    
    df.to_json('data/pandas/period_table.json', orient='records', lines=True, indent=4)
    
    return df


def f05_create_df_from_read_html():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    # Use the first match to the table of S&P 500 companies
    df_list = pd.read_html(url, match='Symbol')
    # Assuming the first table is the S&P 500 list
    df = df_list[0]
    df.to_csv('data/pandas/sp500_wikipedia.csv')
    print(df)
    
    # Assuming you have a DataFrame named df
    # Change the CIK column to string type
    df['CIK'] = df['CIK'].astype(str)

    # Assuming you have a DataFrame named df
    # Convert 'Date Added' and 'Founded' columns to datetime
    df['Date Added'] = pd.to_datetime(df['Date Added'])
    df['Founded'] = pd.to_datetime(df['Founded'])
    
    # Check the DataFrame to ensure the changes have been made
    print(df.dtypes)
   
    # Display basic information about the DataFrame
    print(df.info())

    # Descriptive statistics of numeric columns
    print(df.describe())

    # Handling missing values (dropna or fillna)
    df.dropna(inplace=True)
    # OR
    df.fillna(0, inplace=True)

    # Grouping and aggregating data
    # grouped_df = df.groupby('Department').agg({'Salary': 'mean', 'Age': 'max'})
    grouped_df = df.groupby('GICS Sector'))
    print(grouped_df)

    return df


def medart_20_codes():
    # https://towardsdev.com/20-pandas-codes-to-elevate-your-data-analysis-skills-85e1be818b08
    
    import pandas as pd

    # Creating a basic example dataset dict of lists
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emily'],
        'Age': [25, 30, 22, 35, 28],
        'Salary': [50000, 60000, 45000, 70000, 55000],
        'Department': ['HR', 'Finance', 'IT', 'Marketing', 'HR']
    }

    df = pd.DataFrame(data)
    print(df)

    # Display basic information about the DataFrame
    df.info()

    # Descriptive statistics of numeric columns
    df.describe()

    # Handling missing values (dropna or fillna)
    df.dropna(inplace=True)
    # OR
    df.fillna(0, inplace=True)

    # Grouping and aggregating data
    grouped_df = df.groupby('Department').agg({'Salary': 'mean', 'Age': 'max'})
    print(grouped_df)

    # Filtering data based on conditions
    filtered_df = df[df['Age'] > 25]
    print(filtered_df)

    # Sorting data
    sorted_df = df.sort_values(by='Salary', ascending=False)
    print(sorted_df)

    # Creating new columns
    df['Bonus'] = df['Salary'] * 0.1


    # Merging DataFrames
    other_data = {
        'Department': ['HR', 'Finance', 'IT'],
        'Location': ['City1', 'City2', 'City3']
    }

    other_df = pd.DataFrame(other_data)
    merged_df = pd.merge(df, other_df, on='Department', how='left')
    print(merged_df)

    # Creating a pivot table
    pivot_table = df.pivot_table(index='Department', values='Salary', aggfunc='mean')
    print(pivot_table)

    # Data visualization with Pandas
    #import matplotlib.pyplot as plt

    df.plot(kind='bar', x='Name', y='Salary', title='Salary Distribution')
    #plt.show()

    # Applying a custom function to a column
    df['Salary'] = df['Salary'].apply(lambda x: x + 5000)

    # Removing duplicates based on a subset of columns
    df.drop_duplicates(subset=['Name'], keep='first', inplace=True)

    # Renaming columns
    df.rename(columns={'Salary': 'MonthlySalary'}, inplace=True)

    # String operations on a column
    df['NameLength'] = df['Name'].apply(len)


    # Binning data into intervals
    bins = [0, 30, 40, 50, float('inf')]
    labels = ['<30', '30-40', '40-50', '50+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)


def medart_iterator():
    import pandas as pd
    import numpy as np

    # Sample data: A list of dictionaries
    data = [
        {'Name': 'Alice', 'Age': 30, 'City': 'New York'},
        {'Name': 'Bob', 'Age': 25, 'City': 'Paris'},
        {'Name': 'Charlie', 'Age': 35, 'City': 'London'}
    ]
    # Creating a DataFrame
    df = pd.DataFrame(data)
    print(df)

    # Iterrows
    for index, row in df.iterrows():
        print(f"Index: {index}, Name: {row['Name']}, Age: {row['Age']}, City: {row['City']}")

    # Itertuples    
    for row in df.itertuples(index=True, name='Pandas'):
        print(f"Index: {row.Index}, Name: {row.Name}, Age: {row.Age}, City: {row.City}")

    # Using iterrows() to filter rows
    filtered_rows = [row for index, row in df.iterrows() if row['Age'] > 30]
    print(pd.DataFrame(filtered_rows))

    # Using itertuples() for the same operation
    filtered_rows = [row for row in df.itertuples(index=False) if row.Age > 30]
    print(pd.DataFrame(filtered_rows))

    # Define a condition to filter rows (e.g., age greater than 30)
    # Apply the condition to filter the rows
    filtered_df = df[df['Age'] > 30]

    # Print the filtered DataFrame
    print(filtered_df)


    # Define a custom function to apply
    def custom_operation(row):
        return f"{row['Name']} from {row['City']} is {row['Age']} years old."

    # Apply the function across each row
    df['Description'] = df.apply(custom_operation, axis=1)
    print(df[['Description']])

    # Vectorized operation to calculate a new column
    df['AgeNextYear'] = df['Age'] + 1
    print(df[['Name', 'Age', 'AgeNextYear']])

    # Using apply() to classify rows
    def age_group(row):
        if row['Age'] < 30:
            return 'Young'
        else:
            return 'Mature'

    df['AgeGroup'] = df.apply(age_group, axis=1)
    print(df[['Name', 'Age', 'AgeGroup']])

    # Vectorized approach for classifying rows
    df['AgeGroup'] = np.where(df['Age'] < 30, 'Young', 'Mature')
    print(df[['Name', 'Age', 'AgeGroup']])



def main():
    
    employee_df = f01_create_df_from_dict()
    #print(employee_df)
    #planets_df = f02_create_df_from_list()
  
    #err elements_df  = f03_create_df_from_csv()
    #ok  elements_df  = f04_create_df_from_json()
    #err download_from_kaggle()
    #ok sp500_df = f05_create_df_from_read_html()

    #ok medart_20_codes()
    #medart_iterator()


main()

#####################################################################
# Deprecated Code
#####################################################################
def f03_create_df_from_csv():
    """
    Reads a CSV file from the given URL and returns a DataFrame.
    
    Parameters:
    - url: str, The URL to the CSV file.
    
    Returns:
    - DataFrame containing the data read from the CSV file.

    https://www.kaggle.com/datasets/vinicius150987/titanic3/download?datasetVersionNumber=1
    """
    try:
        # Read the CSV file from the URL
        url = 'https://www.kaggle.com/datasets/vinicius150987/titanic3/download?datasetVersionNumber=1'
        df = pd.read_csv(url)
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

    if df is not None:
        print(df.head())  # Display the first few rows of the DataFrame
