import json, os
from parse_code import parse_code
from make_sequence import make_sequence_file

config = json.load(open("config.json"))
layout_library = json.load(open("layout_library.json"))

def mkdir_if_not(dirpath):
    if os.path.exists(dirpath):
        pass
    else:
        dirpath = os.path.normpath(dirpath)
        os.mkdir(dirpath)

if __name__ == "__main__":
    metadata = False
    while not metadata:
        code = input("Scan barcode or type in code: ")
        metadata = parse_code(code)
    plate_pos = input("Please enter autosampler position (R/G/B/Y): ")
    layout = layout_library[metadata["layout_key"]]
    layout_name = layout["name"]
    layout = layout["layout"]
    mkdir_if_not(os.path.join(config["parent_dir"], layout_name + "_" + metadata["condition_time"]))
    make_sequence_file(layout, metadata, plate_pos, layout_name)