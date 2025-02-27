# Projeto Diques

Repositório contendo scripts, para modelagem e inversão magnética 2D de diques finos.
**Tipo de projeto:** Cooperação internacional  

**Autor:** Felipe Lisbona Cavalcante    
**Atribuição:** Coorientação  

**Instituição de pesquisa responsável:** Instituto de Astronomia, Geofísica e Ciências Atmosféricas (IAG) - USP  
**Supervisor:** Carlos Alberto Mendonça

**Instituição de pesquisa parceira:** Queen's University Belfast (QUB)  
**Projeto de pesquisa associado:** GEMINI  
**Supervisor:** Ulrich S. Ofterdinger  

**Pesquisadora Iniciação Científica:** Olga Mayumi Moreira Hanazumi

## Índice

- [Objetivos](#objetivos)
- [Conteúdo do Repositório](#conteúdo-do-repositório)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Especificações Técnicas Utilizadas](#especificações-técnicas-utilizadas)
- [Instruções de Uso](#instruções-de-uso)
- [Licença](#licença)

## Objetivos

- Realizar modelagem e inversão magnética 2D de diques dinos.
- Analisar a viabilidade do uso das ferramentas nos basaltos da província de Antrim na Irlanda do Norte.
- Identificar diques com potencial contribuição associada à energia geotérmica.
- Alvos iniciais são diques intrudindo o aquífero Sherwood.

## Conteúdo do Repositório

Este repositório contém os arquivos necessários para a reprodução dos resultados obtidos nesta pesquisa. O conteúdo está organizado em pastas que contêm:

- **Scripts:** utilizados para a modelagem do problema direto, processamento, inversões e análise de dados.

## Estrutura de Pastas

A organização deste repositório segue a estrutura abaixo:

```plaintext
Projeto_Diques/
├── README.md                    # Este arquivo
├── config_env.txt               # Arquivo de configuração do ambiente virtual
├── fwd/
│   ├── Input/
│   │   └── (arquivos de entrada para executar o problema direto)
│   ├── Output/
│   │   └── (arquivos de saída do problema direto)
│   ├── 1_PyDyke_Extent_n_Disturb.py (arquivo para execução do problema direto)
│   ├── 2_PyDyke_cut_data.py (arquivo para recortar os dados)
│   ├── func_*.py (arquivos contendo funções para execução do problema direto)
├── inv/
│   ├── Input/
│   │   └── (arquivos de entrada para executar o problema inverso)
│   ├── Output/
│   │   └── (arquivos de saída do problema inverso)
│   ├── 1_PyDyke_simple_filt.py (arquivo para filtrar dados)
│   ├── 2_PyDyke_d2T.py (arquivo para calcular a derivada segunda dos dados)
│   ├── 3_PyDyke_lims.py (arquivo para definir limites do modelo)
│   ├── 4_PyDyke_calc_initial.py (arquivo para calcular a solução inicial do problema)
│   ├── 5_PyDyke_inv.py (arquivo para executar o problema inverso)
│   ├── 6_PyDyke_plot.py (arquivo para plotar os resultados do problema inverso)
│   ├── 7_PyDyke_STD.py (arquivo para plotar calcular o desvio padrão das soluções)
│   ├── 8_PyDyke_join_exit_std.py (arquivo para compilar soluções e probabilidades em tabela)
│   ├── func_*.py (arquivos contendo funções para execução do problema inverso)
```


## Especificações Técnicas Utilizadas

Códigos originais e testes desenvolvidos em um notebook com as seguintes especificações:

- **Processador:** Intel Core i5 de 12ª geração (3,3 GHz)
- **Memória:** 16 GB de RAM DDR4 (3200 MHz)
- **Sistema Operacional:** Ubuntu 24.04

Os seguintes softwares e linguagens de programação foram utilizados:

### Ambiente Python
- Python 3.7.16

## Instruções de Uso

O correto funcionamento dos programas dependem da instalação das bibliotecas e pacotes necessários. 
Isso pode ser facilmente resolvido em sistemas baseados em Linux através de 4 etapas: 
  1. Criar um ambiente virtual com Conda utilizando o comando: ```conda create --name nome_do_ambiente python=3.7.16```
  2. Ativar o ambiente virtual com o comando: ```conda activate nome_do_ambiente```
  3. Baixar o arquivo config_env.txt.
  4. Executar o comando XXX---XXX

Com o ambiente virtual configurado, os códigos Python podem ser executados com comandos do tipo ```python 1_exemplo.py```, ou utilizando botões da sua IDE favorita. A ordem para a execução dos códigos segue a numeração arábica crescente do prefixo dos arquivos ".py".
