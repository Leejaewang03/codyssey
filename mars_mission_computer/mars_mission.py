import time
import json
import random

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


class MissionComputer:
    def __init__(self):
        # [수행과제 2, 3] 화성 기지의 환경 값을 저장할 사전(Dict) 객체
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        
        # [수행과제 4] DummySensor 클래스를 ds라는 이름으로 인스턴스화
        self.ds = DummySensor()
        
        # [보너스 과제] 5분 평균을 구하기 위해 데이터를 누적시킬 별도의 사전 객체
        self.history_values = {
            'mars_base_internal_temperature': [],
            'mars_base_external_temperature': [],
            'mars_base_internal_humidity': [],
            'mars_base_external_illuminance': [],
            'mars_base_internal_co2': [],
            'mars_base_internal_oxygen': []
        }

    def get_sensor_data(self):
        # [수행과제 5] 센서 데이터 갱신, JSON 출력, 반복 처리
        print('=== 미션 컴퓨터 시스템 가동 ===')
        print('(안내: 터미널에서 "Ctrl + C"를 누르면 시스템이 종료됩니다.)\n')
        
        # [보너스 과제] 특정 키를 입력받아 시스템을 멈추기 위한 예외 처리 (KeyboardInterrupt)
        try:
            # 무한 반복 루프
            while True:
                # 더미 센서의 값을 랜덤으로 새로 생성
                self.ds.set_env()
                
                # 1. 센서의 값을 가져와서 env_values에 담는다.
                self.env_values = self.ds.get_env()
                
                # 5분 평균을 계산하기 위해 현재 값들을 history_values에 차곡차곡 저장
                for key, value in self.env_values.items():
                    self.history_values[key].append(value)
                
                # 2. env_values의 값을 json 형태로 화면에 출력한다.
                # json.dumps()의 indent=4 옵션을 사용하면 들여쓰기가 깔끔하게 적용됩니다.
                json_output = json.dumps(self.env_values, indent=4)
                print('[현재 화성 기지 환경 데이터]')
                print(json_output)
                
                # 3. 5분에 한 번씩 평균값 출력 (보너스 과제)
                # 루프가 5초에 한 번씩 도니까, 60번이 모이면 300초(5분)가 됩니다.
                if len(self.history_values['mars_base_internal_temperature']) >= 60:
                    print('\n=======================================')
                    print('     [5분 경과] 환경 데이터 평균 요약     ')
                    print('=======================================')
                    
                    average_data = {}
                    for key, value_list in self.history_values.items():
                        # 리스트의 모든 값을 더한 뒤(sum), 개수로 나누어(len) 평균을 구합니다.
                        avg = round(sum(value_list) / len(value_list), 4)
                        average_data[key] = avg
                    
                    # 평균값도 동일하게 JSON 형태로 출력
                    print(json.dumps(average_data, indent=4))
                    print('=======================================\n')
                    
                    # 평균을 출력했으니, 다음 5분을 위해 누적된 리스트를 비워줍니다.
                    for key in self.history_values:
                        self.history_values[key].clear()
                
                # 4. 5초에 한 번씩 반복 (대기)
                time.sleep(5)
                
        # 터미널에서 Ctrl + C를 누를 경우 실행되는 구문
        except KeyboardInterrupt:
            # 지시사항의 오타('Sytem stoped….')를 그대로 반영하여 출력
            print('\nSytem stoped….')


if __name__ == '__main__':
    # [수행과제 6] MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화
    RunComputer = MissionComputer()
    
    # [수행과제 7] 지속적으로 환경 값을 출력하도록 메소드 호출
    RunComputer.get_sensor_data()