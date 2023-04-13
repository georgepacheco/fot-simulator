#!/usr/bin/env bash
# -----------------------------------------------------------------
# Script    : instala_dependencias
# Descricao : instala dependecias da aplicação com base no arquivo requirements.txt
# Versao    : 0.2
# Autor     : Mayki Santos
# Data      : 30/09/2022
#-------------------------------------------------------------------
# Como usar : Copie este arquivo para a pasta '/commands' do container 
#-------------------------------------------------------------------


echo "BAIXANDO DEPENDENCIAS"
cd /fot-simulator/sensores
pip install -r requirements.txt &> "$PASTA_LOGS/pipInstall.log" || exit 3
echo "DEPENDENCIAS INSTALADAS..."

exit 0