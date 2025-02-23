### 문제 설명

---

나 이런스타 안스타~

### 문제 풀이

---

- 주요 사용 기법: SQL Logic misconfiguration, XSS
- (문제 풀이):
    1. 회원 가입 시 id에 대한 PRIMARY KEY (UNIQUE)가 적용되어 있지 않아 중복 가입 가능
    2. id 명이 admin인지 아닌지로 서비스 여부를 판단하는 내부 bot 서비스에 접근
    3. bot 계정만 볼 수 있는 1번(id) 방 채팅에 FLAG가 있음
    4. XSS를 통해 1번방 채팅 내용을 전송

### FLAG

---

- `Layer7{smooth_like_jelly_ya_x5emyeje0dfwbc0y7boramae0247js2sc4f60c}`
