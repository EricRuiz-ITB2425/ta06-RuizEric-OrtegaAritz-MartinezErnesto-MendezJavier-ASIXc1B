import os
import logging
from typing import Tuple, List, Dict
import csv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='procesamiento_archivos.log'
)


def detect_delimiter(line: str) -> str:
    """
    Detecta el delimitador más probable en una línea.

    Args:
        line (str): Línea de texto a analizar

    Returns:
        str: Delimitador detectado
    """
    possible_delimiters = ['\t', ',', ';', '|']
    delimiter_counts = {delimiter: line.count(delimiter) for delimiter in possible_delimiters}
    return max(delimiter_counts.items(), key=lambda x: x[1])[0]


def analyze_file_structure(file_path: str, num_preview_rows: int = 5) -> Dict:
    """
    Analiza la estructura del archivo incluyendo delimitador, columnas y primeras filas.

    Args:
        file_path (str): Ruta al archivo
        num_preview_rows (int): Número de filas a previsualizar

    Returns:
        Dict: Diccionario con la información del análisis
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Leer las primeras líneas para análisis
            preview_lines = [next(file).strip() for _ in range(num_preview_rows)]

            # Detectar delimitador usando la primera línea
            delimiter = detect_delimiter(preview_lines[0])

            # Contar columnas
            num_columns = len(preview_lines[0].split(delimiter))

            return {
                'delimiter': delimiter,
                'num_columns': num_columns,
                'preview_lines': preview_lines
            }

    except StopIteration:
        return {
            'delimiter': None,
            'num_columns': 0,
            'preview_lines': []
        }
    except Exception as e:
        logging.error(f"Error analizando {file_path}: {str(e)}")
        return {
            'delimiter': None,
            'num_columns': 0,
            'preview_lines': []
        }


def check_header(file_path: str) -> Tuple[bool, Dict]:
    """
    Verifica si un archivo tiene la cabecera correcta y analiza su estructura.

    Args:
        file_path (str): Ruta al archivo a verificar

    Returns:
        Tuple[bool, Dict]: (Es válido, Información del análisis)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Leer las dos primeras líneas para la verificación de cabecera
            header = [next(file).strip() for _ in range(2)]

            # Verificar el formato de la cabecera
            is_valid = (
                    len(header) == 2 and
                    header[0] == "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1" and
                    header[1].startswith("P")
            )

            # Analizar la estructura del archivo
            file_analysis = analyze_file_structure(file_path)

            return is_valid, file_analysis

    except Exception as e:
        logging.error(f"Error al procesar {file_path}: {str(e)}")
        return False, {}


def process_directory(directory: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Procesa todos los archivos en el directorio especificado.

    Args:
        directory (str): Ruta al directorio a procesar

    Returns:
        Tuple[List[Dict], List[Dict]]: Lista de archivos buenos y malos con su análisis
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"El directorio {directory} no existe")

    good_files = []
    bad_files = []

    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if not os.path.isfile(file_path):
                continue

            logging.info(f"Procesando archivo: {filename}")
            is_good, analysis = check_header(file_path)

            file_info = {
                'filename': filename,
                'analysis': analysis
            }

            if is_good:
                good_files.append(file_info)
                logging.info(f"Archivo correcto: {filename}")
            else:
                bad_files.append(file_info)
                logging.warning(f"Archivo incorrecto: {filename}")

    except Exception as e:
        logging.error(f"Error al procesar el directorio: {str(e)}")
        raise

    return good_files, bad_files


def write_results(good_files: List[Dict], bad_files: List[Dict], output_file: str = 'resultado_revision.txt'):
    """
    Escribe los resultados detallados en un archivo.

    Args:
        good_files (List[Dict]): Lista de archivos buenos con su análisis
        bad_files (List[Dict]): Lista de archivos malos con su análisis
        output_file (str): Nombre del archivo de salida
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as result_file:
            result_file.write("=== RESUMEN DE LA REVISIÓN ===\n\n")
            result_file.write(f"Total archivos procesados: {len(good_files) + len(bad_files)}\n")
            result_file.write(f"Archivos correctos: {len(good_files)}\n")
            result_file.write(f"Archivos incorrectos: {len(bad_files)}\n\n")

            result_file.write("=== ARCHIVOS CORRECTOS ===\n")
            for file_info in sorted(good_files, key=lambda x: x['filename']):
                result_file.write(f"\nArchivo: {file_info['filename']}\n")
                result_file.write(f"Delimitador: {repr(file_info['analysis']['delimiter'])}\n")
                result_file.write(f"Número de columnas: {file_info['analysis']['num_columns']}\n")
                result_file.write("Primeras líneas:\n")
                for i, line in enumerate(file_info['analysis']['preview_lines'], 1):
                    result_file.write(f"  {i}: {line}\n")
                result_file.write("-" * 50 + "\n")

            result_file.write("\n=== ARCHIVOS INCORRECTOS ===\n")
            for file_info in sorted(bad_files, key=lambda x: x['filename']):
                result_file.write(f"\nArchivo: {file_info['filename']}\n")
                if file_info['analysis']:
                    result_file.write(f"Delimitador: {repr(file_info['analysis']['delimiter'])}\n")
                    result_file.write(f"Número de columnas: {file_info['analysis']['num_columns']}\n")
                    result_file.write("Primeras líneas:\n")
                    for i, line in enumerate(file_info['analysis']['preview_lines'], 1):
                        result_file.write(f"  {i}: {line}\n")
                else:
                    result_file.write("No se pudo analizar el archivo\n")
                result_file.write("-" * 50 + "\n")

        logging.info(f"Resultados guardados en {output_file}")

    except Exception as e:
        logging.error(f"Error al escribir resultados: {str(e)}")
        raise


def main():
    """Función principal del programa"""
    directory = '../assets/dades'

    try:
        logging.info("Iniciando procesamiento de archivos")
        good_files, bad_files = process_directory(directory)
        write_results(good_files, bad_files)
        logging.info("Procesamiento completado con éxito")

        # Imprimir resumen en consola
        print(f"\nProcesamiento completado:")
        print(f"- Total archivos: {len(good_files) + len(bad_files)}")
        print(f"- Archivos correctos: {len(good_files)}")
        print(f"- Archivos incorrectos: {len(bad_files)}")
        print("\nRevisa 'resultado_revision.txt' para más detalles")

    except Exception as e:
        logging.error(f"Error en la ejecución principal: {str(e)}")
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
