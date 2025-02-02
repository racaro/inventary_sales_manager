import pandas as pd
import os

class ExcelHandler:
    def __init__(self, data_folder, sheet_name):
        """
        Inicializa la clase con la ruta del archivo y el nombre de la hoja.
        :param data_folder: Ruta del directorio de datos.
        :param sheet_name: Nombre de la hoja del archivo Excel.
        """
        self.data_folder = data_folder
        self.sheet_name = sheet_name
        self.file_path = self._find_excel_file()
        self.columns = ["Fecha de venta", "Accion", "Producto", "Botellas vendidas", "Precio total venta", "Precio botella", "Cliente", "Observaciones", "Metodo de pago"]

    def _find_excel_file(self):
        """
        Busca un archivo Excel en el directorio de datos.
        :return: Ruta del archivo Excel.
        """
        files = [f for f in os.listdir(self.data_folder) if f.endswith(".xlsx")]
        if not files:
            raise FileNotFoundError(f"No se encontró ningún archivo Excel en {self.data_folder}.")
        return os.path.join(self.data_folder, files[0])
    
    def load_data(self, sheet_name=None):
        """
        Carga los datos desde el archivo Excel.
        :param sheet_name: Nombre de la hoja donde se cargarán los datos.
        :return: DataFrame con los datos cargados.
        """
        sheet = sheet_name if sheet_name else self.sheet_name
        try:
            data = pd.read_excel(self.file_path, sheet_name=sheet)
            return data
        except FileNotFoundError:
            return pd.DataFrame()
        
    def clean_data(self, data):
        """
        Limpia los datos del archivo Excel que tengan columnas vacías a partir del tamaño de columnas.
        :param data: DataFrame con los datos a limpiar.
        :param columns: Lista con los nombres de las columnas.
        :return: DataFrame con los datos limpios.
        """
        data_set = data.iloc[:, :len(self.columns)]
        data_set_clean = data_set[~data_set["Accion"].isin(["Embotellado", "embotellado", "Etiquetado", "etiquetado"])]
        return data_set_clean

    def save_data(self, data, sheet_name=None):
        """
        Carga los datos desde el archivo Excel.
        :param df: DataFrame con los datos a guardar.
        :param sheet_name: Nombre de la hoja donde se guardarán los datos.
        :return: DataFrame con los datos cargados.
        """
        sheet = sheet_name if sheet_name else self.sheet_name
        with pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            data.to_excel(writer, sheet_name=sheet, index=False)

    def append_sale(self, data, new_sale, sheet_name=None):
        """
        Agrega una nueva fila (venta) al archivo Excel.
        :param data: DataFrame con los datos actuales.
        :param new_sale: Diccionario con los datos de la nueva venta.
        :return: DataFrame con los datos actualizados.
        """
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

    def get_summary(self, data):
        """
        Devuelve un resumen estadístico de las ventas por producto.
        :param df: DataFrame con los datos de las ventas.
        :return: Diccionario con el resumen de ventas.
        """
        try:
            if "Producto" in data.columns:
                data["Producto"] = data["Producto"].astype(str).str.lower()
            summary = data.groupby("Producto")["Precio total venta"].sum()
            return summary
        except Exception as e:
            raise RuntimeError(f"Error al generar el resumen: {e}")
