import os
from datetime import datetime
import csv

def check_header(file_path, log_file):
    try:
        with open(file_path, 'r') as file:
            lines = [file.readline().strip() for _ in range(2)]
            if len(lines) < 2:
                missing_line_number = 2 if len(lines) == 1 else 1
                return False, missing_line_number, "La línea no existe"
            if lines[0] != "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1":
                return False, 1, f"La línea no cumple los requisitos: {lines[0]}"
            if not lines[1].endswith("-1"):
                return False, 2, f"La línea no cumple los requisitos: {lines[1]}"
            return True, None, None
    except Exception as e:
        log_file.write(f"Error leyendo el archivo {file_path}: {e}\n")
        return False, None, None

def process_file(file_path, log_file):
    total_values = 0
    missing_values = 0
    yearly_data = {}

    try:
        with open(file_path, 'r') as file:
            file.readline()
            file.readline()

            for i, line in enumerate(file, start=3):
                parts = line.strip().split()
                if len(parts) < 3 or len(parts) != 34:
                    log_file.write(f"{file_path}: Línea {i} mal formateada ({line.strip()})\n")
                    continue

                try:
                    year = int(parts[1])
                    values = list(map(float, parts[3:]))

                    if len(values) != 31:
                        log_file.write(f"{file_path}: Línea {i} con valores incompletos ({line.strip()})\n")
                        continue

                except ValueError as ve:
                    log_file.write(f"{file_path}: Línea {i} no se pudo parsear ({ve})\n")
                    continue

                total_values += len(values)
                missing_values += values.count(-999)

                valid_values = [v for v in values if v != -999]
                if year not in yearly_data:
                    yearly_data[year] = []
                yearly_data[year].append(sum(valid_values))

    except Exception as e:
        log_file.write(f"Error procesando el archivo {file_path}: {e}\n")

    return total_values, missing_values, yearly_data

def calculate_statistics(yearly_data):
    yearly_precipitation = {year: sum(values) for year, values in yearly_data.items()}
    yearly_average = {year: sum(values) / len(values) for year, values in yearly_data.items() if values}
    return yearly_precipitation, yearly_average

def main(directory):
    good_files_count = 0
    total_files_processed = 0
    total_values_processed = 0
    total_missing_values = 0
    combined_yearly_data = {}

    logs_dir = os.path.join(directory, '../../E02/logs')
    os.makedirs(logs_dir, exist_ok=True)

    log_filepath = os.path.join(logs_dir, "TA06.log")
    results_filepath = os.path.join(logs_dir, "resultados.txt")
    csv_filepath = os.path.join(logs_dir, "resultados.csv")

    with open(log_filepath, 'w') as log_file, open(results_filepath, 'w') as results_file, open(csv_filepath, 'w', newline='') as csv_file:
        log_file.write("Proceso de revisión de archivos:\n")
        log_file.write(f"Fecha y hora: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Año', 'Total Precipitación (L/m²)', 'Promedio Precipitación (L/m²)'])

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                log_file.write(f"Revisando archivo: {file_path}\n")
                is_good, incorrect_line_number, incorrect_line = check_header(file_path, log_file)
                if is_good:
                    good_files_count += 1
                    total_files_processed += 1
                    log_file.write(f"{file_path}: Cabecera correcta\n")

                    total_values, missing_values, yearly_data = process_file(file_path, log_file)
                    total_values_processed += total_values
                    total_missing_values += missing_values

                    for year, values in yearly_data.items():
                        if year not in combined_yearly_data:
                            combined_yearly_data[year] = []
                        combined_yearly_data[year].extend(values)
                else:
                    log_file.write(f"Archivo: {filename}\n")
                    log_file.write(f"Linea {incorrect_line_number}: {incorrect_line}\n\n")

        yearly_precipitation, yearly_average = calculate_statistics(combined_yearly_data)

        results_file.write(f"\nTotal de archivos con cabeceras correctas: {good_files_count:,}\n")
        results_file.write(f"Archivos procesados: {total_files_processed:,}\n")
        results_file.write(f"Total de valores procesados: {total_values_processed:,}\n")
        results_file.write(f"Valores faltantes (-999): {total_missing_values:,}\n")
        if total_values_processed > 0:
            percentage_missing_values = (total_missing_values / total_values_processed) * 100
        else:
            percentage_missing_values = 0
        results_file.write(f"Porcentaje de datos faltantes: {percentage_missing_values:.2f}%\n")

        results_file.write("\nEstadísticas de precipitaciones:\n")
        for year in sorted(yearly_precipitation):
            total_precip = yearly_precipitation[year]
            avg_precip = yearly_average.get(year, 0)
            results_file.write(f"{year}: Total {total_precip:,} L/m² - Promedio {avg_precip:.2f} L/m²\n")
            csv_writer.writerow([year, total_precip, avg_precip])

if __name__ == "__main__":
    main('../assets/dades')
#a