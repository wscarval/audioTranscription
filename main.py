import whisper
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# Criar janela principal
root = tk.Tk()
root.title("Transcrição de Áudio")
root.geometry("450x350")
root.resizable(False, False)

audio_file_path = ""
transcricao_em_andamento = False
modo_transcricao = tk.StringVar(value="srt")  # Opção padrão: legenda (.srt)

def selecionar_arquivo():
    """ Abre o explorador de arquivos para selecionar um arquivo de áudio. """
    global audio_file_path
    audio_file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos de áudio", "*.wav;*.mp3;*.m4a;*.flac")]
    )
    if audio_file_path:
        label_status.config(text=f"Selecionado: {os.path.basename(audio_file_path)}")

def loading_text():
    """ Exibe um efeito de carregamento na interface. """
    text_variations = ["Transcrevendo.", "Transcrevendo..", "Transcrevendo..."]
    i = 0
    while transcricao_em_andamento:
        label_status.config(text=text_variations[i % len(text_variations)])
        i += 1
        root.update_idletasks()
        root.after(500)

def transcrever_audio():
    """ Transcreve o áudio selecionado e salva como .srt (legenda) ou .txt (texto puro). """
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
        # Carregar modelo Whisper otimizado
        model = whisper.load_model("large-v3")

        # Processar transcrição
        result = model.transcribe(audio_file_path, language="english")

        # Obter modo de transcrição escolhido pelo usuário
        formato = modo_transcricao.get()
        output_filename = os.path.splitext(audio_file_path)[0] + f".{formato}"

        if formato == "srt":
            # Salvar como legenda SRT
            with open(output_filename, "w", encoding="utf-8") as f:
                for i, segment in enumerate(result["segments"]):
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"].strip()

                    # Formatar tempo no estilo SRT (hh:mm:ss,ms)
                    start_time_str = f"{int(start_time // 3600):02}:{int(start_time % 3600 // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
                    end_time_str = f"{int(end_time // 3600):02}:{int(end_time % 3600 // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"

                    # Escrever no arquivo SRT
                    f.write(f"{i+1}\n{start_time_str} --> {end_time_str}\n{text}\n\n")
        else:
            # Salvar como texto simples
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(result["text"])

        transcricao_em_andamento = False
        label_status.config(text="Transcrição concluída! Arquivo salvo.")
        messagebox.showinfo("Sucesso", f"Arquivo salvo como:\n{output_filename}")

        btn_download.config(state=tk.NORMAL)
        btn_download.filename = output_filename

    except Exception as e:
        transcricao_em_andamento = False
        label_status.config(text="Erro na transcrição!")
        messagebox.showerror("Erro", str(e))

def baixar_arquivo():
    """ Abre o arquivo gerado. """
    if btn_download.filename:
        os.startfile(os.path.abspath(btn_download.filename))

# Criar interface gráfica
label_title = tk.Label(root, text="Transcrição de Áudio", font=("Arial", 14, "bold"))
label_title.pack(pady=10)

btn_selecionar = tk.Button(root, text="Selecionar Arquivo de Áudio", command=selecionar_arquivo, width=25)
btn_selecionar.pack(pady=5)

label_status = tk.Label(root, text="Nenhum arquivo selecionado", font=("Arial", 10))
label_status.pack(pady=5)

# Opções de formato de saída (Legenda ou Texto)
frame_opcoes = tk.Frame(root)
frame_opcoes.pack(pady=5)

tk.Label(frame_opcoes, text="Escolha o formato:").pack(anchor="w")

radio_srt = tk.Radiobutton(frame_opcoes, text="Legenda (.srt)", variable=modo_transcricao, value="srt")
radio_srt.pack(anchor="w")

radio_txt = tk.Radiobutton(frame_opcoes, text="Texto Simples (.txt)", variable=modo_transcricao, value="txt")
radio_txt.pack(anchor="w")

btn_transcrever = tk.Button(root, text="Iniciar Transcrição", command=lambda: threading.Thread(target=transcrever_audio).start(), width=25)
btn_transcrever.pack(pady=10)

btn_download = tk.Button(root, text="Abrir Arquivo Gerado", command=baixar_arquivo, state=tk.DISABLED, width=25)
btn_download.pack(pady=5)

root.mainloop()
