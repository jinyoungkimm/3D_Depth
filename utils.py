######## 3D 비전 카메라에서 최초로 저장한 csv 파일로부터 바로 이미지를 추출 에러가 뜬다. 고로 아래 과정을 통하여 csv 파일을 다듬어 주어야 한다 ####
# https://pylife.tistory.com/entry/PythonPandas-ParserError-Error-tokenizing-data -> 에러 해결에 참조한 사이트


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


