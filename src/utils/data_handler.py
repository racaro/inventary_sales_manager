import pandas as pd

class ExcelHandler:
    def __init__(self, file_path, sheet_name="Sheet1"):
        """
        Inicializa la clase con la ruta del archivo y el nombre de la hoja.
        """
        self.file_path = file_path
        self.sheet_name = sheet_name

    def load_data(self):
        """
        Carga los datos desde el archivo Excel.
        :return: DataFrame con los datos cargados.
        """
        try:
            data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            return data
        except Exception as e:
            raise FileNotFoundError(f"Error al cargar el archivo Excel: {e}")

    def save_data(self, df):
        """
        Guarda un DataFrame en el archivo Excel.
        :param df: DataFrame que se guardará.
        """
        try:
            with pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name=self.sheet_name, index=False)
        except Exception as e:
            raise RuntimeError(f"Error al guardar los datos en el archivo Excel: {e}")

    def append_sale(self, new_sale):
        """
        Agrega una nueva fila (venta) al archivo Excel.
        :param new_sale: Diccionario con los datos de la venta.
        """
        try:
            df = self.load_data()
            df = pd.concat([df, pd.DataFrame([new_sale])], ignore_index=True)
            self.save_data(df)
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
