#!/usr/bin/env bash
# -----------------------------------------------------------------
# Script    : inicializa_aplicacao
# Descricao : inicializa e publica dados dos sensores
# Versao    : 0.1
# Autor     : Mayki Santos
# Data      : 07/10/2022
#-------------------------------------------------------------------

. /etc/profile

if [ $(conf.sh EXEC_INSTAL_DEP) -eq 0 ]; then
    # instala dependencias da aplicação
    instala_dependencias.sh || exit 1
    conf.sh EXEC_INSTAL_DEP 1
fi

#testa_conexao_mqtt.sh

cd /fot-simulator/sensores/sim && \
service openvswitch-switch start && \
service mosquitto restart && \
mn -c && \
${COMANDO_MININET}


# mosquitto_pub -h server.mqtt -t topic -m "teste"

