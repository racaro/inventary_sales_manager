import streamlit as st
import pandas as pd
from datetime import datetime
from src.utils.data_handler import ExcelHandler
from src.utils import general_functions as gf

EXCEL_FILE = "Template_Manu.xlsx"
SHEET_NAME = "Variables template"
excel_path = "src/data/" + EXCEL_FILE

data = ExcelHandler(excel_path, SHEET_NAME)
st.set_page_config(layout="wide")
st.title("Gestión de Inventario y Ventas")
# data_frame = data.load_data()
# df_columns_upper = [col.upper() for col in data_frame.columns]
col1, col2, col3, col4 = st.columns([6, 6, 6, 6])

with col1:
    fecha = st.date_input("Fecha de venta", value=datetime.today())
    producto = st.selectbox("Producto", ["", "Sembra 2023", "Otro"])
    accion = st.selectbox("Acción", ["", "Venta", "Etiquetado", "Embotellado", "Otro"])

with col2:
    cantidad = st.number_input("Botellas vendidas", min_value=1, step=1)
    precio_venta = st.selectbox("Precio de venta", ["", 7.5, 9, 12, 14])

with col3:
    metodo_pago = st.selectbox("Método de pago", ["", "Bizum", "Efectivo", "Factura", "Otro"])
    cliente = st.selectbox("Tipo de cliente", ["", "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"])

with col4:
    observaciones = st.text_area("Observaciones")
    precio_total = gf.calculate_total_price(cantidad, precio_venta) if precio_venta and cantidad else 0
    st.markdown(f"**Precio total venta:** {precio_total:.2f} €")

if st.button("Guardar venta"):
    if not accion or not precio_venta or not producto or not cliente:
        st.error("Por favor, completa todos los campos obligatorios.")
    else:
        new_sale = {
            "Fecha": fecha,
            "acción": accion,
            "Producto": producto.lower(),
            "num bot": cantidad,
            "precio total": precio_total,
            "precio botella": precio_total / cantidad if cantidad > 0 else 0,
            "cliente": cliente,
            "observaciones": observaciones,
            "Método de pago": metodo_pago
        }

        data.append_sale(new_sale, sheet_name=SHEET_NAME)
        st.success("Venta guardada correctamente")

with st.expander("Historial de Ventas"):
    data_frame = data.load_data()
    st.dataframe(data_frame, use_container_width=True)

with st.expander("Resumen de Ventas"):
    summary = data.get_summary()
    st.write(summary)
    st.bar_chart(summary)