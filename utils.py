import os
import csv
import pandas as pd

# A 폴더와 B 폴더 경로 설정
input_folder_path = './csv'
output_folder_path = './csv'

# A 폴더 안에 있는 모든 CSV 파일 찾기
csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

# 각 CSV 파일에 대해 처리
for csv_file_name in csv_files:
    # CSV 파일 경로 설정
    input_file_path = os.path.join(input_folder_path, csv_file_name)

    # CSV 파일 열기
    with open(input_file_path, 'rt') as file:
        reader = csv.reader(file)
        csv_list = []
        for row in reader:
            csv_list.append(row)

    # DataFrame으로 변환
    df = pd.DataFrame(csv_list)

    # 결과를 B 폴더에 저장
    output_file_path = os.path.join(output_folder_path, csv_file_name)
    df.to_csv(output_file_path, index=False, header=False)


