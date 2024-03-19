import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# Cargar el conjunto de datos
@st.cache_data
def load_data():
    df = pd.read_csv("google_scholar_analysis2.csv")
    return df


st.header('Indicadores de impacto científico de Agrosavia', divider='rainbow')
df = load_data()
indices = ['pergoomet_hindex', 'pergoomet_awindex',
           'pergoomet_eindex','pergoomet_gindex','pergoomet_hcindex']


col1, col2, col3, col4, col5 = st.columns(5)

hindex=  round(df['pergoomet_hindex'].mean())
awindex=  round(df['pergoomet_awindex'].mean(),2)
eindex= round(df['pergoomet_eindex'].mean(),2)
gindex= round(df['pergoomet_gindex'].mean())
hcindex= round(df['pergoomet_hcindex'].mean())

col1.metric("h index", hindex)
col2.metric("aw Index", awindex)
col3.metric("e index",  eindex)
col4.metric("g index",  eindex)
col5.metric("hc index",  eindex)

# Obtener la lista única de valores para la columna de interés
options = sorted(df['nombre'].unique())

# Crear una caja de lista para seleccionar el valor
selected_option = st.selectbox('Seleccionar el nombre de la persona:', options)

# Filtrar el DataFrame según la selección
filtered_df = df[df['nombre'] == selected_option]

grupos = filtered_df['uniorg_nombre'].unique()


select_data = df[df['uniorg_nombre'].isin(grupos)]
# Mostrar el DataFrame filtrado
# Group data together

rango_hindex = range(0, select_data['pergoomet_hindex'].max()+1)
hist_data = select_data[['nombre','pergoomet_hindex','uniorg_nombre']].pivot('nombre', 'uniorg_nombre','pergoomet_hindex')
#st.write(select_data[['nombre','pergoomet_hindex']])
#st.write(hist_data)

datos = pd.DataFrame(0, index=range(len(rango_hindex)), columns=grupos)
datos['hindex'] = rango_hindex

#st.dataframe(hist_data[grupos[0]].dropna().astype('int').value_counts())
# Mostrar el DataFrame
#print(dict(hist_data[grupos[0]].dropna().astype('int').value_counts()))

for grupo in grupos:
    valores = dict(hist_data[grupo].dropna().astype('int').value_counts())
    mask = datos['hindex'].isin(valores.keys())
    datos.loc[mask, grupo] = datos.loc[mask,'hindex'].replace(valores)
#st.dataframe(datos)

# Crear una figura de Plotly con gráfico de barras
fig = go.Figure()

# Agregar las barras para cada columna
for column in datos[grupos].columns:  # Ignorar la primera columna ('Categoria')
    fig.add_trace(go.Bar(x=datos['hindex'], y=datos[column], name=column))

# Agregar línea vertical punteada roja en un valor específico de x
 # Este valor específico debe estar presente en el eje x
valor_especifico_x = filtered_df[filtered_df['nombre'] == selected_option]['pergoomet_hindex'].unique()
fig.add_vline(x=int(valor_especifico_x), line_dash='dash', line_color='red', line_width=5)

# Agregar anotación para describir la línea roja punteada
# fig.add_annotation(x=valor_especifico_x, y=datos.max().min(), text="h index personal", showarrow=True,
#                    arrowhead=0, ax=-valor_especifico_x, ay=-300)
# Actualizar el diseño del gráfico
fig.update_layout(
    title='Frecuencia de valores',
    xaxis_title='h index',
    yaxis_title='Cantidad de personas con este valor',
    barmode='group',  # Agrupar las barras
    width=800,  # Ancho de la figura en píxeles
    height=600,  # Altura de la figura en píxeles
    legend=dict(x=0.5, y=1.0)
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
# Texto con diferentes colores
# Texto con diferentes colores
texto_colores = """
<span style="color:red">----   </span> Valor de h index para la persona seleccionada.
"""

# Mostrar texto con diferentes colores
st.markdown(texto_colores, unsafe_allow_html=True)

st.dataframe(hist_data)