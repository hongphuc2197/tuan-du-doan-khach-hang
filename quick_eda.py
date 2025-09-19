import pandas as pd

print('EDA Analysis')
df = pd.read_csv('user_actions_students_576.csv')
print(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users')
print(f'Events: {df["event_type"].value_counts().to_dict()}')
print(f'Ages: {df["age"].min()}-{df["age"].max()}')
print(f'Income: {df["income_level"].value_counts().to_dict()}')
print(f'Education: {df["education"].value_counts().to_dict()}')
print(f'Price range: ${df["price"].min()}-${df["price"].max()}')
print('Done!')
