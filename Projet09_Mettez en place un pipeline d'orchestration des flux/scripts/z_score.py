import pandas as pd
df=pd.read_csv("jointure.csv")

mean_price = df['price'].mean()
std_price = df['price'].std()

df['z_score']=((df['price']-mean_price)/std_price).abs()

result= df[df['z_score'] > 2]
result.to_csv("Premiums.csv", index=False)

result= df[df['z_score'] <= 2]
result.to_csv("Ordinaires.csv", index=False)
