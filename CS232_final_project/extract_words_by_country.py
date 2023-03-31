import pandas as pd

df = pd.read_csv(r'/Users/veronica/Desktop/CS232_final_project/clothing_prompts_results - clothing_prompts_results.csv')

#df = df[(df['country'] == 'US_CA')| (df['country'] == 'Neutral')]
df = df[['country','pred1', 'pred2', 'pred3','pred4','pred5','pred6']]
df = df.sort_values(by=['country'], ascending=True)

# clean data
df['pred1'] = df['pred1'].map(lambda x: x.strip('OTHER').strip(':').strip('\n'))
df['pred2'] = df['pred2'].map(lambda x: x.strip('OTHER').strip(':').strip('\n'))
df['pred3'] = df['pred3'].map(lambda x: x.strip('OTHER').strip(':').strip('\n'))
df['pred4'] = df['pred4'].map(lambda x: x.strip('OTHER').strip(':').strip('\n'))
df['pred5'] = df['pred5'].map(lambda x: x.strip('OTHER').strip(':').strip('\n'))
df['pred6'] = df['pred6'].map(lambda x: x.strip('OTHER').strip(':').strip('\n'))
print(df)

df.to_csv('/Users/veronica/Desktop/CS232_final_project/words_extracted(CA+Neutral).csv')