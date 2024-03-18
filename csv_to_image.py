import os
import glob
import pandas as pd
import numpy as np
from PIL import Image

# 시작과 끝 좌표 설정
start_row, start_col = 60, 157
end_row, end_col = 1350, 700

# A 폴더 안에 있는 모든 CSV 파일 찾기
input_folder_path = './csv'
output_folder_path = './csv_to_images'
csv_files = glob.glob(os.path.join(input_folder_path, '*.csv'))

# 각 CSV 파일에 대해 처리
for csv_file in csv_files:
    # CSV 파일 로드
    df = pd.read_csv(csv_file, header=None)

    # 이미지 크기 계산
    image_width = end_col - start_col + 1
    image_height = end_row - start_row + 1

    # 이미지 배열 생성
    image_data = np.full((image_height, image_width, 3), 255, dtype=np.uint8)  # 모든 픽셀을 하얀색으로 초기화

    # 특정 범위의 셀 값 확인 및 이미지 배열에 픽셀 그리기
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            cell_value = df.iloc[row - 1, col - 1]  # DataFrame은 0부터 인덱싱되므로 1을 빼줌
            if 16 <= cell_value <= 18:
                image_data[row - start_row, col - start_col] = [0, 0, 0]  # 검은색 픽셀

    # 이미지 생성
    image = Image.fromarray(image_data)

    # 이미지 저장
    file_name = os.path.splitext(os.path.basename(csv_file))[0] + '.png'
    output_file_path = os.path.join(output_folder_path, file_name)
    image.save(output_file_path)