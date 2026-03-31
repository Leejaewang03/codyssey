import pickle

# 'rb' (Read Binary) 모드로 읽어옵니다.
with open('Mars_Base_Inventory_List.bin', 'rb') as file:
    # 묶여있던 데이터를 파이썬 리스트로 다시 풀어냅니다.
    recovered_data = pickle.load(file)
    
    print(recovered_data)