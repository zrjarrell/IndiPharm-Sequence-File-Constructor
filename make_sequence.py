import json, os
import pandas as pd

config = json.load(open("config.json"))

header = ["blank1", "blank2", "s9", "cofactors","s9-cofactors", "drug-diluent",
          "positive1", "positive2", "positive3", "positive4", "positive5"]
header_wells = ["D12", "D12", "D1", "E1", "E12", "A1", "A2", "A3", "F12", "G12", "H12"]
tail = ["blank3", "blank4"]
tail_wells = ["D12", "D12"]

def lead_zero(i):
    if len(str(i)) == 1:
        return "0" + str(i)
    else:
        return str(i)

def make_exp_sample_list(layout, metadata):
    sample_middle = []
    well_middle = []
    i = 1
    for key, value in layout.items():
        well_middle += [key, key]
        sample_name = f'{lead_zero(i)}_{value["generic_name"]}_{metadata["condition_time"]}'
        sample_middle += [sample_name + "_1", sample_name + "_2"]
        i += 1
    return sample_middle, well_middle

def condition_bookends(piece, piece_wells, metadata):
    samples = []
    wells = []
    for i in range(0, len(piece)):
        labeled_sample = f'{piece[i]}_{metadata["condition_time"]}'
        samples += [labeled_sample + "_1", labeled_sample + "_2"]
        wells += [piece_wells[i], piece_wells[i]]
    return samples, wells

def make_sample_list(layout, metadata):
    samples, wells = condition_bookends(header, header_wells, metadata)
    samples += ["qstd_1", "qstd_2", "qstd_3", "qstd_4", "qstd_5", "qstd_6"]
    wells += ["F1", "F1", "F1", "F1", "F1", "F1"]
    sample_mid, well_mid = make_exp_sample_list(layout, metadata)
    samples += sample_mid
    wells += well_mid
    samples += ["qstd_7", "qstd_8", "qstd_9", "qstd_10", "qstd_11", "qstd_12"]
    wells += ["F1", "F1", "F1", "F1", "F1", "F1"]
    sample_tail, well_tail = condition_bookends(tail, tail_wells, metadata)
    samples += sample_tail
    wells += well_tail
    return samples, wells

def make_sequence_file(layout, metadata, plate_pos, layout_name):
    samples, wells = make_sample_list(layout, metadata)
    plate_wells = []
    for well in wells:
        plate_wells += [f"{plate_pos}:{well}"]
    sample_types = ["Unknown"] * len(samples)
    path = os.path.join(config["parent_dir"], layout_name + "_" + metadata["condition_time"])
    paths = [path] * len(samples)
    methods = config["methods_files"] * int(len(samples) / 2)
    channel = [1, 2] * int(len(samples) / 2)
    volumes = [3] * len(samples)
    sequence_dict = {"Sample Type": sample_types, "File Name": samples, "Sample ID": samples, "Path": paths, "Instrument Method": methods, "L1 ChannelSelect": channel, "Position": plate_wells, "Inj Vol": volumes}
    sequence_table = pd.DataFrame(sequence_dict)
    filename = os.path.join(config["parent_dir"], layout_name + "_" + metadata["condition_time"], layout_name + "_" + metadata["condition_time"] + "_sequence_file.csv")
    sequence_table.to_csv(filename, index=False)
    header = "Bracket Type=2\n"
    with open(filename, "r") as file:
        content = file.read()
    with open(filename, "w") as file:
        file.write(header + content)
