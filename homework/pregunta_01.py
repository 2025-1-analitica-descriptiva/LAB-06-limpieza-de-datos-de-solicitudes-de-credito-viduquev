import pandas as pd
import os
from typing import List
from datetime import datetime

# Normaliza texto: pasa a minúsculas y reemplaza guiones/barras por espacios
def normalizar_texto(texto: str) -> str:
    if not isinstance(texto, str):
        return texto
    return texto.lower().replace('_', ' ').replace('-', ' ')

# Aplica limpieza de texto a un conjunto de columnas
def limpiar_columnas_texto(df: pd.DataFrame, columnas: List[str]) -> pd.DataFrame:
    df = df.copy()
    for columna in columnas:
        df[columna] = df[columna].apply(normalizar_texto)
    return df

# Convierte montos monetarios desde texto a float, eliminando símbolos y separadores
def convertir_monto(monto: str) -> float:
    if not isinstance(monto, str):
        return monto
    return float(monto.replace('$', '').replace(',', '').replace('.00', '').strip())

# Convierte fechas desde 'dd/mm/yyyy' o 'yyyy/mm/dd' a objeto datetime
def convertir_fecha(fecha_str: str) -> datetime:
    partes = fecha_str.split('/')
    if len(partes[0]) > 2:  # ya viene como año/mes/día
        anio, mes, dia = partes
    else:  # día/mes/año
        dia, mes, anio = partes
    return pd.to_datetime(f"{anio}-{mes}-{dia}")

# Guarda un DataFrame como CSV, creando la carpeta de salida si es necesario
def guardar_como_csv(df: pd.DataFrame, ruta_salida: str = 'files/output/solicitudes_de_credito.csv'):
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df.to_csv(ruta_salida, index=True, sep=';')

# Función principal para limpiar y transformar el dataset
def pregunta_01():
    # Cargar dataset original
    df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';', index_col=0)

    # Eliminar duplicados y valores nulos
    df.drop_duplicates(keep='first', inplace=True)
    df.dropna(inplace=True)

    # Normalizar texto en columnas específicas
    columnas_a_normalizar = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']
    df = limpiar_columnas_texto(df, columnas_a_normalizar)

    # Limpiar monto del crédito
    df['monto_del_credito'] = df['monto_del_credito'].apply(convertir_monto)

    # Convertir fechas
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(convertir_fecha)

    # Eliminar duplicados nuevamente por seguridad
    df.drop_duplicates(keep='first', inplace=True)

    # Guardar resultado en CSV
    guardar_como_csv(df)

    return df

if __name__ == "__main__":
    pregunta_01()
