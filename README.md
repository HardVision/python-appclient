Script com todo o código finalizado e as características necessárias para a captura e consulta dos dados.
Aqui está um **README completo, organizado e profissional**, ensinando exatamente como rodar sua aplicação Python usando **venv**, **pip**, **requirements.txt** e configurando corretamente o arquivo **.env** conforme suas regras.

Você pode copiar e colar diretamente no repositório.
Escrevi em um formato padrão para GitHub.

---

# 🐍 **Guia de Execução — Aplicação Python com venv + pip**

Este projeto utiliza um ambiente virtual (**venv**), variáveis de ambiente via arquivo **.env**, e gerenciamento de dependências com `requirements.txt`.

Siga os passos abaixo para configurar e executar corretamente.

---

# 📦 **1. Pré-requisitos**

Certifique-se de ter instalado:

* **Python 3.8+**
* **pip** (já acompanha o Python)
* **Git** (opcional)

Verifique com:

```bash
python --version
pip --version
```

---

# 🧪 **2. Criar o ambiente virtual (venv)**

Na raiz do projeto, execute:

### **Windows**

```bash
python -m venv venv
```

### **Linux / Mac**

```bash
python3 -m venv venv
```

---

# ▶️ **3. Ativar o ambiente virtual**

### **Windows**

```bash
venv\Scripts\activate
```
Ou

```bash
.\venv\Scripts\activate
```

### **Linux / Mac**

```bash
source venv/bin/activate
```

Quando ativado, o terminal exibirá algo como:

```
(venv) C:\seu-projeto>
```

---

# 📥 **4. Instalar as dependências**

Com o **venv ativado**, execute:

```bash
pip install -r requirements.txt
```

Estas são as bibliotecas usadas pelo projeto:

```
psutil
mysql-connector-python
python-dotenv
tabulate
numpy
pandas
getmac
slack_sdk
```

---

# 🔐 **5. Configurar o arquivo `.env`**

Crie um arquivo chamado **`.env`** na raiz do projeto:

> ⚠️ **O nome deve ser exatamente `.env` (sem extensão)**
> ⚠️ **Não inclua aspas nos valores**

Exemplo:

```
USER_DB=seu_usuario_do_db
PASSWORD_DB=sua_senha
HOST_DB=localhost
DATABASE_DB=hardvision
SLACK_BOT=token_slack
```

---


---

# 🚫 **7. Desativar o ambiente virtual**

Quando terminar de usar:

```bash
deactivate
```

---

# ♻️ **8. Atualizar dependencies (opcional)**

Caso você instale novas libs:

```bash
pip freeze > requirements.txt
```

---
