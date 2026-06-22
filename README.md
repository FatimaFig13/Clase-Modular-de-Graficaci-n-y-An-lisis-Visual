# Visualizador de Datos 📊

Clase modular en Python para la generación de gráficos estadísticos a partir de archivos CSV. Desarrollada aplicando principios de **Programación Orientada a Objetos (POO)**, con enfoque en **modularidad**, **reutilización** y **robustez**.

Este proyecto es el resultado de una refactorización completa de la clase original `VisualizadorSalud`, transformándola en una herramienta genérica capaz de trabajar con cualquier dataset estructurado en formato CSV.

---

## ✨ Características

- **Totalmente genérica**: No depende de nombres de columnas fijos.
- **Robusta**: Manejo de errores, validaciones y mensajes claros.
- **Modular**: Métodos reutilizables.
- **Interactiva**: Menú en consola para generar gráficos fácilmente.
- Soporta **barras agrupadas** (Seaborn + Matplotlib).
- Preparada para extenderse con más tipos de gráficos (líneas, plotly, etc.).

---

## Requisitos

- Python 3.8 o superior
- Librerías:

```bash
matplotlib
seaborn
pandas
```

Puedes instalarlas con:

```bash
pip install -r requirements.txt
```

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/FatimaFig13/Clase-Modular-de-Graficaci-n-y-An-lisis-Visual.git
```

2. Ingresa a la carpeta del proyecto:

```bash
cd Clase-Modular-de-Graficaci-n-y-An-lisis-Visual
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## Uso

Ejecuta el programa:

```bash
python graficos.py
```

Se abrirá un menú interactivo donde podrás:

- Cargar tu archivo CSV
- Seleccionar columnas para los ejes X, Y y agrupación
- Aplicar filtros (opcional)
- Generar y guardar automáticamente la gráfica


