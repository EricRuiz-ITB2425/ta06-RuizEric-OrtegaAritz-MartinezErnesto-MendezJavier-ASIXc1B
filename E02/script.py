import os
from datetime import datetime

def check_header(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [file.readline().strip() for _ in range(2)]
            # Verificar que hay al menos dos líneas
            if len(lines) < 2:
                return False
            # Verificar que la cabecera es correcta
            if lines[0] == "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1" and lines[1].endswith("-1"):
                return True
            else:
                return False
    except Exception as e:
        print(f"Error leyendo el archivo {file_path}: {e}")
        return False

def main(directory):
    good_files = []
    bad_files = []

    # Crear la carpeta 'logs' si no existe
    logs_dir = os.path.join(directory, '../../E02/logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Obtener la fecha y hora actuales
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Nombre del archivo de log
    log_filename = f"logs_{current_time}.log"

    # Ruta completa del archivo de log
    log_filepath = os.path.join(logs_dir, log_filename)

    # Escribir los logs en el archivo de log
    with open(log_filepath, 'w') as log_file:
        log_file.write("Proceso de revisión de archivos:\n")
        log_file.write(f"Fecha y hora: {current_time}\n")

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                log_file.write(f"Revisando archivo: {file_path}\n")
                is_good = check_header(file_path)
                if is_good:
                    good_files.append(filename)
                    log_file.write(f"{file_path}: Cabecera correcta\n")
                else:
                    bad_files.append(filename)
                    log_file.write(f"{file_path}: Cabecera incorrecta\n")

    # Nombre del archivo de resultados
    results_filename = f"resultados_revision_{current_time}.txt"

    # Ruta completa del archivo de resultados
    results_filepath = os.path.join(logs_dir, results_filename)

    # Escribir los resultados en el archivo de resultados
    with open(results_filepath, 'w') as result_file:
        result_file.write("Archivos buenos:\n")
        for filename in good_files:
            result_file.write(f"{filename}: True\n")
        result_file.write("\nArchivos nulos:\n")
        for filename in bad_files:
            result_file.write(f"{filename}: False\n")

if __name__ == "__main__":
    # Reemplaza '../assets/dades' con la ruta real de la carpeta que contiene los archivos
    main('../assets/dades')