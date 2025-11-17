# 🔧 Remover .nvmrc do GitHub

O arquivo `.nvmrc` ainda está no seu repositório GitHub e está causando erro no Render.

## ✅ Solução Rápida

### Opção 1: Via Git (Recomendado)

Execute estes comandos no terminal (na pasta do projeto):

```bash
# Remover o arquivo do Git
git rm .nvmrc

# Fazer commit
git commit -m "Remove .nvmrc file"

# Enviar para GitHub
git push
```

### Opção 2: Via GitHub Web

1. Acesse: https://github.com/finmogg-maker/painel-seita
2. Clique no arquivo `.nvmrc`
3. Clique no ícone de lixeira (Delete)
4. Faça commit da remoção
5. No Render, clique em "Manual Deploy" → "Deploy latest commit"

### Opção 3: Criar arquivo .gitignore

Se o arquivo continuar aparecendo, adicione ao `.gitignore`:

```
.nvmrc
package.json
netlify.toml
.netlifyignore
```

## 🚀 Depois de Remover

1. No Render, vá em "Manual Deploy"
2. Clique em "Deploy latest commit"
3. Aguarde o build
4. ✅ Deve funcionar agora!



