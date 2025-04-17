# 🤖 EXECUT AI - v0.1

*EXECUT AI* é uma aplicação *low code* construída em Python que utiliza a API da OpenAI para interpretar solicitações do usuário e transformá-las automaticamente em scripts executáveis no seu computador. Com isso, a IA interage com programas e arquivos locais, ampliando sua atuação para além da web.

---

## 🚀 Funcionalidades

- Interface amigável feita com `tkinter`.
- Integração com a **API da OpenAI**.
- Interpretação de comandos textuais e geração automática de scripts Python.
- Execução imediata do script gerado.
- Armazenamento do script no diretório `Downloads`, com pastas organizadas por data e hora.
- Instalação automática de bibliotecas essenciais (`tkinter`, `openai`, `pyperclip`).
- Limpeza e formatação do código gerado com base em padrões Markdown.

---

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/WesmDev/Execut-Ai.git
   cd EXECUT-AI
   ```

2. Execute o script principal:
   ```bash
   python execut_ai.py
   ```

> 📝 O script instala automaticamente as dependências necessárias, mas você pode instalar manualmente com:
> ```bash
> pip install openai pyperclip
> ```

---

## 🔐 Configuração da API

Para funcionar corretamente, é necessário fornecer uma chave da **OpenAI API**. Você pode fazer isso de duas formas:

- Definindo a variável de ambiente `OPENAI_API_KEY`, ou
- Informando manualmente quando solicitado na interface.

---

## 🛠️ Como Usar

1. Digite uma tarefa descritiva na interface.
2. Clique em **"GERAR SCRIPT"**.
3. O código será criado, salvo e poderá ser executado automaticamente.
4. Você verá o status da operação na parte inferior da janela.

---

### 📽️ Demonstração em Vídeo

Confira como o **EXECUT AI** funciona na prática:

🔗 [Assista ao vídeo demonstrativo no LinkedIn](https://www.linkedin.com/posts/wesleymendonca-dev_inovacao-innovation-tecnologia-activity-7317883144429363200-qqMU?utm_source=share&utm_medium=member_desktop&rcm=ACoAACKe8HMBEIVD2ZA-0C686DfwjjASTzJiVXs)

---

## 📁 Estrutura de Pastas

Os scripts gerados serão salvos em:

```
Downloads/
└── EXECUT_AI_YYMMDD-HHMMSS/
    └── EXECUT_AI_YYMMDD-HHMMSS.py
```

---

## 📝 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [`LICENSE`](LICENSE) para mais detalhes.

---

## 👤 Autor

**Wesley Mendonça**  
🔗 [www.linkedin.com/in/wesleymendonca-dev/](https://www.linkedin.com/in/wesleymendonca-dev/)  
📧 wesleymendoncadev@gmail.com

---

## ☕ Apoio

Se este projeto te ajudou ou te inspirou, considere fazer uma doação para me apoiar:

- 💖 **Chave Pix**: `wesleymendoncadev@gmail.com`

Obrigado pelo apoio! 🙏
