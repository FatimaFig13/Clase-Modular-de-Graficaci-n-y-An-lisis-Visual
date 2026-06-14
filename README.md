# VisualizadorSalud 📊

Clase en Python para centralizar y automatizar la generación de gráficos estadísticos a partir del dataset de tasas de enfermedades oftalmológicas en México (2000–2022), aplicando principios de Programación Orientada a Objetos (POO).

---

## Requisitos

- Python 3.14
- Las siguientes librerías (ver `requirements.txt`):

```
matplotlib
seaborn
plotly
pandas
```

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/FatimaFig13/Clase-Modular-de-Graficaci-n-y-An-lisis-Visual.git
```

2. Entra a la carpeta del proyecto:

```bash
cd Clase-Modular-de-Graficaci-n-y-An-lisis-Visual
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## Uso

Ejecuta el archivo principal:

```bash
python graficos.py
```

Se mostrará un menú en consola donde puedes elegir la gráfica que deseas generar:

```
Elija la grafica que desea visualizar:
[1] Grafica de barras de sexo
[2] Grafica de linea temporal
[3] Grafica de barras de Entidades
[4] Salir
Seleccion:
```

Las gráficas generadas se guardan automáticamente en la misma carpeta del proyecto:

| Opción | Archivo | Librería |
|--------|---------|----------|
| 1 | `barras_sexo.png` | Seaborn |
| 2 | `linea_temporal.png` | Matplotlib |
| 3 | `barras_estados.html` | Plotly |

> La gráfica 3 se guarda como `.html` y puede abrirse en cualquier navegador para explorarla de forma interactiva.
