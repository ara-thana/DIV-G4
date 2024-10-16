import pandas as pd

# informacion_peliculas_con_platforms.xlsx was edited manually for a smoother merge
archivo_1 = 'informacion_peliculas_con_platforms_edited.xlsx'
archivo_2 = '../data/output/archivo_actualizado_tmdb.xlsx'
df1 = pd.read_excel(archivo_1)
df2 = pd.read_excel(archivo_2)
combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df.to_excel('../data/output/archivo_combinado.xlsx', index=False)