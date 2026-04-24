# DataLux_DAAD

Aplicación de análisis de datos desarrollada en Python con arquitectura modular.

## Tecnologías
- Python
- Pandas
- PySide6

# README — Dataset.py

El objetivo de este README es describir específicamente todo lo hecho para el archivo `Dataset.py`, que se encarga de cargar datos desde archivos `.csv`, `.tsv` y de leer tablas desde una base de datos PostgreSQL, además de realizar un análisis exploratorio básico (EDA) sobre los datos cargados.

---

## Tabla de contenido

1. [Estructura general del archivo](#1-estructura-general-del-archivo)
2. [Clases de representación de fuentes](#2-clases-de-representación-de-fuentes)
3. [Clase DataSet](#3-clase-dataset)
4. [Clases de perfil de columna](#4-clase-columnprofile)
5. [Análisis exploratorio — DatasetProfiler](#5-análisis-exploratorio--datasetprofiler)
6. [Loaders — carga de datos](#6-loaders--carga-de-datos)
7. [Detección automática de fuente](#7-detección-automática-de-fuente)
8. [Punto de entrada — main](#8-punto-de-entrada--main)
9. [Dependencias](#9-dependencias)
10. [Flujo completo de ejecución](#10-flujo-completo-de-ejecución)

---

## 1. Estructura general del archivo

El archivo está organizado en las siguientes secciones, en este orden:

```
Dataset.py
│
├── Clases de fuentes de datos
│   ├── TSVFile
│   ├── CSVFile
│   └── PostgreSQLConnection
│
├── DataSet
│
├── ColumnProfile
│
├── DatasetProfiler  (EDA)
│
├── Loaders
│   ├── TSVLoader
│   ├── CSVLoader
│   └── DBLoader
│
├── DataSourceDetector
│
└── main (__name__ == "__main__")
```

El diseño sigue el principio de separación de responsabilidades: cada clase tiene una sola tarea. Las clases de fuentes solo guardan parámetros, los loaders solo leen datos, `DataSet` solo almacena, y `DatasetProfiler` solo analiza.

---

## 2. Clases de representación de fuentes

Estas clases no leen datos por sí solas. Son contenedores de configuración que los loaders utilizan para saber cómo leer cada fuente.

### `TSVFile`

Representa un archivo delimitado por tabulaciones (`.tsv`).

| Atributo | Tipo | Default | Descripción |
|---|---|---|---|
| `file_path` | `str` | — | Ruta completa al archivo |
| `file_name` | `str` | — | Nombre del archivo |
| `delimiter` | `str` | `"\t"` | Caracter separador |
| `encoding` | `str` | `"utf-8"` | Codificación del archivo |
| `has_header` | `bool` | `True` | Si la primera fila son nombres de columna |

**Métodos:**
- `exists()` — intenta abrir el archivo; devuelve `True` si es accesible, `False` si no existe o no tiene permisos.
- `validate_format()` — llama a `exists()` y devuelve su resultado. Se mantiene separado para que en el futuro se puedan agregar más validaciones sin cambiar la lógica del loader.

### `CSVFile`

Idéntica en estructura a `TSVFile`, pero con delimitador `,` por default. Se separó en su propia clase para que el sistema pueda distinguir explícitamente entre ambos tipos de archivo y aplicar configuraciones diferentes si se necesita en el futuro.

### `PostgreSQLConnection`

Guarda los parámetros necesarios para conectarse a una base de datos PostgreSQL.

| Atributo | Tipo | Default | Descripción |
|---|---|---|---|
| `host` | `str` | `"localhost"` | Dirección del servidor |
| `port` | `int` | `5432` | Puerto de conexión |
| `database` | `str` | `None` | Nombre de la base de datos |
| `username` | `str` | `None` | Usuario de PostgreSQL |
| `password` | `str` | `None` | Contraseña |

**Método:**
- `is_complete()` — devuelve `True` solo si `database`, `username` y `password` tienen valor. Si alguno está vacío, el `DBLoader` sabrá que debe pedirlos por terminal.

---

## 3. Clase `DataSet`

Es el contenedor central del sistema. Sin importar si los datos vienen de un `.csv`, `.tsv` o de PostgreSQL, todos los loaders devuelven siempre un `DataSet`. Esto permite que el resto del sistema (procesamiento, modelos, visualización) reciba siempre el mismo tipo de objeto.

| Atributo | Tipo | Descripción |
|---|---|---|
| `data` | `pd.DataFrame` | Los datos completos en memoria |
| `row_count` | `int` | Número de filas |
| `column_count` | `int` | Número de columnas |
| `columns` | `List[str]` | Nombres de columnas |
| `source_file` | `TSVFile / CSVFile / PostgreSQLConnection` | Referencia a la fuente original |

**Métodos:**
- `get_shape()` — devuelve `(filas, columnas)` como tupla.
- `get_columns()` — devuelve la lista de nombres de columna.
- `preview(n=5)` — devuelve las primeras `n` filas usando `df.head(n)`.
- `update_data(new_data)` — reemplaza el DataFrame y recalcula `row_count`, `column_count` y `columns` para que no queden desincronizados cuando las capas de procesamiento modifiquen los datos.

---

## 4. Clase `ColumnProfile`

Guarda el perfil básico de una columna individual: su nombre, tipo de dato y cantidad de valores nulos. El `DatasetProfiler` crea un `ColumnProfile` por cada columna del dataset durante el análisis.

---

## 5. Análisis exploratorio — `DatasetProfiler`

Es la clase encargada del EDA (Exploratory Data Analysis). Recibe un `DataSet` y calcula estadísticas sobre sus datos.

### Análisis que realiza

**Estructura general:**
- Número total de filas
- Número total de columnas
- Nombre de cada columna (header)
- Tipo de dato de cada columna (`int64`, `float64`, `object`, etc.)
- Cantidad de valores nulos por columna

**Estadísticas numéricas** (solo columnas con dtype numérico):
- Promedio (`mean`)
- Valor mínimo (`min`)
- Valor máximo (`max`)

### Métodos principales

| Método | Descripción |
|---|---|
| `analyze()` | Recorre todas las columnas y construye la lista de `ColumnProfile` |
| `get_summary()` | Devuelve un diccionario con filas, columnas y detalle por columna |
| `get_numeric_columns()` | Usa `select_dtypes(include="number")` para filtrar columnas numéricas |
| `get_categorical_columns()` | Filtra columnas de tipo `object` o `category` |
| `get_target_candidates()` | Devuelve columnas numéricas con 20 o menos valores únicos (candidatas a variable objetivo) |
| `get_numeric_means()` | Promedio de cada columna numérica, redondeado a 4 decimales |
| `get_numeric_mins()` | Valor mínimo de cada columna numérica |
| `get_numeric_maxs()` | Valor máximo de cada columna numérica |
| `print_report()` | Imprime el reporte completo formateado en terminal |

### Ejemplo de salida en terminal

```
───────────────────────────────────────────────────────
  REPORTE EDA — DATASET
───────────────────────────────────────────────────────
  Filas    : 743
  Columnas : 2

───────────────────────────────────────────────────────
  DETALLE POR COLUMNA
───────────────────────────────────────────────────────
  Columna                   Tipo          Nulos
  -------                   ----          -----
  hora                      float64           0
  trafico                   float64         318

───────────────────────────────────────────────────────
  ESTADÍSTICAS NUMÉRICAS
───────────────────────────────────────────────────────
  Columna                       Promedio       Mínimo       Máximo
  -------                       --------       ------       ------
  hora                           11.5155       0.0000      23.0000
  trafico                     16354.4918     203.0000   27889.0000
───────────────────────────────────────────────────────
```

---

## 6. Loaders — carga de datos

Los loaders son los únicos que leen datos. Todos devuelven un `DataSet`.

### `TSVLoader`

Recibe un `TSVFile`, valida que exista con `validate_format()`, y usa `pd.read_csv()` con el delimitador `\t` para leerlo. Si `has_header` es `False`, pandas genera nombres de columna numéricos (`0, 1, 2...`) en lugar de tomar la primera fila como encabezado.

### `CSVLoader`

Idéntico a `TSVLoader` en lógica, pero recibe un `CSVFile` con delimitador `,`.

### `DBLoader`

Es el loader más complejo. Su flujo es:

1. **Verificar credenciales** — llama `is_complete()` en la conexión. Si faltan datos, ejecuta `_prompt_missing_fields()` que los pide uno a uno por terminal. La contraseña se pide con `getpass` para que no se muestre en pantalla.
2. **Construir URL de conexión** — arma la cadena `postgresql+psycopg2://usuario:password@host:puerto/base` que requiere SQLAlchemy.
3. **Probar la conexión** — ejecuta `SELECT 1` antes de continuar. Si falla, lanza un `ConnectionError` con el mensaje del error original.
4. **Pedir nombre de tabla** — llama `_ask_table_name()` que pide el nombre por terminal.
5. **Leer la tabla completa** — ejecuta `SELECT * FROM "nombre_tabla"` usando `pd.read_sql()`, que convierte el resultado directamente a DataFrame.
6. **Devolver `DataSet`** — construye y retorna el objeto con el DataFrame y sus metadatos.

> Las comillas dobles alrededor del nombre de tabla en el query (`"nombre_tabla"`) son necesarias en PostgreSQL para respetar mayúsculas y minúsculas en los nombres.

**Dependencias requeridas para BD:**
```bash
pip install sqlalchemy psycopg2-binary
```

---

## 7. Detección automática de fuente — `DataSourceDetector`

Es el punto de entrada inteligente del sistema. Recibe un string del usuario y decide qué loader usar.

### Lógica de detección

| Lo que escribe el usuario | Acción |
|---|---|
| Ruta terminada en `.csv` | Crea `CSVFile` + `CSVLoader` |
| Ruta terminada en `.tsv` | Crea `TSVFile` + `TSVLoader` |
| `bd`, `db`, `database`, `postgresql`, `postgres` | Crea `PostgreSQLConnection` + `DBLoader` |
| Cualquier otra cosa | Lanza `ValueError` con mensaje explicativo |

### Pregunta de encabezado

Para archivos `.csv` y `.tsv`, antes de cargar pregunta al usuario si el archivo tiene encabezado:

```
¿El archivo tiene encabezado (nombres de columnas)? (s/n):
```

Acepta como "sí": `s`, `si`, `sí`, `y`, `yes`. Acepta como "no": `n`, `no`. Si el usuario escribe otra cosa, vuelve a preguntar en lugar de crashear. Esta pregunta no aplica para BD porque PostgreSQL siempre tiene nombres de columna.

---

## 8. Punto de entrada — `main`

El bloque `if __name__ == "__main__"` se ejecuta solo cuando se corre el archivo directamente con `python Dataset.py`. Muestra un menú en terminal, recibe la fuente del usuario, carga el dataset con `DataSourceDetector.load()` e imprime el reporte EDA completo.

```
═══════════════════════════════════════════════════════
  DataLux — Carga de Datos
═══════════════════════════════════════════════════════
  Opciones:
    • Ruta a un archivo .csv   (ej: datos.csv)
    • Ruta a un archivo .tsv   (ej: datos.tsv)
    • 'db'                     (conexión a PostgreSQL)

  Ingresa la fuente de datos:
```

Cuando el archivo se importe desde otro módulo (como `Datalux.py` o `MainApp.py`), este bloque no se ejecuta — solo quedan disponibles las clases para que el orquestador las use.

---

## 9. Dependencias

| Librería | Uso | Instalación |
|---|---|---|
| `pandas` | Lectura de archivos y manipulación de datos | `pip install pandas` |
| `sqlalchemy` | Motor de conexión a PostgreSQL | `pip install sqlalchemy` |
| `psycopg2-binary` | Driver de PostgreSQL para SQLAlchemy | `pip install psycopg2-binary` |

`pandas` es necesaria siempre. `sqlalchemy` y `psycopg2-binary` solo son necesarias si se va a usar la fuente de base de datos.

---

## 10. Flujo completo de ejecución

```
Usuario ejecuta: python Dataset.py
        │
        ▼
    Menú en terminal
        │
        ▼
    Usuario ingresa fuente
        │
        ├─── termina en .csv ──► pregunta header ──► CSVLoader ──► DataSet
        │
        ├─── termina en .tsv ──► pregunta header ──► TSVLoader ──► DataSet
        │
        └─── escribe "bd"    ──► pide credenciales ──► prueba conexión
                                      │
                                      ▼
                                 pide nombre de tabla
                                      │
                                      ▼
                                 SELECT * FROM tabla ──► DataSet
        │
        ▼
    DatasetProfiler.print_report()
        │
        ├── Filas y columnas
        ├── Tipo y nulos por columna
        └── Promedio, mínimo y máximo de columnas numéricas
```
