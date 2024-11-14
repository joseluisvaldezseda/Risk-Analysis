import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
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
    # Combinar los datos de las hojas seleccionadas
    df_combined = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas], ignore_index=True)
    
    # Filtrar los datos por negocios, departamento y plazo
    df_filtrado = df_combined[df_combined["NEGOCIO"].isin(negocios_seleccionados)]
    if departamento != "Todos":
        df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO / PRODUCTO"].isin(departamento)]
    if plazo_meses != "Todos":
        df_filtrado = df_filtrado[df_filtrado["PLAZO MESES"] == plazo_meses]
    
    # Filtrar por el umbral de CARTERA CAPITAL TOTAL y condiciones adicionales
    df_filtrado = df_filtrado[df_filtrado["CARTERA CAPITAL TOTAL"] >= 100000]
    df_filtrado = df_filtrado[df_filtrado["TASA"] == "CON TASA"]
    df_filtrado = df_filtrado.dropna(subset=[eje_x, eje_y])
    df_filtrado = df_filtrado[(df_filtrado[eje_x] != 0) & (df_filtrado[eje_y] != 0)]
    
    # Crear gráfico de dispersión interactivo con etiquetas visibles
    fig = px.scatter(
        df_filtrado,
        x=eje_x,
        y=eje_y,
        size="CARTERA CAPITAL TOTAL",
        color="NEGOCIO",
        color_discrete_map=colores_negocios,
        hover_name="DEPARTAMENTO / PRODUCTO",
        hover_data={
            "PLAZO MESES": True,
            "CARTERA CAPITAL TOTAL": True,
            eje_x: True,
            eje_y: True
        },
        text="DEPARTAMENTO / PRODUCTO",  # Agregar etiquetas estáticas
        title=f"Gráfico de dispersión para negocios seleccionados - {plazo_meses} meses" if plazo_meses != "Todos" else "Gráfico de dispersión para negocios seleccionados - Todos los periodos",
        size_max=50  # Ajusta este valor para incrementar el tamaño máximo de los círculos
    )
    
    # Ajustes de la visualización
    fig.update_traces(
        textposition='middle right',  # Posición de las etiquetas a la derecha del círculo
        textfont=dict(size=8),        # Tamaño de la etiqueta
        marker=dict(opacity=0.6, line=dict(width=1, color='DarkSlateGrey'))
    )
    fig.update_layout(
        xaxis_title=eje_x,
        yaxis_title=eje_y,
        legend_title="Negocios",
        height=650
    )
    
    # Mostrar el gráfico en Streamlit
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
hojas_seleccionadas_disp = st.multiselect("Selecciona las hojas para el gráfico de dispersión:", list(dfs.keys()), default=["TOTAL CARTERA_resumen"])
negocios_disp = st.multiselect("Selecciona los negocios para el gráfico de dispersión:", options=list(colores_negocios.keys()))
# Obtener los plazos únicos disponibles en los datos
# Selector de plazo en meses con opción de "Todos"
# Cambia el slider por un selectbox que incluya la opción "Todos los periodos"
plazo_meses_disp = st.selectbox("Selecciona el plazo (en meses) para el gráfico de dispersión:", options=["Todos"] + list(range(1, 60)), index=1)
# Filtro dinámico de departamentos en función de los negocios y las hojas seleccionadas
# Filtro dinámico de departamentos en función de los negocios y las hojas seleccionadas
if hojas_seleccionadas_disp and negocios_disp:
    df_seleccionado = pd.concat([dfs[hoja] for hoja in hojas_seleccionadas_disp], ignore_index=True)
    departamentos_filtrados = df_seleccionado[df_seleccionado["NEGOCIO"].isin(negocios_disp)]["DEPARTAMENTO / PRODUCTO"].unique()
    departamentos_seleccionados = st.multiselect("Selecciona los departamentos para el gráfico de dispersión:", options=["Todos"] + list(departamentos_filtrados), default="Todos")
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
