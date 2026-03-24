# inventory_analysis.py

# 파이썬 기본 제공 모듈인 pickle을 가져옵니다. (별도의 외부 패키지가 아닙니다)
# 리스트 객체를 이진 파일로 저장할 때 사용합니다.
import pickle

def analyze_inventory():
    file_path = 'Mars_Base_Inventory_List.csv'
    danger_file_path = 'Mars_Base_Inventory_danger.csv'
    binary_file_path = 'Mars_Base_Inventory_List.bin'
    
    try:
        # [수행과제 1] CSV 파일 읽어서 전체 출력
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_content = file.read()
            print('=== 1. 원본 CSV 파일 전체 출력 ===')
            print(raw_content)
            
        # [수행과제 2] 파일 내용을 파이썬 리스트(List) 객체로 변환
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        if not lines:
            print('안내: 파일이 비어 있습니다.')
            return
            
        # 첫 번째 줄은 제목(헤더)이므로 쉼표(,)를 기준으로 나누어 따로 저장합니다.
        header = lines[0].strip().split(',')
        data_list = []
        
        # 두 번째 줄부터 데이터 처리 시작
        for line in lines[1:]:
            line = line.strip()
            if line:  # 빈 줄이 아닐 경우에만 리스트에 추가합니다.
                row = line.split(',')
                data_list.append(row)
                
        # [수행과제 3] 배열 내용을 인화성이 높은 순(내림차순)으로 정렬
        # 인화성 수치는 5번째 항목(인덱스 4)에 있습니다.
        # 문자열을 float(실수)로 변환하여 크기를 비교하고, reverse=True로 내림차순 정렬합니다.
        data_list.sort(key=lambda x: float(x[4]), reverse=True)
        
        # [수행과제 4] 인화성 지수가 0.7 이상인 목록 뽑아서 별도 출력
        danger_list = []
        print('\n=== 2. 인화성 지수 0.7 이상 위험 물질 목록 (내림차순) ===')
        print(','.join(header))  # 제목 출력
        
        for row in data_list:
            flammability = float(row[4])
            if flammability >= 0.7:
                danger_list.append(row)
                print(','.join(row))
                
        # [수행과제 5] 인화성 지수 0.7 이상인 목록을 CSV 포맷으로 저장
        # 쓰기 모드('w')로 파일을 엽니다.
        with open(danger_file_path, 'w', encoding='utf-8') as file:
            file.write(','.join(header) + '\n')
            for row in danger_list:
                file.write(','.join(row) + '\n')
                
        print(f'\n안내: 위험 물질 목록이 {danger_file_path} 파일로 저장되었습니다.')
        
        # =====================================================================
        # [보너스 과제 1] 인화성 순서로 정렬된 배열(List)을 이진(Binary) 파일로 저장
        # 이진 파일은 'wb' (Write Binary) 모드를 사용합니다.
        # =====================================================================
        full_sorted_list = [header] + data_list
        with open(binary_file_path, 'wb') as bin_file:
            # 리스트 객체 형태 그대로 이진 파일로 포장(dump)합니다.
            pickle.dump(full_sorted_list, bin_file)
            
        print(f'안내: 정렬된 배열이 이진 파일 {binary_file_path}로 저장되었습니다.')
        
        # =====================================================================
        # [보너스 과제 2] 저장된 이진 파일을 다시 읽어 들여서 화면에 출력
        # 이진 파일을 읽을 때는 'rb' (Read Binary) 모드를 사용합니다.
        # =====================================================================
        with open(binary_file_path, 'rb') as bin_file:
            # 이진 파일의 포장을 풀어(load) 다시 파이썬 리스트 객체로 복원합니다.
            loaded_list = pickle.load(bin_file)
            
        print('\n=== 3. 이진 파일에서 읽어 들인 데이터 확인 (상위 5개만 출력) ===')
        for item in loaded_list[:5]:
            print(item)
        print('... (이하 생략)')
            
    except FileNotFoundError:
        print('오류: 파일을 찾을 수 없습니다. 파일 이름을 확인해 주세요.')
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    analyze_inventory()