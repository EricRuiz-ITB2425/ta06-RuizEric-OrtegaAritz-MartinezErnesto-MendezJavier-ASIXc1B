import os
import logging
from typing import Tuple, List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='procesamiento_archivos.log'
)


def check_header(file_path: str) -> bool:
    """
    Verifica si un archivo tiene la cabecera correcta.

    Args:
        file_path (str): Ruta al archivo a verificar

    Returns:
        bool: True si la cabecera es correcta, False en caso contrario
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Leer las dos primeras líneas
            header = [next(file).strip() for _ in range(2)]

            # Verificar el formato de la cabecera
            return (
                    len(header) == 2 and
                    header[0] == "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1" and
                    header[1].startswith("P")
            )
    except StopIteration:
        logging.error(f"El archivo {file_path} tiene menos de 2 líneas")
        return False
    except Exception as e:
        logging.error(f"Error al procesar {file_path}: {str(e)}")
        return False


def process_directory(directory: str) -> Tuple[List[str], List[str]]:
    """
    Procesa todos los archivos en el directorio especificado.

    Args:
        directory (str): Ruta al directorio a procesar

    Returns:
        Tuple[List[str], List[str]]: Lista de archivos buenos y malos
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
            is_good = check_header(file_path)

            if is_good:
                good_files.append(filename)
                logging.info(f"Archivo correcto: {filename}")
            else:
                bad_files.append(filename)
                logging.warning(f"Archivo incorrecto: {filename}")

    except Exception as e:
        logging.error(f"Error al procesar el directorio: {str(e)}")
        raise

    return good_files, bad_files


def write_results(good_files: List[str], bad_files: List[str], output_file: str = 'resultado_revision.txt'):
    """
    Escribe los resultados en un archivo.

    Args:
        good_files (List[str]): Lista de archivos buenos
        bad_files (List[str]): Lista de archivos malos
        output_file (str): Nombre del archivo de salida
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as result_file:
            result_file.write("=== Resumen de la revisión ===\n\n")
            result_file.write(f"Total archivos procesados: {len(good_files) + len(bad_files)}\n")
            result_file.write(f"Archivos correctos: {len(good_files)}\n")
            result_file.write(f"Archivos incorrectos: {len(bad_files)}\n\n")

            result_file.write("Archivos correctos:\n" + "=" * 20 + "\n")
            for filename in sorted(good_files):
                result_file.write(f"✓ {filename}\n")

            result_file.write("\nArchivos incorrectos:\n" + "=" * 20 + "\n")
            for filename in sorted(bad_files):
                result_file.write(f"✗ {filename}\n")

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