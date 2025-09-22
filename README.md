```
'suba
Simple Utility for Broadcasting AIMP
```

[English](#) | [한국어](README_KR.md) | [中文](README_CN.md)

---

### what

Discord Rich Presence for AIMP.  
No plugins required.

### why

AIMP doesn't have native Discord support.  
'suba fixes that.

### how

```
INSTALL_SUBA.bat
```

---

### setup

**discord**
1. https://discord.com/developers/applications
2. New Application → name it 'suba
3. Rich Presence → Art Assets → upload images
4. Name them: `album` and `clover`
5. Copy Application ID

**config**
```json
{
  "discord_app_id": "YOUR_ID",
  "large_image_key": "album",
  "small_image_key": "clover"
}
```

---

### run

```
start_suba.bat          // with console
suba_hidden.vbs         // no console
```

---

### roadmap

```
1.0.0   current         track display
1.1.0   soon            progress bar
1.2.0   later           custom templates
2.0.0   eventually      album art from mp3
```

---

### requirements

- Windows 10+
- Python 3.8+
- AIMP
- Discord

---

### build

```
pip install pypresence==4.3.0
python suba.py
```

---

```
made by red.py
inspired by Yotsuba&!
```
