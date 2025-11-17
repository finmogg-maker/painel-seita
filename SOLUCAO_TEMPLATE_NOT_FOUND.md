# 🔧 SOLUÇÃO: TemplateNotFound - login.html

## ❌ ERRO QUE VOCÊ ESTÁ VENDO

```
jinja2.exceptions.TemplateNotFound: login.html
```

## 🔍 CAUSA DO PROBLEMA

O Render não está encontrando a pasta `templates/` com os arquivos HTML.

**Isso geralmente acontece porque:**
- ❌ A pasta `templates/` não foi enviada para o GitHub
- ❌ Os arquivos HTML não estão no repositório
- ❌ O Git está ignorando os templates

---

## ✅ SOLUÇÃO PASSO A PASSO

### **PASSO 1: Verificar se templates estão no Git**

No terminal, execute:

```bash
git status
```

**Se você ver `templates/` listado como "untracked files", significa que não estão no Git!**

### **PASSO 2: Adicionar templates ao Git**

```bash
# Adicionar pasta templates completa
git add templates/

# Verificar se foi adicionado
git status

# Deve mostrar templates/ como "new file" ou "modified"
```

### **PASSO 3: Fazer commit**

```bash
git commit -m "Adicionar templates ao repositório"
```

### **PASSO 4: Enviar para GitHub**

```bash
git push origin main
```

(ou `git push origin master` se sua branch for master)

### **PASSO 5: Verificar no GitHub**

1. Acesse: https://github.com/finmogg-maker/seu-repositorio
2. Verifique se existe a pasta `templates/`
3. Verifique se existem os arquivos:
   - ✅ `templates/login.html`
   - ✅ `templates/index.html`
   - ✅ `templates/admin.html`

### **PASSO 6: Atualizar deploy no Render**

1. No Render, vá em seu serviço
2. Clique em **"Manual Deploy"** → **"Deploy latest commit"**
3. Aguarde o deploy completar

---

## 🔍 VERIFICAÇÃO RÁPIDA

Execute estes comandos para verificar:

```bash
# Ver todos os arquivos que o Git está rastreando
git ls-files templates/

# Deve mostrar:
# templates/admin.html
# templates/index.html
# templates/login.html

# Se não mostrar nada, os templates não estão no Git!
```

---

## 🆘 SE AINDA NÃO FUNCIONAR

### **Forçar adicionar mesmo se estiver ignorado:**

```bash
# Forçar adicionar templates
git add -f templates/

# Commit
git commit -m "Forçar adicionar templates"

# Push
git push
```

### **Verificar estrutura de pastas:**

No Render, a estrutura deve ser:

```
/opt/render/project/src/
├── app.py
├── requirements.txt
├── Procfile
├── templates/
│   ├── login.html
│   ├── index.html
│   └── admin.html
└── static/
    └── images/
```

---

## ✅ JÁ CORRIGI NO CÓDIGO

Atualizei o `app.py` para especificar explicitamente:
```python
app = Flask(__name__, template_folder='templates', static_folder='static')
```

Isso garante que o Flask encontre os templates mesmo no Render.

---

## 📝 RESUMO

**O problema é:** Templates não estão no GitHub → Render não encontra → Erro 500

**A solução é:** Adicionar templates ao Git → Push → Redeploy no Render

---

## 🚀 COMANDOS RÁPIDOS (Copie e Cole)

```bash
git add templates/
git status
git commit -m "Adicionar templates ao repositório"
git push origin main
```

Depois faça redeploy no Render!

