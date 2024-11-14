import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px


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
# Colores personalizados para cada negocio
colores_negocios = {
    "EL BODEGON": "red",
    "LA MARINA": "green",
    "PROGRESSA": "purple"
}

def crear_grafico_dispersión(hojas_seleccionadas, negocios_seleccionados, departamento, plazo_meses, eje_x, eje_y):
    df_combined = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas], ignore_index=True)
    
    # Filtra los datos por los negocios seleccionados, departamento y plazo
    df_filtrado = df_combined[df_combined["NEGOCIO"].isin(negocios_seleccionados)]
    if departamento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO / PRODUCTO"] == departamento]
    if plazo_meses != "Todos":
        df_filtrado = df_filtrado[df_filtrado["PLAZO MESES"] == plazo_meses]
    
    # Filtra por el umbral de CARTERA CAPITAL TOTAL y limpia datos
    df_filtrado = df_filtrado[df_filtrado["CARTERA CAPITAL TOTAL"] >= 100000]
    df_filtrado = df_filtrado[df_filtrado["TASA"] == "CON TASA"]
    df_filtrado = df_filtrado.dropna(subset=[eje_x, eje_y])
    df_filtrado = df_filtrado[(df_filtrado[eje_x] != 0) & (df_filtrado[eje_y] != 0)]

    # Crea gráfico de dispersión interactivo con plotly
    fig = px.scatter(
        df_filtrado, 
        x=eje_x, 
        y=eje_y,
        color="NEGOCIO",
        size="CARTERA CAPITAL TOTAL",
        hover_name="DEPARTAMENTO / PRODUCTO",
        text="DEPARTAMENTO / PRODUCTO",
        hover_data={
        "PLAZO MESES": True,
        "CARTERA CAPITAL TOTAL": True,
        eje_x: True,
        eje_y: True
    },
        color_discrete_map=colores_negocios,
        title=f"Gráfico de dispersión para negocios seleccionados - {plazo_meses} meses" if plazo_meses != "Todos" else "Gráfico de dispersión para negocios seleccionados - Todos los periodos"

    )

    fig.update_layout(
        xaxis_title=eje_x,
        yaxis_title=eje_y,
        legend_title="Negocios",
        template="simple_white"
    )

    st.plotly_chart(fig)




# Función para crear el gráfico combinado de barras y línea
def crear_grafico_barras_linea(df, negocio, plazo_meses):
    # Filtra los datos por negocio y por plazo, o todos los periodos
    df_filtrado = df[df["NEGOCIO"] == negocio]
    if plazo_meses != "Todos":
        df_filtrado = df_filtrado[df_filtrado["PLAZO MESES"] == plazo_meses]
    # Filtra por el umbral de CARTERA CAPITAL TOTAL
    df_filtrado = df_filtrado[df_filtrado["CARTERA CAPITAL TOTAL"] >= 100000]
    # Continua con el proceso de filtrado y generación del gráfico como antes
    df_filtrado = df_filtrado.dropna(subset=["RRR", "%USGAAP 90 PONDERADO"])
    df_filtrado = df_filtrado[(df_filtrado["RRR"] != 0)]
    df_filtrado = df_filtrado.sort_values(by='RRR', ascending=False)

    fig, ax1 = plt.subplots(figsize=(15, 7), dpi=800)
    barplot = sns.barplot(x='DEPARTAMENTO / PRODUCTO', y='RRR', data=df_filtrado, palette="coolwarm", dodge=False, edgecolor='black', ax=ax1)
    for i, row in enumerate(df_filtrado.itertuples()):
        barplot.text(i, row.RRR + 0.02, f"{row.RRR:.1f}x", ha="center", fontweight='bold', fontsize=10)

    ax1.set_xlabel("Departamento / Producto")
    ax1.set_ylabel("RRR")
    ax1.set_title(f"Gráfico de barras para {negocio} - {plazo_meses} meses" if plazo_meses != "Todos" else f"Gráfico de barras para {negocio} - Todos los periodos")
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
negocios_disp = st.multiselect("Selecciona los negocios para el gráfico de dispersión:", options=list(colores_negocios.keys()))
# Obtener los plazos únicos disponibles en los datos
# Selector de plazo en meses con opción de "Todos"
# Cambia el slider por un selectbox que incluya la opción "Todos los periodos"
plazo_meses_disp = st.selectbox("Selecciona el plazo (en meses) para el gráfico de dispersión:", options=["Todos"] + list(range(1, 60)), index=1)
# Filtro dinámico de departamentos en función de los negocios y las hojas seleccionadas
if hojas_seleccionadas_disp and negocios_disp:
    df_seleccionado = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_disp], ignore_index=True)
    departamentos_filtrados = df_seleccionado[df_seleccionado["NEGOCIO"].isin(negocios_disp)]["DEPARTAMENTO / PRODUCTO"].unique()
    departamento_disp = st.selectbox("Selecciona el departamento para el gráfico de dispersión:", options=["Todos"] + list(departamentos_filtrados))
else:
    departamento_disp = "Todos"

# Define las opciones limitadas para los ejes X e Y
opciones_columnas = ["%USGAAP 90 PONDERADO", "RRR", "RRR (con margen)", "MARGEN", "TASA ACTIVA PONDERADA"]

# Selecciona la columna para el eje X y el eje Y, usando solo las opciones permitidas
eje_x = st.selectbox("Selecciona la variable para el Eje X en el gráfico de dispersión:", opciones_columnas)
eje_y = st.selectbox("Selecciona la variable para el Eje Y en el gráfico de dispersión:", opciones_columnas)

# Mostrar gráfico de dispersión
crear_grafico_dispersión(hojas_seleccionadas_disp, negocios_disp, departamento_disp, plazo_meses_disp, eje_x, eje_y)

# Widgets para el gráfico de barras y línea
st.header("Gráfico de Barras y Línea")
hoja_seleccionada_barras = st.selectbox("Selecciona la hoja para el gráfico de barras y línea:", list(dfs.keys()))

# Carga directamente el DataFrame sin usar pd.concat
df_barras = dfs[hoja_seleccionada_barras]
negocios_barras = dfs["TOTAL CARTERA_resumen"]["NEGOCIO"].unique()
negocio_barras = st.selectbox("Selecciona el negocio para el gráfico de barras y línea:", negocios_barras)
plazo_meses_barras = st.selectbox("Selecciona el plazo (en meses) para el gráfico de barras y línea:", options=["Todos"] + list(range(1, 25)), index=1)


#df_barras = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_barras], ignore_index=True)

# Mostrar gráfico de barras y línea
crear_grafico_barras_linea(df_barras, negocio_barras, plazo_meses_barras)
