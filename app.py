import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from src.utils.data_handler import ExcelHandler
from src.utils import general_functions as gf

SHEET_NAME = "Variables template"
excel_path = "src/data/"
stock_inicial = 1850
data = ExcelHandler(excel_path, SHEET_NAME)
st.set_page_config(layout="wide")
st.title("Gestión de Inventario y Ventas")

# 🔄 Cargar y limpiar datos
def load_sales():
    return data.clean_data(data.load_data(sheet_name=SHEET_NAME))

data_frame = load_sales()

modal = Modal(key="confirm_modal", title="Confirmar datos de la venta")

with st.sidebar:
    if "fecha" not in st.session_state:
        st.session_state["fecha"] = datetime.now()
    if "producto" not in st.session_state:
        st.session_state["producto"] = ""
    if "cantidad" not in st.session_state:
        st.session_state["cantidad"] = 1
    if "precio_total_venta" not in st.session_state:
        st.session_state["precio_total_venta"] = 0.0
    if "metodo_pago" not in st.session_state:
        st.session_state["metodo_pago"] = ""
    if "cliente" not in st.session_state:
        st.session_state["cliente"] = ""
    if "observaciones" not in st.session_state:
        st.session_state["observaciones"] = ""
    if "accion" not in st.session_state:
        st.session_state["accion"] = ""

    fecha = st.date_input("Fecha de venta", value=datetime.now())
    accion = st.selectbox("Acción", ["Venta", "Etiquetado", "Embotellado", "Otro"])
    producto = st.selectbox("Producto", ["Sembra 2023"])
    cantidad = st.number_input("Botellas vendidas", min_value=1, step=1)
    precio_total_venta = st.number_input("Precio total venta", min_value=0.0, step=0.1)
    metodo_pago = st.selectbox("Método de pago", ["Bizum", "Efectivo", "Factura", "Otro"])
    cliente = st.selectbox("Tipo de cliente", ["Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"])
    observaciones = st.text_area("Observaciones")

    if st.button("Guardar venta"):
        if not accion or not producto or not cliente:
            st.error("Completa todos los campos obligatorios.")
        else:
            st.session_state["new_sale"] = {
                "Fecha de venta": fecha,
                "Accion": accion,
                "Producto": producto.lower(),
                "Botellas vendidas": cantidad,
                "Precio total venta": precio_total_venta,
                "Precio botella": round(precio_total_venta / cantidad if cantidad > 0 else 0, 2),
                "Cliente": cliente,
                "Observaciones": observaciones,
                "Metodo de pago": metodo_pago
            }
            modal.open()

if modal.is_open():
    with modal.container():
        st.write("<h3 style='text-align:center;'>¿Los siguientes datos son correctos?</h3>", unsafe_allow_html=True)
        st.table(pd.DataFrame([st.session_state["new_sale"]]))

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Confirmar", key="confirmar"):
                data.append_sale(st.session_state["new_sale"], sheet_name=SHEET_NAME)
                st.success("Guardado correctamente")
                modal.close()
                st.session_state["data_updated"] = True
                st.session_state["fecha"] = datetime.now()
                st.session_state["producto"] = ""
                st.session_state["cantidad"] = 1
                st.session_state["precio_total_venta"] = 0.0
                st.session_state["metodo_pago"] = ""
                st.session_state["cliente"] = ""
                st.session_state["observaciones"] = ""
                st.session_state["accion"] = ""
                st.experimental_rerun()

        with col3:
            if st.button("❌ Cancelar", key="cancelar"):
                st.warning("Cancelado.")
                modal.close()

if "data_updated" in st.session_state and st.session_state["data_updated"]:
    data_frame = load_sales()
    st.session_state["data_updated"] = False

if len(data_frame):
    # Realizar cálculos adicionales
    botellas_consumidas = sum(data_frame['Botellas vendidas'])
    stock_actual = stock_inicial - botellas_consumidas
    ventas_totales = round(sum(data_frame['Precio total venta']), 2)
    precio_medio = round(ventas_totales / sum(data_frame['Botellas vendidas']), 2)

    # Visualización de cálculos
    st.subheader("Visualización de Cálculos")
    st.markdown(f"""
        <style>
        .box-container {{
            display: flex;
            justify-content: space-between;
        }}
        .box {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            height: 80px;
            width: 150px;
            border-radius: 10px;
            margin: 10px;
            font-size: 12px;
            font-weight: bold;
        }}
        .box1 {{ background-color: rgba(255, 182, 193, 0.5); }}  /* lightcoral con 50% transparencia */
        .box2 {{ background-color: rgba(144, 238, 144, 0.5); }}  /* lightgreen con 50% transparencia */
        .box3 {{ background-color: rgba(135, 206, 250, 0.5); }}  /* lightskyblue con 50% transparencia */
        .box4 {{ background-color: rgba(255, 215, 0, 0.5); }}  /* gold con 50% transparencia */
        </style>
        <div class="box-container">
            <div class="box box1">
                Stock disponible<br>
                <span style="font-size: 24px;">{stock_actual}</span>
            </div>
            <div class="box box2">
                Botellas consumidas<br>
                <span style="font-size: 24px;">{botellas_consumidas}</span>
            </div>
            <div class="box box3">
                Precio medio botella<br>
                <span style="font-size: 24px;">{precio_medio}€</span>
            </div>
            <div class="box box4">
                Beneficio bruto<br>
                <span style="font-size: 24px;">{ventas_totales}€</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.subheader("Resumen de Ventas por tipo de Cliente")
    summary_cliente_bar = data.get_summary_TipoCliente_bar(data_frame)
    st.write(summary_cliente_bar)
    fig_bar = go.Figure(data=[go.Bar(x=summary_cliente_bar.index, y=summary_cliente_bar.values, marker_color='#DA70D6')])  # Lila pastel
    fig_bar.update_layout(title_text="Ventas por Cliente", xaxis_title="Cliente", yaxis_title="Botellas vendidas")
    st.plotly_chart(fig_bar)

with col2:
    st.subheader("Resumen de Ventas por tipo de Cliente")
    summary_cliente_pie = data.get_summary_TipoCliente_pie(data_frame)
    fig_pie = go.Figure(data=[go.Pie(labels=summary_cliente_pie.index, values=summary_cliente_pie.values, hole=.3,
                                     marker=dict(colors=['#FFC0CB', '#DDA0DD', '#E6E6FA', '#C71585']))])  # Granate, morado, lila pastel
    fig_pie.update_layout(title_text="Ventas por Cliente")
    st.plotly_chart(fig_pie)

with col3:
    st.subheader("Resumen de Ventas por tipo de Venta")
    summary_venta_bar = data.get_summary_TipoVenta_bar(data_frame)
    st.write(summary_venta_bar)
    fig_venta_bar = go.Figure(data=[go.Bar(x=summary_venta_bar.index, y=summary_venta_bar.values, marker_color='#9370DB')])  # Morado pastel
    fig_venta_bar.update_layout(title_text="Ventas por Método de Pago", xaxis_title="Método de Pago", yaxis_title="Precio Total Venta")
    st.plotly_chart(fig_venta_bar)
    
st.markdown("<br><br>", unsafe_allow_html=True) 
   
with st.expander("Historial de Ventas"):
    st.dataframe(data_frame, use_container_width=True)
