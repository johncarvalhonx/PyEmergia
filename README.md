# Documentação Detalhada: PyEmergia

## Sumário

1.  [Introdução](#1-introdução)
2.  [Estrutura do Programa](#2-estrutura-do-programa)
3.  [Constantes e Configurações Globais](#3-constantes-e-configurações-globais)
    * [Configurações da Janela e Diretório de Dados](#31-configurações-da-janela-e-diretório-de-dados)
    * [Paleta de Cores](#32-paleta-de-cores)
    * [Definições de Fonte](#33-definições-de-fonte)
4.  [Classes Utilitárias](#4-classes-utilitárias)
    * [Classe `Tooltip`](#41-classe-tooltip)
5.  [Gerenciamento de Dados](#5-gerenciamento-de-dados)
    * [Classe `DataManager`](#51-classe-datamanager)
        * [Atributos](#511-atributos)
        * [Gerenciamento de LCI (Inventário do Ciclo de Vida)](#512-gerenciamento-de-lci-inventário-do-ciclo-de-vida)
        * [Gerenciamento de Transformidades](#513-gerenciamento-de-transformidades)
        * [Persistência de Dados](#514-persistência-de-dados)
        * [Outros Métodos](#515-outros-métodos)
6.  [Cálculo de Emergia](#6-cálculo-de-emergia)
    * [Classe `EmergyCalculator`](#61-classe-emergycalculator)
        * [Atributos](#611-atributos)
        * [Método `_get_required_transformities`](#612-método-_get_required_transformities)
        * [Método `calculate_emergy`](#613-método-calculate_emergy)
        * [Método `get_results`](#614-método-get_results)
7.  [Interface Gráfica do Usuário (GUI)](#7-interface-gráfica-do-usuário-gui)
    * [Classe `DataManagementFrame`](#71-classe-datamanagementframe)
        * [Propósito e Estrutura](#711-propósito-e-estrutura)
        * [Funcionalidades Principais](#712-funcionalidades-principais)
        * [Atualização da Interface](#713-atualização-da-interface)
    * [Classe `SimulationFrame`](#72-classe-simulationframe)
        * [Propósito e Estrutura](#721-propósito-e-estrutura)
        * [Funcionalidades Principais](#722-funcionalidades-principais)
    * [Classe `ResultsFrame`](#73-classe-resultsframe)
        * [Propósito e Estrutura](#731-propósito-e-estrutura)
        * [Funcionalidades Principais](#732-funcionalidades-principais)
    * [Classe Principal `Application`](#74-classe-principal-application)
        * [Inicialização e Configuração](#741-inicialização-e-configuração)
        * [Estilização da Interface](#742-estilização-da-interface)
        * [Gerenciamento de Abas (Frames)](#743-gerenciamento-de-abas-frames)
        * [Métodos de Atualização e Interação](#744-métodos-de-atualização-e-interação)
8.  [Ponto de Entrada da Aplicação](#8-ponto-de-entrada-da-aplicação)
9.  [Dependências](#9-dependências)

---

## 1. Introdução

O programa "Calculadora de Emergia Quântica (vEnhanced)" é uma aplicação de desktop desenvolvida em Python com a biblioteca Tkinter para a interface gráfica. Seu objetivo principal é fornecer uma ferramenta para realizar cálculos de emergia, uma métrica de avaliação ambiental que quantifica a energia solar equivalente necessária, direta ou indiretamente, para gerar um produto ou serviço.

A aplicação permite ao usuário:
* Gerenciar dados de Inventário do Ciclo de Vida (LCI).
* Gerenciar valores de transformidade (UEVs - Unit Emergy Values).
* Salvar e carregar sessões de dados.
* Executar diferentes tipos de cálculos emergéticos (Emergia Total, Soma de Inputs Diretos, Índices Emergéticos).
* Visualizar os resultados em formato textual e gráfico.

Este documento descreve em detalhes a arquitetura do programa, suas classes, métodos e funcionalidades.

---

## 2. Estrutura do Programa

O programa é modularizado em várias classes, cada uma com responsabilidades específicas:

* **Constantes e Configurações:** Define parâmetros globais como título da janela, dimensões, cores e fontes.
* **`Tooltip`:** Classe utilitária para exibir dicas de ferramenta (tooltips) em widgets da interface.
* **`DataManager`:** Responsável por gerenciar todos os dados da aplicação, incluindo a matriz LCI e os valores de transformidade. Implementa a lógica de adição, remoção, modificação, salvamento e carregamento desses dados.
* **`EmergyCalculator`:** Contém a lógica para realizar os cálculos de emergia com base nos dados fornecidos pelo `DataManager`.
* **Frames da Interface (`DataManagementFrame`, `SimulationFrame`, `ResultsFrame`):** Cada uma dessas classes representa uma aba na interface principal, organizando as funcionalidades para o usuário.
    * `DataManagementFrame`: Permite a entrada e gerenciamento de dados LCI e transformidades.
    * `SimulationFrame`: Permite a configuração e execução dos cálculos emergéticos.
    * `ResultsFrame`: Exibe os resultados dos cálculos em formato textual e gráfico.
* **`Application`:** Classe principal da interface gráfica, que herda de `tk.Tk`. É responsável por inicializar a janela, configurar estilos, criar e gerenciar as abas (notebook) e coordenar a interação entre as diferentes partes da aplicação.

O fluxo de dados geralmente ocorre da seguinte forma:
1.  O usuário insere dados LCI e transformidades através da `DataManagementFrame`, que os armazena no `DataManager`.
2.  O usuário configura um tipo de cálculo e parâmetros na `SimulationFrame`.
3.  Ao executar a simulação, a `SimulationFrame` invoca o `EmergyCalculator`, passando os dados necessários (obtidos do `DataManager`) e os parâmetros da simulação.
4.  O `EmergyCalculator` processa os dados e retorna os resultados.
5.  A `Application` atualiza a `ResultsFrame` para exibir os resultados.

---

## 3. Constantes e Configurações Globais

No início do script, são definidas diversas constantes e configurações que padronizam a aparência e o comportamento da aplicação.

### 3.1 Configurações da Janela e Diretório de Dados

* `WINDOW_TITLE`: Define o título da janela principal da aplicação.
    * **Implementação:** `WINDOW_TITLE = "Calculadora de Emergia Quântica (vEnhanced)"`
    * **Propósito:** Identificar a aplicação na barra de título da janela.
* `WINDOW_GEOMETRY`: Define as dimensões iniciais da janela principal (largura x altura).
    * **Implementação:** `WINDOW_GEOMETRY = "1350x980"`
    * **Propósito:** Estabelecer um tamanho padrão para a janela que acomode todos os elementos da interface.
* `DATA_DIR`: Especifica o nome do diretório onde os arquivos de sessão salvos pelo usuário serão armazenados.
    * **Implementação:** `DATA_DIR = "data_saved_sessions"`
    * **Propósito:** Organizar os dados salvos pelo usuário em um local específico. O script também garante que este diretório seja criado se não existir.

### 3.2 Paleta de Cores

Uma paleta de cores customizada, denominada "Elegância Tecnológica Quântica", é definida para criar uma identidade visual coesa e moderna para a aplicação.
* **Implementação:** Diversas variáveis `COLOR_*` (e.g., `COLOR_BACKGROUND_DEEP_SPACE`, `COLOR_ACCENT_CYAN_ELECTRIC`).
* **Propósito:** Padronizar as cores usadas em fundos, textos, acentos, bordas e tooltips, garantindo uma estética consistente e agradável. As cores escolhidas buscam um tema escuro ("deep space", "panel") com acentos vibrantes ("cyan electric", "magenta neon") para destaque.

### 3.3 Definições de Fonte

São definidas famílias de fontes e tamanhos para diferentes elementos textuais da interface.
* **Implementação:** Variáveis `FONT_FAMILY_*` (e.g., `FONT_FAMILY_TITLES`, `FONT_FAMILY_BODY`) e `FONT_SIZE_*` (e.g., `FONT_SIZE_NORMAL`, `FONT_SIZE_LARGE`).
* **Propósito:** Garantir a legibilidade e uma hierarquia visual clara através da tipografia. São definidas fontes primárias (`Cerdion`, `Elsone`) e fallbacks (`Segoe UI`, `Helvetica`) caso as primárias não estejam disponíveis no sistema do usuário. Os tamanhos padronizam a apresentação do texto em diferentes contextos (títulos, corpo de texto, tooltips, etc.).

---

## 4. Classes Utilitárias

### 4.1 Classe `Tooltip`

Esta classe é responsável por criar e gerenciar janelas de dica de ferramenta (tooltips) que aparecem quando o cursor do mouse passa sobre um widget.

* **`__init__(self, widget, text, app_font_body)`**
    * **Propósito:** Inicializar o tooltip, associando-o a um widget específico e definindo o texto da dica.
    * **Implementação:** Armazena o widget, o texto da dica e a fonte do corpo da aplicação. Vincula os eventos `<Enter>`, `<Leave>` e `<ButtonPress>` do widget aos métodos `show_tip` e `hide_tip`.
* **`show_tip(self, event=None)`**
    * **Propósito:** Exibir a janela do tooltip.
    * **Implementação:** Se não houver um tooltip já visível e o texto da dica não for vazio, cria uma nova janela `tk.Toplevel` sem decorações de janela (`wm_overrideredirect(True)`). Posiciona o tooltip próximo ao widget. Um `ttk.Frame` e um `ttk.Label` são usados dentro do `Toplevel` para exibir o texto da dica com o estilo e fonte apropriados.
* **`hide_tip(self, event=None)`**
    * **Propósito:** Ocultar e destruir a janela do tooltip.
    * **Implementação:** Se um tooltip estiver visível, destrói a janela `Toplevel` e redefine `self.tooltip_window` para `None`.

---

## 5. Gerenciamento de Dados

### 5.1 Classe `DataManager`

Esta classe centraliza todo o gerenciamento de dados da aplicação, incluindo a matriz de Inventário do Ciclo de Vida (LCI) e os valores de transformidade. Utiliza a biblioteca Pandas para manipulação eficiente de dados tabulares.

#### 5.1.1 Atributos

* `self.lci_df`: Um DataFrame do Pandas que armazena a matriz LCI. As linhas representam os fluxos de entrada e as colunas representam os processos ou produtos.
* `self.transformities`: Um dicionário que armazena os valores de transformidade. As chaves são os nomes dos fluxos e os valores são dicionários contendo o valor (`'value'`) e a unidade (`'unit'`) da transformidade.
* `self.lci_units`: Um dicionário que armazena as unidades para cada fluxo de entrada (linhas) e processo/produto (colunas) da matriz LCI.

#### 5.1.2 Gerenciamento de LCI (Inventário do Ciclo de Vida)

* **`add_lci_input_flow(self, flow_name, unit="")`**
    * **Propósito:** Adicionar um novo fluxo de entrada (linha) à matriz LCI.
    * **Implementação:** Verifica se o nome do fluxo é válido e se já não existe. Se for um novo fluxo, adiciona uma nova linha ao DataFrame `lci_df`, preenchida com `np.nan`. A unidade do fluxo é armazenada em `lci_units`. Exibe mensagens de erro ou aviso conforme necessário.
* **`add_lci_process_column(self, process_name, unit="")`**
    * **Propósito:** Adicionar um novo processo ou produto (coluna) à matriz LCI.
    * **Implementação:** Verifica se o nome do processo é válido e se já não existe. Se for um novo processo, adiciona uma nova coluna ao DataFrame `lci_df`, preenchida com `np.nan`. A unidade do processo é armazenada em `lci_units`.
* **`set_lci_value(self, flow_name, process_name, value_str)`**
    * **Propósito:** Definir o valor na célula da matriz LCI correspondente a um fluxo e um processo específicos.
    * **Implementação:** Converte `value_str` para float e o atribui à célula `(flow_name, process_name)` no `lci_df`. Realiza validações para garantir que o fluxo e o processo existam e que o valor seja numérico.
* **`remove_lci_input_flow(self, flow_name)`**
    * **Propósito:** Remover um fluxo de entrada (linha) da matriz LCI.
    * **Implementação:** Remove a linha correspondente do `lci_df` e a entrada associada de `lci_units`.
* **`remove_lci_process_column(self, process_name)`**
    * **Propósito:** Remover um processo ou produto (coluna) da matriz LCI.
    * **Implementação:** Remove a coluna correspondente do `lci_df` e a entrada associada de `lci_units`.
* **`get_lci_dataframe(self)`**
    * **Propósito:** Retornar uma cópia do DataFrame LCI.
    * **Implementação:** Retorna `self.lci_df.copy()` para evitar modificações externas diretas.
* **`get_lci_matrix_for_calc(self)`**
    * **Propósito:** Retornar a matriz LCI como um array NumPy, com valores `NaN` preenchidos com 0, para uso nos cálculos.
    * **Implementação:** Retorna `self.lci_df.fillna(0).values`.
* **`get_lci_process_names_for_calc(self)`**
    * **Propósito:** Retornar os nomes das colunas (processos) e linhas (fluxos) da LCI.
    * **Implementação:** Retorna um dicionário com as listas de nomes.
* **`get_lci_unit(self, name)`**
    * **Propósito:** Obter a unidade de um fluxo ou processo específico.
    * **Implementação:** Retorna a unidade de `self.lci_units` ou uma string vazia se não encontrada.

#### 5.1.3 Gerenciamento de Transformidades

* **`add_transformity(self, flow_name, value_str, unit_str="sej/unidade_original")`**
    * **Propósito:** Adicionar ou atualizar um valor de transformidade para um fluxo específico.
    * **Implementação:** Converte `value_str` para float e armazena o valor e a unidade em `self.transformities` usando `flow_name` como chave. Valida se o nome do fluxo e o valor são válidos.
* **`remove_transformity(self, flow_name)`**
    * **Propósito:** Remover um valor de transformidade.
    * **Implementação:** Remove a entrada correspondente de `self.transformities`.
* **`get_transformity(self, flow_name)`**
    * **Propósito:** Obter o valor numérico de uma transformidade para um fluxo.
    * **Implementação:** Retorna o valor da transformidade ou `None` se não encontrada.
* **`get_transformity_with_unit(self, flow_name)`**
    * **Propósito:** Obter o valor e a unidade de uma transformidade para um fluxo.
    * **Implementação:** Retorna o dicionário `{'value': ..., 'unit': ...}` ou `None`.
* **`get_all_transformities(self)`**
    * **Propósito:** Retornar uma cópia de todos os dados de transformidade.
    * **Implementação:** Retorna `self.transformities.copy()`.

#### 5.1.4 Persistência de Dados

* **`save_data_to_json(self, filepath)`**
    * **Propósito:** Salvar todos os dados da sessão atual (LCI, unidades LCI e transformidades) em um arquivo JSON.
    * **Implementação:** Constrói um dicionário com os dados (convertendo o DataFrame LCI para formato `split` para serialização JSON) e o salva no `filepath` especificado. Exibe mensagens de sucesso ou erro.
* **`load_data_from_json(self, filepath)`**
    * **Propósito:** Carregar dados de uma sessão previamente salva de um arquivo JSON.
    * **Implementação:** Lê o arquivo JSON, reconstrói o DataFrame LCI a partir do formato `split` e carrega as unidades LCI e as transformidades. Exibe mensagens de sucesso ou erro. Valida a estrutura dos dados carregados.

#### 5.1.5 Outros Métodos

* **`clear_all_data(self)`**
    * **Propósito:** Limpar todos os dados de LCI e transformidades armazenados.
    * **Implementação:** Reinicializa `self.lci_df` para um DataFrame vazio e `self.transformities` e `self.lci_units` para dicionários vazios.

---

## 6. Cálculo de Emergia

### 6.1 Classe `EmergyCalculator`

Esta classe encapsula a lógica para realizar os diferentes tipos de cálculos de emergia. Ela depende do `DataManager` para obter os dados de entrada necessários.

#### 6.1.1 Atributos

* `self.data_manager`: Uma instância da classe `DataManager`, fornecendo acesso aos dados LCI e de transformidade.
* `self.results`: Um dicionário para armazenar os resultados do último cálculo realizado.

#### 6.1.2 Método `_get_required_transformities(self, input_flow_names, parameters)`

* **Propósito:** Obter os valores de transformidade necessários para um cálculo. Prioriza valores fornecidos manualmente através do dicionário `parameters` e, em seguida, busca na tabela de transformidades gerenciada pelo `DataManager`.
* **Implementação:**
    1.  Itera sobre os `input_flow_names` (nomes dos fluxos de entrada da LCI).
    2.  Para cada nome de fluxo, verifica se uma transformidade manual foi fornecida em `parameters` (com uma chave no formato `transformity_NomeDoFluxo`).
    3.  Se encontrada e válida (numérica), usa esse valor.
    4.  Caso contrário, tenta obter a transformidade do `DataManager`.
    5.  Se nenhuma transformidade for encontrada para um fluxo necessário, registra-o como ausente.
    6.  Reporta erros se valores manuais forem inválidos ou se transformidades obrigatórias estiverem ausentes.
    7.  Retorna um dicionário com os valores de transformidade (`final_tf`) ou `None` em caso de erro crítico.

#### 6.1.3 Método `calculate_emergy(self, parameters=None)`

* **Propósito:** Realizar o cálculo de emergia com base no tipo de cálculo especificado em `parameters` e nos dados disponíveis.
* **Implementação:**
    * Obtém o `calculation_type` de `parameters` (padrão: `"direct_inputs_sum"`).
    * Inicializa `self.results` e um resumo do cálculo (`msg_res`).
    * **Tipo de Cálculo `"total_emergy"`:**
        1.  Obtém a matriz LCI (`lci_mat`) e os nomes dos fluxos/processos do `DataManager`.
        2.  Verifica se os dados LCI são válidos.
        3.  Chama `_get_required_transformities` para obter o vetor de transformidades (`tf_vec`) alinhado com os fluxos de entrada da LCI.
        4.  Se a LCI ou as transformidades estiverem vazias, trata os casos de emergias zeradas.
        5.  Verifica a compatibilidade dimensional entre a LCI e o vetor de transformidades.
        6.  Calcula a emergia por fluxo de entrada para cada processo: `em_vals_in = lci_mat * tf_vec[:, np.newaxis]` (multiplicação elemento a elemento, onde `tf_vec` é transmitido pelas colunas).
        7.  Calcula a emergia total por processo: `total_em_proc = np.sum(em_vals_in, axis=0)`.
        8.  Armazena os resultados (`emergy_per_input_flow_for_each_process` e `total_emergy_per_process`) em `self.results` como DataFrames/Series do Pandas.
    * **Tipo de Cálculo `"direct_inputs_sum"`:**
        1.  Obtém a matriz LCI e os nomes dos processos.
        2.  Se a LCI estiver vazia, a soma é zero.
        3.  Calcula a soma dos inputs diretos para cada processo: `total_in_proc = np.sum(lci_mat, axis=0)`.
        4.  Armazena o resultado (`sum_of_direct_inputs_per_process`) em `self.results`.
    * **Tipo de Cálculo `"emergy_indices"`:**
        1.  Obtém os valores agregados de emergia Renovável (R), Não Renovável (N) e Comprada (F) de `parameters`. Valida se são numéricos e não negativos.
        2.  Obtém o Yield (Y) de `parameters`. Se não fornecido, calcula como `Y = R + N + F`. Valida Y.
        3.  Calcula os índices:
            * **EYR (Emergy Yield Ratio):** `Y / F`. Lida com `F = 0`.
            * **ELR (Environmental Loading Ratio):** `(N + F) / R`. Lida com `R = 0`.
            * **ESI (Emergy Sustainability Index):** `EYR / ELR`. Lida com `ELR = 0` ou valores `NaN`/`inf`.
        4.  Armazena os índices formatados em `self.results`.
        5.  Adiciona interpretações básicas dos índices ao resumo.
    * Se o tipo de cálculo não for implementado, registra uma mensagem.
    * Armazena o `msg_res` (resumo do cálculo) em `self.results["calculation_summary"]`.
    * Retorna `True` em caso de sucesso, `False` em caso de erro que impeça o cálculo.

#### 6.1.4 Método `get_results(self)`

* **Propósito:** Retornar os resultados do último cálculo.
* **Implementação:** Retorna o dicionário `self.results`.

---

## 7. Interface Gráfica do Usuário (GUI)

A interface gráfica é construída usando Tkinter e o módulo `ttk` para widgets temáticos. A aplicação é organizada em abas (usando `ttk.Notebook`).

### 7.1 Classe `DataManagementFrame(ttk.Frame)`

Esta classe representa a aba "Gerenciamento de Dados", onde o usuário pode inserir, visualizar e modificar os dados da Matriz LCI e da Tabela de Transformidades.

#### 7.1.1 Propósito e Estrutura

* **Propósito:** Fornecer uma interface intuitiva para a entrada e gerenciamento dos dados base para os cálculos de emergia.
* **Estrutura:**
    * Utiliza um `tk.Canvas` com uma `ttk.Scrollbar` para permitir a rolagem do conteúdo caso ele exceda o tamanho da aba.
    * Contém seções distintas (LabelFrames) para:
        * **Controles Gerais:** Botões para salvar e carregar dados da sessão.
        * **Matriz LCI:** Botões para adicionar/remover processos (colunas) e fluxos (linhas), definir valores LCI, e um `ttk.Treeview` para exibir a matriz.
        * **Tabela de Transformidades:** Botões para adicionar/editar e remover transformidades, e um `ttk.Treeview` para exibir a tabela.
    * Um botão para limpar todos os dados manuais.
    * Labels instrutivas guiam o usuário.

#### 7.1.2 Funcionalidades Principais (Métodos de Callback)

* **`save_session_data(self)`:** Abre um diálogo para o usuário escolher o local e nome do arquivo para salvar os dados da sessão (LCI e transformidades) via `DataManager`.
* **`load_session_data(self)`:** Abre um diálogo para o usuário selecionar um arquivo JSON de sessão para carregar os dados via `DataManager`. Após o carregamento, atualiza as exibições na interface.
* **`add_lci_flow(self)`:** Solicita ao usuário o nome e a unidade (opcional) de um novo fluxo de entrada LCI através de `simpledialog.askstring`. Chama `DataManager.add_lci_input_flow` e atualiza a exibição.
* **`add_lci_process(self)`:** Similar ao `add_lci_flow`, mas para adicionar um novo processo/produto (coluna) LCI.
* **`set_lci_value_dialog(self)`:** Solicita ao usuário o nome do fluxo, nome do processo e o valor numérico para preencher uma célula da matriz LCI. Chama `DataManager.set_lci_value`.
* **`remove_lci_flow_dialog(self)`:** Solicita o nome de um fluxo de entrada para remover da LCI, com confirmação.
* **`remove_lci_process_by_name(self)`:** Solicita o nome de um processo/produto para remover da LCI, com confirmação.
* **`add_edit_transformity(self)`:** Solicita o nome do fluxo, o valor da transformidade e sua unidade. Se a transformidade já existir, preenche os diálogos com os valores atuais para edição. Chama `DataManager.add_transformity`.
* **`remove_transformity_dialog(self)`:** Solicita o nome de um fluxo para remover sua transformidade, com confirmação.
* **`clear_all_manual_data(self)`:** Pede confirmação e, se positivo, chama `DataManager.clear_all_data` para limpar todos os dados de LCI e transformidades, atualizando as exibições.

#### 7.1.3 Atualização da Interface

* **`update_lci_button_states(self)`:** Habilita ou desabilita os botões de manipulação da LCI com base no estado atual da matriz LCI (e.g., não se pode adicionar um fluxo se não houver processos).
* **`refresh_lci_display(self)`:** Limpa e recarrega o `ttk.Treeview` da LCI com os dados atuais do `DataManager.lci_df`. Formata os nomes das colunas e linhas para incluir suas unidades. Os valores numéricos são formatados em notação científica.
* **`refresh_transformity_display(self)`:** Limpa e recarrega o `ttk.Treeview` das transformidades com os dados atuais do `DataManager.transformities`.

### 7.2 Classe `SimulationFrame(ttk.Frame)`

Representa a aba "Simulação Emergética", onde o usuário seleciona o tipo de análise, configura parâmetros e executa os cálculos.

#### 7.2.1 Propósito e Estrutura

* **Propósito:** Permitir a configuração e execução dos cálculos de emergia.
* **Estrutura:**
    * Um `ttk.Combobox` para selecionar o tipo de cálculo (`total_emergy`, `direct_inputs_sum`, `emergy_indices`).
    * Um `ttk.LabelFrame` para "Parâmetros para Índices Emergéticos" (R, N, F, Y), que é exibido condicionalmente se o tipo de cálculo for "emergy_indices". Contém `ttk.Entry` para cada parâmetro.
    * Um `ttk.LabelFrame` para "Parâmetros Adicionais", com um `ttk.Entry` onde o usuário pode fornecer transformidades manuais (que sobrescrevem as da tabela) ou outros parâmetros chave-valor.
    * Um botão "Executar Cálculo".
    * Um botão "Ajuda: Tipos de Cálculos e Parâmetros" que abre uma janela informativa.
    * Um `ttk.Label` de status (`self.status_label`) para fornecer feedback ao usuário sobre a prontidão para o cálculo.

#### 7.2.2 Funcionalidades Principais

* **`on_calc_type_change(self, event=None)`:** Chamado quando o tipo de cálculo é alterado no combobox. Mostra ou oculta o frame de parâmetros para índices emergéticos conforme necessário. Atualiza o label de status.
* **`update_status(self)`:** Verifica a disponibilidade de dados LCI e transformidades no `DataManager` e o tipo de cálculo selecionado para atualizar a mensagem no `self.status_label`, informando ao usuário se está pronto para calcular ou se dados/parâmetros são necessários.
* **`run_simulation(self)`:**
    1.  Obtém o tipo de cálculo selecionado.
    2.  Valida se dados LCI existem, se necessário para o tipo de cálculo.
    3.  Constrói um dicionário `sim_params` com `calculation_type`.
    4.  Processa a string de "Parâmetros Adicionais": divide por `;`, depois por `=`, converte valores para float se possível, e adiciona ao `sim_params`.
    5.  Se o cálculo for de "emergy_indices", coleta os valores dos campos R, N, F, Y, valida-os e os adiciona ao `sim_params`.
    6.  Chama `self.controller.emergy_calculator.calculate_emergy(parameters=sim_params)`.
    7.  Se o cálculo for bem-sucedido, exibe uma mensagem de sucesso e chama `self.controller.update_results_display()` para atualizar a aba de resultados.

### 7.3 Classe `ResultsFrame(ttk.Frame)`

Representa a aba "Resultados e Gráficos", onde os resultados dos cálculos são exibidos.

#### 7.3.1 Propósito e Estrutura

* **Propósito:** Apresentar os resultados dos cálculos de emergia de forma clara, tanto textualmente quanto graficamente.
* **Estrutura:**
    * Dividida em duas seções principais (LabelFrames):
        * **Resultados Textuais:** Um `tk.Text` widget (somente leitura) para exibir um resumo do cálculo e tabelas detalhadas dos resultados. Inclui uma barra de rolagem. Um botão "Exportar Texto" permite salvar o conteúdo.
        * **Visualização Gráfica:** Um `ttk.Frame` (`self.chart_frame`) para exibir um gráfico de pizza (usando Matplotlib) mostrando a contribuição de emergia de cada fluxo de entrada para um processo/produto selecionado. Um `ttk.Combobox` (`self.chart_data_selector`) permite ao usuário escolher qual processo/produto visualizar no gráfico.

#### 7.3.2 Funcionalidades Principais

* **`display_results_and_chart(self, results_data)`:**
    * **Propósito:** Atualizar a exibição dos resultados textuais e o gráfico.
    * **Implementação:**
        1.  Limpa o widget `tk.Text`.
        2.  Extrai o "calculation_summary" de `results_data` e o insere no widget de texto com formatação especial.
        3.  Itera sobre os demais itens em `results_data` (que geralmente são DataFrames ou Series do Pandas), formata-os como string (usando `.to_string()` com formatação de float) e os insere no widget de texto, precedidos por um título.
        4.  Configura tags no `tk.Text` para aplicar estilos (fonte, cor, espaçamento) aos cabeçalhos e ao corpo do texto.
        5.  Chama `populate_chart_selector` para atualizar as opções do combobox do gráfico.
        6.  Chama `update_pie_chart` para redesenhar o gráfico com base nos novos resultados.
* **`populate_chart_selector(self, results_data)`:**
    * **Propósito:** Preencher o `ttk.Combobox` com os nomes dos processos/produtos para os quais um gráfico de contribuição de emergia pode ser gerado (tipicamente, as colunas do resultado `total_emergy_per_process`).
    * **Implementação:** Se `results_data` contiver `total_emergy_per_process` (uma Series do Pandas), usa seu índice (nomes dos processos) como opções para o combobox. Seleciona a primeira opção válida por padrão.
* **`update_pie_chart_from_event(self, event=None)`:** Método de conveniência para ser usado como callback do evento `<<ComboboxSelected>>` do seletor de gráfico, chamando `update_pie_chart()`.
* **`update_pie_chart(self, original_results_data=None)`:**
    * **Propósito:** Gerar e exibir um gráfico de pizza das contribuições de emergia para o processo/produto selecionado.
    * **Implementação:**
        1.  Limpa qualquer gráfico anterior do `self.chart_frame`.
        2.  Obtém os resultados atuais (do argumento ou do `EmergyCalculator`).
        3.  Verifica se os dados necessários para o gráfico existem (`emergy_per_input_flow_for_each_process` DataFrame) e se um processo válido foi selecionado.
        4.  Extrai os dados de contribuição para o processo selecionado, filtrando valores muito pequenos ou zero.
        5.  Se não houver dados significativos, exibe uma mensagem.
        6.  Cria uma `matplotlib.figure.Figure` e um `Axes` (subplot).
        7.  Usa `ax.pie()` para desenhar o gráfico de pizza com os dados, rótulos (nomes dos fluxos de entrada), porcentagens automáticas (`autopct`), cores e estilos. As fontes e cores são customizadas para combinar com o tema da aplicação.
        8.  Adiciona uma legenda se o número de fatias for pequeno.
        9.  Usa `FigureCanvasTkAgg` para embutir a figura Matplotlib no frame Tkinter.
* **`export_results(self)`:**
    * **Propósito:** Salvar o conteúdo do widget de resultados textuais em um arquivo de texto.
    * **Implementação:** Obtém todo o texto do `tk.Text`. Se houver conteúdo, abre um diálogo `filedialog.asksaveasfilename` para o usuário escolher o nome e local do arquivo. Salva o texto no arquivo, prefixado com um cabeçalho informativo.

### 7.4 Classe Principal `Application(tk.Tk)`

Esta é a classe raiz da interface gráfica, orquestrando todos os outros componentes visuais e a lógica de interação.

#### 7.4.1 Inicialização e Configuração

* **`__init__(self, data_manager, emer_calc)`:**
    * **Propósito:** Inicializar a janela principal da aplicação.
    * **Implementação:**
        * Chama `super().__init__()`.
        * Tenta carregar as fontes definidas (`FONT_FAMILY_TITLES`, `FONT_FAMILY_BODY`). Se não encontradas, usa as fontes fallback. As fontes efetivamente carregadas são armazenadas em `self.APP_FONT_TITLES` e `self.APP_FONT_BODY`.
        * Armazena as instâncias de `DataManager` e `EmergyCalculator`.
        * Define o título (`WINDOW_TITLE`) e a geometria (`WINDOW_GEOMETRY`) da janela.
        * Configura a cor de fundo principal (`COLOR_BACKGROUND_DEEP_SPACE`).
        * Inicializa e aplica os estilos `ttk` (detalhado abaixo).
        * Cria o `ttk.Notebook` e adiciona as instâncias das classes de frame (`DataManagementFrame`, `SimulationFrame`, `ResultsFrame`) como abas.

#### 7.4.2 Estilização da Interface

Uma parte significativa do construtor `Application` é dedicada à configuração de estilos `ttk` para customizar a aparência dos widgets.
* **Implementação:**
    * `self.style = ttk.Style(self)`: Obtém o objeto de estilo.
    * `self.style.theme_use('clam')`: Define um tema base que permite mais customização.
    * Uma série de chamadas `self.style.configure()` e `self.style.map()` são usadas para definir propriedades (cor de fundo, cor de primeiro plano, fonte, borda, padding, etc.) para diferentes tipos de widgets (`TFrame`, `TLabel`, `TButton`, `TNotebook`, `TCombobox`, `Treeview`, `TLabelFrame`, `TEntry`, `TScrollbar`) e seus estados (normal, ativo, focado, hover, pressionado).
    * Estilos específicos são criados, como `Title.TLabel`, `Header.TLabel`, `Primary.TButton`, `Tooltip.TFrame`, `Quantum.Vertical.TScrollbar`, para aplicar formatação distinta a elementos chave.
* **Propósito:** Criar uma interface visualmente coesa e atraente, alinhada com a paleta de cores "Elegância Tecnológica Quântica" e as definições de fonte. Isso substitui a aparência padrão dos widgets Tkinter/ttk.

#### 7.4.3 Gerenciamento de Abas (Frames)

* **Implementação:**
    * Um `ttk.Frame` (`container`) é criado para conter o `ttk.Notebook`.
    * Um `ttk.Notebook` é instanciado.
    * Um dicionário `tab_names` mapeia nomes de abas para as classes de frame correspondentes.
    * O código itera sobre `tab_names`, instancia cada classe de frame (passando `notebook` como pai e `self` como `controller`) e adiciona o frame ao notebook usando `notebook.add()`.
    * As instâncias dos frames são armazenadas em `self.frames` para referência futura.
* **Propósito:** Organizar a interface em seções lógicas (abas), tornando a navegação e o uso mais fáceis para o usuário. O `controller` (a instância de `Application`) é passado para os frames para que eles possam interagir com outras partes da aplicação (e.g., `DataManager`, `EmergyCalculator`, outros frames).

#### 7.4.4 Métodos de Atualização e Interação

* **`update_results_display(self)`:** Chamado após um cálculo bem-sucedido. Obtém a instância de `ResultsFrame` de `self.frames` e chama seu método `display_results_and_chart`, passando os resultados do `EmergyCalculator`.
* **`update_data_display(self)`:** Chamado quando os dados no `DataManager` são alterados (e.g., após carregar uma sessão, adicionar/remover um fluxo). Atualiza as exibições na `DataManagementFrame` (LCI e tabelas de transformidade) e o status na `SimulationFrame`.
* **`show_calculation_types_window(self)`:** Cria e exibe uma nova janela `tk.Toplevel` contendo informações detalhadas sobre os tipos de cálculos suportados, como fornecer parâmetros e exemplos.
    * **Implementação:** A janela é modal (`transient`, `grab_set`). Seu conteúdo é formatado usando `tk.Text` com tags para estilização, explicando cada tipo de cálculo.
    * **Propósito:** Fornecer ajuda contextual ao usuário sobre como usar as funcionalidades de simulação.

---

## 8. Ponto de Entrada da Aplicação

O bloco `if __name__ == "__main__":` é o ponto de entrada quando o script é executado diretamente.

* **Implementação:**
    1.  Cria uma instância de `DataManager`.
    2.  Cria uma instância de `EmergyCalculator`, passando o `DataManager`.
    3.  Cria uma instância da `Application`, passando o `DataManager` e o `EmergyCalculator`.
    4.  Chama `app.mainloop()` para iniciar o loop de eventos Tkinter, tornando a interface gráfica visível e interativa.
* **Propósito:** Inicializar os componentes principais da aplicação e iniciar a interface gráfica.

---

## 9. Dependências

O programa requer as seguintes bibliotecas Python:

* **tkinter:** (Geralmente incluído na instalação padrão do Python) Para a interface gráfica do usuário.
    * `tkinter.ttk`: Para widgets temáticos.
    * `tkinter.filedialog`: Para diálogos de abrir/salvar arquivo.
    * `tkinter.messagebox`: Para caixas de mensagem padrão.
    * `tkinter.font`: Para manipulação de fontes.
    * `tkinter.simpledialog`: Para diálogos simples de entrada de dados.
* **pandas:** Para manipulação de dados tabulares (matriz LCI).
* **numpy:** Para operações numéricas, especialmente com arrays (usado internamente pelo Pandas e nos cálculos).
* **matplotlib:** Para a geração de gráficos (gráfico de pizza na aba de resultados).
    * `matplotlib.figure.Figure`
    * `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`
    * `matplotlib.pyplot` (usado para `get_cmap`)
    * `matplotlib.font_manager.FontProperties`
* **os:** Para interações com o sistema operacional (verificar/criar diretório de dados).
* **json:** Para salvar e carregar dados da sessão em formato JSON.
* **datetime:** Para gerar timestamps para nomes de arquivos de sessão e exportação.

É recomendado instalar `pandas`, `numpy` e `matplotlib` se não estiverem presentes no ambiente Python:
```bash
pip install pandas numpy matplotlib
