# 🎶 Transcrição de Áudio para Legendas (SRT)

Este projeto permite transcrever automaticamente áudios em texto e gerar legendas no formato `.srt` utilizando **OpenAI Whisper**. Além disso, conta com uma interface gráfica para facilitar a seleção do arquivo e exibe um **loading animado** durante a transcrição.

## 📌 Recursos
✅ Interface gráfica com **Tkinter**  
✅ **Suporte a vários formatos de áudio** (`.wav`, `.mp3`, `.m4a`, `.flac`)  
✅ **Transcrição automática** com Whisper  
✅ **Geração de legenda (.srt) sincronizada**  
✅ **Botão de download** para abrir a legenda  
✅ **Loading animado** durante a transcrição  

---

## 📦 **Instalação**

### 1️⃣ **Instale o Python (se ainda não tiver)**
Baixe e instale o **Python 3.9+**:  
🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

**Verifique a instalação:**  
python --version
pip install openai-whisper tkinter ffmpeg-python
pip install ffmpeg-python
python -m whisper --help

git clone https://github.com/wscarval/audioTranscription.git
cd transcricao-whisper
