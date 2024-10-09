# ProjetoIntegradoT2

Desenvolvido por: Victor Alberti, Kauã Ribeiro, Júlio Magalhães e Samuel Farias

## Descrição do Projeto

  O ProjetoIntegradoT2 visa criar um sistema de rádio automatizado para aviação, onde a frequência de operação do dispositivo é alterada automaticamente com base na área de voo selecionada pelo piloto. Isso elimina a necessidade de configurar manualmente a         
  frequência do rádio, tornando o processo mais eficiente e seguro. O sistema foi desenvolvido como uma solução IoT, utilizando o protocolo MQTT para transportar a informação da frequência adequada para cada região de comunicação.

## Dependências

  Para executar o sistema, o dispositivo responsável pela consulta ao Broker MQTT e a leitura Serial precisa:

   - Ser capaz de executar códigos em Python 3.11.2.
   - Ter capacidade de conectar-se à internet.
   - Possuir as bibliotecas Python necessárias instaladas (PREENCHER com os nomes das bibliotecas específicas).

## Configuração da Interface Serial

  Para garantir o funcionamento correto, é necessário ajustar a interface Serial no arquivo App.py. Isso pode ser feito na linha 17 do código:

    ser = serial.Serial("{Sua interface, Ex: ttyUSB0}", baudrate=115200, timeout=1)
    
  Substitua {Sua interface, Ex: ttyUSB0} pelo nome da sua interface Serial.

## Instruções de Uso

## 1. Definir a Frequência (controle.py)
   
  Execute o código controle.py para definir a frequência a ser utilizada para cada área de voo. Durante a execução, o sistema solicitará que você informe a frequência de cada região. Se tudo estiver correto, a mensagem de sucesso aparecerá no console.

## 2. Leitura Serial (App.py)
   
  Após definir as frequências, execute o código App.py no dispositivo que fará a leitura da interface Serial. O console exibirá as frequências obtidas por meio da comunicação com o broker MQTT.

## 3. Painel de Controle Físico
   
  O painel de controle possui 6 botões e 2 LEDs, com as seguintes funções:

    Botão 1: Seleciona a frequência da Área A.
    
    Botão 2: Seleciona a frequência da Área B.
    
    Botão 3: Seleciona a frequência da Área C.
    
    Botão 4: Seleciona a frequência da Área D.
    
    Botão 5: Seleciona a frequência da Área E.
    
    Botão 6: Ativa o modo de emergência.
    
    LED 1: Pisca 3 vezes para indicar que a frequência foi trocada e gravada.
    
    LED 2: Pisca para indicar perda de conexão com o broker MQTT.

  ### Utilizando o Painel de Controle
  
  O piloto deve inicialmente selecionar a área de voo (por exemplo, Área C) e aguardar 3 piscadas do LED 1, confirmando que a frequência foi ajustada com sucesso. Se for necessário mudar de área durante o voo (por exemplo, para a Área E), o sistema ajustará   
  automaticamente a nova frequência e o LED 1 piscará novamente 3 vezes.
  
  Se o LED 2 começar a piscar, isso indica um problema de comunicação. Neste caso, o piloto deve ativar o modo de emergência pressionando o botão 6.

  ### Modo de Emergência
  O modo de emergência troca a frequência de operação do rádio para a frequência de emergência (geralmente a frequência de maior alcance e menor valor).
  Enquanto o modo de emergência estiver ativo, qualquer frequência de outra área será ignorada.
  Ao desativar o modo de emergência, a última frequência recebida será automaticamente gravada.
  Para desativar o modo de emergência, pressione o botão 6 novamente.
