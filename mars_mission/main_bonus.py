def analyze_log():
    file_path = 'mission_computer_main.log'
    problem_file_path = 'problem_log.txt'
    
    try:
        # 1. 파일 읽기 ('r' 모드)
        with open(file_path, 'r', encoding='utf-8') as file:
            # 파일의 모든 줄을 리스트 형태로 가져옵니다.
            lines = file.readlines()
            
        if not lines:
            print('로그 파일이 비어 있습니다.')
            return
            
        # 2. 데이터 분리 및 시간 역순 정렬
        header = lines[0]         # 첫 번째 줄은 제목(헤더)
        data_lines = lines[1:]    # 두 번째 줄부터 끝까지가 실제 데이터
        
        # [::-1]을 사용하여 데이터 목록의 순서를 뒤집습니다.
        reversed_lines = data_lines[::-1]
        
        # 3. 화면 출력 (최신순)
        print('=== 미션 컴퓨터 로그 분석 시작 (최신순) ===')
        print(header.strip())
        for line in reversed_lines:
            print(line.strip())
        print('=== 미션 컴퓨터 로그 분석 종료 ===')
        
        # 4. 문제가 되는 부분 따로 저장 ('w' 모드)
        # 위험을 알리는 키워드 목록을 만듭니다.
        keywords = ['unstable', 'explosion', 'powered down']
        
        with open(problem_file_path, 'w', encoding='utf-8') as error_file:
            # 새 파일의 맨 윗줄에도 제목(헤더)을 적어줍니다.
            error_file.write(header)
            
            # 원래 순서의 데이터를 하나씩 확인합니다.
            for line in data_lines:
                for keyword in keywords:
                    if keyword in line:
                        # 위험 키워드가 발견되면 파일에 쓰고 검사를 중단(break)합니다.
                        error_file.write(line)
                        break
                        
        print('\n안내: 문제가 발생한 로그가 problem_log.txt 파일에 따로 저장되었습니다.')
        
    except FileNotFoundError:
        print('오류: 로그 파일을 찾을 수 없습니다. 파일 이름을 확인해 주세요.')
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    analyze_log()