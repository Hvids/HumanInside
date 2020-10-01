import  pandas as pd
from tqdm import tqdm
path_pd_cc = '../../data/csv/cultural_centers.csv'

df = pd.read_csv(path_pd_cc)

from ParserPage import ParserPassport

lats = []
longs = []
for i, row in tqdm(df.iterrows(),desc='Update Geo'):
    if pd.isna(row.latitude):
        lat, long = ParserPassport.get_geo_by_adress(row.adress)
        lats.append(lat)
        longs.append(long)
    else:
        lats.append(row['latitude'])
        longs.append(row['logitute'])
df['latitude'] = lats
df['logitute'] = longs

df.to_csv(path_pd_cc, index=False)