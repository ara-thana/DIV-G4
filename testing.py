import pandas as pd

# Load the large CSV file
input_file = 'TMDB_movie_dataset_1.csv'
df = pd.read_csv(input_file)

# Get the total number of rows in the file
total_rows = len(df)

# Calculate the number of rows per file (split into 5)
rows_per_file = total_rows // 5

# Split and save to smaller files
for i in range(5):
    start_row = i * rows_per_file
    # For the last file, take all remaining rows
    if i == 4:
        smaller_df = df[start_row:]
    else:
        smaller_df = df[start_row:start_row + rows_per_file]
    
    output_file = f'data/TMDB_movie_dataset_1_{i+1}.csv'
    smaller_df.to_csv(output_file, index=False)
    print(f'Saved {output_file}')