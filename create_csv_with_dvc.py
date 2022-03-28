import pandas as pd

df = pd.read_csv('player_stats.csv', index_col=0)
df.to_csv("dvc_players_stats.csv")