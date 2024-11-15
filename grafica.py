import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
import plotly.express as px
import random


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
colores_variables = {var: f"#{random.randint(0, 0xFFFFFF):06x}" for var in ejes_y}


def crear_grafico_dispersión_extendido(hojas_seleccionadas, negocios_seleccionados, departamento, plazo_meses, eje_x, ejes_y):
    df_combined = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas], ignore_index=True)
    
    # Filtrar los datos
    df_filtrado = df_combined[df_combined["NEGOCIO"].isin(negocios_seleccionados)]
    if departamento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO / PRODUCTO"].isin(departamento)]
    if plazo_meses != "Todos":
        df_filtrado = df_filtrado[df_filtrado["PLAZO MESES"] == plazo_meses]
    
    df_filtrado = df_filtrado[df_filtrado["CARTERA CAPITAL TOTAL"] >= 100000]
    df_filtrado = df_filtrado[df_filtrado["TASA"] == "CON TASA"]
    df_filtrado = df_filtrado.dropna(subset=[eje_x] + ejes_y)
    
    # Crear figura
    fig = go.Figure()
    
    # Agregar puntos y líneas para cada variable seleccionada en el eje Y
    for eje_y in ejes_y:
        fig.add_trace(go.Scatter(
            x=df_filtrado[eje_x],
            y=df_filtrado[eje_y],
            mode='markers+lines',
            marker=dict(color=colores_variables[eje_y], size=10, opacity=0.7),
            line=dict(color=colores_variables[eje_y], width=1),
            name=f"{eje_y} (círculos y líneas)"
        ))
    
    # Ajustar el diseño
    fig.update_layout(
        title="Gráfico de dispersión con múltiples variables en el eje Y",
        xaxis_title=eje_x,
        yaxis_title="Variables del eje Y",
        legend_title="Variables",
        height=650
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
    df_filtrado = df_filtrado.dropna(subset=["RRR", "%USGAAP 90 PONDERADO"])
    df_filtrado = df_filtrado[df_filtrado["RRR"] != 0]
    df_filtrado = df_filtrado.sort_values(by='RRR', ascending=False)
    
    # Crear gráfico de barras y línea en plotly
    fig = go.Figure()
    
    # Gráfico de barras para RRR
    fig.add_trace(go.Bar(
        x=df_filtrado['DEPARTAMENTO / PRODUCTO'],
        y=df_filtrado['RRR'],
        name='RRR',
        marker_color='blue',
        text=[f"{rrr:.1f}x" for rrr in df_filtrado['RRR']],  # Mostrar valores en cada barra
        textposition='outside'
    ))
    
    # Gráfico de línea para %USGAAP 90 PONDERADO
    fig.add_trace(go.Scatter(
        x=df_filtrado['DEPARTAMENTO / PRODUCTO'],
        y=df_filtrado['%USGAAP 90 PONDERADO'],
        name='%USGAAP 90 PONDERADO',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(width=2)
    ))
    
    # Configuración del diseño
    fig.update_layout(
        title=f"Gráfico de barras y línea para {negocio} - {plazo_meses} meses" if plazo_meses != "Todos" else f"Gráfico de barras y línea para {negocio} - Todos los periodos",
        xaxis_title="Departamento / Producto",
        yaxis_title="RRR",
        yaxis2=dict(
            title="%USGAAP 90 PONDERADO",
            overlaying='y',
            side='right'
        ),
        legend=dict(title="Indicadores"),
        height=700
    )
    
    fig.update_traces(textfont_size=10)
    fig.update_xaxes(tickangle=80)
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
# Título de la aplicación
st.title("Análisis de RRR y Morosidad")

# Widgets para el gráfico de dispersión
st.header("Gráfico de Dispersión")
hojas_seleccionadas_disp = st.multiselect("Selecciona las hojas:", list(dfs.keys()), default=["TOTAL CARTERA_resumen"])
negocios_disp = st.multiselect("Selecciona los negocios:", options=list(colores_negocios.keys()))
# Obtener los plazos únicos disponibles en los datos
# Selector de plazo en meses con opción de "Todos"
# Cambia el slider por un selectbox que incluya la opción "Todos los periodos"
plazo_meses_disp = st.selectbox("Selecciona el plazo (en meses):", options=["Todos"] + list(range(1, 60)), index=1)
# Filtro dinámico de departamentos en función de los negocios y las hojas seleccionadas
# Filtro dinámico de departamentos en función de los negocios y las hojas seleccionadas
if hojas_seleccionadas_disp and negocios_disp:
    df_seleccionado = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_disp], ignore_index=True)
    departamentos_filtrados = df_seleccionado[df_seleccionado["NEGOCIO"].isin(negocios_disp)]["DEPARTAMENTO / PRODUCTO"].unique()
    departamentos_seleccionados = st.multiselect("Selecciona los departamentos:", options=["Todos"] + list(departamentos_filtrados), default="Todos")
