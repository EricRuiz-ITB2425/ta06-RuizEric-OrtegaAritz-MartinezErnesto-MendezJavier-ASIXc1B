import os
from datetime import datetime


def check_header(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [file.readline().strip() for _ in range(2)]
            # Verificar que hay al menos dos líneas
            if len(lines) < 2:
                missing_line_number = 2 if len(lines) == 1 else 1
                return False, missing_line_number, "La línea no existe"
            # Verificar que la cabecera es correcta
            if lines[0] != "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1":
                return False, 1, f"La línea no cumple los requisitos: {lines[0]}"
            if not lines[1].endswith("-1"):
                return False, 2, f"La línea no cumple los requisitos: {lines[1]}"
            # Si ambas líneas son correctas
            return True, None, None
    except Exception as e:
        print(f"Error leyendo el archivo {file_path}: {e}")
        return False, None, None


def process_file(file_path):
    total_values = 0
    missing_values = 0
    lines_processed = 0

    try:
        with open(file_path, 'r') as file:
            # Saltar las dos primeras líneas (cabeceras)
            file.readline()
            file.readline()

            for line in file:
                lines_processed += 1
                values = line.strip().split()[3:]  # Omitir las primeras tres columnas
                total_values += len(values)
                missing_values += values.count('-999')

    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")

    return total_values, missing_values, lines_processed


def main(directory):
    good_files_count = 0
    bad_files = []
    total_files_processed = 0
    total_values_processed = 0
    total_missing_values = 0
    total_lines_processed = 0

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
                is_good, incorrect_line_number, incorrect_line = check_header(file_path)
                if is_good:
                    good_files_count += 1
                    total_files_processed += 1
                    log_file.write(f"{file_path}: Cabecera correcta\n")

                    total_values, missing_values, lines_processed = process_file(file_path)
                    total_values_processed += total_values
                    total_missing_values += missing_values
                    total_lines_processed += lines_processed
                else:
                    bad_files.append((filename, incorrect_line_number, incorrect_line))
                    log_file.write(f"{file_path}: Cabecera incorrecta\n")

    # Calcular el porcentaje de datos faltantes
    if total_values_processed > 0:
        percentage_missing_values = (total_missing_values / total_values_processed) * 100
    else:
        percentage_missing_values = 0

    # Nombre del archivo de resultados
    results_filename = f"resultados_revision_{current_time}.txt"

    # Ruta completa del archivo de resultados
    results_filepath = os.path.join(logs_dir, results_filename)

    # Escribir los resultados en el archivo de resultados
    with open(results_filepath, 'w') as result_file:
        result_file.write(f"Total de archivos con cabeceras correctas: {good_files_count:,}\n\n")
        result_file.write("Archivos nulos:\n")
        for filename, incorrect_line_number, incorrect_line in bad_files:
            result_file.write(f"Archivo: {filename}\n")
            result_file.write(f"Linea {incorrect_line_number}: {incorrect_line}\n\n")

        result_file.write("Resumen de procesamiento de datos:\n")
        result_file.write(f"Total de valores procesados: {total_values_processed:,}\n")
        result_file.write(f"Valores faltantes (-999): {total_missing_values:,}\n")
        result_file.write(f"Porcentaje de datos faltantes: {percentage_missing_values:.2f}%\n")
        result_file.write(f"Archivos procesados: {total_files_processed:,}\n")
        result_file.write(f"Lineas procesadas: {total_lines_processed:,}\n")


if __name__ == "__main__":
    # Reemplaza '../assets/dades' con la ruta real de la carpeta que contiene los archivos
    main('../../assets/dades')