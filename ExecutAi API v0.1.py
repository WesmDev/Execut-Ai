# EXECUT AI API - v0.1
import subprocess
import sys
import os
import threading
import time
import asyncio
import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Lista de bibliotecas necessárias
bibliotecas = [
    "tkinter", "openai", "pyperclip"
]

for biblioteca in bibliotecas:
    try:
        __import__(biblioteca)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", biblioteca], check=True)

print("✅ Todas as bibliotecas estão instaladas e atualizadas!")

import openai
import pyperclip

# Configure a chave de API (atenção: não compartilhe essa chave em ambientes públicos)
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    chave_api = simpledialog.askstring("API Key", "Insira a sua chave de API da OpenAI:")
    openai.api_key = chave_api
    root.destroy()

def update_status(msg, status_label):
    """
    Atualiza a mensagem de status tanto na interface quanto no terminal.
    """
    status_label.config(text=msg)
    print(msg)

def limpar_script(resposta_gpt: str) -> str:
    """
    Recebe a resposta bruta do GPT, que pode conter blocos de código
    entre ```python e ``` ou texto adicional.
    Retorna apenas as linhas de código Python consolidadas em um único bloco,
    removendo formatação markdown e trechos irrelevantes.
    """
    # Regex para capturar blocos de código contidos entre ```python e ```
    pattern = r"```python(.*?)```"
    
    # Findall retorna todas as ocorrências; DOTALL permite capturar quebras de linha
    code_blocks = re.findall(pattern, resposta_gpt, flags=re.DOTALL)
    
    # Se não houver blocos de código em markdown, tentar extrair linhas relevantes
    if not code_blocks:
        lines = []
        for line in resposta_gpt.splitlines():
            line = line.strip()
            # Ignorar linhas vazias, 'Tarefa', comentários extra ou markdown
            if line and not line.startswith("#") and "Tarefa" not in line and not line.startswith("```"):
                lines.append(line)
        return "\n".join(lines)
    
    # Se encontrar um ou mais blocos de código, une todos num único script
    script_limpo = []
    for block in code_blocks:
        block = block.strip()
        script_limpo.append(block)

    return "\n\n".join(script_limpo)

def gerar_script(prompt_solicitacao):
    """
    Gera o código Python para realizar a tarefa com base na solicitação do usuário,
    utilizando a nova interface assíncrona da OpenAI (v1.0.0+).
    
    Referência: Migration Guide Python OpenAI (https://github.com/openai/openai-python/discussions/742).
    """
    system_prompt = ("Você é um gerador de scripts Python. Responda APENAS com o código "
                     "necessário para realizar a tarefa solicitada.")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_solicitacao}
    ]
    
    async def async_call():
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )
        return response.choices[0].message['content']
    
    try:
        codigo_bruto = asyncio.run(async_call())
        # Limpa o script, removendo blocos markdown e unificando tudo em um só
        codigo_limpo = limpar_script(codigo_bruto)
        return codigo_limpo
    except Exception as e:
        return f"# Erro ao gerar script: {e}"

def iniciar_execucao(solicitacao, status_label):
    if not solicitacao.strip():
        messagebox.showwarning("Atenção", "Por favor, insira uma solicitação antes de continuar.")
        return

    def processo():
        update_status("⏳ Gerando script via API...", status_label)
        timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
        # Cria uma pasta exclusiva no diretório Downloads para a solicitação
        nome_pasta = f"EXECUT_AI_{timestamp}"
        pasta_base = os.path.join(os.path.expanduser("~"), "Downloads", nome_pasta)
        os.makedirs(pasta_base, exist_ok=True)

        prompt = f"Tarefa:\n{solicitacao.strip()}"
        codigo = gerar_script(prompt)
        if codigo.startswith("# Erro"):
            update_status(codigo, status_label)
            return

        script_path = os.path.join(pasta_base, f"{nome_pasta}.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(codigo)

        resposta = messagebox.askyesno("Executar agora?", 
            f"O script foi gerado com sucesso e salvo em:\n{script_path}\nDeseja executá-lo agora?")
        if resposta:
            update_status("⚙️ Executando script agora...", status_label)
            try:
                exec(codigo, globals())
                update_status("✅ Script executado com sucesso!", status_label)
            except Exception as e:
                update_status(f"❌ Erro na execução: {e}", status_label)
        else:
            update_status(f"✅ Script salvo com sucesso em: {script_path}", status_label)

    threading.Thread(target=processo).start()

def construir_interface():
    janela = tk.Tk()
    janela.title("EXECUT AI")
    janela.configure(bg="#f0f0f0")
    janela.geometry("520x460")
    janela.resizable(False, False)

    # Faixa superior com assinatura
    frame_topo = tk.Frame(janela, bg="#4A90E2", height=35)
    frame_topo.pack(fill="x")
    tk.Label(
        frame_topo,
        text="| WES M. DEV | www.linkedin.com/in/wesleymendonca-dev/",
        bg="#4A90E2", fg="white",
        font=("Helvetica", 10, "bold")
    ).place(relx=0.5, rely=0.5, anchor="center")

    # Título e descrição
    tk.Label(janela, text="EXECUT AI API", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=(10, 0))
    tk.Label(janela, text="Use IA para gerar e executar scripts via OpenAI API",
             font=("Helvetica", 11), bg="#f0f0f0").pack()

    # Caixa de entrada para a tarefa
    frame_entrada = tk.Frame(janela, bg="#f5f5f5", bd=2, relief="groove")
    frame_entrada.pack(padx=20, pady=15, fill="x")
    tk.Label(frame_entrada, text="Descreva a tarefa que deseja executar:",
             bg="#f5f5f5", font=("Helvetica", 10)).pack(anchor="w", padx=10, pady=(8, 0))
    entrada = tk.Text(frame_entrada, height=7, width=55, font=("Courier", 10))
    entrada.pack(padx=10, pady=10)

    # Botão para gerar o script
    botao = tk.Button(janela, text="GERAR SCRIPT", font=("Helvetica", 11, "bold"),
                      bg="#A8E6A3", fg="black", padx=10, pady=5,
                      command=lambda: iniciar_execucao(entrada.get("1.0", "end"), status_label))
    botao.pack(pady=(0, 15))

    # Label de status
    tk.Label(janela, text="Status:", bg="#f0f0f0", anchor="w", font=("Helvetica", 10)).pack(padx=20, anchor="w")
    status_label = tk.Label(janela, text="", bg="white", fg="black",
                            relief="sunken", anchor="w", font=("Courier", 9), width=64)
    status_label.pack(padx=20, pady=(0, 10), fill="x")

    janela.mainloop()

if __name__ == "__main__":
    construir_interface()
