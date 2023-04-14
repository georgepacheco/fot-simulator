# FoT-Simulator

## Pré Requisitos


* Ubuntu 20.04 ou superior

* [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)


* [Docker desktop (opcional)](https://docs.docker.com/desktop/install/linux-install/)

## Instalação

1. Usando o terminal, acesse a pasta principal do fot-simulator.

2. Execute o comando `docker compose -f docker-compose-local_docker.yml up -d`

## Exemplos de Uso

Após instalação, o container entra em execução e a simulação inicia. Para verificar os dados que estão sendo publicados pelo sensores é necessário usar o terminal do container em execução e se subscrever nos tópicos onde os dados estão sendo publicados.

#### Exemplo 1 - Subscrevendo em todos os tópicos de um gateway

`mosquitto_sub -h "10.0.0.24" -t "#"`

#### Exemplo 2 - Subscrevendo em um tópico de um sensor

`mosquitto_sub -h "10.0.0.24" -t "dev/sc01/RES"`

## Configurar Dispositivos

O simulador está configurado com alguns dispositivos (sensores e gateways), porém é possível modificar essa configuração padrão alterando a quantidade de sensores e gateways existentes, bem como as associações eles. Para isso é necessário alterar dois arquivos localizados na pasta `/sim`: `data_hosts.json` e `association_hosts.json`. No primeiro estão disponíveis todos os dispositivos da simulação e no segundo a forma como estão associados, ou seja, em qual gateway um sensor está conectado.



