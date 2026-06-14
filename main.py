from typing import Union, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import mysql.connector
import re
import requests


#@app. get가져오는거 post새로운데이터만들때 put데이터전체수정 patch데이터일부수정 delete데이터삭제

#SQL : SELECT조회 INSERT추가 UPDATE수정 DELETE삭제
#SQL 테이블관련 ,  CREATE:TABLE생성 DROP:TABLE삭제 ALTER:TABLE수정 
#SQL 조건절 , WHERE:조건 ORDER BY:정렬 GROUP BY:그룹핑 INTO:데이터삽입 VALUES:데이터삽입 SET:데이터수정

#fechall() : 여러 행을 가져올 때 사용
#fetchone() : 한 행을 가져올 때 사용
#lastrowid : 마지막으로 삽입된 행의 ID를 반환
#commit() : 데이터베이스에 변경 사항을 저장하는 메서드
#cursor() : 데이터베이스와 상호 작용하기 위한 커서를 생성하는 메서드
#dictionary=True : 커서가 반환하는 결과를 딕셔너리 형태로 반환하도록 설정하는 옵션
#cursor.execute() : SQL 쿼리를 실행하는 메서드


def get_connection():
    return mysql.connector.connect(
        host="qlabcode.cafe24.com",
        user="qlabcode",
        passwd="zbfoq1004@",
        database="qlabcode",
        charset="utf8"
    )


#고유번호 / 이메일 / 이름 / 반 / 번호 / 멘토인가? / 멘토번호 / 멘티번호 / 매칭중인가? 
def get_db():  #때려박은거 리턴

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentalk_userinfo")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


class StudentCreate(BaseModel):
    student_id: Optional[int] = None
    name: Optional[str] = None
    student_num: Optional[int] = None
    is_mentor: Optional[int] = None
    mentor_student_id: Optional[int] = None
    mentee_student_id: Optional[int] = None
    chat_room_id: Optional[int] = None
    is_matching: Optional[int] = None
    reports: Optional[str] = None


class MessageCreate(BaseModel):
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    message: Optional[str] = None
    sent_at: Optional[str] = None


app = FastAPI(
        openapi_url="/api", # 실제 API URL
        docs_url="/docs", # Swagger UI URL
        redoc_url="/redoc", # ReDoc URL
        )


origins = [
    "*",  # 프론트 주소
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],        # 모든 메서드 허용
    allow_headers=["*"],        # 모든 헤더 허용
)


@app.get("/get_student_info")
def get_student_info(): 
    return get_db()


