import json, sys
import pandas as pd

layout_library = json.load(open("layout_library.json"))

def name_layout(code):
    num = int(code) + 1
    return f"drug-layout-{num}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Include 2-digit layout code and layout table filepath in command.")
        print("Ex: 'python layout-transformer.py ## ./path/to/layout/table.csv'")
    else:
        code = sys.argv[1]
        path = sys.argv[2]
        layout_table = pd.read_csv(path)
        layout_table.iloc[:,0] = layout_table.iloc[:,0].str.replace(" ", "_")
        layout_table.iloc[:,0] = layout_table.iloc[:,0].str.lower()
        layout_table.fillna(value="none", inplace=True)
        layout_dict = {}
        for i in layout_table.index:
            layout_dict[layout_table.iloc[i, 3]] = {
                "generic_name": layout_table.iloc[i, 0],
                "pharmakon_plate": layout_table.iloc[i, 1],
                "pharmakon_well": layout_table.iloc[i, 2]
            }
        layout_library[code] = {
            "name": name_layout(code),
            "layout": layout_dict
            }
        json.dump(layout_library, open("layout_library.json", 'w'), indent=4)