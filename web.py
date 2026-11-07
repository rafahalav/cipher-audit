import streamlit as st
import sys
import os
import json
import datetime
import webbrowser
import streamlit.components.v1 as components

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.llm_engine import CipherAuditEngine

st.set_page_config(page_title="CIPHER AUDIT", page_icon="🛡️", layout="wide")

# Estética Cyberdeck / Relatório Profissional
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .report-card {
        border-left: 5px solid;
        background-color: #1a1d24;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .critica { border-color: #ff4b4b; }
    .alta { border-color: #ffaa00; }
    .media { border-color: #ffff00; }
    .baixa { border-color: #00cc00; }
    .seguranca { border-color: #00ff00; }
    .code-block {
        background-color: #000000;
        color: #00ff00;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.9em;
    }
    .file-path {
        background-color: #1a1d24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #2d3748;
        font-family: monospace;
        font-size: 0.85em;
        margin: 5px 0;
    }
    /* ESTILO DO BOTÃO VERDE */
    .stButton>button {
        background-color: #00ff00 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background-color: #00cc00 !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ CIPHER AUDIT")
st.subheader("Relatório Automatizado de Hardening Linux")
st.caption("Análise de configurações, logs e permissões com inteligência de nível sênior.")

# Carregar Prompt
base_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(base_dir, "prompts", "system_prompt_audit.txt")
try:
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
except FileNotFoundError:
    st.error("❌ system_prompt_audit.txt não encontrado.")
    st.stop()

# Garantir que a pasta reports existe
os.makedirs("reports", exist_ok=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    mode = st.radio("Motor de Inferência:", ["Nuvem (Groq 120B - Recomendado)", "Local (Ollama 1.5B)"])
    engine_mode = 'web' if "Nuvem" in mode else 'cli'
    
    st.markdown("---")
    st.info("💡 **Dica:** Cole a saída de comandos como `cat /etc/ssh/sshd_config` ou `ufw status verbose` para melhores resultados.")

# Área Principal
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Entrada de Dados")
    filename = st.text_input("Nome do Arquivo/Contexto:", "sshd_config")
    audit_input = st.text_area("Cole o conteúdo da configuração ou log aqui:", height=300, placeholder="Ex:\nPermitRootLogin yes\nPasswordAuthentication yes")
    
    if st.button("🔍 Executar Auditoria", type="primary", use_container_width=True):
        if not audit_input.strip():
            st.warning("Por favor, insira algum conteúdo para auditar.")
        else:
            with st.spinner("🛡️ Analisando configurações em busca de vulnerabilidades..."):
                try:
                    engine = CipherAuditEngine(mode=engine_mode)
                    results = engine.audit(audit_input, system_prompt, filename)
                    st.session_state.audit_results = results
                    st.session_state.audit_filename = filename
                    st.success("✅ Auditoria concluída com sucesso!")
                except Exception as e:
                    st.error(f"❌ Erro na auditoria: {e}")

with col2:
    st.markdown("### 📊 Relatório de Vulnerabilidades")
    
    if "audit_results" in st.session_state:
        results = st.session_state.audit_results
        filename = st.session_state.audit_filename
        
        # Resumo
        critica_count = sum(1 for r in results if r.get("severidade") == "CRÍTICA")
        alta_count = sum(1 for r in results if r.get("severidade") == "ALTA")
        
        st.markdown(f"🔴 **Críticas:** {critica_count} | 🟠 **Altas:** {alta_count} | 📁 **Total de achados:** {len(results)}")
        st.divider()
        
        # Variáveis para o HTML
        html_cards = ""
        
        for item in results:
            sev = item.get("severidade", "BAIXA").upper()
            css_class = "critica" if sev == "CRÍTICA" else "alta" if sev == "ALTA" else "media" if sev == "MÉDIA" else "seguranca" if sev == "SEGURANÇA" else "baixa"
            color_hex = "#ff4b4b" if sev == "CRÍTICA" else "#ffaa00" if sev == "ALTA" else "#ffff00" if sev == "MÉDIA" else "#00ff00"
            
            # Renderiza no Streamlit
            st.markdown(f"""
            <div class="report-card {css_class}">
                <h4 style="margin-top:0; color: {color_hex};">
                    ⚠️ {item.get('vulnerabilidade', 'Desconhecido')}
                </h4>
                <p><strong>📍 Localização:</strong> {item.get('localizacao', 'N/A')}</p>
                <p><strong>💥 Impacto:</strong> {item.get('impacto', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if item.get("comando_correcao") and item.get("comando_correcao") != "Nenhuma ação necessária.":
                st.markdown("🛡️ **Comando de Correção:**")
                st.code(item["comando_correcao"], language="bash")

            # Monta o HTML para o arquivo
            html_cards += f"""
            <div class="report-card {css_class}">
                <h3 style="color: {color_hex};">⚠️ {item.get('vulnerabilidade', 'Desconhecido')}</h3>
                <p><strong>📍 Localização:</strong> {item.get('localizacao', 'N/A')}</p>
                <p><strong>💥 Impacto:</strong> {item.get('impacto', 'N/A')}</p>
                <div class="code-block">
                    <strong>🛡️ Correção:</strong><br>
                    <code>{item.get('comando_correcao', 'N/A')}</code>
                </div>
            </div>
            """

        # --- SALVAMENTO AUTOMÁTICO NA PASTA REPORTS ---
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = filename.replace(" ", "_").replace("/", "_")
        
        # 1. Salvar JSON
        json_path = f"reports/audit_{safe_filename}_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        # 2. Gerar e Salvar HTML Standalone
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>CIPHER AUDIT - {safe_filename}</title>
            <style>
                body {{ background-color: #0e1117; color: #e0e0e0; font-family: sans-serif; padding: 20px; }}
                .report-card {{ border-left: 5px solid; background-color: #1a1d24; padding: 15px; border-radius: 8px; margin-bottom: 15px; }}
                .critica {{ border-color: #ff4b4b; }} .alta {{ border-color: #ffaa00; }} .media {{ border-color: #ffff00; }} .baixa {{ border-color: #00cc00; }} .seguranca {{ border-color: #00ff00; }}
                .code-block {{ background-color: #000; color: #0f0; padding: 10px; border-radius: 5px; font-family: monospace; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <h1>🛡️ CIPHER AUDIT Report</h1>
            <h2>Alvo: {safe_filename} | Data: {timestamp}</h2>
            <p>🔴 Críticas: {critica_count} | 🟠 Altas: {alta_count} | Total: {len(results)}</p>
            <hr>
            {html_cards}
        </body>
        </html>
        """
        html_path = f"reports/audit_{safe_filename}_{timestamp}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # --- SEÇÃO DE RELATÓRIOS SALVOS (LIMPA E FUNCIONAL) ---
        st.markdown("---")
        st.markdown("### 💾 Relatórios Salvos Automaticamente")
        
        # Caminho absoluto para os arquivos
        abs_json_path = os.path.abspath(json_path)
        abs_html_path = os.path.abspath(html_path)
        
        st.markdown(f"""
        <div class="file-path">
            📄 <strong>JSON:</strong> {abs_json_path}
        </div>
        <div class="file-path">
            🌐 <strong>HTML:</strong> {abs_html_path}
        </div>
        """, unsafe_allow_html=True)
        
        # Botão único e funcional para abrir o arquivo no navegador do SO (AGORA VERDE!)
        if st.button("🌐 Abrir Relatório HTML no Navegador", use_container_width=True):
            webbrowser.open(f'file://{abs_html_path}')
            st.success("✅ Relatório aberto em uma nova aba!")
        
        # Pré-visualização do HTML dentro do Streamlit
        st.markdown("---")
        st.markdown("### 👁️ Pré-visualização do Relatório")
        components.html(html_content, height=600, scrolling=True)

    else:
        st.info("Aguardando dados para auditoria...")
