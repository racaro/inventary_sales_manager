import pandas as pd

class ExcelHandler:
    def __init__(self, file_path, sheet_name):
        """
        Inicializa la clase con la ruta del archivo y el nombre de la hoja.
        """
        self.file_path = file_path
        self.sheet_name = sheet_name

    def load_data(self, sheet_name=None):
        """Carga los datos desde el archivo Excel."""
        sheet = sheet_name if sheet_name else self.sheet_name
        try:
            data = pd.read_excel(self.file_path, sheet_name=sheet)
            return data
        except FileNotFoundError:
            return pd.DataFrame()

    def save_data(self, df, sheet_name=None):
        """
        Carga los datos desde el archivo Excel.
        :return: DataFrame con los datos cargados.
        """
        sheet = sheet_name if sheet_name else self.sheet_name
        with pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet, index=False)

    def append_sale(self, new_sale, sheet_name=None):
        """Agrega una nueva fila (venta) al archivo Excel."""
        sheet = sheet_name if sheet_name else self.sheet_name
        try:
            df = self.load_data(sheet)

            # Si el archivo estaba vacío, crea un DataFrame con las columnas correctas
            if df.empty:
                df = pd.DataFrame(columns=new_sale.keys())

            # Agregar la nueva venta
            df = pd.concat([df, pd.DataFrame([new_sale])], ignore_index=True)

            # Guardar los cambios en el archivo Excel
            self.save_data(df, sheet)

        except Exception as e:
            raise RuntimeError(f"Error al agregar una nueva venta: {e}")


    def get_summary(self):
        """
        Devuelve un resumen estadístico de las ventas por producto.
        :return: Diccionario con el resumen de ventas.
        """
        try:
            df = self.load_data()
            if "Producto" in df.columns:
                df["Producto"] = df["Producto"].astype(str).str.lower()
            summary = df.groupby("Producto")["precio total"].sum()
            return summary
        except Exception as e:
            raise RuntimeError(f"Error al generar el resumen: {e}")
