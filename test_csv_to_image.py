import os
import glob
import pandas as pd
import numpy as np
from PIL import Image

# 시작과 끝 좌표 설정
start_row, start_col = 60, 157
end_row, end_col = 1350, 700

# csv 폴더 안에 있는 모든 CSV 파일 찾기
input_folder_path = './csv'
output_folder_path = './csv_to_images'
csv_files = glob.glob(os.path.join(input_folder_path, '*.csv'))

# 각 CSV 파일에 대해 처리
for csv_file in csv_files:

    print(csv_file)

    # CSV 파일 로드
    df = pd.read_csv(csv_file, low_memory=False)

    # NaN 값을 0으로 대체
    df.fillna(0, inplace=True)

    # 숫자로 변환 가능한 열만 선택하여 NumPy 배열로 변환
    numeric_columns = df.select_dtypes(include=[np.number])
    data_array = numeric_columns.to_numpy(dtype=np.float64)


    # 이미지 크기 계산
    image_width = end_col - start_col + 1
    image_height = end_row - start_row + 1


    # 이미지 배열 생성
    image_data = np.full((image_height, image_width, 3), 255, dtype=np.uint8)  # 모든 픽셀을 하얀색으로 초기화


    # 특정 범위의 셀 값 확인 및 이미지 배열에 픽셀 그리기
    row_indices = np.arange(start_row - 1, end_row)
    col_indices = np.arange(start_col - 1, end_col)


    # 해당 범위의 데이터 추출
    data_range = data_array[row_indices[:, None], col_indices]

    # NaN 값이 있는 위치에 0으로 설정
    data_range[np.isnan(data_range)] = 0

    # 픽셀 색상 설정
    black_pixels = (data_range >= 16) & (data_range <= 18)

    # 검은색 픽셀로 설정
    image_data[black_pixels] = [0, 0, 0]

    # 이미지 생성
    image = Image.fromarray(image_data)

    # 이미지 저장
    file_name = os.path.splitext(os.path.basename(csv_file))[0] + '.png'
    output_file_path = os.path.join(output_folder_path, file_name)
    image.save(output_file_path)