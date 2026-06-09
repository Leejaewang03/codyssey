import zipfile
import itertools
import string
import time
import os
from concurrent.futures import ProcessPoolExecutor

def extract_with_password(zip_path, password):
    """메모리 1바이트 읽기 (최고속 복호화)"""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            first_file = zf.namelist()[0]
            with zf.open(first_file, pwd=password.encode('utf-8')) as f:
                f.read(1)
        return True
    except Exception:
        return False

# =====================================================================
# [휴리스틱 알고리즘] 사람이 자주 쓰는 암호 패턴을 생성합니다.
# =====================================================================
def check_heuristic_chunk(args):
    zip_path, pattern_type, prefix = args
    letters = string.ascii_lowercase
    digits = string.digits
    
    # 패턴 1: [영문 4자리 + 숫자 2자리] (예: mars01)
    if pattern_type == '4L_2D':
        # prefix는 첫 번째 영문자
        for l2, l3, l4 in itertools.product(letters, repeat=3):
            for d1, d2 in itertools.product(digits, repeat=2):
                password = prefix + l2 + l3 + l4 + d1 + d2
                if extract_with_password(zip_path, password):
                    return password

    # 패턴 2: [영문 5자리 + 숫자 1자리] (예: apple1)
    elif pattern_type == '5L_1D':
        for l2, l3, l4, l5 in itertools.product(letters, repeat=4):
            for d1 in itertools.product(digits, repeat=1):
                password = prefix + l2 + l3 + l4 + l5 + d1
                if extract_with_password(zip_path, password):
                    return password
                    
    return None

def unlock_zip_heuristic(zip_path='emergency_storage_key.zip'):
    print('\n=== [휴리스틱 모드] 인간 심리 기반 초고속 패턴 해킹 ===')
    
    if not os.path.exists(zip_path):
        print(f'오류: {zip_path} 파일을 찾을 수 없습니다.')
        return

    start_time = time.time()
    print(f'- 시작 시간: {time.ctime(start_time)}')
    
    # 1순위: 영문 4자리 + 숫자 2자리 패턴 작업 생성 (a~z로 시작하는 26개 덩어리)
    print('- 1순위 공격: [영문4 + 숫자2] 패턴 검색 중... (약 40~50초 소요)')
    tasks_1 = [(zip_path, '4L_2D', char) for char in string.ascii_lowercase]
    
    with ProcessPoolExecutor() as executor:
        for result in executor.map(check_heuristic_chunk, tasks_1):
            if result is not None:
                elapsed = time.time() - start_time
                print('\n*** 빙고! 휴리스틱 패턴 적중! ***')
                print(f'- 찾은 비밀번호: [{result}]')
                print(f'- 총 소요 시간: {elapsed:.2f}초')
                return result

    # 1순위에서 실패하면 2순위 공격 진행
    print('- 2순위 공격: [영문5 + 숫자1] 패턴 검색 중... (약 2~3분 소요)')
    tasks_2 = [(zip_path, '5L_1D', char) for char in string.ascii_lowercase]
    
    with ProcessPoolExecutor() as executor:
        for result in executor.map(check_heuristic_chunk, tasks_2):
            if result is not None:
                elapsed = time.time() - start_time
                print('\n*** 빙고! 휴리스틱 패턴 적중! ***')
                print(f'- 찾은 비밀번호: [{result}]')
                print(f'- 총 소요 시간: {elapsed:.2f}초')
                return result

    print('\n실패: 휴리스틱 패턴을 벗어난 특이한 비밀번호입니다. 무차별 대입이 필요합니다.')


if __name__ == '__main__':
    unlock_zip_heuristic()