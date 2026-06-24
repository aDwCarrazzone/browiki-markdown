# Central de Suporte

# Central de Suporte

![CDSuporte2](https://cdn.jsdelivr.net/gh/aDwCarrazzone/browiki-images@main/8/85/CDSuporte2.jpg)

A Central de Suporte é um serviço de atendimento ao cliente oferecido pela GnJoy LATAM para resolução de problemas do jogo.

1. Para a Central de Suporte, **[acesse este site](https://gravityus.freshdesk.com/pt-BR/support/home)**.
2. Você deverá logar usando a conta GnJoy criada.
3. Assim que entrar, um novo botão aparecerá na página inicial: **[Enviar um Ticket](https://gravityus.freshdesk.com/pt-BR/support/tickets/new)**.

Alguns problemas no jogo são bastante comuns e pode ser que a solução para seu erro esteja listada abaixo.

:   **Dicas:**

    :   O jogo normalmente fica instalado em `C:\Arquivos de Programa (x86)\Ragnarok`
    :   É altamente recomendável você NÃO atualizar o jogo no meio de uma manutenção.
    :   Atente-se às notícias de manutenções extraordinárias no [site oficial](https://ro.gnjoylatam.com/pt/news/notice).

## Site

### 429 Too Many Requests

1. Esse erro acontece quando o site está recebendo muitos acessos.
2. Aguarde alguns minutos e tente atualizar a página novamente.

### Domínio de E-mail

1. Ao se cadastrar no jogo, a mensagem aparece: *Não é possível se cadastrar com esse domínio de e-mail*.
2. Ela surge quando você está tentando criar uma conta com um serviço de e-mail bloqueado para criação.

## Game Guard

### An illegal program has been detected

1. Acesse a pasta onde o jogo está instalado no seu computador.
2. Procure pelo arquivo RagnarokKR.ini.
3. Delete esse arquivo (RagnarokKR.ini).
4. Baixe o novo arquivo de configuração:
5. [Clique aqui](https://ro1patch.gnjoylatam.com/LIVE/rolatam/ROLatam_ini.zip) para baixar o arquivo ROLatam.ini (formato ZIP)
6. Extraia o conteúdo do arquivo ZIP.
7. Coloque o arquivo ROLatam.ini extraído na pasta de instalação do Ragnarok, substituindo o antigo RagnarokKR.ini.

## OTP

### TokenAgency

Está sendo investigado e a equipe está focada em retomar o acesso o mais rápido possível para todos que estão enfrentando esse problema.

### FAIL TO RECOGNIZING OTP(500) [9191]

O erro 500 [9101] pode aparecer nas seguintes situações:

1. O código de verificação OTP não foi inserido.
2. Um caractere não numérico foi digitado no campo do código.
3. O código OTP inserido está incorreto.

O OTP deve ser registrado com o mesmo endereço de e-mail usado para fazer login.

Por exemplo:

:   briansong@xxxx.com
:   BRIANSONG@xxxx.com

O login da GnJoy LATAM trata esses exemplos como a mesma conta, mas o sistema OTP os considera contas diferentes, podendo enviar códigos distintos para cada uma.

Certifique-se de usar a mesma grafia exata do e-mail ao fazer login e registrar o OTP.

## Jogo

### Erro do Sistema

1. A seguinte mensagem aparece: *A execução de código não pode continuar porque MSVCP140\_ATOMIC\_WAIT.dll não foi encontrado*.
2. É só instalar a versão mais recente do Pacote Redistribuível do Microsoft Visual C++.
3. Use o site oficial da Microsoft para fazer o download seguro.

### NO MSG 22

1. Este erro geralmente aparece após períodos de manutenção do servidor.
2. É importante observar que este problema deve ser resolvido assim que o servidor retornar à capacidade operacional mais próxima de 100%.
3. Se você estiver enfrentando este problema, pedimos que seja paciente e aguarde mais alguns minutos antes de tentar fazer login novamente.

### Cannot find File: sprite

1. É altamente recomendável você NÃO atualizar o jogo durante uma manutenção.
2. Aguarde o anúncio do fim da manutenção do jogo oficialmente.
3. Feche completamente o jogo e reinicie o computador.
4. Na barra de pesquisa do windows, digite `cmd` e dê enter.
5. Na janela, digite `ipconfig/flushdns` e dê enter.
6. Feche a janela e tente realizar o patch normalmente.
7. Caso o problema persista, tente reinstalar o jogo.

### Cannot init d3d OR grf file has problem

1. Esse erro possui 3 soluções documentadas:
   1. Experimente atualizar os drivers da placa de vídeo e de áudio do seu computador.
   2. Instale ou atualize uma versão atualizada do [DirectX](https://www.microsoft.com/pt-br/download/details.aspx?id=35).
   3. Na pasta onde o jogo está instalado, renomeie o arquivo `dbghelp.dll` para `dbghelp_old.dll`.
2. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### Ragnarok MFC has stopped working

1. Reinstale seu jogo.
2. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### Rag.exe - Ponto de entrada não encontrado

1. Vá para onde a pasta do jogo está instalada no seu computador.
2. Renomeie o arquivo `dbghelp.dll` para `dbghelp_old.dll`.
3. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### Rag.exe não está respondendo

1. Esse erro acontece quando algum programa está aberto e causando conflito com o seu jogo.
2. Alguns exemplos são determinados antivírus e os softwares da logitech ou razer.
3. Tente reinstalar o jogo.
4. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### Gravity(tm) Error Handler

1. Esse erro não possui uma solução padrão.
2. É necessário enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### attempt to call an nil value

1. Reinstale seu jogo.
2. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### table index is nil

1. Reinstale seu jogo.
2. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### Tela branca

1. Abra o `Setup.exe` do jogo.
2. Na aba "System", procure pela linha *Config. Gráfica* e clique no menu logo abaixo.
3. Selecione a placa gráfica que seu computador usa como padrão.
4. Pressione OK para confirmar as alterações.
5. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

### Screenshot distorcida

1. Esse erro acontece quando a resolução do seu jogo é maior que resolução do seu computador.
2. Abra o Setup.exe do jogo e selecione a dimensão da tela igual ou inferior à resolução do seu windows.
3. Pressione OK para confirmar as alterações.

## Conexão

### O servidor ainda reconhece seu último log-in

1. Esse erro acontece quando você erra sua senha 1 vez e tenta acessar de novo com a senha correta.
2. Você precisa aguardar pelo menos 5 segundos após a primeira tentativa.

### Não foi possível conectar-se ao servidor

1. Verifique se o jogo está em Manutenção nas notícias do [site oficial](https://ro.gnjoylatam.com/pt/news/notice).
2. Confira nas redes sociais da empresa (Discord, Facebook, Fórum, etc...) se não há um aviso de instabilidades ou de quedas repentinas dos servidores.

### Falha na transferência do arquivo

1. Feche o patch cliente e tente novamente.
2. Se o problema persistir, experimente reiniciar o computador.
3. Caso persista, digite `cmd` na barra de pesquisas do windows e presisone enter.
4. Na janela, digite `ipconfig/flushdns` e dê enter.
5. Feche a janela e tente realizar o patch normalmente.
6. Em alguns casos, recomenda-se fazer a instalação manual do arquivo com erro.

### Falha ao tentar conexão com o servidor de Patch

1. Feche o patch cliente e tente novamente.
2. Se o problema persistir, experimente reiniciar o computador.
3. Caso persista, digite `cmd` na barra de pesquisas do windows e presisone enter.
4. Na janela, digite `ipconfig/flushdns` e dê enter.
5. Feche a janela e tente realizar o patch normalmente.

### Falha ao escrever o arquivo

1. Reinstale seu jogo.
2. Caso o problema persista, você precisará enviar um ticket para a Central de Suporte para ter orientação mais precisa.

| *[Ragnarök Online](Ragnar%C3%B6k%20Online.md "Ragnarök Online")* | | |
| --- | --- | --- |
| Início | [Servidores](Ragnar%C3%B6k%20Online.md#Servidores "Ragnarök Online") · [Episódios](Epis%C3%B3dios.md "Episódios") · [Game Master](Game%20Master.md "Game Master") · [Glossário](Gloss%C3%A1rio.md "Glossário") · [JoyCoins](../Itens/JoyCoins.md "JoyCoins") · *Central de Suporte* · [Links](Links.md "Links") | |
| Geral | [Interface](Interface.md "Interface") · [Comandos](Comandos.md "Comandos") · [Mapas](../Lugares%20em%20Ragnar%C3%B6k/Mapas.md "Mapas") · [Negociação](Negocia%C3%A7%C3%A3o.md "Negociação") · [Quests](../Quest/Quests.md "Quests") · [Serviços](Servi%C3%A7os.md "Serviços") · [Efeitos negativos](Efeitos%20negativos.md "Efeitos negativos") |
| Sistemas | [Conquistas](Conquistas.md "Conquistas") · [RODEX](../Sem%20categoria/RODEX.md "RODEX") · [Replay](Replay.md "Replay") · [Navegação](Navega%C3%A7%C3%A3o.md "Navegação") · [Lojinha de Rua](Lojinha%20de%20Rua.md "Lojinha de Rua") · [Estilista](Estilista.md "Estilista") · [Combinação](../Itens/Combina%C3%A7%C3%A3o.md "Combinação") · [Grupo](Grupo.md "Grupo") · [Clã](../PvP/Cl%C3%A3.md "Clã") · [Reputação](Reputa%C3%A7%C3%A3o.md "Reputação") |
| Personagens | [Classes](Classes.md "Classes") (*[Builds](Guias%20de%20Classe.md "Guias de Classe")*) · [Nível](N%C3%ADvel.md "Nível") · [Drop](N%C3%ADvel.md#Drop "Nível") · [Experiência](N%C3%ADvel.md#Experiência "Nível") · [Atributos](Atributos.md "Atributos") / [Talentos](Talentos.md "Talentos") · [Habilidades](../Habilidades%20especiais/Habilidades.md "Habilidades") · [Família](Fam%C3%ADlia.md "Família") · [RolePlay](RolePlay.md "RolePlay") |
