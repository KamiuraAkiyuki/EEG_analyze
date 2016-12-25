import glob
import re
from datetime import datetime

def get_matched_files(folder_path, pattern):
    if folder_path[-1] == "/":
        folder_path = folder_path[:-1]
    files = glob.glob(folder_path + "/*")
    matched_files = [file for file in files if re.match(pattern, file)]
    sorted_files = []
    for fi in matched_files:
        epoc_csv = re.search(r".*\-(?P<timeinfo>[0-9]{2}\.[0-9]{2}\.[0-9]{2}(\-|\.)[0-9]{2}\.[0-9]{2}\.[0-9]{2})\.csv", fi)
        if epoc_csv:
            day_info_strs = re.split(r"\.|\-", epoc_csv.groups("timeinfo")[0])
            day_info_strs[2] = "20" + day_info_strs[2]
            day_info_str = '.'.join(day_info_strs)
            measure_time = datetime.strptime(day_info_str, "%d.%m.%Y.%H.%M.%S")
            sorted_files.append([measure_time, fi])
        else:
            measure_time = datetime(9999, 12, 31, 12, 59, 59)
            sorted_files.append([measure_time, fi])
    sorted_files = sorted(sorted_files, key=lambda x: x[0])
    return sorted_files

def print_matched_files(folder_path, pattern):
    sorted_files = get_matched_files(folder_path, pattern)
    i = 0
    while(i < len(sorted_files)):
        print(sorted_files[i][0].strftime("%m/%d: ") + sorted_files[i][1])
        for j in range(i+1, len(sorted_files)):
            if(sorted_files[i][0].strftime("%Y-%m-%d") == sorted_files[j][0].strftime("%Y-%m-%d")):
                print('       ' + sorted_files[j][1])
                i = j
        i += 1

def select_csv_file():
    #######
    print_matched_files('datas/', r".+\.csv")

    input_str = input(">>> ")
    path = input_str
    return path
