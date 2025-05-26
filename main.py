from tkinter import Tk, Button, Label, filedialog, Entry, PhotoImage, Canvas, messagebox, Frame
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
import os


# === Função para converter imagens ou textos em PDF ===
def convert_to_pdf(input_paths, output_path):
    try:
        if all(path.lower().endswith(('.jpg', '.jpeg', '.png')) for path in input_paths):
            c = pdf_canvas.Canvas(output_path, pagesize=letter)
            page_width, page_height = letter

            for img_path in input_paths:
                img = Image.open(img_path)
                img = img.convert("RGB")
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height

                if img_width > page_width or img_height > page_height:
                    if aspect_ratio > 1:
                        new_width = page_width
                        new_height = page_width / aspect_ratio
                    else:
                        new_height = page_height
                        new_width = page_height * aspect_ratio
                else:
                    new_width = img_width
                    new_height = img_height

                x_offset = (page_width - new_width) / 2
                y_offset = (page_height - new_height) / 2

                c.drawInlineImage(img, x_offset, y_offset, width=new_width, height=new_height)
                c.showPage()  # Cria uma nova página

            c.save()
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso em:\n{output_path}")

        elif all(path.lower().endswith(('.txt',)) for path in input_paths):
            c = pdf_canvas.Canvas(output_path, pagesize=letter)

            for txt_path in input_paths:
                with open(txt_path, 'r', encoding="utf-8") as f:
                    text = f.readlines()

                textobject = c.beginText(50, 750)
                textobject.setFont("Sanserif", 12)

                for line in text:
                    textobject.textLine(line.strip())

                c.drawText(textobject)
                c.showPage()  # Nova página para cada arquivo de texto

            c.save()
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso em:\n{output_path}")

        else:
            messagebox.showerror("Erro", "Selecione arquivos do mesmo tipo: apenas imagens ou apenas textos.")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


# === Funções auxiliares ===
def escolher_arquivos():
    arquivos = filedialog.askopenfilenames(
        title="Selecione arquivos",
        filetypes=(("Imagens e Textos", "*.jpg *.jpeg *.png *.txt"), ("Todos os arquivos", "*.*"))
    )
    lista_arquivos.clear()
    lista_arquivos.extend(arquivos)

    if arquivos:
        entrada_arquivos.delete(0, 'end')
        entrada_arquivos.insert(0, "; ".join([os.path.basename(arq) for arq in arquivos]))

        mostrar_preview(arquivos[0])


def escolher_diretorio():
    pasta = filedialog.askdirectory(title="Selecione a pasta para salvar o PDF")
    if pasta:
        entrada_pasta_saida.delete(0, 'end')
        entrada_pasta_saida.insert(0, pasta)


def executar_conversao():
    if not lista_arquivos:
        messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo.")
        return

    pasta_saida = entrada_pasta_saida.get()
    nome_pdf = entrada_nome_pdf.get()

    if not pasta_saida or not nome_pdf:
        messagebox.showwarning("Aviso", "Informe o nome do PDF e selecione a pasta de saída.")
        return

    if not nome_pdf.endswith('.pdf'):
        nome_pdf += '.pdf'

    caminho_saida = os.path.join(pasta_saida, nome_pdf)
    convert_to_pdf(lista_arquivos, caminho_saida)


def mostrar_preview(caminho):
    try:
        if caminho.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = Image.open(caminho)
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)

            canvas_preview.delete("all")
            canvas_preview.create_image(100, 100, image=img_tk)
            canvas_preview.image = img_tk
        else:
            canvas_preview.delete("all")
            canvas_preview.create_text(100, 100, text="(Prévia não disponível)", fill="gray")
    except Exception as e:
        print(f"Erro na prévia: {e}")


# === Interface Gráfica ===
janela = Tk()
janela.title("Conversor de Arquivos para PDF")
janela.geometry("600x400")
janela.resizable(False, False)
janela.configure(bg="#f0f0f0")

lista_arquivos = []

# Frame de seleção
frame_selecao = Frame(janela, bg="#f0f0f0")
frame_selecao.pack(pady=10)

Label(frame_selecao, text="Arquivos selecionados:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
entrada_arquivos = Entry(frame_selecao, width=50)
entrada_arquivos.grid(row=0, column=1, padx=5)
Button(frame_selecao, text="Selecionar Arquivos", command=escolher_arquivos).grid(row=0, column=2, padx=5)

# Frame de saída
frame_saida = Frame(janela, bg="#f0f0f0")
frame_saida.pack(pady=10)

Label(frame_saida, text="Pasta de saída:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
entrada_pasta_saida = Entry(frame_saida, width=40)
entrada_pasta_saida.grid(row=0, column=1, padx=5)
Button(frame_saida, text="Selecionar Pasta", command=escolher_diretorio).grid(row=0, column=2, padx=5)

Label(frame_saida, text="Nome do PDF:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
entrada_nome_pdf = Entry(frame_saida, width=40)
entrada_nome_pdf.grid(row=1, column=1, padx=5, pady=5)

# Frame de preview
frame_preview = Frame(janela, bg="#f0f0f0")
frame_preview.pack(pady=10)

Label(frame_preview, text="Prévia do arquivo:", bg="#f0f0f0").pack()
canvas_preview = Canvas(frame_preview, width=200, height=200, bg="white", bd=2, relief="ridge")
canvas_preview.pack()

# Botão de conversão
Button(janela, text="Converter para PDF", command=executar_conversao, bg="#4CAF50", fg="white",
       font=("Arial", 12, "bold")).pack(pady=15)

janela.mainloop()
