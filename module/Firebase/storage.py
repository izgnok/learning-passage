"""
firebase storage와 연동

동작 정의
모델 파라미터 파일이 업로드 -> 업로드 이벤트 감지 -> 모델 파라미터 전이

test
임의 파일 업로드 -> 업로드 이벤트 감지 -> 업로드된 파일 메타 데이터 출력
"""

from .firebase import *
from firebase_admin import firestore



class Storage:
    def __init__(self) -> None:
        fm = FirebaseManager() # firebase 계정 연결
        db = firestore.client() # storage 연결  
        