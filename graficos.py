import os #libreria para interactuar con el sistema operativo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizador:

    def __init__(self, ruta_csv, encoding="utf-8"): #constructor para cargar el dataset
        if not isinstance(ruta_csv, str) or not ruta_csv.strip():
            raise ValueError("`ruta_csv` debe ser una cadena no vacia.")
        if not os.path.isfile(ruta_csv):
            raise FileNotFoundError(f"No se encontro el archivo: {ruta_csv}")
        
        self.ruta_csv = ruta_csv
        try:
            self.df = pd.read_csv(ruta_csv, low_memory=False, encoding=encoding)
        except pd.errors.EmptyDataError:
            raise ValueError(f"El archivo '{ruta_csv}' está vacío.")
        except pd.errors.ParserError as e:
            raise ValueError(f"No se pudo interpretar '{ruta_csv}' como csv: {e}")
        
        if self.df.empty:
            raise ValueError(f"El archivo: '{ruta_csv}' no contiene fila de datos")
        
        print(f"Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")

    # ---- Utilidades internas de validación ------------------------------------

    def _validar_columnas(self, columnas):
        faltantes = [c for c in columnas if c not in self.df.columns]
        if faltantes:
            disponibles = ", ".join(self.df.columns)
            raise KeyError(
                f"Las siguientes columnas no existen en el dataset: {faltantes}. "
                f"Columnas disponibles: {disponibles}"
            )

    def _a_numerico(self, serie, nombre_columna):
        original_no_nulos = serie.notna().sum()
        convertida = pd.to_numeric(serie, errors="coerce")
        nuevos_nulos = convertida.isna().sum() - serie.isna().sum()

        if nuevos_nulos > 0:
            print(
                f"Aviso: {nuevos_nulos} de {original_no_nulos} valores en "
                f"'{nombre_columna}' no son numéricos y se convirtieron a NaN."
            )
        return convertida

    def _filtrar(self, filtros):
        if filtros:
            self._validar_columnas(filtros.keys())

        mask = pd.Series(True, index=self.df.index)
        for columna, valor in (filtros or {}).items():
            if isinstance(valor, (list, tuple, set)):
                mask &= self.df[columna].isin(valor)
            else:
                mask &= (self.df[columna] == valor)

        data = self.df[mask].copy()
        if data.empty:
            raise ValueError(
                f"El filtro aplicado {filtros} no arrojó ninguna fila. "
                "Verifique los valores de filtrado."
            )
        return data

    # ---- Transformación -------------------------------------------------------

    def preparar_datos(self, columnas, filtros=None, columnas_numericas=None, ordenar_por=None):

        self._validar_columnas(columnas)

        duplicadas = {c for c in columnas if columnas.count(c) > 1}
        if duplicadas:
            raise ValueError(
                f"Las columnas {sorted(duplicadas)} se repiten en la selección "
                f"{columnas}. Cada parámetro (columna_x, columna_y, columna_grupo) "
                "debe referirse a una columna distinta."
            )

        data = self._filtrar(filtros) if filtros else self.df.copy()
        data = data[columnas].copy()

        for col in (columnas_numericas or []):
            data[col] = self._a_numerico(data[col], col)

        if ordenar_por:
            self._validar_columnas([ordenar_por])
            data = data.sort_values(ordenar_por)

        return data.reset_index(drop=True)

    # ---- Guardado centralizado ------------------------------------------------

    def _guardar(self, fig, nombre_archivo):
        directorio = os.path.dirname(nombre_archivo)
        if directorio and not os.path.isdir(directorio):
            os.makedirs(directorio, exist_ok=True)

        try:
            fig.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
        except Exception as e:
            print(f"No se pudo guardar la gráfica en '{nombre_archivo}': {e}")
            return
        print(f"Gráfica guardada como: {nombre_archivo}")

    # ---- Visualización --------------------------------------------------------

    def grafica_barras_agrupadas(
            self,
            columna_x,
            columna_y,
            columna_grupo,
            filtros=None,
            paleta=None,
            titulo="",
            etiqueta_x="",
            etiqueta_y="",
            mostrar=True,
            guardar=False,
            nombre_archivo="barras.png"
    ):
        data = self.preparar_datos(
            columnas=[columna_x, columna_y, columna_grupo],
            filtros=filtros,
            columnas_numericas=[columna_y],
            ordenar_por=columna_x,
        )

        fig, ax = plt.subplots(figsize=(14, 6))
        sns.barplot(data=data, x=columna_x, y=columna_y, hue=columna_grupo, palette=paleta, ax=ax, errorbar=None)
        ax.set_title(titulo, fontsize=13, fontweight="bold", pad=14)
        ax.set_xlabel(etiqueta_x or columna_x, fontsize=11)
        ax.set_ylabel(etiqueta_y or columna_y, fontsize=11)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.legend(title=columna_grupo)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()

        if guardar:
            self._guardar(fig, nombre_archivo)
        if mostrar:
            plt.show()
        else:
            plt.close(fig)
        return fig


# ---- Uso ------------------------------------------------------------------

def _pedir_filtro_opcional():
    resp = input("¿Quiere filtrar filas antes de graficar? (s/n): ").strip().lower()
    if resp != "s":
        return None

    columna = input("Columna a filtrar (ej. SEXO): ").strip()
    valores = input(
        "Valor(es) a incluir, separados por coma (ej. Hombres,Mujeres): "
    ).strip()
    lista_valores = [v.strip() for v in valores.split(",") if v.strip()]
    if not lista_valores:
        return None
    if len(lista_valores) == 1:
        return {columna: lista_valores[0]}
    return {columna: lista_valores}


def _menu_interactivo():
    ruta = input("Ruta del archivo CSV: ").strip()
    try:
        viz = Visualizador(ruta)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error al cargar el dataset: {e}")
        return

    while True:
        seleccion = input(
            "\nElija una opción:\n"
            "[1] Graficar barras agrupadas\n"
            "[2] Salir\n"
            "Selección: "
        ).strip()

        try:
            if seleccion == "1":
                columna_x = input("Columna X (eje horizontal): ").strip()
                columna_y = input("Columna Y (valores numéricos): ").strip()
                columna_grupo = input("Columna de agrupación (color): ").strip()
                filtros = _pedir_filtro_opcional()
                viz.grafica_barras_agrupadas(
                    columna_x=columna_x,
                    columna_y=columna_y,
                    columna_grupo=columna_grupo,
                    filtros=filtros,
                    guardar=True,
                )
            elif seleccion == "2":
                print("Adiós!")
                break
            else:
                print("Selección no válida")
        except (KeyError, ValueError) as e:
            print(f"No se pudo generar la gráfica: {e}")


if __name__ == "__main__":
    _menu_interactivo()
