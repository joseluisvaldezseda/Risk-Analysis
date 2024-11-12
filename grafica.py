import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar estilo de Seaborn
sns.set(style="white")

# Cargar datos
ruta_archivo = 'Resumen_Cartera_Morosidad.xlsx'

# Obtener las hojas disponibles en el archivo
hojas_disponibles = pd.ExcelFile(ruta_archivo).sheet_names

# Título de la aplicación
st.title("Análisis de Cartera y Morosidad")

# Selección de la hoja
hoja = st.selectbox("Selecciona la hoja:", hojas_disponibles)

# Cargar los datos de la hoja seleccionada
df = pd.read_excel(ruta_archivo, sheet_name=hoja)

# Selección de negocio y plazo
negocios = df["NEGOCIO"].unique()
negocio = st.selectbox("Selecciona el negocio:", negocios)
plazo_meses = st.slider("Selecciona el plazo (en meses):", min_value=1, max_value=24, value=6)

# Filtrar los datos según el negocio y plazo, y eliminar filas con valores nulos o cero en RRR y RRR (con margen)
df_filtrado = df[(df["NEGOCIO"] == negocio) & (df["PLAZO MESES"] == plazo_meses)]
df_filtrado = df_filtrado.dropna(subset=["RRR", "RRR (con margen)", "%USGAAP 90 PONDERADO"])
df_filtrado = df_filtrado[(df_filtrado["RRR"] != 0) & (df_filtrado["RRR (con margen)"] != 0)]

# Ordenar el DataFrame por RRR de mayor a menor
df_filtrado = df_filtrado.sort_values(by='RRR', ascending=False)

# Crear gráfico con dos ejes
fig, ax1 = plt.subplots(figsize=(20, 8))

# Graficar las barras de RRR
barplot = sns.barplot(
    x='DEPARTAMENTO / PRODUCTO',
    y='RRR',
    data=df_filtrado,
    palette="coolwarm",
    dodge=False,
    edgecolor='black',
    ax=ax1
)

# Agregar etiquetas a las barras de RRR
for i, row in enumerate(df_filtrado.itertuples()):
    barplot.text(i, row.RRR + 0.02, f"{row.RRR:.1f}x", 
                 color='black', ha="center", fontweight='bold', fontsize=10)

# Configuraciones de gráfico para el eje de barras
ax1.set_xlabel("Departamento / Producto", fontsize=12)
ax1.set_ylabel("RRR", fontsize=12)
ax1.set_title(f"Gráfico de barras para {negocio} - {plazo_meses} meses", fontsize=14)
ax1.tick_params(axis='x', rotation=80, labelsize=10)

# Crear un segundo eje y graficar %USGAAP 90 PONDERADO como una línea
ax2 = ax1.twinx()
ax2.plot(df_filtrado['DEPARTAMENTO / PRODUCTO'], df_filtrado['%USGAAP 90 PONDERADO'], 
         color='red', marker='o', linewidth=2, label="%USGAAP 90 PONDERADO")
ax2.set_ylabel("%USGAAP 90 PONDERADO", fontsize=12, color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Ajustar el gráfico para evitar superposición
fig.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)
