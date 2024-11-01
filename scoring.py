import pandas as pd
import matplotlib.pyplot as plt

# name of exported Qualtrics survey file
survey_path = "survey.csv"

df = pd.read_csv(survey_path)
df = df.iloc[:,17:]

model_1_rankings = []
model_2_rankings = []
model_3_rankings = []
model_4_rankings = []
model_5_rankings = []

# Group columns by model suffixes
for col in df:
    if col.endswith('_1'):
        model_1_rankings.append(df[col][2:])
    elif col.endswith('_2'):
        model_2_rankings.append(df[col][2:])
    elif col.endswith('_3'):
        model_3_rankings.append(df[col][2:])
    elif col.endswith('_4'):
        model_4_rankings.append(df[col][2:])
    elif col.endswith('_8'):
        model_5_rankings.append(df[col][2:])

# Convert grouped lists into DataFrames
model_1_df = pd.DataFrame(model_1_rankings)
model_1_df = model_1_df.apply(pd.to_numeric, errors='coerce')

model_2_df = pd.DataFrame(model_2_rankings)
model_2_df = model_2_df.apply(pd.to_numeric, errors='coerce')

model_3_df = pd.DataFrame(model_3_rankings)
model_3_df = model_3_df.apply(pd.to_numeric, errors='coerce')

model_4_df = pd.DataFrame(model_4_rankings)
model_4_df = model_4_df.apply(pd.to_numeric, errors='coerce')

model_5_df = pd.DataFrame(model_5_rankings)
model_5_df = model_5_df.apply(pd.to_numeric, errors='coerce')

# Model 1 scores
# model average across all prompts
total_average_1 = model_1_df.stack().mean()
# model average for each prompt
row_averages_1 = model_1_df.mean(axis=1)

# Model 2 scores
# model average across all prompts
total_average_2 = model_2_df.stack().mean()
# model average for each prompt
row_averages_2 = model_2_df.mean(axis=1)

# Model 3 scores
# model average across all prompts
total_average_3 = model_3_df.stack().mean()
# model average for each prompt
row_averages_3 = model_3_df.mean(axis=1)

# Model 4 scores
# model average across all prompts
total_average_4 = model_4_df.stack().mean()
# model average for each prompt
row_averages_4 = model_4_df.mean(axis=1)

# Model 5 scores
# model average across all prompts
total_average_5 = model_5_df.stack().mean()
# model average for each prompt
row_averages_5 = model_5_df.mean(axis=1)

models = ["aMUSEd", "Dall-E-Mini", "SDV1-4", "SD-base", "SDXLTurbo"]
averages = [total_average_1, total_average_2, total_average_3, total_average_4, total_average_5]
plt.figure(figsize=(8, 5))
plt.bar(models, averages, color='skyblue')
plt.xlabel("Models")
plt.ylabel("Average Score")
plt.title("Histogram of Model Averages")
plt.show()
