# mars_mission_computer.py

import random
from datetime import datetime

class DummySensor:
    def __init__(self):
        # [수행과제 2] env_values 사전(Dictionary) 객체 초기화
        # 딕셔너리의 키(Key)는 문자열이므로 ''를 사용합니다.
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        # [수행과제 3, 4] 주어진 범위 안의 랜덤 값을 생성하여 사전에 채웁니다.
        # random.uniform(a, b)는 a와 b 사이의 무작위 실수(float)를 반환합니다.
        # round(값, 소수점자리수)를 사용하여 값을 깔끔하게 다듬습니다.
        
        # 1. 화성 기지 내부 온도 (18~30도)
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2)
        
        # 2. 화성 기지 외부 온도 (0~21도)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0.0, 21.0), 2)
        
        # 3. 화성 기지 내부 습도 (50~60%)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50.0, 60.0), 2)
        
        # 4. 화성 기지 외부 광량 (500~715 W/m2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500.0, 715.0), 2)
        
        # 5. 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        
        # 6. 화성 기지 내부 산소 농도 (4%~7%)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        # [보너스 과제] get_env()가 호출될 때 값을 파일에 로그로 남깁니다.
        log_file_path = 'sensor_log.txt'
        
        # 현재 날짜와 시간을 'YYYY-MM-DD HH:MM:SS' 형식으로 가져옵니다.
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 로그 파일에 기록하기 위해 문자열을 조립합니다. (CSV 형태와 유사하게 콤마로 구분)
        # f-string을 사용하여 변수들을 쉽게 결합합니다.
        log_entry = (
            f"{now},"
            f"{self.env_values['mars_base_internal_temperature']},"
            f"{self.env_values['mars_base_external_temperature']},"
            f"{self.env_values['mars_base_internal_humidity']},"
            f"{self.env_values['mars_base_external_illuminance']},"
            f"{self.env_values['mars_base_internal_co2']},"
            f"{self.env_values['mars_base_internal_oxygen']}\n"
        )
        
        # 'a' (Append) 모드로 파일을 열어 기존 내용 끝에 로그를 추가합니다.
        try:
            with open(log_file_path, 'a', encoding='utf-8') as file:
                file.write(log_entry)
        except Exception as e:
            print(f'로그 저장 중 오류 발생: {e}')
            
        # [수행과제 5] 갱신된 env_values 사전을 반환(return)합니다.
        return self.env_values


# 코드가 직접 실행될 때만 작동하는 메인 블록입니다.
if __name__ == '__main__':
    # [수행과제 6] DummySensor 클래스를 ds라는 이름의 인스턴스로 만듭니다.
    ds = DummySensor()
    
    print('=== 화성 기지 더미 센서 테스트 시작 ===')
    
    # [수행과제 7] set_env()를 호출하여 랜덤 값을 생성하고 세팅합니다.
    ds.set_env()
    print('센서 값이 무작위로 세팅되었습니다.')
    
    # [수행과제 7] get_env()를 호출하여 값을 가져오고(로그도 남김), 그 결과를 화면에 확인합니다.
    current_env = ds.get_env()
    
    print('\n[현재 센서 측정값]')
    for key, value in current_env.items():
        print(f'- {key}: {value}')
        
    print('\n안내: 측정값이 sensor_log.txt 파일에 성공적으로 기록되었습니다.')
    print('=== 화성 기지 더미 센서 테스트 종료 ===')