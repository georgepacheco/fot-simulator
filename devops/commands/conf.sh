#!/usr/bin/env bash
# -----------------------------------------------------------------
# Script    : conf.sh
# Descricao : permite consultar ou editar valores de um arquivo de configuração para controle de execução do script
# Versao    : 0.2
# Autor     : Mayki Santos
# Data      : 21/10/2022
#-------------------------------------------------------------------
# Como usar : Crie um arquivo chamado "controle.conf" na raiz do sistema e defina suas variaveis no formato CHAVE=valor
#             O script recebe 1 ou 2 parametros, exemplo:
#               * conf.sh MINHA_CHAVE - retorna o valor da chave
#               * conf.sh MINHA_CHAVE NOVO_VALOR - altera o valor da chave
#             Esse script é útil para controlar o estado de algusn scripts   
#-------------------------------------------------------------------

################## VARIAVEIS ################## 
nome_arquivo=/controle.conf
declare -A lista_parametros
###############################################

ler_variaveis(){
    #ler arquivo e cria array associativo
    elementos=$(grep '\w\=\w' $nome_arquivo)
    IFS=$'\n'
    for linha in $elementos; do
        IFS='='
        chave_valor=($linha)
        lista_parametros["${chave_valor[0]}"]="${chave_valor[1]}"
    done
}


retorna_variavel(){
    chave=$1
    ler_variaveis
    #verifica se chave existe
    if [ -n lista_parametros[$chave] ]; then
        echo "${lista_parametros[$chave]}"
    else
        exit 3
    fi
}

altera_variavel(){
    chave=$1
    valor=$(retorna_variavel $chave)
    novo_valor=$2
    
    #verifica se chave existe
    if [ -n lista_parametros[$chave] ]; then
        #cria arquivo temporario
        temp=$(mktemp)
        #verifica se tem permissao nos arquivos
        if [ ! -x $temp ]; then
            chmod u+x $temp
        fi
        if [ ! -x $nome_arquivo ]; then
            chmod u+x $nome_arquivo
        fi
        #altera o valor da chave
        sed s/"$chave=$valor"/"$chave=$novo_valor"/ $nome_arquivo > $temp
        cat $temp > $nome_arquivo
        exit 0
    else
        exit 3
    fi
}


case $# in
    1)
        valor=$(retorna_variavel $1)
        echo "$valor"
        ;;
    2)
        altera_variavel $1 $2
        ;;
    *)
        exit 2
        ;;
esac