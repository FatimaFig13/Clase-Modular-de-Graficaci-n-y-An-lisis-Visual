import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px


class VisualizadorSalud:
    """
    Clase para centralizar y automatizar la generación
    de gráficos estadísticos del dataset H_Rates.
    """

#--------Constructor: carga el CSV y guarda el DataFrame.--------------------------------------------------------------------------------------------
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.df = pd.read_csv(ruta_csv, low_memory=False)
        print(f"Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")


#--------Metodos: Transformacion-------------------------------------------------------------------------------------------------------------------------------
    def _preparar_barras_sexo(self):
        mask = (
            (self.df["ENT_CVE"] == "Total") &
            (self.df["RANGO_EDAD"] == "Total") &
            (self.df["CAUSA_DEF"] == "H") &
            (self.df["SEXO"].isin(["Hombres", "Mujeres"]))
        )
        data = self.df[mask][["ANIO_REGIS", "SEXO", "CONTEO"]].copy()
        data["CONTEO"] = pd.to_numeric(data["CONTEO"], errors="coerce")
        return data.sort_values("ANIO_REGIS")
    
    def _preparar_linea_temporal(self):
        mask = (
            (self.df["ENT_CVE"] == "Total") &
            (self.df["SEXO"] == "Total") &
            (self.df["RANGO_EDAD"] == "Total") &
            (self.df["CAUSA_DEF"] == "H")
        )
        data = self.df[mask][["ANIO_REGIS", "TASA_100K"]].copy()
        data["TASA_100K"] = pd.to_numeric(data["TASA_100K"], errors="coerce")
        return data.sort_values("ANIO_REGIS")
    
    def _preparar_barras_estados(self):
        mask = (
            (self.df["MUN_CVE"] == "Total") &
            (self.df["SEXO"] == "Total") &
            (self.df["RANGO_EDAD"] == "Total") &
            (self.df["CAUSA_DEF"] == "H") &
            (self.df["ENT_CVE"] != "Total")       # excluye el total nacional
        )
        data = self.df[mask][["ENT_NAME", "TASA_100K"]].copy()
        data["TASA_100K"] = pd.to_numeric(data["TASA_100K"], errors="coerce")

        # Promedio por estado y ordenar de mayor a menor
        data = (
            data.groupby("ENT_NAME", as_index=False)["TASA_100K"]
            .mean()
            .sort_values("TASA_100K", ascending=True)  # ascending=True para que el mayor quede arriba en barras horizontales
        )
        return data
    
#--------Metodos: Visualizacion-------------------------------------------------------------------------------------------------------------------------------
    def grafica_barras_sexo(self, guardar=False, nombre_archivo="barras_sexo.png"):
        data = self._preparar_barras_sexo()

        fig, ax = plt.subplots(figsize=(14, 6))

        sns.barplot(
            data=data,
            x="ANIO_REGIS",
            y="CONTEO",
            hue="SEXO",
            palette={"Hombres": "#1a6eb5", "Mujeres": "#e05c8a"},
            ax=ax
        )

        ax.set_title(
            "Casos registrados por sexo y año\nMéxico, 2000–2022",
            fontsize=13, fontweight="bold", pad=14
        )
        ax.set_xlabel("Año", fontsize=11)
        ax.set_ylabel("Número de casos", fontsize=11)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.legend(title="Sexo")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()

        if guardar:
            plt.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
            print(f"Gráfica guardada como: {nombre_archivo}")

        plt.show()

    def grafica_linea_temporal(self, guardar=False, nombre_archivo="linea_temporal.png"):
        data = self._preparar_linea_temporal()

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(data["ANIO_REGIS"], data["TASA_100K"],
                color="#1a6eb5", linewidth=2.5, marker="o",
                markersize=6, markerfacecolor="white", markeredgewidth=2)

        ax.fill_between(data["ANIO_REGIS"], data["TASA_100K"],
                        alpha=0.12, color="#1a6eb5")

        max_row = data.loc[data["TASA_100K"].idxmax()]
        ax.annotate(
            f'Máximo: {max_row["TASA_100K"]:.4f}\n({int(max_row["ANIO_REGIS"])})',
            xy=(max_row["ANIO_REGIS"], max_row["TASA_100K"]),
            xytext=(max_row["ANIO_REGIS"] + 1, max_row["TASA_100K"] + 0.005),
            fontsize=9, color="#1a6eb5",
            arrowprops=dict(arrowstyle="->", color="#1a6eb5", lw=1.2)
        )

        ax.set_title("Tasa de enfermedades oculares por 100,000 habitantes\nMéxico, 2000–2022",
                    fontsize=13, fontweight="bold", pad=14)
        ax.set_xlabel("Año", fontsize=11)
        ax.set_ylabel("Tasa por 100,000 hab.", fontsize=11)
        ax.set_xticks(data["ANIO_REGIS"])
        ax.set_xticklabels(data["ANIO_REGIS"], rotation=45, ha="right", fontsize=9)
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.4f"))
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()

        if guardar:
                plt.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
                print(f"Gráfica guardada como: {nombre_archivo}")

        plt.show()

    def grafica_barras_estados(self, guardar=False, nombre_archivo="barras_estados.html", carpeta="graficas"):
        data = self._preparar_barras_estados()

        fig = px.bar(
            data,
            x="TASA_100K",
            y="ENT_NAME",
            orientation="h",                        # barras horizontales
            color="TASA_100K",
            color_continuous_scale="Blues",
            labels={
                "TASA_100K": "Tasa promedio por 100,000 hab.",
                "ENT_NAME": "Estado"
            },
            title="Ranking de estados por tasa promedio de enfermedades oculares<br>México, 2000–2022"
        )

        fig.update_layout(
            height=750,
            coloraxis_showscale=False,
            title_font_size=14,
            xaxis_title="Tasa promedio por 100,000 hab.",
            yaxis_title="",
            plot_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#eeeeee")
        )

        fig.show()

        if guardar:
                plt.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
                print(f"Gráfica guardada como: {nombre_archivo}")

        plt.show()
#--------Uso-------------------------------------------------------------------------------------------------------------------------------
viz = VisualizadorSalud("H_Rates.csv")
viz.grafica_barras_sexo(guardar=True)
viz.grafica_linea_temporal(guardar=True)
viz.grafica_barras_estados(guardar=True)