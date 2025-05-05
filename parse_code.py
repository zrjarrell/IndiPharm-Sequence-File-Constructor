import datetime

condition_dict = {
    "0": "source",
    "1": "A-drug-only",
    "2": "B-w-s9",
    "3": "C-w-s9-nadph",
    "4": "D-w-udpga",
    "5": "E-w-paps",
    "6": "F-w-gsh",
    "7": "G-w-acetyl",
    "8": "H-w-sam",
    "9": "I-w-all"
}

def get_condition(condition, time):
    output_str = condition_dict[condition]
    if time == "0":
        if condition == "1":
            output_str = "J" + output_str[1:]
        elif condition == "9":
            output_str = "K" + output_str[1:]
        output_str += "_0hr"
    else:
        output_str += "_24hr"
    return output_str

def get_review_date(days):
    day0 = datetime.datetime.strptime("5/1/25", "%m/%d/%y")
    end_date = day0 + datetime.timedelta(days=int(days))
    return end_date.strftime("%m-%d-%Y")

def check_checksum(code):
    if len(code) < 12:
        return False
    sum = 0
    for digit in code[0:9]:
        sum += int(digit)
    if sum % 10 == int(code[9]):
        return True
    else:
        return False

def get_concentration(conc):
    conc = (int(conc) + 1) * 10
    return f"{conc} uM"

def parse_code(code):
    valid = check_checksum(code)
    if not valid:
        print("Invalid code.")
        return valid
    else:
        metadata = {"code": code}
        metadata["layout_key"] = code[0:2]
        metadata["condition_time"] = get_condition(code[2], code[10])
        metadata["review_date"] = get_review_date(code[5:9])
        metadata["concentration"] = get_concentration(code[3:5])
        return metadata