import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar estilo de Seaborn
sns.set_theme(style="white")

# Cargar datos
ruta_archivo = 'Resumen_Cartera_Morosidad.xlsx'
dfs = {
    "TOTAL CARTERA_resumen": pd.read_excel(ruta_archivo, sheet_name="TOTAL CARTERA_resumen"),
    "PRIMERA COMPRA_resumen": pd.read_excel(ruta_archivo, sheet_name="PRIMERA COMPRA_resumen"),
    "RECOMPRA_resumen": pd.read_excel(ruta_archivo, sheet_name="RECOMPRA_resumen")
}

# Expandir el ancho de la aplicación en Streamlit
st.set_page_config(layout="wide")

# Función para crear el gráfico de dispersión
def crear_grafico_dispersión(hojas_seleccionadas, negocio, plazo_meses, eje_x, eje_y):
    df_combined = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas], ignore_index=True)
    df_filtrado = df_combined[(df_combined["NEGOCIO"] == negocio) & (df_combined["PLAZO MESES"] == plazo_meses)]
    df_filtrado = df_filtrado.dropna(subset=[eje_x, eje_y])
    df_filtrado = df_filtrado[(df_filtrado[eje_x] != 0) & (df_filtrado[eje_y] != 0)]

    fig, ax = plt.subplots(figsize=(15, 7),dpi=800)
    sns.scatterplot(
        x=df_filtrado[eje_x],
        y=df_filtrado[eje_y],
        s=df_filtrado["CARTERA CAPITAL TOTAL"] * 0.0001,  # Tamaño de puntos ajustado
        alpha=0.5,
        color='deepskyblue',
        ax=ax
    )
    for i in range(df_filtrado.shape[0]):
        ax.text(df_filtrado[eje_x].iloc[i], df_filtrado[eje_y].iloc[i], df_filtrado["DEPARTAMENTO / PRODUCTO"].iloc[i],
                fontsize=4, ha='right', va='bottom', fontweight='bold', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

    ax.set_xlabel(eje_x)
    ax.set_ylabel(eje_y)
    ax.set_title(f"Gráfico de dispersión para {negocio} - {plazo_meses} meses")
    ax.legend([], [], frameon=False)  # Oculta la leyenda de tamaño
    st.pyplot(fig)

# Función para crear el gráfico combinado de barras y línea
def crear_grafico_barras_linea(df, negocio, plazo_meses):
    df_filtrado = df[(df["NEGOCIO"] == negocio) & (df["PLAZO MESES"] == plazo_meses)]
    df_filtrado = df_filtrado.dropna(subset=["RRR", "RRR (con margen)", "%USGAAP 90 PONDERADO"])
    df_filtrado = df_filtrado[(df_filtrado["RRR"] != 0) & (df_filtrado["RRR (con margen)"] != 0)]
    df_filtrado = df_filtrado.sort_values(by='RRR', ascending=False)

    fig, ax1 = plt.subplots(figsize=(15, 7),dpi=800)
    barplot = sns.barplot(x='DEPARTAMENTO / PRODUCTO', y='RRR', data=df_filtrado, palette="coolwarm", dodge=False, edgecolor='black', ax=ax1)
    for i, row in enumerate(df_filtrado.itertuples()):
        barplot.text(i, row.RRR + 0.02, f"{row.RRR:.1f}x", ha="center", fontweight='bold', fontsize=10)

    ax1.set_xlabel("Departamento / Producto")
    ax1.set_ylabel("RRR")
    ax1.set_title(f"Gráfico de barras para {negocio} - {plazo_meses} meses")
    ax1.tick_params(axis='x', rotation=80, labelsize=10)
    ax1.grid(False)
   
    ax2 = ax1.twinx()
    ax2.plot(df_filtrado['DEPARTAMENTO / PRODUCTO'], df_filtrado['%USGAAP 90 PONDERADO'], color='red', marker='o', linewidth=2)
    ax2.set_ylabel("%USGAAP 90 PONDERADO", color='red')
    fig.tight_layout()
    st.pyplot(fig)

# Título de la aplicación
st.title("Análisis de Cartera y Morosidad")

# Widgets para el gráfico de dispersión
st.header("Gráfico de Dispersión")
hojas_seleccionadas_disp = st.multiselect("Selecciona las hojas para el gráfico de dispersión:", list(dfs.keys()), default=["TOTAL CARTERA_resumen"])
negocios_disp = dfs["TOTAL CARTERA_resumen"]["NEGOCIO"].unique()
negocio_disp = st.selectbox("Selecciona el negocio para el gráfico de dispersión:", negocios_disp)
plazo_meses_disp = st.slider("Selecciona el plazo (en meses) para el gráfico de dispersión:", 1, 24, 6)
columnas_numericas = pd.concat(dfs.values(), ignore_index=True).select_dtypes(include=['float64', 'int64']).columns
eje_x = st.selectbox("Selecciona la variable para el Eje X en el gráfico de dispersión:", columnas_numericas)
eje_y = st.selectbox("Selecciona la variable para el Eje Y en el gráfico de dispersión:", columnas_numericas)

# Mostrar gráfico de dispersión
crear_grafico_dispersión(hojas_seleccionadas_disp, negocio_disp, plazo_meses_disp, eje_x, eje_y)

# Widgets para el gráfico de barras y línea
st.header("Gráfico de Barras y Línea")
hoja_seleccionada_barras = st.selectbox("Selecciona la hoja para el gráfico de barras y línea:", list(dfs.keys()))
negocios_barras = dfs["TOTAL CARTERA_resumen"]["NEGOCIO"].unique()
negocio_barras = st.selectbox("Selecciona el negocio para el gráfico de barras y línea:", negocios_barras)
plazo_meses_barras = st.slider("Selecciona el plazo (en meses) para el gráfico de barras y línea:", 1, 24, 6)

df_barras = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_barras], ignore_index=True)

# Mostrar gráfico de barras y línea
crear_grafico_barras_linea(df_barras, negocio_barras, plazo_meses_barras)
