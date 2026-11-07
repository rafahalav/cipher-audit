#!/bin/bash
echo "🛡️ CIPHER AUDIT - Iniciando sistemas..."

if ! pgrep -x "ollama" > /dev/null; then
    echo "⚙️ Iniciando Ollama em background..."
    ollama serve > /dev/null 2>&1 &
    sleep 2
fi

if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
fi

echo "🌐 Abrindo interface Web de Auditoria..."
streamlit run web.py
