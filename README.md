# ⚛️ PyEmergia ⚛️

Desenvolvido por **João Pedro Villas Boas de Carvalho**

Uma aplicação de desktop com interface gráfica (GUI) construída em Python para realizar análises de emergia. Este programa permite o gerenciamento detalhado de dados de Inventário do Ciclo de Vida (LCI), o manejo de Transformidades (Unit Emergy Values - UEVs), a execução de diversos cálculos emergéticos e a visualização e exportação dos resultados.

**IMPORTANTE**

Este é um projeto abrangente, desenvolvido para fins acadêmicos ou pessoais. Ele possui uma gama significativa de funcionalidades e uma interface gráfica elaborada. Fique à vontade para explorar, modificar e utilizar o código conforme suas necessidades!

---

## 🔧 Funcionalidades Principais

O sistema é organizado em abas para facilitar a navegação e o uso:

### Aba: Gerenciamento de Dados
- **Matriz LCI (Inventário do Ciclo de Vida):**
    - ✅ Adicionar, remover e editar Processos/Produtos (colunas da matriz).
    - ✅ Adicionar, remover e editar Fluxos de Entrada (linhas da matriz).
    - ✅ Definir valores quantitativos para cada célula da matriz LCI.
    - ✅ Especificar unidades para fluxos e processos.
- **Tabela de Transformidades (UEVs):**
    - ✅ Criar, editar e remover entradas na tabela de transformidades.
    - ✅ Especificar unidades para as transformidades (ex: sej/J, sej/g).
- **Persistência de Dados:**
    - ✅ Salvar a sessão de trabalho atual (dados LCI, unidades, transformidades) em um arquivo JSON.
    - ✅ Carregar uma sessão de trabalho a partir de um arquivo JSON previamente salvo.
- **Limpeza de Dados:**
    - ✅ Opção para remover todos os dados inseridos manualmente (LCI e transformidades).

### Aba: Simulação Emergética
- **Seleção de Tipo de Análise:**
    - ✅ Calcular **Emergia Total por Processo**.
    - ✅ Calcular **Soma dos Inputs Diretos** (quantidades físicas).
    - ✅ Calcular **Índices Emergéticos** (EYR, ELR, ESI).
- **Parâmetros de Cálculo:**
    - ✅ Inserir valores agregados de emergia (R, N, F, Y) para o cálculo de índices.
    - ✅ Fornecer transformidades manuais que podem sobrescrever os valores da tabela para cálculos específicos.
- **Execução e Ajuda:**
    - ✅ Botão para executar o cálculo selecionado.
    - ✅ Janela de ajuda detalhando os tipos de cálculo e os parâmetros necessários.

### Aba: Resultados e Gráficos
- **Apresentação de Resultados:**
    - ✅ Exibição textual detalhada dos sumários e resultados dos cálculos.
    - ✅ Opção para exportar os resultados textuais para um arquivo `.txt`.
- **Visualização Gráfica:**
    - ✅ Geração de gráfico de pizza para visualizar a contribuição percentual de cada fluxo de entrada para a emergia total de um processo/produto selecionado (aplicável ao cálculo de "Emergia Total").
    - ✅ Seletor de processo para o gráfico de pizza.

### Funcionalidades Gerais da UI
- ✅ Interface gráfica organizada em abas intuitivas.
- ✅ Tooltips (dicas de ferramenta) informativas para botões e campos.
- ✅ Feedback ao usuário através de labels de status e caixas de diálogo.
- ✅ Hook global de exceções para melhor tratamento de erros inesperados.
- ✅ Paleta de cores e fontes customizadas para uma experiência visual coesa (com fallbacks para fontes padrão).

---

## 🚀 Tecnologias Utilizadas

- **Linguagem Principal:** Python 3.x
- **Interface Gráfica (GUI):** `tkinter` (com o módulo `ttk` para widgets temáticos)
- **Manipulação de Dados Tabulares:** `pandas`
- **Operações Numéricas:** `numpy`
- **Geração de Gráficos:** `matplotlib`
- **Serialização de Dados:** `json` (para salvar e carregar sessões)
- **Módulos Padrão:** `os`, `datetime`, `enum`, `sys`, `traceback`

---

## ⚙️ Configuração e Uso

### 🔹 Passo 1: Pré-requisitos

- Garanta que você tem o **Python 3** instalado (preferencialmente 3.7 ou superior).
- O `pip` (gerenciador de pacotes do Python) é necessário para instalar as dependências.

### 🔹 Passo 2: Obter o Código

- Faça o download ou clone o arquivo Python (`.py`) contendo o script para um diretório em seu computador.

### 🔹 Passo 3: Instalar Dependências

