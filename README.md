# ANALISE DA BASE DE DADOS SRAG 2023 DO OPEN DATA SUS

## CONTEXTUALIZAÇÃO

<div style="text-align: justify">

A vigilância da Síndrome Respiratória Aguda Grave (SRAG) no Brasil 
foi estruturada pelo Ministério da Saúde a partir da pandemia de Influenza 
A(H1N1) em 2009, integrando-se à rede já existente de monitoramento da Síndrome
Gripal (SG). A rede foi então expandida em 2020 para incorporar o acompanhamento 
do novo coronavírus (SARS-CoV-2) durante a pandemia de COVID-19, criando um sistema
unificado de acompanhamento das síndromes respiratórias graves. 

Os dados são dinâmicos e estão sujeitos a alterações decorrentes da investigação, 
ou mesmo correções de erros de digitação, pelas equipes de vigilância epidemiológica 
que desenvolvem o serviço nas três esferas de gestão. A análise contemplará apenas um 
recorte específico dos dados, restrita ao período de 2023, selecionado com base em 
diretrizes previamente estabelecidas.

</div>

## OBJETIVOS

<div style="text-align: justify">
O objetivo desta análise é avaliar a base de dados de Síndrome Respiratória Aguda 
Grave do ano de 2023 disponível em 
https://opendatasus.saude.gov.br/dataset/srag-2021-a-2024. O estudo busca identificar 
padrões, fatores de risco e tendências epidemiológicas, gerando subsídios para 
decisões em saúde pública, direcionamento de recursos e fortalecimento de medidas de 
prevenção e controle.
</div>

## ANÁLISE DESCRITIVA E EXPLORATÓRIA DOS DADOS

<div style="text-align: justify">
Os dados são referentes a duzentos e setenta e nove mil e quatrocentos e cinquenta
e três notificações de casos de síndromes respiratórias graves, sendo esses casos 
categorizados em Síndrome Gripal (SG), Síndrome Respiratória Aguda Grave UTI (SRAG-UTI) 
e Síndrome Respiratória Aguda Grave - Hospitalizado (SRAG-Hospitalizado).


Na etapa inicial de tratamento dos dados, foi conduzida uma análise exploratória 
com foco na avaliação da proporção dos valores nulos por variável. 
Foi identificado que do total de 194 variáveis, 7 apresentavam 100% de ausência de registros 
e foram excluídas. A base de dados resultante passou a contar com 187 variáveis válidas. 
A segunda análise considerou a exclusão de variáveis com mais de 60% de valores nulos, 
aplicando critérios adicionais como:


- variáveis que não estavam descritas no dicionário de dados;
- variáveis que eram relevantes somente para uma subpopulação específica;
- variáveis categóricas com distribuição extremamente desbalanceadas.

Essa estratégia buscou assegurar maior consistência, relevância analítica e robustez dos 
dados para as etapas subsequentes de processamento e modelagem. Após essas exclusões, a base 
final de trabalho passou a contar com 86 variáveis válidas.

Seguindo o raciocínio apresentado nos dados faltantes, outros quatro campos foram 
desconsiderados da análise por não constarem no dicionário de dados, sendo incerta a sua 
pertinência para o estudo.
</div>



