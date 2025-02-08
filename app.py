import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from src.utils.data_handler import ExcelHandler

SHEET_NAME = "Variables template"
excel_path = "src/data/"
stock_inicial = 1850
data = ExcelHandler(excel_path, SHEET_NAME)
st.set_page_config(layout="wide")
st.markdown(
"<div style='text-align: center; font-size: 40px; font-weight: bold;'>GESTIÓN DE INVENTARIO Y VENTAS</div>",
unsafe_allow_html=True
)

def load_sales():
    return data.clean_data(data.load_data(sheet_name=SHEET_NAME))

data_frame = load_sales()
modal_append = Modal(key="confirm_modal", title="Confirmar datos de la venta")
modal_remove = Modal(key="confirm_modal_remove", title="Confirmar datos de la venta a eliminar")

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
    accion = st.selectbox("Acción", ["Seleccione", "Venta", "Otro"], index=0)
    producto = st.selectbox("Producto", ["Seleccione", "Sembra 2023"], index=0)
    cantidad = st.number_input("Botellas vendidas", min_value=1, step=1)
    precio_total_venta = st.number_input("Precio total venta", min_value=0.0, step=0.1)
    metodo_pago = st.selectbox("Método de pago", ["Seleccione", "Bizum", "Efectivo", "Factura", "Otro"], index=0)
    cliente = st.selectbox("Tipo de cliente", ["Seleccione", "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"], index=0)
    observaciones = st.text_area("Observaciones")

    left, right = st.columns(2)    
    
    with left:
        if st.button("Guardar venta", key="guardar_venta", use_container_width=True):
            if producto == "Seleccione" or metodo_pago == "Seleccione" or cliente == "Seleccione" or accion == "Seleccione":
                st.error("Completa todos los campos obligatorios.")
            else:
                st.session_state["new_sale"] = {
                    "Fecha de venta": fecha,
                    "Accion": accion.upper(),
                    "Producto": producto.upper(),
                    "Botellas vendidas": cantidad,
                    "Precio total venta": round(precio_total_venta, 2),
                    "Precio botella": round(precio_total_venta / cantidad if cantidad > 0 else 0, 2),
                    "Cliente": cliente.upper(),
                    "Observaciones": observaciones,
                    "Metodo de pago": metodo_pago.upper()
                }
                modal_append.open()
    
    number = st.selectbox("Seleccione la venta a eliminar", range(data_frame.shape[0]))
    
    with right:
        if st.button("Eliminar venta", type="primary", key="eliminar_venta", use_container_width=True) and data_frame.shape[0] > 0:
            modal_remove.open()

if modal_append.is_open():
    with modal_append.container():
        st.write("<h3 style='text-align:center;'>¿Los siguientes datos son correctos?</h3>", unsafe_allow_html=True)
        st.table(pd.DataFrame([st.session_state["new_sale"]]))
        col1, _, col3 = st.columns(3)
        with col1:
            if st.button("✅ Confirmar", key="confirmar"):
                data.append_sale(st.session_state["new_sale"], sheet_name=SHEET_NAME)
                st.success("Guardado correctamente")
                modal_append.close()
                st.session_state["data_updated"] = True
                st.session_state["fecha"] = datetime.now()
                st.session_state["producto"] = "Seleccionar"
                st.session_state["cantidad"] = 1
                st.session_state["precio_total_venta"] = 0.0
                st.session_state["metodo_pago"] = "Seleccionar"
                st.session_state["cliente"] = "Seleccionar"
                st.session_state["observaciones"] = ""
                st.session_state["accion"] = "Seleccionar"
                st.experimental_rerun()

        with col3:
            if st.button("❌ Cancelar", key="cancelar"):
                st.warning("Cancelado.")
                modal_append.close()
    
if modal_remove.is_open():
    with modal_remove.container():
        st.write("<h3 style='text-align:center;'>¿Los siguientes datos son correctos?</h3>", unsafe_allow_html=True)
        st.table(data_frame.iloc[[number]])
        col1, _, col3 = st.columns(3)
        with col1:
            if st.button("✅ Confirmar", key="confirmar"):
                data.remove_sale(number)
                st.success("Eliminado correctamente")
                modal_remove.close()
                st.session_state["data_updated"] = True
                st.experimental_rerun()

        with col3:
            if st.button("❌ Cancelar", key="cancelar"):
                st.warning("Cancelado.")
                modal_remove.close()

if "data_updated" in st.session_state and st.session_state["data_updated"]:
    data_frame = load_sales()
    st.session_state["data_updated"] = False

if len(data_frame):
    botellas_consumidas = sum(data_frame['Botellas vendidas'])
    stock_actual = stock_inicial - botellas_consumidas
    ventas_totales = round(sum(data_frame['Precio total venta']), 2)
    precio_medio = round(ventas_totales / sum(data_frame['Botellas vendidas']), 2)

    st.subheader("Visualización de cálculos")
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

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Resumen de ventas por cliente", divider=True)
    summary_cliente_bar = data.get_summary(data_frame, "Cliente", "Botellas vendidas")
    fig_bar = go.Figure(data=[go.Bar(x=summary_cliente_bar.index, y=summary_cliente_bar.values, marker_color='#DA70D6')])
    fig_bar.update_layout(title_text="Evolución de ventas por cliente", xaxis_title="Cliente", yaxis_title="Botellas vendidas")
    st.plotly_chart(fig_bar)
    summary_cliente_pie = data.get_summary(data_frame, "Cliente", "Botellas vendidas")
    fig_pie = go.Figure(data=[go.Pie(labels=summary_cliente_pie.index, values=summary_cliente_pie.values, hole=.3,
                                     marker=dict(colors=['#FFC0CB', '#DDA0DD', '#E6E6FA', '#C71585']))])
    st.plotly_chart(fig_pie)

with col2:
    st.subheader("Resumen de ventas por tipo de venta", divider=True)
    summary_venta_bar = data.get_summary(data_frame, "Metodo de pago", "Precio total venta")
    fig_venta_bar = go.Figure(data=[go.Bar(x=summary_venta_bar.index, y=summary_venta_bar.values, marker_color='#9370DB')])
    fig_venta_bar.update_layout(title_text="Evolución de ventas por método de pago", xaxis_title="Método de pago", yaxis_title="Precio total venta")
    st.plotly_chart(fig_venta_bar)
    _, col2, _ = st.columns([1, 4, 1])
    with col2: 
        st.write(summary_venta_bar)
    
st.markdown("<br><br>", unsafe_allow_html=True) 
   
with st.expander("Historial de ventas"):
    st.dataframe(data_frame, use_container_width=True)
