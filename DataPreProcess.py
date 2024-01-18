# import pandas as pd

# # 任务1: 修改文件扩展名
# def convert_dcm_to_jpg(csv_path, output_path):
#     df = pd.read_csv(csv_path)
#     df['path'] = df['path'].str.replace('.dcm', '.jpg')
#     df.to_csv(output_path, index=False)

# convert_dcm_to_jpg("/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/cxr-record-list.csv", "/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/cxr-record-jpg-list.csv")

# # 任务2: 合并两个CSV文件
# def merge_csv(record_csv, study_csv, output_path):
#     record_df = pd.read_csv(record_csv)
#     study_df = pd.read_csv(study_csv)
#     merged_df = pd.merge(record_df, study_df, on=['subject_id', 'study_id'], suffixes=('_record', '_study'))
#     merged_df.to_csv(output_path, index=False)

# merge_csv("/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/cxr-record-jpg-list.csv", "/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/cxr-study-list.csv", "/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/cxr-record-study-list.csv")

# import os
# import re
# import csv
# from shutil import copyfile

# def extract_findings(text):
#     """
#     Extracts the 'FINDINGS' section from the text.
#     """
#     start = text.find("FINDINGS:")
#     if start == -1:
#         return ""
#     start += len("FINDINGS:")
#     end = text.find("IMPRESSION:", start)
#     if end == -1:
#         end = len(text)
#     return text[start:end].strip()

# def extract_impression(text):
#     """
#     Extracts the 'IMPRESSION' section from the text.
#     """
#     start = text.find("IMPRESSION:")
#     if start == -1:
#         return ""
#     start += len("IMPRESSION:")
#     end = text.find("\n\n", start)
#     if end == -1:
#         end = len(text)
#     return text[start:end].strip()

# def process_file(file_path, output_dir, input_dir, invalid_files):
#     """
#     Processes a single file, extracting the required sections and checking if they are valid.
#     Preserves the directory structure of the input file in the output directory.
#     """
#     with open(file_path, 'r') as file:
#         text = file.read()
#         findings = extract_findings(text)
#         impression = extract_impression(text)

#         if not findings and not impression or len(findings.split()) < 3 and len(impression.split()) < 3:
#             invalid_files.append(file_path)
#             return False

#         # 修改的部分: 保持原始文件的目录结构
#         relative_path = os.path.relpath(file_path, input_dir)
#         new_file_path = os.path.join(output_dir, relative_path)

#         os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

#         with open(new_file_path, 'w') as new_file:
#             if len(findings.split()) >= 3 and len(impression.split()) >= 3:
#                 new_file.write(f"{findings}\n{impression}".strip())
#             elif len(findings.split()) < 3:
#                 new_file.write(f"{impression}".strip())
#             elif len(impression.split()) < 3:
#                 new_file.write(f"{findings}".strip())
#         return True

# INPUT_DIR = "/remote-home/share/22-yuewu-22210240319/mimic-cxr-report/files"
# OUTPUT_DIR = "/remote-home/share/22-yuewu-22210240319/mimic-cxr-report/preprocessed_files/"
# CSV_PATH = "/remote-home/share/22-yuewu-22210240319/mimic-cxr-report/invalid_files.csv"

# invalid_files = []

# # Process each file in the input directory
# for root, dirs, files in os.walk(INPUT_DIR):
#     for file in files:
#         if file.endswith('.txt'):
#             file_path = os.path.join(root, file)
#             process_file(file_path, OUTPUT_DIR, INPUT_DIR, invalid_files)

# # Save the invalid files to a CSV
# with open(CSV_PATH, 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(['Invalid File Path'])
#     for file in invalid_files:
#         csvwriter.writerow([file])

import csv

# 读取无效文件路径
invalid_files = set()
with open("/remote-home/share/22-yuewu-22210240319/mimic-cxr-report/invalid_files.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        if row:  # 确保行不为空
            invalid_files.add(row[0])

# 处理cxr-record-study_list.csv文件，移除无效的行
valid_rows = []
with open("/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/cxr-record-study-list.csv", 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # 保存标题行
    valid_rows.append(header)
    for row in reader:
        if row and row[4] not in invalid_files:  # 假设无效文件路径在第五列
            valid_rows.append(row)

# 将有效的行数据写入新文件
with open("/remote-home/share/22-yuewu-22210240319/mimic-cxr-jpg/physionet.org/files/mimic-cxr-jpg/2.0.0/valid-cxr-record-study-list.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(valid_rows)
