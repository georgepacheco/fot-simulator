Informacoes sobre arquivos e execução de experimentos

Pasta de trabalho:
/home/mininet/sim

Iniciar experimentos:
sudo python2 sim.py

Descricao dos arquivos:

-data_hosts.json
	-Arquivo com informações no formato json dos hosts que irão compor a rede
-association_hosts.json
	- Arquivo com informações sobre associações entre sensores e gateways, i.e, define o gateway que cada sensor irá se comunicar
-config.json
	-Configs sobre os sensores/dispositivos virtuais, modificações no arquivo serão espelhadas
	para todos os sensores do experimento.
	-Informações como: ip do broker e dados do protocolo TATU (publish, collect).
	OBS: Porta do broker está hardcoding como 1883 (arquivos sim.py e call_main.py)
-main.py; sensors.py tatu.py
	-Arquivos que criam os sensores/disp virtuais e implementam a lógica e interpretaçao do 
	protocolo TATU
-utils_hosts.py
	-Funções úteis para manipular informações que estão armazenadas no arquivo data_hosts.json
	-Utilizado principalmente para criar o experimento e indicar informações dos hosts
-create_topo.py
	-Cria os links, switches e constrói a topologia
	-Basea-se nos dados obtidos em data_hosts.json
-sim.py
	-Arquivo gerador do experimento
	-Criação dos sensores virtuais: Função init_sensors, nela são ajustados qual tipo de sensor criado e o fluxo de comunicação e iniciado
	-Criação do Flow entre sensores e Broker: Função init_flow
	OBS: sensor "soilmoistureSensor" gerou erro no Storage.


Abrir terminal do host no CLI: xterm h1
Nome do browser: midori​
