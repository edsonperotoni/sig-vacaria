#!/bin/bash

# 1. Nome da pasta onde ficarão os arquivos do ambiente virtual
VENV_NAME=".venv"

echo "--- 🛠️ Iniciando configuração do ambiente Python ---"

# 2. Verifica se a pasta do ambiente já existe
# O sinal '!' significa 'não'. Então lemos: "Se não existir o diretório..."
if [ ! -d "$VENV_NAME" ]; then
    echo "> Criando ambiente virtual em $VENV_NAME..."
    python -m venv $VENV_NAME
else
    echo "> Ambiente $VENV_NAME já existe. Pulando criação."
fi

# 3. Atualiza o gerenciador de pacotes e instala as bibliotecas
echo "> Instalando dependências ..."
# Usamos o caminho direto do pip dentro da venv para garantir que instale no lugar certo
./$VENV_NAME/bin/pip install --upgrade pip
./$VENV_NAME/bin/pip install -r requirements.txt

echo "--- ✅ Tudo pronto! ---"
echo "Para ativar no Fish, use: source $VENV_NAME/bin/activate.fish"
echo "Para ativar no Bash, use: source $VENV_NAME/bin/activate"

# Dica para usuários de Arch/CachyOS ou qualquer um com shell Fish
echo ""
echo "No Arch Linux ou CachyOS Linux, podes criar uma abreviação para o comando de ativação:"
echo "abbr --add venv_up 'source $VENV_NAME/bin/activate.fish'"