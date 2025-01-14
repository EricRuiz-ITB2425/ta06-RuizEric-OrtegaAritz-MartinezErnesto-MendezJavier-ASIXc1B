import os
import logging
from typing import Tuple, List
from colorama import init, Fore, Style
import re
from datetime import datetime

# Inicializar colorama para que funcione en Windows
init()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='procesamiento_archivos.log'
)


def natural_sort_key(s):
    """
    Función auxiliar para ordenación natural de strings con números.
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]


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
        raise FileNotFoundError(f"{Fore.RED}El directorio {directory} no existe{Style.RESET_ALL}")

    good_files = []
    bad_files = []

    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if not os.path.isfile(file_path):
                continue

            print(f"{Fore.CYAN}Procesando archivo: {filename}{Style.RESET_ALL}")
            is_good = check_header(file_path)

            if is_good:
                good_files.append(filename)
                print(f"{Fore.GREEN}✓ Archivo correcto: {filename}{Style.RESET_ALL}")
            else:
                bad_files.append(filename)
                print(f"{Fore.RED}✗ Archivo incorrecto: {filename}{Style.RESET_ALL}")

    except Exception as e:
        logging.error(f"Error al procesar el directorio: {str(e)}")
        raise

    return good_files, bad_files


def write_results(good_files: List[str], bad_files: List[str], output_file: str = 'resultado_revision.txt'):
    """
    Escribe los resultados en un archivo con ordenación numérica.

    Args:
        good_files (List[str]): Lista de archivos buenos
        bad_files (List[str]): Lista de archivos malos
        output_file (str): Nombre del archivo de salida
    """
    try:
        # Obtener fecha y hora actual en UTC
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        current_user = "AritzOrtega-ITB2425"  # Usuario actual

        with open(output_file, 'w', encoding='utf-8') as result_file:
            # Cabecera con información temporal
            result_file.write(f"=== Resumen de la revisión ===\n")
            result_file.write(f"Current Date and Time (UTC): {current_time}\n")
            result_file.write(f"Current User's Login: {current_user}\n\n")

            # Estadísticas
            total_files = len(good_files) + len(bad_files)
            result_file.write(f"Total archivos procesados: {total_files}\n")
            result_file.write(f"Archivos correctos: {len(good_files)}\n")
            result_file.write(f"Archivos incorrectos: {len(bad_files)}\n\n")

            # Archivos correctos ordenados numéricamente
            result_file.write("Archivos correctos:\n" + "=" * 20 + "\n")
            for i, filename in enumerate(sorted(good_files, key=natural_sort_key), 1):
                result_file.write(f"{i}. ✓ {filename}\n")

            # Archivos incorrectos ordenados numéricamente
            result_file.write("\nArchivos incorrectos:\n" + "=" * 20 + "\n")
            for i, filename in enumerate(sorted(bad_files, key=natural_sort_key), 1):
                result_file.write(f"{i}. ✗ {filename}\n")

        print(f"{Fore.GREEN}Resultados guardados en {output_file}{Style.RESET_ALL}")

    except Exception as e:
        error_msg = f"Error al escribir resultados: {str(e)}"
        logging.error(error_msg)
        print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
        raise


def main():
    """Función principal del programa"""
    directory = '../assets/dades'

    try:
        print(f"\n{Fore.CYAN}=== Iniciando procesamiento de archivos ==={Style.RESET_ALL}\n")
        good_files, bad_files = process_directory(directory)
        write_results(good_files, bad_files)

        # Imprimir resumen en consola con colores
        total = len(good_files) + len(bad_files)
        print(f"\n{Fore.CYAN}=== Resumen del Procesamiento ==={Style.RESET_ALL}")
        print(f"Total archivos: {Fore.YELLOW}{total}{Style.RESET_ALL}")
        print(f"Archivos correctos: {Fore.GREEN}{len(good_files)}{Style.RESET_ALL}")
        print(f"Archivos incorrectos: {Fore.RED}{len(bad_files)}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Revisa 'resultado_revision.txt' para más detalles{Style.RESET_ALL}\n")

    except Exception as e:
        error_msg = f"Error en la ejecución principal: {str(e)}"
        logging.error(error_msg)
        print(f"\n{Fore.RED}{error_msg}{Style.RESET_ALL}")
        raise


if __name__ == "__main__":
    main()
