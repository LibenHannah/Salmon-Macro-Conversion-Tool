import os
import sys

def read_slot_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing file: {os.path.basename(file_path)}")

    coords = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip().lstrip("\ufeff") for line in f.readlines()]

    for i, line in enumerate(lines):
        if "|" not in line:
            raise ValueError(
                f"Invalid coordinate format in {os.path.basename(file_path)} line {i+1}: {line}"
            )

        x, y = line.split("|")
        x = x.lstrip("\ufeff")
        y = y.lstrip("\ufeff")

        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ValueError(
                f"Coordinates must be integers in {os.path.basename(file_path)} line {i+1}: {line}"
            )

        coords.append((x, y))

    if len(coords) < 5:
        coords.extend([(0, 0)] * (5 - len(coords)))
    elif len(coords) > 5:
        coords = coords[:5]

    return coords


def convert_coordinate_v1_to_v2(folder_path):
    required_files = {
        "Slot1.txt": "Unit1",
        "Slot2.txt": "Unit2",
        "Slot3.txt": "Unit3",
        "Slot4.txt": "Unit4",
        "speed.txt": "Unit5",
        "taka.txt":  "Unit6"
    }

    final_units = {}

    for filename, unit_name in required_files.items():
        file_path = os.path.join(folder_path, filename)
        coords = read_slot_file(file_path)
        final_units[unit_name] = coords

    output_lines = []
    for unit_name in ["Unit1", "Unit2", "Unit3", "Unit4", "Unit5", "Unit6"]:
        coords = final_units[unit_name]
        encoded = "".join(f"{x},{y}|" for x, y in coords)
        output_lines.append(f"{unit_name}={encoded}")

    return "\n".join(output_lines)


def save_output(v2_text, output_path):
    folder = os.path.dirname(output_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(v2_text)
