# AutoU Email Intelligence 📧🤖

Uma solução premium para **classificação automática e resposta inteligente de emails**, desenvolvida para o Desafio Técnico da AutoU.

![Status](https://img.shields.io/badge/status-production--ready-brightgreen) ![Python](https://img.shields.io/badge/python-3.11-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Sobre o Projeto

Sistema web que utiliza **Inteligência Artificial** para automatizar o processamento de emails em empresas do setor financeiro, classificando-os como **Produtivos** (requerem ação) ou **Improdutivos** (apenas informativos) e gerando **respostas automáticas** contextuais.

---

## ✨ Funcionalidades

- ✅ **Classificação Inteligente**: AI identifica emails como Produtivos ou Improdutivos
- ✅ **Respostas Automáticas**: Sugestões de resposta baseadas no contexto
- ✅ **Interface Premium**: Design moderno com Glassmorphism e animações suaves
- ✅ **Multi-formato**: Suporta upload de `.txt`, `.pdf` ou texto direto
- ✅ **Processamento NLP**: Remoção de stop words e lemmatização em português
- ✅ **Modo Offline**: Funciona sem API key usando heurísticas inteligentes

---

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask** - Framework web
- **NLTK** - Processamento de linguagem natural
- **OpenAI API** - Classificação e geração de respostas (opcional)
- **PyPDF** - Extração de texto de PDFs

### Frontend
- **HTML5, CSS3, JavaScript** (Vanilla)
- **Google Fonts** - Tipografia (Outfit)
- **Glassmorphism Design System**

---

## 📦 Instalação Local

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/autou-email-intelligence.git
cd autou-email-intelligence
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente (Opcional)**
```bash
# Copie o template
cp .env.example .env

# Edite o arquivo .env e adicione sua chave OpenAI (se possuir)
# OPENAI_API_KEY=sk-...
```

> **Nota:** Se você não configurar a API Key, o sistema funcionará em **modo offline** usando classificação por palavras-chave.

4. **Execute o servidor**
```bash
python backend/app.py
```

5. **Acesse no navegador**
```
http://localhost:5000
```

---

## 🚀 Deploy na Nuvem

### Render (Recomendado - Gratuito)

1. Crie uma conta em [Render.com](https://render.com)
2. Clique em **"New +" → "Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `autou-email-classifier`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 backend.app:app`
5. **(Opcional)** Adicione variável de ambiente:
   - Key: `OPENAI_API_KEY`
   - Value: `sua-chave-aqui`
6. Clique em **"Create Web Service"**

Pronto! Sua aplicação estará disponível em `https://autou-email-classifier.onrender.com`

### Alternativas
- **Railway.app**: Processo similar ao Render
- **Heroku**: Use `heroku login` e `git push heroku main`

---

## 📁 Estrutura do Projeto

```
autou-email-intelligence/
├── backend/
│   ├── app.py              # Servidor Flask e rotas
│   └── nlp_engine.py       # Motor de NLP e AI
├── frontend/
│   ├── index.html          # Interface principal
│   ├── style.css           # Estilos (Glassmorphism)
│   └── script.js           # Lógica do frontend
├── examples/
│   ├── email_produtivo_1.txt
│   ├── email_produtivo_2.txt
│   ├── email_improdutivo_1.txt
│   └── email_improdutivo_2.txt
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testando a Aplicação

### Usando Exemplos Prontos
Na pasta `examples/` você encontrará 4 emails de teste:
- **Produtivos**: Problema técnico, solicitação de atualização
- **Improdutivos**: Agradecimento, felicitações

### Teste Manual
1. Acesse a aplicação
2. Escolha entre **"Upload de Arquivo"** ou **"Texto Direto"**
3. Envie um email de exemplo
4. Observe a classificação e resposta sugerida

---

## 🎨 Características Visuais

- **Paleta de Cores**: Dark mode com gradientes Indigo/Pink
- **Glassmorphism**: Efeitos de vidro fosco com `backdrop-filter`
- **Animações**: Hover effects, loading spinner, fade-in transitions
- **Tipografia**: Google Fonts (Outfit) para visual moderno
- **Responsivo**: Funciona em desktop e mobile

---

## 🔧 Configuração Avançada

### Ajustando o Modelo AI
No arquivo `backend/nlp_engine.py`, você pode modificar:
- Modelo OpenAI (linha 55): `gpt-3.5-turbo` → `gpt-4`
- Temperatura (linha 73): `0.7` → ajuste criatividade
- Palavras-chave offline (linha 93): adicione termos específicos

### Personalizando Respostas
Edite os templates de resposta em `nlp_engine.py` (linhas 108-111)

---

## 📝 Licença

Este projeto foi desenvolvido como parte do Processo Seletivo da AutoU.

---

## 👤 Autor

**[Seu Nome]**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)

---

## 🙏 Agradecimentos

Desenvolvido com dedicação para o desafio AutoU 2024. 🚀
