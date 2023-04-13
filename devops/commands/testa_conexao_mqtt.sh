#!/usr/bin/env bash
# -----------------------------------------------------------------
# Script    : teste_conexao_mqtt
# Descricao : Aguarda a conexao com o MQTT, 
# Versao    : 0.2
# Autor     : Mayki Santos
# Data      : 21/10/2022
#-------------------------------------------------------------------
# Como usar : Copie este arquivo e suas dependencias para a pasta '/fot-simulator/commands' do container.
#-------------------------------------------------------------------


echo "Testando conexao com o MQTT"
until nc -vz $MQTT_SENDER_URL $MQTT_SENDER_PORT &> /dev/null; do
    echo "aguardando conexao com MQTT..."
    sleep 4
done

echo "Conexao com MQTT estabelecida"