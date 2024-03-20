# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create a simple dataset using pandas
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 34, 29, 32],
        'City': ['New York', 'Paris', 'Berlin', 'London']}
df = pd.DataFrame(data)

# Display the DataFrame
print("DataFrame:")
print(df)

# Basic calculation: Average age
average_age = np.mean(df['Age'])
print("\nAverage Age:", average_age)

# Visualize the ages using a bar chart
plt.figure(figsize=(8, 4))
plt.bar(df['Name'], df['Age'], color='skyblue')
plt.xlabel('Name')
plt.ylabel('Age')
plt.title('Age of Individuals')
plt.show()
