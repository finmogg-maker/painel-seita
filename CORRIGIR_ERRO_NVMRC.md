# 🔧 CORRIGIR: Erro do .nvmrc no Render

## ❌ Problema

O arquivo `.nvmrc` ainda está no seu repositório GitHub e está causando este erro:
```
Invalid node version specification '# Este arquivo evita que o Netlify tente instalar Python'
```

## ✅ SOLUÇÃO RÁPIDA

### **Opção 1: Remover via GitHub Web (MAIS FÁCIL)**

1. Acesse seu repositório: https://github.com/finmogg-maker/painel-seita
2. Procure pelo arquivo `.nvmrc` na lista de arquivos
3. Clique no arquivo `.nvmrc`
4. Clique no ícone de **lixeira** (Delete) no canto superior direito
5. Digite uma mensagem de commit: `Remove .nvmrc file`
6. Clique em **"Commit changes"**
7. No Render, vá em **"Manual Deploy"** → **"Deploy latest commit"**

### **Opção 2: Remover via Git (se tiver Git instalado)**

Abra o terminal na pasta do projeto e execute:

```bash
git rm .nvmrc
git commit -m "Remove .nvmrc file"
git push
```

Depois, no Render:
- Clique em **"Manual Deploy"** → **"Deploy latest commit"**

### **Opção 3: Criar arquivo vazio (temporário)**

Se não conseguir remover, crie um arquivo `.nvmrc` vazio ou com apenas:
```
18
```
(versão do Node.js válida)

Mas a melhor solução é **remover completamente** o arquivo.

## 🎯 Depois de Remover

1. ✅ Arquivo `.nvmrc` removido do GitHub
2. ✅ No Render, clique em **"Manual Deploy"**
3. ✅ Selecione **"Deploy latest commit"**
4. ✅ Aguarde o build
5. ✅ Site deve funcionar!

## 📝 Arquivos que também podem causar problemas

Se ainda der erro, remova também do GitHub:
- `package.json` (se existir)
- `netlify.toml` (se existir)
- `.netlifyignore` (se existir)

---

**IMPORTANTE**: O arquivo `.nvmrc` foi deletado localmente, mas ainda está no GitHub. Você precisa removê-lo do GitHub também!



