# from dotenv import load_dotenv
# from openai import OpenAI

# class ChatBot:
#     def __init__(self, model, system_message="You are a helpful assitant."):
#         load_dotenv()
#         self.client = OpenAI() # 클래스 내이기 때문에 self.client
#         self.messages = []
#         self.model = model
#         self.add_message("system", system_message)

# # add_message로 정의된 함수 내에서 role이랑 content가 상황에 따라 적절하게 바뀜
#     def add_message(self, role, content):
#         self.messages.append(
#             {
#                 "role":role,
#                 "content": content
#             }
#         )

#     def get_response(self, user_input, print_token_usage=False, response_format={"type":"text"}):
#         self.add_message("user",user_input)
#         completion = self.client.chat.completions.create(
#             model=self.model,
#             messages=self.messages,
#             response_format=response_format
#         )

#         if print_token_usage:
#             print("="*50)
#             # print(completion.usage.model_dump_json(indent=4))
#             print("- 전송 토큰량:", completion.usage.prompt_tokens)
#             print("- 응답 토큰량:", completion.usage.completion_tokens)
#             print("- 전체 토큰량:", completion.usage.total_tokens)
#             print("="*50)

#         response = completion.choices[0].message.content
#         self.add_message("assistant", response)
#         return response

    
#     # 토큰 정상화
#     def reset(self):
#         self.messages = self.messages[:1] # 시스템 메시지만 남기기. 첫번째 리스트 요소만 남기기


import json
from dotenv import load_dotenv

class ChatBot:
    def __init__(self, model, system_message="You are a helpful assistant."):
        # load_dotenv()
        # self.client = OpenAI()  # <-- 이 부분을 주석 처리하여 API 키 검사를 피합니다.
        self.messages = []
        self.model = model
        self.add_message("system", system_message)

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_response(self, user_input, context=None, print_token_usage=False, response_format={"type": "text"}):
        # 유저 메시지 추가
        self.add_message("user", user_input)
        
        # 스크린샷용 가짜 전문 답변 (JSON 형식)
        # project_audiologist.py에서 json.loads()를 사용하므로 반드시 JSON 형식이어야 합니다.
        fake_response_dict = {
            "상태 요약": "고주파 영역(4kHz 이상)에서 대칭적인 급격한 하강을 보이는 감각신경성 난청 양상입니다. 전형적인 소음성 난청 혹은 노인성 난청의 초기 단계로 판단됩니다.",
            "권장 조치": "정밀 어음 판별 검사(WRS)를 통해 명료도를 파악해야 하며, 고음역대 이득 조절이 가능한 RIC형 보청기 피팅이 권장됩니다.",
            "추천": "이명 차폐를 위한 화이트 노이즈 발생기 사용과 더불어, 청각 피로를 줄이기 위한 충분한 휴식을 추천드립니다."
        }
        
        # 실제로는 문자열 형태로 반환해야 함
        response = json.dumps(fake_response_dict, ensure_ascii=False)
        
        self.add_message("assistant", response)
        
        # 스크린샷 찍을 때 터미널이 깨끗하게 보이도록 출력
        if print_token_usage:
            print("="*50)
            print("MOCK MODE: No tokens used")
            print("="*50)
            
        return response