1.  Navegue até o diretório onde você salvou o script usando seu terminal ou prompt de comando:
    ```bash
    cd /caminho/para/o/diretorio/do/script
    ```
2.  Instale as bibliotecas Python necessárias:
    ```bash
    pip install pandas numpy matplotlib
    ```
    * `tkinter` geralmente já vem incluído na instalação padrão do Python. Se não, pode ser necessário instalá-lo separadamente dependendo do seu sistema operacional e da forma como o Python foi instalado (ex: `sudo apt-get install python3-tk` em sistemas Debian/Ubuntu).

### 🔹 Passo 4: (Opcional) Instalar Fontes Customizadas

- O programa tenta utilizar as fontes "Cerdion" para títulos e "Elsone" para o corpo do texto.
- Se estas fontes não estiverem instaladas em seu sistema, o programa utilizará fontes de fallback como "Segoe UI" ou "Helvetica".
- Para a experiência visual pretendida, você pode procurar e instalar estas fontes ("Cerdion", "Elsone") no seu sistema operacional.

### 🔹 Passo 5: Executar o Script

- Execute o programa a partir do seu terminal:
    ```bash
    python PyEmergia.py
    ```

- A aplicação criará automaticamente um diretório chamado `data_saved_sessions` no mesmo local do script, se ele não existir. Este diretório é usado para armazenar os arquivos de sessão salvos.

### 🔹 Passo 6: Interagir com a Aplicação

- A interface gráfica principal será aberta, apresentando três abas:
    1.  **Gerenciamento de Dados:** Para inserir, editar, carregar e salvar seus dados de LCI e transformidades.
    2.  **Simulação Emergética:** Para configurar e executar os cálculos emergéticos.
    3.  **Resultados e Gráficos:** Para visualizar e exportar os resultados dos cálculos.
- Utilize os botões, campos de entrada e menus de seleção dentro de cada aba para interagir com a calculadora.
- Tooltips (dicas) aparecerão ao pairar o mouse sobre muitos elementos da interface, fornecendo informações adicionais.

---

## 🌐 Acessando as Funcionalidades

- **Aba "Gerenciamento de Dados":**
    - Use os botões numerados "1. Novo Processo", "2. Novo Fluxo", "3. Definir Valor LCI" para construir sua matriz.
    - Adicione/edite transformidades na seção correspondente.
    - Salve sua sessão usando "Salvar Dados da Sessão" para continuar o trabalho posteriormente ou carregue uma sessão existente com "Carregar Dados da Sessão".
- **Aba "Simulação Emergética":**
    - Selecione o tipo de análise desejado no menu dropdown.
    - Se estiver calculando "Índices Emergéticos", preencha os campos R, N, F (e Y, opcionalmente).
    - Para o cálculo de "Emergia Total", você pode fornecer transformidades manuais no campo "Parâmetros Adicionais" para sobrescrever valores da tabela (formato: `transformity_NomeDoFluxo=ValorNumerico`).
    - Clique em "Executar Cálculo".
- **Aba "Resultados e Gráficos":**
    - Os resultados textuais do último cálculo serão exibidos. Use "Exportar Texto" para salvá-los.
    - Se você executou o cálculo de "Emergia Total por Processo", um gráfico de pizza será gerado. Use o menu dropdown para selecionar qual processo/produto visualizar.

---

## 🧠 Limitações e Possíveis Melhorias Futuras

- 🎨 **Disponibilidade de Fontes:** A experiência visual ideal depende da instalação das fontes customizadas ("Cerdion", "Elsone"). Sem elas, fontes de fallback são usadas.
- 💻 **Compatibilidade Visual entre SOs:** Interfaces Tkinter podem ter pequenas variações visuais ou de comportamento entre diferentes sistemas operacionais.
- 📊 **Validação Avançada de Dados:** Embora haja validação para entradas numéricas, validações mais complexas (ex: consistência de unidades entre LCI e transformidades) não são implementadas.
- 🧪 **Testes Automatizados:** A adição de um framework de testes (ex: `unittest` ou `pytest`) poderia melhorar a robustez e facilitar futuras modificações.
- 📦 **Empacotamento:** Para facilitar a distribuição, o script poderia ser empacotado em um executável standalone (ex: usando `PyInstaller` ou `cx_Freeze`).
- 📈 **Opções de Gráficos:** Expandir as opções de visualização gráfica (ex: gráficos de barras para comparar processos, séries temporais se aplicável).
- 🌐 **Internacionalização (i18n):** Adaptar a interface para múltiplos idiomas.

---

## 👨‍💻 Autor

**João Pedro Villas Boas de Carvalho**
