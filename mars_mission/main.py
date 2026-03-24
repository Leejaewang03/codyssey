# main.py

def analyze_log():
    # 대입문 = 앞뒤로 공백을 줍니다. 문자열은 ''를 사용합니다.
    file_path = 'mission_computer_main.log'
    
    try:
        # 내장 함수인 open을 사용하며, UTF-8 인코딩을 지정합니다.
        with open(file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
            
            print('=== 미션 컴퓨터 로그 분석 시작 ===')
            print(log_content)
            print('=== 미션 컴퓨터 로그 분석 종료 ===')
            
    except FileNotFoundError:
        print('오류: 로그 파일을 찾을 수 없습니다. 파일 이름을 확인해 주세요.')
    except Exception as e:
        # 부득이하게 문자열 내에 변수를 넣기 위해 f-string과 ''를 사용합니다.
        print(f'알 수 없는 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    analyze_log()