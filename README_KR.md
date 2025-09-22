[suba-readme-kr (1).md](https://github.com/user-attachments/files/22457138/suba-readme-kr.1.md)
```
'suba
Simple Utility for Broadcasting AIMP
```

[English](README.md) | [한국어](#) | [中文](README_CN.md)

---

### 뭔데

AIMP용 Discord Rich Presence.  
플러그인 필요 없음.

### 왜

AIMP는 Discord 지원 안 함.  
'suba가 해결함.

### 어떻게

```
INSTALL_SUBA.bat
```

---

### 설정

**디스코드**
1. https://discord.com/developers/applications
2. New Application → 이름: 'suba
3. Rich Presence → Art Assets → 이미지 업로드
4. 이름 지정: `album` 그리고 `clover`
5. Application ID 복사

**설정파일**
```json
{
  "discord_app_id": "YOUR_ID",
  "large_image_key": "album",
  "small_image_key": "clover"
}
```

---

### 실행

```
start_suba.bat          // 콘솔 표시
suba_hidden.vbs         // 백그라운드
```

---

### 로드맵

```
1.0.0   현재            트랙 표시
1.1.0   곧              진행률 표시
1.2.0   나중에          커스텀 템플릿
2.0.0   언젠가          mp3에서 앨범아트
```

---

### 필요한 것

- Windows 10+
- Python 3.8+
- AIMP
- Discord

---

### 빌드

```
pip install pypresence==4.3.0
python suba.py
```

---

```
made by red.py
inspired by Yotsuba&!
```
