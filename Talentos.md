---
title: "Talentos"
source: https://browiki.org/wiki/Talentos
namespace: 0
revision: 46329
retrieved: 2026-06-23T21:03:27Z
categories:
  - "Informações básicas"
---

# Talentos

![Poder](images/2/2f/Poder.png)

![Criatividade](images/5/58/Criatividade.png)

![Sabedoria](images/1/10/Sabedoria.png)

![Stamina](images/8/8d/Stamina.png)

Talentos são características adquiridas quando seu personagem atinge a **[Classe](Classe.md "Classe") 4**.

A partir do nível 201, seu personagem deixa de receber pontos de [atributos](Atributos.md "Atributos") e passa a ganhar pontos de talento.

A janela de Talentos pode ser aberta pelo [comando](Comando.md "Comando") `Alt + A` e selecionar "*Talentos*".

![Traitwnd](images/4/41/Traitwnd.png)

- Os talentos não podem passar de 100 pontos.
- Ao mudar para [Classe](Classe.md "Classe") 4, você já recebe 7 pontos para distribuir.
- A cada 1 nível de base, você recebe 3 pontos de talentos.
- A cada 5 níveis de base, você recebe +4 pontos.

Para saber como investir esses pontos ou resetá-los, **[veja no guia abaixo](#Investimento)**.

## AP

Ponto de Atividade (**AP**) é uma mecânica exclusiva das [Classes](Classes.md "Classes") 4.

Geralmente, existem duas habilidades "*supremas*" que consomem a maior parte dos seus AP.

A quantidade máxima de AP que você pode acumular é 200, independentemente da classe.

Ao morrer em qualquer mapa ou entrar em um mapa [PvP](PvP.md "PvP") ou [GdE](GdE.md "GdE"), você perde todos os seus AP.

![APinterface](images/a/a3/APinterface.png)

## Talentos Primários

### Poder

Poder (**POD**) é uma característica voltada para classes físicas.

Ele influencia apenas em danos físicos causados.

- A cada 1 ponto:
  - [ATQ](ATQ.md "ATQ") de atributo +5.
  - Duração de [Letargia](Letargia.md "Letargia") -0,08 segundos.
- A cada 3 pontos:
  - [P.ATQ](P.ATQ.md "P.ATQ") +1.

### Stamina

Stamina (**STA**) influencia na sua resiliência, melhorando sua duração na batalha.

- A cada 1 ponto:
  - [TEN](TEN.md "TEN") +1.
  - Duração de [Escuridão](Escuridão.md "Escuridão") e [Intoxicação](Intoxicação.md "Intoxicação") -0,08 segundos.
- A cada 3 pontos:
  - [TEN](TEN.md "TEN") +5.

### Sabedoria

Sabedoria (**SAB**) também aumenta sua resiliência, mas voltado para danos mágicos recebidos.

Se você busca resistência em combate, também é importante investir nesse talento.

- A cada 1 ponto:
  - [TENM](TENM.md "TENM") +1.
  - Duração de [Tristeza](Tristeza.md "Tristeza") e [Eletrificação](Eletrificação.md "Eletrificação") -0,08 segundos.
- A cada 3 pontos:
  - [TENM](TENM.md "TENM") +5.

### Feitiço

Feitiço (**FEI**) é o principal talento das classes mágicas.

Aumenta os danos mágicos causados.

- A cada 1 ponto:
  - [ATQM](ATQM.md "ATQM") +5.
  - Duração de [Quietude](Quietude.md "Quietude") e [Ardência](Ardência.md "Ardência") -0,08 segundos.
- A cada 3 pontos:
  - [S.ATQM](S.ATQM.md "S.ATQM") +1.

### Concentração

Concentração (**CON**) surge como um talento coringa, usado para classes híbridas ou que dependam mais do acerto do que do crítico.

- A cada 1 ponto:
  - [Esquiva](Esquiva.md "Esquiva") +2.
  - [Precisão](Precisão.md "Precisão") +2.
- A cada 5 pontos:
  - [P.ATQ](P.ATQ.md "P.ATQ") +1.
  - [S.ATQM](S.ATQM.md "S.ATQM") +1.

### Criatividade

Criatividade (**CRV**) é uma característica usada por classes específicas, como aquelas voltadas para dano crítico ou para suporte.

- A cada 1 ponto:
  - [C.Mais](C.Mais.md "C.Mais") +1.
  - [Precisão](Precisão.md "Precisão") +2.
  - Duração de [Concretação](Concretação.md "Concretação"), [Azar](Azar.md "Azar") e [Esfriamento](Esfriamento.md "Esfriamento") -0,08 segundos.
  - Aumenta a chance de criação de [Manipular Poção](Manipular Poção.md "Manipular Poção") e [Criar Máquina](Criar Máquina.md "Criar Máquina").
  - Influencia nas chances de [Remoção Sombria Total](Remoção Sombria Total.md "Remoção Sombria Total").

## Talentos Secundários

### Poder de Ataque

Diferente do [ATQ](ATQ.md "ATQ"), o Poder de Ataque (**P.ATQ**) afeta diretamente o dano físico causado.

Ele aumenta o *Status ATQ* e o *Equip ATQ* em valores porcentuais (%).

- Exemplo:
  - 10 de P.ATQ significa um aumento de 10% no *Status ATQ*, indo de 200 para 220.

### Super Ataque Mágico

O Super Ataque Mágico (**S.ATQM**) afeta o dano mágico causado de forma direta.

Ele aumenta o *Status ATQM* e o *Equip ATQM* em valores porcentuais (%).

- Exemplo:
  - 10 de S.ATQM significa um aumento de 10% no *Status ATQM*, indo de 3.000 para 3.300.

### Tenacidade

Antes de calcular a [Defesa Física](DEF.md "DEF"), a Tenacidade (**TEN**) reduz o dano físico normal recebido em valores porcentuais (%).

O `Dano físico final × [{(TEN do Alvo ÷ (TEN do Alvo + 400)) × 80} ÷ 100]` é subtraído do dano físico final.

A redução é limitada em 50%, ou seja, você não pode ter mais que 50% de TEN.

### Tenacidade Mágica

Antes de calcular a [Defesa Mágica](DEFM.md "DEFM"), a Tenacidade Mágica (**TENM**) reduz o dano mágico normal recebido em valores porcentuais (%).

O `Dano mágico final × [{(TENM do Alvo ÷ (TENM do Alvo + 400)) × 80} ÷ 100]` é subtraído do dano mágico final.

A redução é limitada em 50%, ou seja, você não pode ter mais que 50% de TEN.

### Cura Mais

Cura Mais (**C.Mais**) aumenta a efetividade de cura final em valores porcentuais (%).

Esse aumento é aplicado após os efeitos normais de aumento da efetividade de cura.

- Exemplo:
  - Você usa uma [habilidade](Habilidade.md "Habilidade") de regeneração, que cura 20.000 de [HP](HP.md "HP").
  - Se você possuir 20 de C.Mais, cura 24.000 de [HP](HP.md "HP")
  - Ou seja, aumentou em 20% o valor da cura.

A cada 100 pontos, aumenta a área de efeito da habilidade [Mediale Votum](Mediale Votum.md "Mediale Votum").

### Taxa de Dano Crítico

A Taxa de Dano Crítico (**T.CRIT**) aumenta a porcentagem de dano crítico em %.

- Exemplo:
  - Com 0 de T.CRIT, um ataque crítico causa 40% a mais de dano.
  - Com 10 de T.CRIT, o ataque crítico aumenta de 40% para 50%.

Esse efeito não está relacionado ao aumento de *dano crítico* dos [itens](Itens.md "Itens")/[equipamentos](Equipamentos.md "Equipamentos"), é uma nova variável.

## Investimento

Diferente dos [atributos](Atributos.md "Atributos"), o custo para investir em cada talento sempre será de 1 ponto.

Isso torna o sistema mais intuitivo para o usuário, deixando mais fácil a sua distribuição.

Pontos ganhos

|  |  |
| --- | --- |
| A cada 1 nível | 3 Pontos |
| A cada 5 níveis | 7 Pontos |
| Total (nv. 250) | 197 Pontos |

### Reset

- Você pode resetar seus talentos das seguintes formas:
  - [Poção Menos](https://www.divine-pride.net/database/item/consumable?Name=Po%C3%A7%C3%A3o+Menos&Description=&function=&find=Busca%7C)
  - [Sino de Mordomo](https://www.divine-pride.net/database/search?q=Sino+Prateado)
- **Dica:** Após resetar, você pode redistribuir seus atributos mais rápido usando comandos de texto
  - Exemplo: para aumentar o Poder digite `/pow+ número`
  - Cada talento tem um comando de texto específico listado na página [Comandos](Comandos.md#Texto "Comandos").
  - Todo personagem começa com os talentos no 0, se quiser 50 de poder, precisará digitar: /pow+ 50

| *[Ragnarök Online](Ragnarök Online.md "Ragnarök Online")* | | |
| --- | --- | --- |
| Início | [Servidores](Ragnarök Online.md#Servidores "Ragnarök Online") · [Episódios](Episódios.md "Episódios") · [Game Master](Game Master.md "Game Master") · [Glossário](Glossário.md "Glossário") · [JoyCoins](JoyCoins.md "JoyCoins") · *[Central de Suporte](Central de Suporte.md "Central de Suporte")* · [Links](Links.md "Links") | |
| Geral | [Interface](Interface.md "Interface") · [Comandos](Comandos.md "Comandos") · [Mapas](Mapas.md "Mapas") · [Negociação](Negociação.md "Negociação") · [Quests](Quests.md "Quests") · [Serviços](Serviços.md "Serviços") · [Efeitos negativos](Efeitos negativos.md "Efeitos negativos") |
| Sistemas | [Conquistas](Conquistas.md "Conquistas") · [RODEX](RODEX.md "RODEX") · [Replay](Replay.md "Replay") · [Navegação](Navegação.md "Navegação") · [Lojinha de Rua](Lojinha de Rua.md "Lojinha de Rua") · [Estilista](Estilista.md "Estilista") · [Combinação](Combinação.md "Combinação") · [Grupo](Grupo.md "Grupo") · [Clã](Clã.md "Clã") · [Reputação](Reputação.md "Reputação") |
| Personagens | [Classes](Classes.md "Classes") (*[Builds](Guias de Classe.md "Guias de Classe")*) · [Nível](Nível.md "Nível") · [Drop](Nível.md#Drop "Nível") · [Experiência](Nível.md#Experiência "Nível") · [Atributos](Atributos.md "Atributos") / Talentos · [Habilidades](Habilidades.md "Habilidades") · [Família](Família.md "Família") · [RolePlay](RolePlay.md "RolePlay") |
