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
    yearly_data = {}

    try:
        with open(file_path, 'r') as file:
            # Saltar las dos primeras líneas (cabeceras)
            file.readline()
            file.readline()

            for line in file:
                lines_processed += 1
                parts = line.strip().split()
                if len(parts) < 3:
                    continue  # Ignorar líneas mal formateadas
                year = int(parts[1])  # El año está en la segunda columna
                values = list(map(float, parts[3:]))  # Valores de precipitaciones
                total_values += len(values)
                missing_values += values.count(-999)

                # Filtrar valores válidos
                valid_values = [v for v in values if v != -999]
                if year not in yearly_data:
                    yearly_data[year] = []
                yearly_data[year].extend(valid_values)

    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")

    return total_values, missing_values, lines_processed, yearly_data

def calculate_statistics(yearly_data):
    yearly_precipitation = {year: sum(values) for year, values in yearly_data.items()}
    yearly_average = {year: sum(values) / len(values) for year, values in yearly_data.items() if values}
    years = sorted(yearly_precipitation.keys())

    annual_variation = {}
    for i in range(1, len(years)):
        prev_year, current_year = years[i - 1], years[i]
        variation = ((yearly_precipitation[current_year] - yearly_precipitation[prev_year]) /
                     yearly_precipitation[prev_year]) * 100
        annual_variation[current_year] = variation

    most_rainy_year = max(yearly_precipitation, key=yearly_precipitation.get)
    driest_year = min(yearly_precipitation, key=yearly_precipitation.get)

    total_precipitation = sum(yearly_precipitation.values())

    return {
        "yearly_precipitation": yearly_precipitation,
        "yearly_average": yearly_average,
        "annual_variation": annual_variation,
        "most_rainy_year": most_rainy_year,
        "driest_year": driest_year,
        "total_precipitation": total_precipitation
    }

def main(directory):
    good_files_count = 0
    bad_files = []
    total_files_processed = 0
    total_values_processed = 0
    total_missing_values = 0
    total_lines_processed = 0
    combined_yearly_data = {}

    # Crear la carpeta 'logs' si no existe
    logs_dir = os.path.join(directory, '../../E02/logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Obtener la fecha y hora actuales
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Nombre del archivo de log
    log_filename = f"revision_cabeceras_{current_time}.log"

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

                    total_values, missing_values, lines_processed, yearly_data = process_file(file_path)
                    total_values_processed += total_values
                    total_missing_values += missing_values
                    total_lines_processed += lines_processed

                    for year, values in yearly_data.items():
                        if year not in combined_yearly_data:
                            combined_yearly_data[year] = []
                        combined_yearly_data[year].extend(values)
                else:
                    bad_files.append((filename, incorrect_line_number, incorrect_line))
                    log_file.write(f"{file_path}: Cabecera incorrecta\n")

    # Calcular estadísticas
    stats = calculate_statistics(combined_yearly_data)

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
        if total_values_processed > 0:
            percentage_missing_values = (total_missing_values / total_values_processed) * 100
        else:
            percentage_missing_values = 0
        result_file.write(f"Porcentaje de datos faltantes: {percentage_missing_values:.2f}%\n")
        result_file.write(f"Archivos procesados: {total_files_processed:,}\n")
        result_file.write(f"Lineas procesadas: {total_lines_processed:,}\n\n")

        result_file.write("Estadísticas de precipitaciones:\n")
        result_file.write(f"Total de precipitaciones: {stats['total_precipitation']:,}\n")
        result_file.write(f"Año más lluvioso: {stats['most_rainy_year']} ({stats['yearly_precipitation'][stats['most_rainy_year']]:,})\n")
        result_file.write(f"Año más seco: {stats['driest_year']} ({stats['yearly_precipitation'][stats['driest_year']]:,})\n\n")

        result_file.write("Precipitaciones anuales promedio:\n")
        for year, avg in sorted(stats['yearly_average'].items()):
            result_file.write(f"{year}: {avg:.2f} L\n ")

        result_file.write("\nTasa de variación anual de precipitaciones:\n")
        for year, variation in sorted(stats['annual_variation'].items()):
            result_file.write(f"{year}: {variation:.2f}%\n")

if __name__ == "__main__":
    # Reemplaza '../assets/dades' con la ruta real de la carpeta que contiene los archivos
    main('../../assets/dades')
