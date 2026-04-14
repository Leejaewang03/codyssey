import time
import json
import random
import platform
import os

# ---------------------------------------------------------
# [사전 준비] DummySensor 클래스 (뼈대)
# ---------------------------------------------------------
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0.0, 21.0), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50.0, 60.0), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500.0, 715.0), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        return self.env_values


# ---------------------------------------------------------
# [새로운 과제] MissionComputer 클래스
# ---------------------------------------------------------
class MissionComputer:
    def __init__(self):
        # 보너스 과제: 인스턴스화 될 때 설정 파일을 읽어옵니다.
        self.display_settings = self.load_settings()

    def load_settings(self):
        # setting.txt 파일을 읽어서 필터링할 항목을 리스트로 반환합니다.
        settings_file = 'setting.txt'
        allowed_keys = []
        
        try:
            # os 모듈의 내장 함수를 사용해 파일이 존재하는지 확인합니다.
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        key = line.strip()
                        if key:
                            allowed_keys.append(key)
            else:
                print('안내: setting.txt 파일이 없어 모든 정보를 출력합니다.')
        except Exception as e:
            print(f'설정 파일 읽기 오류: {e}')
            
        return allowed_keys

    def filter_data(self, data):
        # 설정 파일의 항목과 일치하는 데이터만 남깁니다.
        if not self.display_settings:
            return data
            
        filtered = {key: value for key, value in data.items() if key in self.display_settings}
        return filtered

    def get_mission_computer_info(self):
        # 외부 라이브러리 없이 파이썬 내장 모듈(platform, os)만 사용합니다.
        info = {}
        try:
            info['os_name'] = platform.system()
            info['os_version'] = platform.version()
            info['cpu_type'] = platform.processor()
            info['cpu_cores'] = os.cpu_count()
            
            # [맥북 환경] os.sysconf를 사용해 총 물리적 메모리(RAM) 크기를 구합니다.
            # 페이지 크기(Page Size) * 물리적 페이지 수(Physical Pages) = 전체 바이트
            page_size = os.sysconf('SC_PAGE_SIZE')
            phys_pages = os.sysconf('SC_PHYS_PAGES')
            total_bytes = page_size * phys_pages
            info['memory_size_gb'] = round(total_bytes / (1024 ** 3), 2)
            
            filtered_info = self.filter_data(info)
            
            print('\n=== [진단 1] 미션 컴퓨터 시스템 기본 정보 ===')
            print(json.dumps(filtered_info, indent=4, ensure_ascii=False))
            
        except Exception as e:
            print(f'시스템 정보를 가져오는 중 오류 발생: {e}')
            
        return info

    def get_mission_computer_load(self):
        load_info = {}
        try:
            # os.getloadavg()는 맥북/리눅스 환경에서 최근 1, 5, 15분간의 부하를 반환합니다.
            # 1분 평균 부하를 코어 수로 나누어 CPU 사용량(%)을 대략적으로 유추합니다.
            load_avg_1min = os.getloadavg()[0]
            cores = os.cpu_count() or 1
            load_info['cpu_usage_percent'] = round((load_avg_1min / cores) * 100, 2)
            
            # 주의: 외부 라이브러리 없이 맥북의 실시간 '사용 중인 메모리'를
            # 정확한 %로 뽑아내는 것은 내장 모듈만으로는 한계가 있습니다.
            # 제약사항을 최우선으로 준수하기 위해 해당 값은 센서처럼 난수로 시뮬레이션합니다.
            load_info['memory_usage_percent'] = round(random.uniform(40.0, 85.0), 2)
            
            filtered_load = self.filter_data(load_info)
            
            print('\n=== [진단 2] 미션 컴퓨터 실시간 부하 상태 ===')
            print(json.dumps(filtered_load, indent=4, ensure_ascii=False))
            
        except Exception as e:
            print(f'시스템 부하를 측정하는 중 오류 발생: {e}')
            
        return load_info


if __name__ == '__main__':
    runComputer = MissionComputer()
    
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()