else:
    departamentos_seleccionados = ["Todos"]

# Modificar el filtro en función de la selección múltiple de departamentos
if "Todos" in departamentos_seleccionados:
    departamento_disp = "Todos"
else:
    departamento_disp = departamentos_seleccionados
# Define las opciones limitadas para los ejes X e Y
opciones_columnas = ["%USGAAP 90 PONDERADO", "RRR", "RRR (con margen)", "MARGEN", "TASA ACTIVA PONDERADA"]

# Selecciona la columna para el eje X y el eje Y, usando solo las opciones permitidas
eje_x = st.selectbox("Selecciona la variable para el Eje X:", opciones_columnas)
# Filtro dinámico de departamentos en función de los negocios y las hojas seleccionadas
if hojas_seleccionadas_disp and negocios_disp:
    df_seleccionado = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_disp], ignore_index=True)
    departamentos_filtrados = df_seleccionado[df_seleccionado["NEGOCIO"].isin(negocios_disp)]["DEPARTAMENTO / PRODUCTO"].unique()
    departamentos_seleccionados = st.multiselect("Selecciona los departamentos para el gráfico de dispersión:", options=["Todos"] + list(departamentos_filtrados), default=["Todos"])
    
    # Verifica si se seleccionó "Todos"
    if "Todos" in departamentos_seleccionados:
        departamento_disp = "Todos"
    else:
        departamento_disp = departamentos_seleccionados
else:
    departamento_disp = "Todos"  # Valor predeterminado si no hay selección de hojas o negocios

# Verifica que haya al menos un negocio y una hoja seleccionados antes de llamar a la función
if hojas_seleccionadas_disp and negocios_disp:
    # Mostrar gráfico de dispersión
    crear_grafico_dispersión(hojas_seleccionadas_disp, negocios_disp, departamento_disp, plazo_meses_disp, eje_x, eje_y)
else:
    st.warning("Por favor, selecciona al menos una hoja y un negocio para generar el gráfico.")

# Mostrar gráfico de dispersión
crear_grafico_dispersión_extendido(hojas_seleccionadas_disp, negocios_disp, departamento_disp, plazo_meses_disp, eje_x, ejes_y)

# Widgets para el gráfico de barras y línea
st.header("Gráfico de Barras y Línea")
hoja_seleccionada_barras = st.selectbox("Selecciona la hoja:", list(dfs.keys()))

# Carga directamente el DataFrame sin usar pd.concat
df_barras = dfs[hoja_seleccionada_barras]
negocios_barras = dfs["TOTAL CARTERA_resumen"]["NEGOCIO"].unique()
negocio_barras = st.selectbox("Selecciona el negocio:", negocios_barras)
plazo_meses_barras = st.selectbox("Selecciona el plazo (en meses):", options=["Todos"] + list(range(1, 25)), index=1)


#df_barras = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_barras], ignore_index=True)

# Mostrar gráfico de barras y línea
crear_grafico_barras_linea(df_barras, negocio_barras, plazo_meses_barras)
