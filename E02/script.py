import os
import logging
from datetime import datetime

# Configuración del logging
now = datetime.now()
date_str = now.strftime("%d-%m-%Y-%H:%M")
log_dir = "logs"
log_filename = f"{date_str}-Errors.log"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filepath = os.path.join(log_dir, log_filename)
logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Configuraciones iniciales
data_dir = os.path.join('..', 'assets', 'dades')
delimitador = '\t'  # Cambiar si es necesario
null_value = -999
num_columnas_esperadas = 36  # Ajustar según el número esperado de valores en cada línea

# Función para validar una línea individual
def validar_linea(linea):
    valores = linea.strip().split(delimitador)
    if len(valores) != num_columnas_esperadas:
        return False
    for valor in valores:
        try:
            float(valor)
        except ValueError:
            return False
    return True

# Función para validar el formato de los archivos
def validar_archivo(filepath):
    try:
        with open(filepath, 'r') as file:
            # Saltar las dos primeras líneas (cabecera y comentarios)
            file.readline()
            file.readline()
            # Leer todas las líneas de datos
            data = file.readlines()
            for i, line in enumerate(data):
                if not validar_linea(line):
                    logging.error(f'Error en archivo {filepath}: formato incorrecto o número de valores incorrecto en la línea {i+3} (contenido: "{line.strip()}")')
                    return False
        return True
    except Exception as e:
        logging.error(f'Error al procesar el archivo {filepath}: {e}')
        return False

# Función para limpiar y procesar los archivos
def procesar_archivo(filepath):
    try:
        with open(filepath, 'r') as file:
            # Saltar las dos primeras líneas (cabecera y comentarios)
            file.readline()
            file.readline()
            # Leer todas las líneas de datos
            data = file.readlines()
            processed_data = []
            for line in data:
                if validar_linea(line):
                    values = [float(v) if v != str(null_value) else None for v in line.strip().split(delimitador)]
                    processed_data.append(values)
                else:
                    logging.error(f'Error en archivo {filepath}: formato incorrecto o número de valores incorrecto en la línea (contenido: "{line.strip()}")')
        return processed_data
    except Exception as e:
        logging.error(f'Error al limpiar el archivo {filepath}: {e}')
        return None

# Función para calcular estadísticas
def calcular_estadisticas(data):
    estadisticas = {}
    num_columns = len(data[0])
    # Calcular estadísticas
    for i in range(num_columns):
        column_data = [row[i] for row in data if row[i] is not None]
        if column_data:
            mean_value = sum(column_data) / len(column_data)
            total_value = sum(column_data)
            percent_missing = (len(data) - len(column_data)) / len(data) * 100
            annual_change_rate = (column_data[-1] - column_data[0]) / len(column_data)
            estadisticas[f'Column_{i+1}'] = {
                'mean': mean_value,
                'total': total_value,
                'percent_missing': percent_missing,
                'annual_change_rate': annual_change_rate,
            }
    return estadisticas

# Procesar todos los archivos en la carpeta
def procesar_carpeta(data_dir):
    estadisticas_totales = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.dat'):  # Asegurarse de trabajar con archivos .dat
            filepath = os.path.join(data_dir, filename)
            if validar_archivo(filepath):
                data = procesar_archivo(filepath)
                if data is not None:
                    stats = calcular_estadisticas(data)
                    estadisticas_totales.append(stats)
    return estadisticas_totales

# Ejecutar el proceso
estadisticas = procesar_carpeta(data_dir)
# Documentar el proceso y resultados
with open('documentacion_proceso.txt', 'w') as f:
    for estadistica in estadisticas:
        f.write(f"{estadistica}\n")

logging.info('Proceso completado exitosamente.')
