import whisper
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

root = tk.Tk()
root.title("Transcrição de Áudio para Legenda")
root.geometry("400x250")
root.resizable(False, False)

audio_file_path = ""

def selecionar_arquivo():
    global audio_file_path
    audio_file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos de áudio", "*.wav;*.mp3;*.m4a;*.flac")]
    )
    if audio_file_path:
        label_status.config(text=f"Selecionado: {os.path.basename(audio_file_path)}")

def loading_text():
    text_variations = ["Transcrevendo.", "Transcrevendo..", "Transcrevendo..."]
    i = 0
    while transcricao_em_andamento:
        label_status.config(text=text_variations[i % len(text_variations)])
        i += 1
        root.update_idletasks()
        root.after(500)

def transcrever_audio():
    global transcricao_em_andamento
    if not audio_file_path:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo de áudio primeiro!")
        return

    transcricao_em_andamento = True
    label_status.config(text="Transcrevendo...")
    root.update()

    loading_thread = threading.Thread(target=loading_text)
    loading_thread.start()

    try:
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file_path, language="portuguese")

        srt_filename = os.path.splitext(audio_file_path)[0] + ".srt"

        with open(srt_filename, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]

                start_time_str = f"{int(start_time // 3600):02}:{int(start_time % 3600 // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
                end_time_str = f"{int(end_time // 3600):02}:{int(end_time % 3600 // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"

                f.write(f"{i+1}\n{start_time_str} --> {end_time_str}\n{text}\n\n")

        transcricao_em_andamento = False
        label_status.config(text="Transcrição concluída! Arquivo salvo.")
        messagebox.showinfo("Sucesso", f"Legenda salva como:\n{srt_filename}")

        btn_download.config(state=tk.NORMAL)
        btn_download.filename = srt_filename

    except Exception as e:
        transcricao_em_andamento = False
        label_status.config(text="Erro na transcrição!")
        messagebox.showerror("Erro", str(e))

def baixar_srt():
    if btn_download.filename:
        os.startfile(os.path.abspath(btn_download.filename))

label_title = tk.Label(root, text="Transcrição de Áudio para Legenda", font=("Arial", 12, "bold"))
label_title.pack(pady=10)

btn_selecionar = tk.Button(root, text="Selecionar Arquivo de Áudio", command=selecionar_arquivo)
btn_selecionar.pack(pady=5)

label_status = tk.Label(root, text="Nenhum arquivo selecionado", font=("Arial", 10))
label_status.pack(pady=5)

btn_transcrever = tk.Button(root, text="Iniciar Transcrição", command=lambda: threading.Thread(target=transcrever_audio).start())
btn_transcrever.pack(pady=10)

btn_download = tk.Button(root, text="Baixar Arquivo SRT", command=baixar_srt, state=tk.DISABLED)
btn_download.pack(pady=5)

root.mainloop()
