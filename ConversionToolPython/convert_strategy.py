import sys
import os

def validate_data_v1_row(raw_row, row_num):
    raw_row = raw_row.lstrip("\ufeff")

    parts = raw_row.split("|")
    if len(parts) != 8:
        raise ValueError(f"Row {row_num}: Expected 8 columns, got {len(parts)}")

    validated = []
    for i, p in enumerate(parts):
        p = p.strip()

        if i in (0, 1, 2, 3, 4, 5, 6, 7):
            try:
                p = int(p)
            except:
                raise ValueError(f"Row {row_num}: Column {i+1} must be integer (got '{p}')")

        validated.append(p)

    activation, slot, unit, upgrade, action, wait_time, auto_ability, special_ability = validated

    if activation not in (0, 1): raise ValueError("Activation must be 0 or 1")
    if not (1 <= slot <= 7): raise ValueError("Slot must be 1–7")
    if not (1 <= unit <= 6): raise ValueError("Unit must be 1–6")
    if not (1 <= upgrade <= 13): raise ValueError("Upgrade must be 1–13")

    if not (1 <= action <= 7): raise ValueError("Action must be 1–7")

    if auto_ability not in (0, 1): raise ValueError("Auto ability must be 0 or 1")
    if special_ability not in (0, 1): raise ValueError("Special ability must be 0 or 1")

    return validated


def decode_data_v1_to_v2(row):
    _, slot, unit, upgrade, action, wait_time, _, special_ability = row

    slot_v2 = "None" if slot == 1 else f"Slot {slot - 1}"
    unit_v2 = "None" if unit == 1 else f"Unit {unit - 1}"
    level_v2 = "Max" if upgrade == 13 else str(upgrade - 1)
    priority_v2 = "None"

    if special_ability == 1:
        action_v2 = "Special Ability"
    else:
        if action in (2, 3):
            action_v2 = "Place"
        elif action == 7:
            action_v2 = "Restart"
        else:
            action_v2 = "None"

    return [slot_v2, unit_v2, level_v2, priority_v2, action_v2, wait_time]


def convert_dataset_v1_to_v2(raw):
    data_v1 = []
    for i, line in enumerate(raw, start=1):
        line = line.strip()
        if not line:
            continue
        validated = validate_data_v1_row(line, i)
        data_v1.append(validated)

    data_v2 = [decode_data_v1_to_v2(r) for r in data_v1]

    TARGET = 124
    filler = ["None", "None", "0", "None", "None", 0]

    if len(data_v2) < TARGET:
        data_v2.extend([filler] * (TARGET - len(data_v2)))
    else:
        data_v2 = data_v2[:TARGET]

    return data_v2


def export_data_v2_as_text(data_v2, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for row in data_v2:
            f.write("|".join(str(x) for x in row) + "\n")


def main():
    if len(sys.argv) < 2:
        print("Drag a DataV1 text file onto convert.bat or convert.py")
        return

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print("File not found:", input_path)
        return

    with open(input_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    data_v2 = convert_dataset_v1_to_v2(raw_lines)

    output_path = os.path.join(os.path.dirname(input_path), "DataV2.txt")
    export_data_v2_as_text(data_v2, output_path)

    print("Conversion complete!")
    print("Saved as:", output_path)


if __name__ == "__main__":
    main()
