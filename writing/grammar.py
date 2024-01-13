from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config, AutoConfig
import openai
from rest_framework import status
import random
import urllib.request
import json

def grammar_wrong_response():
    a = random.randrange(0,4)
    first = ['이런건 어때요?', '제가 한번 제안할게요!', '이게 더 자연스러울 수도 있어요!', '이게 더 나을 수도 있어요!', '이렇게 작문할 수도 있어요!']
    return f"{first[a]}"

def grammar_correct_response():
    a = random.randrange(0,4)
    first = ['완벽해요!', '틀린게 없는 문장이에요!', '너무 좋은걸요?', '완벽한 문장이에요!!', '굉장히 좋은 문장이에요!']
    return f"{first[a]}"

class GrammarCheckView(APIView):
    def post(self, request):
        api_key = config('OPEN_AI')
        text = request.data.get('text')
        sentence = request.data.get('sentence')
        if not text:
            return Response({'response': "", 'ai': "검사할 문장이 없어요!", 'original': "", 'bool': False}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": f"'{text}'문장이 문법적으로 틀렸으면 고쳐줘. '{sentence}'는 포함해야돼. "}, #역할 지정
        ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        request = urllib.request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(request) as response:
            response = json.loads(response.read().decode('utf-8'))
        #return Response({'response': response, 'today': today_sentence}, status=status.HTTP_200_OK)
        target_res = response['choices'][0]['message']['content'].strip()
        if target_res[0] in ("\'", "\""):
            cut_target = target_res.strip("\'\"")
            if text == cut_target:
                res = cut_target
                ai = grammar_correct_response()
                bool = True
            else:
                res = cut_target
                ai = grammar_wrong_response()
                bool = False

        else:
            if text == target_res:
                res = target_res
                ai = grammar_correct_response()
                bool = True
            else:
                res = target_res
                ai = grammar_wrong_response()
                bool = False

        return Response({'response': res, 'ai': ai, 'original': text, 'bool': bool}, status=status.HTTP_200_OK)