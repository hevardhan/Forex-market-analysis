import pandas as pd

# Sample DataFrame
data = {'A': [1, 2, 2, 4, 5]}
df = pd.DataFrame(data)

# Create a 'B' column based on your original condition
df['B'] = df['A'].apply(lambda x: 'Low' if x < 3 else 'High')

# Create a new column 'B_Changes' to track changes in 'B'
df['B_Changes'] = df['B'][df['B'] != df['B'].shift()]

# Fill NaN values in 'B_Changes' with the corresponding 'B' values
# df['B_Changes'].fillna(method='ffill', inplace=True)

# Display the DataFrame
print(df)
