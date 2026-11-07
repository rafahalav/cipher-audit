# 🛡️ CIPHER AUDIT - Automated Linux Hardening Auditor

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-red.svg)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Local_AI-Ollama-orange.svg)](https://ollama.ai/)
[![Groq API](https://img.shields.io/badge/Cloud_AI-Groq_120B-purple.svg)](https://groq.com/)
[![DevSecOps](https://img.shields.io/badge/Focus-DevSecOps-yellow.svg)](https://www.devsecops.org/)

**Auditor Automatizado de Hardening Linux com Geração de Relatórios Estruturados (JSON/HTML) e Inteligência Híbrida (Local + Cloud)**

---

## 🎯 Sobre o Projeto

O **CIPHER AUDIT** é uma ferramenta de auditoria de segurança automatizada que analisa configurações de sistemas Linux, logs de autenticação e permissões de arquivos em busca de vulnerabilidades e más práticas de hardening. Utilizando **arquitetura híbrida de IA** (modelo local leve para privacidade + nuvem pesada para análise profunda), o sistema gera relatórios estruturados em JSON e HTML com classificação CVSS, vetores de ataque e comandos de correção prontos para execução.

### 🏗️ Por Que CIPHER AUDIT?

Ferramentas tradicionais de auditoria (Nessus, OpenVAS) são complexas, caras e exigem infraestrutura dedicada. O CIPHER AUDIT foi projetado para:

1. **Democratizar auditorias de segurança**: Qualquer administrador de sistemas pode rodar análises profissionais sem instalar scanners pesados
2. **Gerar evidências auditáveis**: Relatórios JSON/HTML salvos automaticamente com timestamp, prontos para compliance (LGPD, ISO 27001)
3. **Operar em hardware limitado**: Arquitetura híbrida permite análise profunda via cloud sem sobrecarregar CPUs antigas
4. **Integrar com pipelines DevSecOps**: Saída JSON estruturada pode ser consumida por CI/CD tools (Jenkins, GitLab CI)

---

## ✨ Features Principais

### 🔍 Análise Multi-Camada
- **Configurações de Sistema**: SSH, Apache, Nginx, Firewall (UFW/iptables)
- **Logs de Autenticação**: Detecção de força bruta, login root, IPs suspeitos
- **Permissões de Arquivos**: Identificação de permissões inseguras (777, shadow exposto)
- **Hardening Compliance**: Verificação contra CIS Benchmarks e OWASP Top 10

### 📊 Relatórios Estruturados
- **Classificação CVSS**: 🔴 CRÍTICA | 🟠 ALTA | 🟡 MÉDIA | 🟢 BAIXA
- **Comandos de Correção**: Cada vulnerabilidade inclui comando `sed` pronto para execução
- **Salvamento Automático**: JSON + HTML gerados automaticamente na pasta `reports/`
- **Pré-visualização Embutida**: Visualização do relatório HTML dentro da interface
- **Exportação para Navegador**: Abertura do relatório em tela cheia com um clique

### 🧠 Arquitetura Híbrida de IA
- **Modo Nuvem (Groq 120B)**: Análise profunda com modelo sênior, zero carga local
- **Modo Local (Ollama 1.5B)**: Auditoria offline para ambientes air-gapped
- **Prompt Engineering Avançado**: System prompt força saída JSON estruturada para parsing confiável
- **Temperatura Zero**: Máxima consistência e reprodutibilidade nas análises

---

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.13+
- [Ollama](https://ollama.ai/) instalado (para modo local)
- Conta na [Groq](https://console.groq.com/) com API Key (para modo nuvem)

### 1. Clone o Repositório
```bash
git clone https://github.com/rafahalav/cipher-audit.git
cd cipher-audit
```

### 2. Configure o Ambiente
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Baixar modelo local (opcional, ~1.2GB)
ollama pull qwen2.5:1.5b
```

### 3. Configure a API Key
Crie um arquivo `.env` na raiz do projeto:
```env
GROQ_API_KEY=gsk_sua_chave_aqui
```
Obtenha sua chave em: [https://console.groq.com/keys](https://console.groq.com/keys)

### 4. Execute
```bash
# Iniciar servidor Ollama (se for usar modo local)
ollama serve &

# Lançar interface web
./start.sh
```

Acesse `http://localhost:8501` no navegador.

---

## 💬 Exemplos de Uso

### 🔧 Auditoria de Configuração SSH

**Entrada:**
```text
Nome do Arquivo: sshd_config

Conteúdo:
PermitRootLogin yes
PasswordAuthentication yes
Protocol 1,2
X11Forwarding yes
```

**Saída (Relatório HTML):**
```
🔴 CRÍTICA: Root Login Habilitado
📍 Localização: Linha 1
💥 Impacto: Atacante pode obter acesso root direto via SSH
🛡️ Correção: sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

🟠 ALTA: Autenticação por Senha Habilitada
📍 Localização: Linha 2
💥 Impacto: Vulnerável a ataques de força bruta
🛡️ Correção: sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
```

### 📋 Auditoria de Firewall UFW

**Entrada:**
```text
Nome do Arquivo: ufw_status.txt

Conteúdo:
Status: active
Default: allow (incoming)
22/tcp    ALLOW IN    Anywhere
3306/tcp  ALLOW IN    Anywhere
6379/tcp  ALLOW IN    Anywhere
```

**Saída:**
```
🔴 CRÍTICA: MySQL Exposto à Internet (Porta 3306)
🟠 ALTA: Redis Exposto à Internet (Porta 6379)
🟡 MÉDIA: Política Default Permissiva (allow incoming)
```

### 🔐 Auditoria de Permissões de Arquivos

**Entrada:**
```text
Nome do Arquivo: permissions_check.txt

Conteúdo:
-rw-r--r-- 1 root root 2345 /etc/shadow
-rwxrwxrwx 1 www-data www-data 5678 /var/www/html/config.php
-rw-rw-rw- 1 root root 456 /root/.ssh/authorized_keys
```

**Saída:**
```
🔴 CRÍTICA: /etc/shadow com Permissões 644 (deveria ser 640 ou 000)
🔴 CRÍTICA: config.php com Permissões 777 (execução pública)
🟠 ALTA: authorized_keys com Permissões 666 (SSH inseguro)
```

---

## 🧠 Arquitetura Técnica

### Fluxo de Auditoria
```
┌─────────────────────────────────────────────────────────────┐
│                    CIPHER AUDIT                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐         ┌──────────────────────┐        │
│  │   Entrada    │         │   System Prompt      │        │
│  │  (Config/    │         │   (Força JSON        │        │
│  │   Log)       │         │    Estruturado)      │        │
│  └──────┬───────┘         └──────────┬───────────┘        │
│         │                            │                     │
│         └────────────┬───────────────┘                     │
│                      ▼                                     │
│         ┌────────────────────────┐                         │
│         │   Motor de Inferência  │                         │
│         │   (Híbrido)            │                         │
│         └──────────┬─────────────┘                         │
│                    │                                         │
│         ┌──────────┴─────────────┐                         │
│         ▼                        ▼                         │
│  ┌──────────────┐         ┌──────────────────────┐        │
│  │  Ollama API  │         │    Groq API          │        │
│  │  (Local 1.5B)│         │   (Cloud 120B)       │        │
│  └──────┬───────┘         └──────────┬───────────┘        │
│         │                            │                     │
│         └────────────┬───────────────┘                     │
│                      ▼                                     │
│         ┌────────────────────────┐                         │
│         │   Parser JSON          │                         │
│         │   (Validação + Limpeza)│                         │
│         └──────────┬─────────────┘                         │
│                    │                                         │
│         ┌──────────┴─────────────┐                         │
│         ▼                        ▼                         │
│  ┌──────────────┐         ┌──────────────────────┐        │
│  │  Salvar JSON │         │  Gerar HTML          │        │
│  │  (reports/)  │         │  (reports/)          │        │
│  └──────────────┘         └──────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Decisões de Engenharia

| Decisão | Justificativa |
|---|---|
| **Saída JSON Estruturada** | Permite parsing confiável, integração com CI/CD, e geração de relatórios HTML dinâmicos |
| **Temperatura 0.0** | Máxima reprodutibilidade: mesma entrada sempre gera mesma saída (crítico para auditorias) |
| **Salvamento Automático** | Persistência de evidências: nenhuma auditoria é perdida por fechamento acidental do navegador |
| **HTML Standalone** | Relatórios autocontidos com CSS embutido, abrem offline em qualquer navegador |
| **Prompt Externo** | Separação de responsabilidades: fácil ajustar regras de auditoria sem tocar no código |
| **Arquitetura Híbrida** | Flexibilidade: modo nuvem para análise profunda, modo local para ambientes restritos |

---

## 📊 Por Que Isso Importa para DevSecOps e AI Training?

Empresas como **Scale AI**, **Outlier**, **DataAnnotation** e equipes de **DevSecOps** buscam profissionais que entendam:

1. **Automação de Segurança**: Não apenas rodar scanners, mas construir pipelines de auditoria automatizada
2. **Engenharia de Prompt Estruturado**: Forçar LLMs a gerar saída parseável (JSON) para integração com sistemas
3. **Arquitetura Híbrida**: Projetar sistemas que funcionam tanto offline quanto online
4. **Geração de Relatórios**: Transformar dados brutos de IA em artefatos auditáveis (compliance)
5. **Domínio Especializado**: Conhecimento real de hardening Linux, CVSS, CIS Benchmarks

O CIPHER AUDIT demonstra **todas essas competências** em um projeto funcional, documentado e pronto para produção.

---

## 🛠️ Stack Tecnológica

- **Python 3.13**: Linguagem principal
- **Streamlit**: Interface web interativa com componentes HTML customizados
- **Ollama**: Servidor de inferência local (Qwen2.5 1.5B)
- **Groq API**: Inferência na nuvem (modelo 120B parâmetros)
- **python-dotenv**: Gerenciamento seguro de variáveis de ambiente
- **webbrowser**: Integração com navegador do sistema operacional
- **JSON/HTML**: Formatos de saída para interoperabilidade

---

## 📁 Estrutura do Projeto

```
cipher-audit/
├── core/
│   ├── __init__.py
│   └── llm_engine.py          # Motor de inferência híbrido com parser JSON
├── prompts/
│   └── system_prompt_audit.txt # Prompt sênior de auditoria (força JSON)
├── reports/                    # Relatórios gerados automaticamente (gitignored)
├── web.py                      # Interface Streamlit com pré-visualização HTML
├── start.sh                    # Lançador unificado
├── requirements.txt            # Dependências Python
├── .env                        # API Keys (NÃO commitar)
├── .gitignore                  # Proteção de arquivos sensíveis
└── README.md                   # Este arquivo
```

---

## 🔗 Projetos Relacionados

- **PAI AI Coder**: Assistente de geração de código Python - [github.com/rafahalav/pai-ai-coder](https://github.com/rafahalav/pai-ai-coder)
- **PAI Code Reviewer**: Analisador de código com foco em segurança e performance - [github.com/rafahalav/pai-code-reviewer](https://github.com/rafahalav/pai-code-reviewer)
- **CIPHER IA v2**: Assistente de cibersegurança com chat interativo - [github.com/rafahalav/cipher-ia-v2](https://github.com/rafahalav/cipher-ia-v2)

---

## 🧑‍💻 Autor

**Rafael Halav**  
Technology Professional | Telecommunications | IT | Python | AI | Data  
🔗 [LinkedIn](https://www.linkedin.com/in/rafael-halav) | ✉️ [Contato](mailto:rafa.halav83@gmail.com)

*Desenvolvido com foco em aprendizado contínuo e aplicação prática de Inteligência Artificial em cenários de DevSecOps e recursos limitados.*

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Status**: Active Development  
**Última atualização**: Novembro 2026
```
https://github.com/rafahalav/cipher-audit
