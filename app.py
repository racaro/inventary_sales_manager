import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from datetime import datetime
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
    producto = st.selectbox("Producto", ["", "Sembra 2023"])
    cantidad = st.number_input("Botellas vendidas", min_value=1, step=1)
    precio_total_venta = st.number_input("Precio total venta", min_value=0.0, step=0.1)
    metodo_pago = st.selectbox("Método de pago", ["", "Bizum", "Efectivo", "Factura", "Otro"])
    cliente = st.selectbox("Tipo de cliente", ["", "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"])
    observaciones = st.text_area("Observaciones")
    accion = st.selectbox("Acción", ["", "Venta", "Etiquetado", "Embotellado", "Otro"])

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
    stock_inicial = 1850
    botellas_consumidas = sum(data_frame['Botellas vendidas'])
    stock_actual = stock_inicial - botellas_consumidas
    ventas_totales = round(sum(data_frame['Precio total venta']), 2)
    precio_medio = round(ventas_totales / sum(data_frame['Botellas vendidas']), 2)

    st.title("Visualización de Cálculos")
    st.markdown(f"""
        <style>
        .box-container {{ display: flex; justify-content: space-between; }}
        .box {{ display: flex; align-items: center; justify-content: center;
                flex-direction: column; height: 80px; width: 150px;
                border-radius: 10px; margin: 10px; font-size: 12px; font-weight: bold; }}
        .box1 {{ background-color: rgba(255, 182, 193, 0.5); }}
        .box2 {{ background-color: rgba(144, 238, 144, 0.5); }}
        .box3 {{ background-color: rgba(135, 206, 250, 0.5); }}
        .box4 {{ background-color: rgba(255, 215, 0, 0.5); }}
        </style>
        <div class="box-container">
            <div class="box box1">Stock disponible<br><span style="font-size: 24px;">{stock_actual}</span></div>
            <div class="box box2">Botellas vendidas<br><span style="font-size: 24px;">{botellas_consumidas}</span></div>
            <div class="box box3">Precio medio botella<br><span style="font-size: 24px;">{precio_medio}€</span></div>
            <div class="box box4">Beneficio bruto<br><span style="font-size: 24px;">{ventas_totales}€</span></div>
        </div>
    """, unsafe_allow_html=True)

st.title("Historial de Ventas")
with st.expander("Ver historial de ventas"):
    st.dataframe(data_frame, use_container_width=True)

with st.expander("Resumen de Ventas"):
    summary = data.get_summary(data_frame)
    st.write(summary)
    st.bar_chart(summary)
