from __future__ import annotations

from typing import List, Dict, Tuple, Optional
import pandas as pd


#  REPRESENTACIÓN DE FUENTES DE DATOS

class TSVFile:
    """Representa un archivo delimitado por tabulaciones (.tsv)."""

    def __init__(
        self,
        file_path: str,
        file_name: str,
        delimiter: str = "\t",
        encoding: str = "utf-8",
        has_header: bool = True
    ) -> None:
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.delimiter: str = delimiter
        self.encoding: str = encoding
        self.has_header: bool = has_header

    def exists(self) -> bool:
        try:
            open(self.file_path).close()
            return True
        except OSError:
            return False

    def validate_format(self) -> bool:
        return self.exists()


class CSVFile:
    """Representa un archivo separado por comas (.csv)."""

    def __init__(
        self,
        file_path: str,
        file_name: str,
        delimiter: str = ",",
        encoding: str = "utf-8",
        has_header: bool = True
    ) -> None:
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.delimiter: str = delimiter
        self.encoding: str = encoding
        self.has_header: bool = has_header

    def exists(self) -> bool:
        try:
            open(self.file_path).close()
            return True
        except OSError:
            return False

    def validate_format(self) -> bool:
        return self.exists()


class PostgreSQLConnection:
    """
    Representa los parámetros de conexión a una base de datos PostgreSQL.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.host: str = host
        self.port: int = port
        self.database: Optional[str] = database
        self.username: Optional[str] = username
        self.password: Optional[str] = password

    def is_complete(self) -> bool:
        """Devuelve True si todos los campos obligatorios están llenos."""
        return all([self.database, self.username, self.password])


#  DATASET

class DataSet:
    """Contenedor principal del DataFrame y sus metadatos."""

    def __init__(
        self,
        data: pd.DataFrame,
        row_count: int,
        column_count: int,
        columns: List[str],
        source_file: Optional[TSVFile | CSVFile | PostgreSQLConnection]
    ) -> None:
        self.data: pd.DataFrame = data
        self.row_count: int = row_count
        self.column_count: int = column_count
        self.columns: List[str] = columns
        self.source_file = source_file

    def get_shape(self) -> Tuple[int, int]:
        return (self.row_count, self.column_count)

    def get_columns(self) -> List[str]:
        return self.columns

    def preview(self, n: int = 5) -> pd.DataFrame:
        return self.data.head(n)

    def update_data(self, new_data: pd.DataFrame) -> None:
        self.data = new_data
        self.row_count = len(new_data)
        self.column_count = len(new_data.columns)
        self.columns = list(new_data.columns)


#  PERFIL DE COLUMNA

class ColumnProfile:
    """Perfil estadístico de una sola columna del dataset."""

    def __init__(
        self,
        name: str,
        data_type: str,
        null_count: int
    ) -> None:
        self.name: str = name
        self.data_type: str = data_type
        self.null_count: int = null_count

    def calculate_statistics(self, data: pd.Series) -> Dict:
        return {
            "dtype": str(data.dtype),
            "nulls": int(data.isna().sum())
        }

    def detect_type(self, data: pd.Series) -> str:
        return str(data.dtype)



#  PROFILER (EDA)

class DatasetProfiler:
    """
    Analiza la estructura y estadísticas del dataset.

    EDA incluido:
      - Número de filas y columnas
      - Header (nombres de columnas)
      - Tipo de dato por columna
      - Valores nulos por columna
      - Promedio de columnas numéricas
      - Valor mínimo de columnas numéricas
      - Valor máximo de columnas numéricas
    """

    def __init__(
        self,
        dataset: DataSet,
        column_profiles: Optional[List[ColumnProfile]] = None
    ) -> None:
        self.dataset: DataSet = dataset
        self.column_profiles: List[ColumnProfile] = column_profiles if column_profiles else []

    # análisis base 

    def analyze(self) -> None:
        self.column_profiles = []
        df = self.dataset.data

        for col in df.columns:
            series = df[col]
            profile = ColumnProfile(
                name=col,
                data_type=str(series.dtype),
                null_count=int(series.isna().sum())
            )
            self.column_profiles.append(profile)

    def get_summary(self) -> Dict:
        if not self.column_profiles:
            self.analyze()

        return {
            "rows": self.dataset.row_count,
            "columns": self.dataset.column_count,
            "column_details": {
                p.name: {
                    "dtype": p.data_type,
                    "nulls": p.null_count
                } for p in self.column_profiles
            }
        }

    # columnas por categoría

    def get_numeric_columns(self) -> List[str]:
        """Devuelve los nombres de columnas con dtype numérico."""
        df = self.dataset.data
        return list(df.select_dtypes(include="number").columns)

    def get_categorical_columns(self) -> List[str]:
        """Devuelve los nombres de columnas de tipo object / category."""
        df = self.dataset.data
        return list(df.select_dtypes(include=["object", "category"]).columns)

    def get_target_candidates(self) -> List[str]:
        """Candidatas a variable objetivo: numéricas con baja cardinalidad."""
        df = self.dataset.data
        candidates = []
        for col in self.get_numeric_columns():
            if df[col].nunique() <= 20:
                candidates.append(col)
        return candidates

    # EDA numérico

    def get_numeric_means(self) -> Dict[str, float]:
        """Promedio de cada columna numérica."""
        df = self.dataset.data
        num_cols = self.get_numeric_columns()
        return {col: round(float(df[col].mean()), 4) for col in num_cols}

    def get_numeric_mins(self) -> Dict[str, float]:
        """Valor mínimo de cada columna numérica."""
        df = self.dataset.data
        num_cols = self.get_numeric_columns()
        return {col: float(df[col].min()) for col in num_cols}

    def get_numeric_maxs(self) -> Dict[str, float]:
        """Valor máximo de cada columna numérica."""
        df = self.dataset.data
        num_cols = self.get_numeric_columns()
        return {col: float(df[col].max()) for col in num_cols}

    # reporte final

    def print_report(self) -> None:
        if not self.column_profiles:
            self.analyze()

        summary  = self.get_summary()
        means    = self.get_numeric_means()
        mins     = self.get_numeric_mins()
        maxs     = self.get_numeric_maxs()

        sep = "─" * 55

        print(f"\n{sep}")
        print("  REPORTE EDA — DATASET")
        print(sep)
        print(f"  Filas    : {summary['rows']}")
        print(f"  Columnas : {summary['columns']}")

        print(f"\n{sep}")
        print("  DETALLE POR COLUMNA")
        print(sep)
        print(f"  {'Columna':<25} {'Tipo':<12} {'Nulos':>6}")
        print(f"  {'-------':<25} {'----':<12} {'-----':>6}")
        for col, info in summary["column_details"].items():
            print(f"  {col:<25} {info['dtype']:<12} {info['nulls']:>6}")

        if means:
            print(f"\n{sep}")
            print("  ESTADÍSTICAS NUMÉRICAS")
            print(sep)
            print(f"  {'Columna':<25} {'Promedio':>12} {'Mínimo':>12} {'Máximo':>12}")
            print(f"  {'-------':<25} {'--------':>12} {'------':>12} {'------':>12}")
            for col in means:
                print(
                    f"  {col:<25} "
                    f"{means[col]:>12.4f} "
                    f"{mins[col]:>12.4f} "
                    f"{maxs[col]:>12.4f}"
                )

        print(f"\n{sep}\n")


#  LOADERS

class TSVLoader:
    """Carga un archivo .tsv y devuelve un DataSet."""

    def __init__(self, tsv_file: TSVFile) -> None:
        self.tsv_file: TSVFile = tsv_file

    def load(self) -> DataSet:
        if not self.tsv_file.validate_format():
            raise FileNotFoundError(
                f"No se encontró el archivo o no es un .tsv válido: {self.tsv_file.file_path}"
            )

        header = 0 if self.tsv_file.has_header else None

        df = pd.read_csv(
            self.tsv_file.file_path,
            delimiter=self.tsv_file.delimiter,
            encoding=self.tsv_file.encoding,
            header=header,
        )

        return DataSet(
            data=df,
            row_count=len(df),
            column_count=len(df.columns),
            columns=list(df.columns),
            source_file=self.tsv_file,
        )


class CSVLoader:
    """Carga un archivo .csv y devuelve un DataSet."""

    def __init__(self, csv_file: CSVFile) -> None:
        self.csv_file: CSVFile = csv_file

    def load(self) -> DataSet:
        if not self.csv_file.validate_format():
            raise FileNotFoundError(
                f"No se encontró el archivo o no es un .csv válido: {self.csv_file.file_path}"
            )

        header = 0 if self.csv_file.has_header else None

        df = pd.read_csv(
            self.csv_file.file_path,
            delimiter=self.csv_file.delimiter,
            encoding=self.csv_file.encoding,
            header=header,
        )

        return DataSet(
            data=df,
            row_count=len(df),
            column_count=len(df.columns),
            columns=list(df.columns),
            source_file=self.csv_file,
        )


class DBLoader:
    """
    Carga datos desde PostgreSQL y devuelve un DataSet.
    """

    def __init__(self, connection: PostgreSQLConnection) -> None:
        self.connection: PostgreSQLConnection = connection

    def _prompt_missing_fields(self) -> None:
        """Pide por terminal los campos que falten en la conexión."""
        conn = self.connection
        print("\n Conexión a PostgreSQL")
        if not conn.host:
            conn.host = input("  Host       [localhost]: ").strip() or "localhost"
        if not conn.port:
            port_str = input("  Puerto     [5432]: ").strip()
            conn.port = int(port_str) if port_str else 5432
        if not conn.database:
            conn.database = input("  Base de datos: ").strip()
        if not conn.username:
            conn.username = input("  Usuario: ").strip()
        if not conn.password:
            import getpass
            conn.password = getpass.getpass("  Contraseña: ")

    def _ask_table_name(self) -> str:
        """Pregunta al usuario qué tabla quiere leer."""
        tabla = input(" Nombre de la tabla: ").strip()
        return tabla

    def load(self) -> DataSet:
        try:
            from sqlalchemy import create_engine, text
        except ImportError:
            raise ImportError(
                "Instala sqlalchemy: pip install sqlalchemy psycopg2-binary"
            )

        # Completar campos si faltan
        if not self.connection.is_complete():
            self._prompt_missing_fields()

        conn = self.connection
        url = (
            f"postgresql+psycopg2://{conn.username}:{conn.password}"
            f"@{conn.host}:{conn.port}/{conn.database}"
        )

        print(f"  Conectando a PostgreSQL → {conn.host}:{conn.port}/{conn.database} ...")

        try:
            engine = create_engine(url)
            with engine.connect() as con:
                con.execute(text("SELECT 1"))   
            print("  Conexión exitosa.\n")
        except Exception as e:
            raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")

        # Pedir nombre de tabla y leer todo
        tabla = self._ask_table_name()
        query = f'SELECT * FROM "{tabla}"'

        print(f"  Leyendo tabla: {tabla} ...")
        df = pd.read_sql(query, engine)

        return DataSet(
            data=df,
            row_count=len(df),
            column_count=len(df.columns),
            columns=list(df.columns),
            source_file=conn,
        )


#  Deteccion del tipo de archivo


class DataSourceDetector:
    """
    Detecta el tipo de fuente a partir de la ruta del archivo
    y devuelve el DataSet listo usando el loader correspondiente.
    """

    @staticmethod
    def _ask_has_header() -> bool:
        """Pregunta al usuario si el archivo tiene encabezado."""
        while True:
            respuesta = input("  ¿El archivo tiene encabezado? (s/n): ").strip().lower()
            if respuesta in ("s", "si", "sí", "y", "yes"):
                return True
            elif respuesta in ("n", "no"):
                return False
            print("  Por favor responde 's' para sí o 'n' para no.")

    @staticmethod
    def load(source: str) -> DataSet:
        source_lower = source.strip().lower()

        if source_lower.endswith(".csv"):
            print(f"[Detector] Fuente identificada: CSV → {source}")
            has_header = DataSourceDetector._ask_has_header()
            csv_file = CSVFile(file_path=source, file_name=source, has_header=has_header)
            return CSVLoader(csv_file).load()

        elif source_lower.endswith(".tsv"):
            print(f"[Detector] Fuente identificada: TSV → {source}")
            has_header = DataSourceDetector._ask_has_header()
            tsv_file = TSVFile(file_path=source, file_name=source, has_header=has_header)
            return TSVLoader(tsv_file).load()

        elif source_lower in ("db", "database", "bd", "postgresql", "postgres"):
            print("[Detector] Fuente identificada: PostgreSQL")
            conn = PostgreSQLConnection()          # campos vacíos → DBLoader los pide
            return DBLoader(conn).load()

        else:
            raise ValueError(
                f"No se pudo detectar el tipo de fuente para: '{source}'\n"
                "  Usa archivos .csv, .tsv, o escribe 'db' para PostgreSQL."
            )

if __name__ == "__main__":
    print("═" * 55)
    print("  DataLux — Carga de Datos")
    print("═" * 55)
    print("  Opciones:")
    print("    • Ruta a un archivo .csv   (ej: datos.csv)")
    print("    • Ruta a un archivo .tsv   (ej: datos.tsv)")
    print("    • Si es BD escribe db      (conexión a PostgreSQL)")
    source = input("\n  Ingresa la ruta del archivo: ").strip()

    dataset = DataSourceDetector.load(source)

    print("\n(Filas, Columnas: )")
    print(dataset.get_shape())

    print("\nNombres de columnas: ")
    print(dataset.get_columns())

    print("\nPrimeros 5 reigstros")
    print(dataset.preview())

    profiler = DatasetProfiler(dataset)
    profiler.print_report()