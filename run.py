#!/usr/bin/env python
"""
Script para rodar a aplicação localmente.
Use: python run.py
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

# Importa e roda a aplicação
if __name__ == '__main__':
    # Importa depois de adicionar ao path
    from backend.app import app
    
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 AutoU Email Intelligence")
    print(f"📡 Servidor rodando em: http://localhost:{port}")
    print(f"🛑 Pressione CTRL+C para parar\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