@app.get("/student_info/{student_id}")
def student_info(student_id : int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentalk_userinfo WHERE student_id = %s", (student_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return row


@app.get("/update_is_mentor/{student_id}/{is_mentor}")
def update_is_mentor(student_id : int, is_mentor :int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #cursor.execute("UPDATE mentalk_userinfo SET is_mentor = %s WHERE student_id = %s", (is_mentor, student_id))
    # 첫 번째: 해당 student의 is_mentor 상태 변경
    cursor.execute("UPDATE mentalk_userinfo SET is_mentor = %s, mentee_student_id = NULL WHERE student_id = %s", (is_mentor, student_id))
    
    # 두 번째: 이 student를 mentor으로 가지고 있던 mentee들의 연결 해제
    cursor.execute("UPDATE mentalk_userinfo SET mentor_student_id = NULL WHERE mentor_student_id = %s", (student_id,))

    conn.commit()
    cursor.close()
    conn.close()

    #학생정보 멘토/멘티 부분 업데이트
    #멘토로 승격
    return {"student_id": student_id, "is_mentor": is_mentor}


@app.get("/update_is_matching/{student_id}/{is_matching}")
def update_is_matching(student_id : int, is_matching : int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("UPDATE mentalk_userinfo SET is_matching = %s WHERE student_id = %s", (is_matching, student_id))

    conn.commit()
    cursor.close()
    conn.close()

    return {"student_id": student_id, "is_matching": is_matching}
    #학생정보 매칭중 여부 업데이트


@app.patch("/matching/{mentor_id}/{mentee_id}")
def matching(mentor_id: int, mentee_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("UPDATE mentalk_userinfo SET mentee_student_id = %s WHERE student_id = %s", (mentee_id, mentor_id))
    cursor.execute("UPDATE mentalk_userinfo SET mentor_student_id = %s WHERE student_id = %s", (mentor_id, mentee_id))
    cursor.execute("UPDATE mentalk_userinfo SET chat_room_id = %s WHERE student_id = %s", (mentee_id, mentor_id))
    cursor.execute("UPDATE mentalk_userinfo SET chat_room_id = %s WHERE student_id = %s", (mentor_id, mentee_id))

    conn.commit()
    cursor.close()
    conn.close()    

    return {"mentor_id": mentor_id, "mentee_id": mentee_id}


@app.get("/search_mentor") 
def search_mentor():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentalk_userinfo WHERE is_matching = 1 AND is_mentor = 1")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


@app.get("/un_matching/{mentor_id}/{mentee_id}")
def un_maching(mentor_id : int, mentee_id : int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("UPDATE mentalk_userinfo SET mentee_student_id = NULL WHERE is_mentor = 1 AND student_id = %s", (mentor_id,))
    cursor.execute("UPDATE mentalk_userinfo SET mentor_student_id = NULL WHERE is_mentor = 0 AND student_id = %s", (mentee_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"mentor_id": mentor_id, "mentee_id": mentee_id}
    #학생정보 멘토/멘티 부분 업데이트
    #채팅방 연결 안되게


@app.get("/get_chat/{user1id}/{user2id}")
def get_chat(user1id : int, user2id : int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentalk_messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY sent_at ASC", (user1id, user2id, user2id, user1id))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
    #특정 채팅 내역 조회
    #멘토-멘티로 확인


@app.post("/send_report/{chat_id}")
def send_report(chat_id : int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("INSERT INTO mentalk_report (chat_id) VALUES (%s)", (chat_id,))
    rows = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()

    return rows
#채팅id로 신고하기


@app.get("/get_report")
def get_report():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentalk_report")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
    #신고 전체 조회


@app.get("/delete_report/{student_id}")
def delete_report(student_id : int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("UPDATE mentalk_userinfo SET reports = NULL WHERE student_id = %s", (student_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"student_id": student_id}
    #신고 삭제하기


@app.post("/add_student")
async def add_student(student: Optional[StudentCreate] = None, request: Request = None):
    # Accept student data from JSON body (documented in /docs) or fallback to query params
    data: Dict[str, Any] = {}
    if student:
        data = student.dict(exclude_none=True)

    if not data and request is not None:
        # try raw JSON then query params
        try:
            raw = await request.json()
            if isinstance(raw, dict):
                data = raw
        except Exception:
            data = dict(request.query_params)

    if not data:
        return {"error": "empty student data"}

    # Restrict to allowed fields provided by user
    allowed_fields = {
        "student_id",
        "name",
        "student_num",
        "is_mentor",
        "mentor_student_id",
        "mentee_student_id",
        "chat_room_id",
        "is_matching",
        "reports",
    }

    # keep only allowed keys
    keys = [k for k in data.keys() if k in allowed_fields]
    if not keys:
        return {"error": "no allowed fields provided"}

    # convert integer-like fields
    int_fields = {"student_id", "student_num", "is_mentor", "mentor_student_id", "mentee_student_id", "chat_room_id", "is_matching"}
    values = []
    for k in keys:
        v = data.get(k)
        if k in int_fields:
            try:
                if v == "" or v is None:
                    v_conv = None
                else:
                    v_conv = int(v)
            except Exception:
                v_conv = None
            values.append(v_conv)
        else:
            values.append(v)

    columns = ', '.join(keys)
    placeholders = ', '.join(['%s'] * len(keys))

    conn = get_connection()
    cursor = conn.cursor()

    sql = f"INSERT INTO mentalk_userinfo ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(values))

    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return {"student_id": last_id}
    # 새로운 학생 추가


@app.post("/add_chat")
async def add_chat(message: Optional[MessageCreate] = None, request: Request = None):
    # Accept message via JSON body (documented in /docs) or query params/raw JSON
    data: Dict[str, Any] = {}
    if message:
        data = message.dict(exclude_none=True)

    if not data and request is not None:
        try:
            raw = await request.json()
            if isinstance(raw, dict):
                data = raw
        except Exception:
            data = dict(request.query_params)

    if not data:
        return {"error": "empty message data"}

    # set sent_at to now if not provided
    if not data.get("sent_at"):
        data["sent_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.0")

    allowed_fields = {"sender_id", "receiver_id", "message", "sent_at"}
    keys = [k for k in data.keys() if k in allowed_fields]
    if not keys:
        return {"error": "no allowed fields provided"}

    int_fields = {"sender_id", "receiver_id"}
    values = []
    for k in keys:
        v = data.get(k)
        if k in int_fields:
            try:
                if v == "" or v is None:
                    v_conv = None
                else:
                    v_conv = int(v)
            except Exception:
                v_conv = None
            values.append(v_conv)
        else:
            # keep message and sent_at as-is
            values.append(v)

    columns = ', '.join(keys)
    placeholders = ', '.join(['%s'] * len(keys))

    conn = get_connection()
    cursor = conn.cursor()

    sql = f"INSERT INTO mentalk_messages ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(values))

    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return {"message_id": last_id}


@app.get("/reset_password/{student_num}")
def reset_password(student_num: int):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "UPDATE mentalk_userinfo SET password = %s WHERE student_num = %s"
    cursor.execute(sql, (student_num, student_num))
    conn.commit()
    cursor.close()
    conn.close()

    return {"student_num": student_num, "new_password": student_num}


@app.post("/add_student1/{student_num}/{name}/{password}")
def add_student1(student_num: int, name: str, password: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO mentalk_userinfo (student_num, name, password) VALUES (%s, %s, %s)",
        (student_num, name, password)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return get_db()
'''769064502657-376iorkhb88b45lpd1q49urn4vvsi9bg.apps.googleusercontent.com'''


@app.get("/google_login/{access_token}")
def google_login(access_token: str):

    response = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
    )

    user_info = response.json()
   
    print(user_info["email"])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM mentalk_userinfo WHERE email = %s", (user_info["email"],))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return {"error": "Email not found"}

    return row
