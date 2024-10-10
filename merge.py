import pandas as pd
archivo_informacion = r'C:\Users\María Fernández\Documents\4º año\DIV\informacion_peliculas_scraping.xlsx'
archivo_platforms = r'C:\Users\María Fernández\Documents\4º año\DIV\movies_and_platforms.xlsx'
df_informacion = pd.read_excel(archivo_informacion)
df_platforms = pd.read_excel(archivo_platforms)
df_informacion['Title'] = df_informacion['Title'].str.lower()
df_platforms['Title'] = df_platforms['Title'].str.lower()
df_merged = pd.merge(df_informacion, df_platforms[['Title', 'Platforms']], on='Title', how='left')
df_merged['Title'] = df_merged['Title'].str.title()
nombre_archivo_salida = r'C:\Users\María Fernández\Documents\4º año\DIV\informacion_peliculas_con_platforms.xlsx'
df_merged.to_excel(nombre_archivo_salida, index=False)

print(f"File saved as '{nombre_archivo_salida}'")
