import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkFont, simpledialog
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from enum import Enum, auto
import sys # Utilizado para o hook global de exceções
import traceback # Utilizado para formatar as informações de traceback das exceções

# ==============================================================================
# CALCULADORA DE EMERGIA QUÂNTICA (pyEmergia)
# ==============================================================================
#
# Este script implementa uma aplicação de interface gráfica (GUI) para
# realizar cálculos de análise de emergia.
#
# Funcionalidades Principais:
#
# 1.  Gerenciamento de Dados de Inventário do Ciclo de Vida (LCI):
#     - Adição, remoção e edição de Processos/Produtos (colunas da matriz LCI).
#     - Adição, remoção e edição de Fluxos de Entrada (linhas da matriz LCI).
#     - Definição de valores quantitativos na matriz LCI.
#     - Especificação de unidades para fluxos e processos.
#
# 2.  Gerenciamento de Transformidades (Unit Emergy Values - UEVs):
#     - Criação, edição e remoção de entradas na tabela de transformidades.
#     - Especificação de unidades para as transformidades (ex: sej/J, sej/g).
#
# 3.  Persistência de Dados:
#     - Funcionalidade para salvar a sessão de trabalho atual (dados LCI,
#       unidades, transformidades) em um arquivo JSON.
#     - Funcionalidade para carregar uma sessão de trabalho a partir de um
#       arquivo JSON previamente salvo.
#
# 4.  Limpeza de Dados:
#     - Opção para remover todos os dados inseridos manualmente (LCI e transformidades).
#
# 5.  Cálculos Emergéticos:
#     - Cálculo da Emergia Total por Processo: Baseado nos fluxos da LCI e
#       nas respectivas transformidades.
#     - Soma dos Inputs Diretos: Agregação das quantidades físicas dos fluxos
#       de entrada por processo, sem aplicar transformidades.
#     - Cálculo de Índices Emergéticos: Inclui EYR (Emergy Yield Ratio),
#       ELR (Environmental Loading Ratio) e ESI (Emergy Sustainability Index),
#       a partir de valores agregados de emergia (R, N, F, Y).
#     - Suporte para transformidades manuais durante o cálculo de "Emergia Total",
#       com prioridade sobre os valores da tabela.
#
# 6.  Apresentação de Resultados:
#     - Exibição textual detalhada dos sumários e resultados dos cálculos.
#     - Funcionalidade para exportar os resultados textuais para um arquivo .txt.
#     - Geração de gráfico de pizza para visualização da contribuição percentual
#       de cada fluxo de entrada para a emergia total de um processo/produto selecionado
#       (aplicável ao cálculo de "Emergia Total").
#
# 7.  Interface do Usuário (UI):
#     - Organização em abas para separação lógica das funcionalidades.
#     - Tooltips informativas para botões e campos.
#     - Janela de ajuda detalhando os tipos de cálculo e parâmetros.
#     - Feedback ao usuário através de labels de status e caixas de diálogo.
#
# Arquitetura e Tecnologias:
# - Linguagem: Python
# - Interface Gráfica: Tkinter com o módulo ttk para widgets temáticos.
# - Manipulação de Dados Tabulares: Biblioteca Pandas.
# - Geração de Gráficos: Biblioteca Matplotlib.
# - Estrutura do Código: Orientada a objetos, com classes para gerenciamento
#   de dados, cálculos, e componentes da interface gráfica.
#
# ==============================================================================


# --- Constantes e Configurações Globais ---
WINDOW_TITLE = "Calculadora de Emergia Quântica"
WINDOW_GEOMETRY = "1350x980" # Dimensões iniciais da janela
DATA_DIR = "data_saved_sessions" # Diretório para salvar/carregar sessões

# --- Paleta de Cores ---
# Define o esquema de cores utilizado na aplicação.
COLOR_BACKGROUND_DEEP_SPACE = "#030812"
COLOR_BACKGROUND_PANEL = "#0A1931"
COLOR_BACKGROUND_PANEL_LIGHTER = "#102A43"
COLOR_BACKGROUND_GLASS_EFFECT = "#18244A"
COLOR_ACCENT_CYAN_ELECTRIC = "#0ECCED"
COLOR_ACCENT_MAGENTA_NEON = "#FF00FF"

COLOR_TEXT_PRIMARY = "#F0F0F0"
COLOR_TEXT_SECONDARY = "#B0B0B0"
COLOR_TEXT_ON_ACCENT = "#030812"

COLOR_BORDER_SUBTLE = "#2A3B5F"
COLOR_BORDER_ACTIVE = COLOR_ACCENT_CYAN_ELECTRIC
COLOR_BORDER_BUTTON_LIGHT = "#E0E0E0"

COLOR_TOOLTIP_BG = "#102A43"
COLOR_TOOLTIP_TEXT = "#0ECCED"

# --- Definições de Fonte ---
# Define as famílias de fonte primárias e de fallback.
FONT_FAMILY_TITLES = "Cerdion" 
FONT_FAMILY_BODY = "Elsone"   
FONT_FAMILY_FALLBACK_SANS = "Segoe UI" 
FONT_FAMILY_FALLBACK_GENERIC = "Helvetica" 

# Define tamanhos de fonte padronizados para consistência.
FONT_SIZE_XXSMALL = 8
FONT_SIZE_XSMALL = 9
FONT_SIZE_SMALL = 10
FONT_SIZE_NORMAL = 11 
FONT_SIZE_MEDIUM = 12
FONT_SIZE_LARGE = 16
FONT_SIZE_XLARGE = 18
FONT_SIZE_XXLARGE = 24

# --- Hook Global de Exceções ---
# Configura um manipulador global para exceções não tratadas,
# visando apresentar erros de forma mais controlada ao usuário e facilitar a depuração.
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Manipula exceções não capturadas, exibindo uma messagebox de erro
    e registrando o traceback completo no console.
    """
    error_message_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    user_friendly_message = (f"Ocorreu um erro inesperado na aplicação:\n\n"
                             f"Tipo de Erro: {exc_type.__name__}\n"
                             f"Mensagem: {exc_value}\n\n"
                             "Consulte o console para obter detalhes técnicos completos do erro.\n"
                             "Se o problema persistir, considere reportar o erro com os detalhes do console.")
    
    sys.stderr.write("--- ERRO GLOBAL NÃO TRATADO ---\n")
    sys.stderr.write(error_message_details)
    sys.stderr.write("--- FIM DO RELATÓRIO DE ERRO GLOBAL ---\n")
    
    try:
        if tk._default_root and tk._default_root.winfo_exists(): 
            messagebox.showerror("Erro Crítico na Aplicação", user_friendly_message)
        else: 
            print("ERRO CRÍTICO (GUI não disponível para exibir messagebox):")
            print(user_friendly_message.replace("\n\nConsulte o console para obter detalhes técnicos completos do erro.", "")) 
            print("\nDETALHES TÉCNICOS COMPLETOS:")
            print(error_message_details)
    except Exception as e_handler:
        print("ERRO AO TENTAR EXIBIR O ERRO CRÍTICO:", e_handler)
        print("DETALHES DO ERRO ORIGINAL:")
        print(error_message_details)

# Atribui a função como o manipulador padrão de exceções.
sys.excepthook = global_exception_handler


# --- Enumeração para Tipos de Cálculo ---
class CalculationType(Enum):
    """Define os tipos de cálculo de emergia suportados pela aplicação."""
    TOTAL_EMERGY = "total_emergy"
    DIRECT_INPUTS_SUM = "direct_inputs_sum"
    EMERGY_INDICES = "emergy_indices"

    @classmethod
    def get_display_names_map(cls) -> dict:
        """Retorna um dicionário que mapeia membros do Enum para seus nomes de exibição na UI."""
        return {
            cls.TOTAL_EMERGY: "Emergia Total por Processo",
            cls.DIRECT_INPUTS_SUM: "Soma dos Inputs Diretos",
            cls.EMERGY_INDICES: "Índices Emergéticos (EYR, ELR, ESI)"
        }

    @classmethod
    def from_display_name(cls, display_name: str):
        """Converte um nome de exibição da UI de volta para o membro do Enum correspondente."""
        for member, name_str in cls.get_display_names_map().items():
            if name_str == display_name:
                return member
        print(f"AVISO: Nome de exibição '{display_name}' não encontrado no Enum CalculationType.")
        return None 

    @classmethod
    def get_default(cls):
        """Retorna o tipo de cálculo padrão a ser selecionado na inicialização."""
        return cls.TOTAL_EMERGY

    @classmethod
    def get_all_display_names(cls) -> list[str]:
        """Retorna uma lista de todos os nomes de exibição para popular widgets como Comboboxes."""
        return list(cls.get_display_names_map().values())


# --- Criação do Diretório de Dados ---
# Garante a existência do diretório onde os dados da sessão serão salvos.
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
        print(f"Info: Diretório de dados '{DATA_DIR}' criado com sucesso.")
    except OSError as e:
        print(f"Erro Crítico: Não foi possível criar o diretório de dados '{DATA_DIR}'. Detalhes: {e}")
        messagebox.showerror("Erro de Inicialização", f"Não foi possível criar o diretório de dados necessário: {DATA_DIR}\nVerifique as permissões ou crie o diretório manualmente.\n\nDetalhes: {e}")


# --- Classes Auxiliares ---
class Tooltip:
    """
    Implementa a funcionalidade de tooltip (dica de ferramenta) para widgets Tkinter.
    Exibe uma pequena janela com texto informativo quando o cursor do mouse
    permanece sobre o widget associado.
    """
    def __init__(self, widget, text: str, app_font_body: str):
        self.widget = widget # O widget ao qual a tooltip será anexada.
        self.text = text    # O texto a ser exibido na tooltip.
        self.app_font_body = app_font_body # A família de fonte padrão para o corpo do texto da aplicação.
        self.tooltip_window = None # Referência à janela Toplevel da tooltip (inicialmente None).
        
        # Associa eventos de mouse para mostrar e esconder a tooltip.
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Exibe a janela da tooltip próximo ao widget."""
        # Não faz nada se uma tooltip já estiver visível ou se não houver texto.
        if self.tooltip_window or not self.text:
            return
        
        try:
            # Calcula a posição da tooltip em relação à tela.
            x, y, _, _ = self.widget.bbox("insert") # Obtém as coordenadas relativas do widget.
            x += self.widget.winfo_rootx() + 25    # Adiciona a posição da janela principal e um deslocamento.
            y += self.widget.winfo_rooty() + 25    # Deslocamento para evitar que a tooltip cubra o cursor.

            # Cria a janela Toplevel para a tooltip.
            self.tooltip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True) # Remove as decorações padrão da janela (borda, título).
            tw.wm_geometry(f"+{x}+{y}")   # Define a posição da tooltip.

            # Frame e Label para exibir o texto da tooltip, utilizando estilos definidos.
            frame = ttk.Frame(tw, style="Tooltip.TFrame", padding=1)
            frame.pack()
            label = ttk.Label(frame, text=self.text, justify='left', wraplength=380, # wraplength para quebra de linha automática.
                              font=(self.app_font_body, FONT_SIZE_SMALL), style="Tooltip.TLabel")
            label.pack(ipadx=10, ipady=6) # Padding interno para o texto.
        except tk.TclError as e:
            # Erro comum se o widget for destruído enquanto a tooltip tenta aparecer.
            print(f"Alerta (Tooltip): Falha ao exibir tooltip para {self.widget} (widget pode ter sido destruído). Erro: {e}")
        except Exception as e:
            # Captura outros erros inesperados durante a exibição da tooltip.
            print(f"Erro inesperado em Tooltip.show_tip: {e}\n{traceback.format_exc()}")


    def hide_tip(self, event=None):
        """Destrói a janela da tooltip se ela estiver visível."""
        if self.tooltip_window:
            try:
                # Verifica se a janela da tooltip ainda existe antes de tentar destruí-la.
                if self.tooltip_window.winfo_exists(): 
                    self.tooltip_window.destroy()
            except tk.TclError as e:
                # Pode ocorrer se a janela já foi destruída por outro meio.
                print(f"Alerta (Tooltip): Erro menor ao tentar ocultar tooltip (janela pode já ter sido destruída). Erro: {e}")
            except Exception as e:
                print(f"Erro inesperado em Tooltip.hide_tip: {e}\n{traceback.format_exc()}")
            finally:
                # Garante que a referência à janela da tooltip seja resetada.
                self.tooltip_window = None

class DataManager:
    """
    Responsável pelo gerenciamento centralizado dos dados da aplicação,
    incluindo a Matriz LCI, as transformidades e as unidades associadas.
    Utiliza Pandas DataFrame para a estrutura da LCI.
    """
    def __init__(self):
        # DataFrame para armazenar a Matriz de Inventário do Ciclo de Vida (LCI).
        # Linhas representam fluxos de entrada, colunas representam processos/produtos.
        # dtype=float é especificado para garantir que as colunas sejam numéricas.
        self.lci_df = pd.DataFrame(dtype=float) 
        
        # Dicionário para armazenar as transformidades (Unit Emergy Values - UEVs).
        # Formato: {'nome_do_fluxo': {'value': valor_numerico, 'unit': 'unidade_da_transformidade'}}
        self.transformities = {}  
        
        # Dicionário para armazenar as unidades dos fluxos e processos da LCI.
        # Formato: {'nome_do_fluxo_ou_processo': 'unidade_fisica'}
        self.lci_units = {}        

    def _validate_name(self, name: str, context: str) -> str | None:
        """
        Valida e normaliza um nome fornecido (para fluxo ou processo).
        Retorna o nome normalizado (sem espaços extras) ou None se inválido.
        """
        if name is None: 
            messagebox.showerror("Nome Inválido", f"O nome para '{context}' não pode ser nulo.")
            return None
        
        name_str = str(name).strip() # Converte para string e remove espaços das bordas.
        
        if not name_str: # Verifica se, após o strip, a string ficou vazia.
            messagebox.showerror("Nome Inválido", f"O nome para '{context}' não pode ser vazio ou consistir apenas de espaços.")
            return None
        return name_str # Retorna o nome validado e normalizado.

    def add_lci_input_flow(self, flow_name: str, unit: str = "") -> bool:
        """Adiciona um novo fluxo de entrada (linha) à Matriz LCI."""
        flow_name = self._validate_name(flow_name, "Fluxo de Entrada")
        if not flow_name:
            print("DEBUG DataManager: Nome de fluxo inválido, adição cancelada.")
            return False
        try:
            if flow_name in self.lci_df.index: # Verifica se o fluxo já existe.
                messagebox.showwarning("Fluxo Existente", f"O fluxo de entrada '{flow_name}' já está presente na LCI.")
                return False

            # Adiciona a nova linha. Se o DataFrame não tiver colunas,
            # a linha é criada e será preenchida com NaN quando colunas forem adicionadas.
            # Se já houver colunas, a nova linha é criada com essas colunas (valores NaN).
            if self.lci_df.columns.empty:
                self.lci_df.loc[flow_name] = pd.Series(dtype=float) # Cria a linha, pronta para receber colunas.
            else:
                # Cria uma Series de NaNs com o mesmo índice das colunas existentes.
                new_row_data = pd.Series([np.nan] * len(self.lci_df.columns), index=self.lci_df.columns, dtype=float)
                self.lci_df.loc[flow_name] = new_row_data
            
            self.lci_units[flow_name] = str(unit).strip() # Armazena a unidade do fluxo.
            
            # Log de depuração.
            print(f"DEBUG DataManager: Fluxo '{flow_name}' adicionado. DataFrame LCI atual:")
            print(self.lci_df.to_string()) # .to_string() para melhor visualização no console.
            print(f"Índice LCI: {list(self.lci_df.index)}")
            print(f"Colunas LCI: {list(self.lci_df.columns)}\n")
            return True
        except Exception as e: # Captura qualquer erro durante a operação.
            messagebox.showerror("Erro ao Adicionar Fluxo", f"Falha ao adicionar o fluxo '{flow_name}':\n{e}")
            print(f"ERRO DETALHADO em add_lci_input_flow: {e}\n{traceback.format_exc()}")
            return False


    def add_lci_process_column(self, process_name: str, unit: str = "") -> bool:
        """Adiciona uma nova coluna de processo/produto à Matriz LCI."""
        process_name = self._validate_name(process_name, "Processo/Produto")
        if not process_name:
            print("DEBUG DataManager: Nome de processo inválido, adição cancelada.")
            return False
        try:
            if process_name in self.lci_df.columns: # Verifica se o processo já existe.
                messagebox.showwarning("Processo Existente", f"O processo/produto '{process_name}' já está presente na LCI.")
                return False
            
            # Adiciona a nova coluna. Se já existirem linhas, será preenchida com NaN.
            # Se não houver linhas, a coluna é criada e será preenchida com NaN quando linhas forem adicionadas.
            if self.lci_df.index.empty: # Se não há linhas ainda.
                self.lci_df[process_name] = pd.Series(dtype=float) # Cria a coluna, pronta para receber linhas.
            else: # Se já há linhas.
                self.lci_df[process_name] = np.nan # Adiciona a coluna com NaNs.
                self.lci_df[process_name] = self.lci_df[process_name].astype(float) # Garante o tipo float.
            
            self.lci_units[process_name] = str(unit).strip() # Armazena a unidade do processo.
            
            # Log de depuração.
            print(f"DEBUG DataManager: Processo '{process_name}' adicionado. DataFrame LCI atual:")
            print(self.lci_df.to_string())
            print(f"Índice LCI: {list(self.lci_df.index)}")
            print(f"Colunas LCI: {list(self.lci_df.columns)}\n")
            return True
        except Exception as e: # Captura qualquer erro.
            messagebox.showerror("Erro ao Adicionar Processo", f"Falha ao adicionar o processo '{process_name}':\n{e}")
            print(f"ERRO DETALHADO em add_lci_process_column: {e}\n{traceback.format_exc()}")
            return False

    def set_lci_value(self, flow_name: str, process_name: str, value_str: str) -> bool:
        """Define um valor numérico na célula da LCI especificada pelo fluxo e processo."""
        flow_name = self._validate_name(flow_name, "Fluxo de Entrada")
        process_name = self._validate_name(process_name, "Processo/Produto")
        if not flow_name or not process_name:
            return False 
        try:
            # Verifica se o fluxo e o processo existem antes de tentar definir o valor.
            if flow_name not in self.lci_df.index:
                messagebox.showerror("Erro de LCI", f"Fluxo de Entrada '{flow_name}' não encontrado na LCI. Verifique o nome.")
                return False
            if process_name not in self.lci_df.columns:
                messagebox.showerror("Erro de LCI", f"Processo/Produto '{process_name}' não encontrado na LCI. Verifique o nome.")
                return False
            
            val = float(value_str) # Converte a string para float.
            self.lci_df.loc[flow_name, process_name] = val # Define o valor na célula.
            print(f"DEBUG DataManager: Valor LCI para [{flow_name}, {process_name}] definido como {val}. DataFrame LCI atual:")
            print(self.lci_df.to_string())
            return True
        except ValueError: # Erro se o valor não puder ser convertido para float.
            messagebox.showerror("Valor Inválido", f"O valor '{value_str}' fornecido para LCI não é um número válido.")
            return False
        except Exception as e: # Outros erros.
            messagebox.showerror("Erro ao Definir Valor LCI", f"Falha ao definir o valor para [{flow_name}, {process_name}]:\n{e}")
            print(f"ERRO DETALHADO em set_lci_value: {e}\n{traceback.format_exc()}")
            return False

    def remove_lci_input_flow(self, flow_name: str) -> bool:
        """Remove um fluxo de entrada (linha) da Matriz LCI."""
        flow_name = self._validate_name(flow_name, "Fluxo de Entrada")
        if not flow_name: return False
        try:
            if flow_name in self.lci_df.index:
                self.lci_df.drop(flow_name, axis=0, inplace=True) # axis=0 para remover linha.
                if flow_name in self.lci_units: # Remove a unidade associada.
                    del self.lci_units[flow_name]
                print(f"DEBUG DataManager: Fluxo '{flow_name}' removido. DataFrame LCI atual:\n{self.lci_df.to_string()}\n")
                return True
            messagebox.showwarning("Fluxo Não Encontrado", f"O fluxo de entrada '{flow_name}' não foi encontrado para remoção.")
            return False
        except Exception as e:
            messagebox.showerror("Erro ao Remover Fluxo", f"Falha ao remover o fluxo '{flow_name}':\n{e}")
            print(f"ERRO DETALHADO em remove_lci_input_flow: {e}\n{traceback.format_exc()}")
            return False

    def remove_lci_process_column(self, process_name: str) -> bool:
        """Remove um processo/produto (coluna) da Matriz LCI."""
        process_name = self._validate_name(process_name, "Processo/Produto")
        if not process_name: return False
        try:
            if process_name in self.lci_df.columns:
                self.lci_df.drop(process_name, axis=1, inplace=True) # axis=1 para remover coluna.
                if process_name in self.lci_units: # Remove a unidade associada.
                    del self.lci_units[process_name]
                print(f"DEBUG DataManager: Processo '{process_name}' removido. DataFrame LCI atual:\n{self.lci_df.to_string()}\n")
                return True
            messagebox.showwarning("Processo Não Encontrado", f"O processo/produto '{process_name}' não foi encontrado para remoção.")
            return False
        except Exception as e:
            messagebox.showerror("Erro ao Remover Processo", f"Falha ao remover o processo '{process_name}':\n{e}")
            print(f"ERRO DETALHADO em remove_lci_process_column: {e}\n{traceback.format_exc()}")
            return False

    def get_lci_dataframe(self) -> pd.DataFrame:
        """Retorna uma cópia do DataFrame LCI para evitar modificações externas diretas."""
        return self.lci_df.copy()

    def get_lci_matrix_for_calc(self) -> np.ndarray:
        """Retorna a matriz LCI como um array NumPy, preenchendo valores NaN com 0 (para cálculos)."""
        return self.lci_df.fillna(0).values

    def get_lci_names_for_calc(self) -> dict:
        """Retorna os nomes das linhas (fluxos) e colunas (processos) da LCI."""
        return {
            "columns": [str(col) for col in self.lci_df.columns],
            "rows": [str(idx) for idx in self.lci_df.index]
        }

    def get_lci_unit(self, name: str) -> str:
        """Retorna a unidade associada a um fluxo ou processo, se existir."""
        return self.lci_units.get(str(name).strip(), "") # Retorna string vazia se não encontrar.

    def add_transformity(self, flow_name: str, value_str: str, unit_str: str = "sej/unidade_original") -> bool:
        """Adiciona ou atualiza uma entrada na tabela de transformidades."""
        flow_name = self._validate_name(flow_name, "Fluxo para Transformidade")
        if not flow_name:
            return False
        
        try:
            value = float(value_str) # Converte o valor para float.
            self.transformities[flow_name] = {
                'value': value,
                'unit': str(unit_str).strip() if unit_str else "sej/unidade_original" # Unidade padrão.
            }
            print(f"DEBUG DataManager: Transformidade para '{flow_name}' adicionada/atualizada: {self.transformities[flow_name]}")
            return True
        except ValueError:
            messagebox.showerror("Valor Inválido", f"O valor da transformidade '{value_str}' deve ser um número.")
            return False
        except Exception as e:
            messagebox.showerror("Erro ao Adicionar Transformidade", f"Falha ao adicionar a transformidade para '{flow_name}':\n{e}")
            print(f"ERRO DETALHADO em add_transformity: {e}\n{traceback.format_exc()}")
            return False


    def remove_transformity(self, flow_name: str) -> bool:
        """Remove uma entrada da tabela de transformidades."""
        flow_name = self._validate_name(flow_name, "Fluxo para Transformidade")
        if not flow_name: return False
        try:
            if flow_name in self.transformities:
                del self.transformities[flow_name]
                print(f"DEBUG DataManager: Transformidade para '{flow_name}' removida.")
                return True
            messagebox.showwarning("Transformidade Não Encontrada", f"A transformidade para o fluxo '{flow_name}' não foi encontrada.")
            return False
        except Exception as e:
            messagebox.showerror("Erro ao Remover Transformidade", f"Falha ao remover a transformidade para '{flow_name}':\n{e}")
            print(f"ERRO DETALHADO em remove_transformity: {e}\n{traceback.format_exc()}")
            return False

    def get_transformity_value(self, flow_name: str) -> float | None:
        """Retorna apenas o valor numérico de uma transformidade."""
        data = self.transformities.get(str(flow_name).strip())
        return data['value'] if data else None
        
    def get_transformity_with_unit(self, flow_name: str) -> dict | None:
        """Retorna o valor e a unidade de uma transformidade."""
        return self.transformities.get(str(flow_name).strip())

    def get_all_transformities(self) -> dict:
        """Retorna uma cópia de todas as transformidades armazenadas."""
        return self.transformities.copy()

    def clear_all_data(self):
        """Limpa todos os dados armazenados (LCI, transformidades, unidades)."""
        try:
            self.lci_df = pd.DataFrame(dtype=float) # Cria um novo DataFrame vazio.
            self.transformities = {}    # Reseta os dicionários.
            self.lci_units = {}         
            print("DEBUG DataManager: Todos os dados (LCI, Transformidades, Unidades) foram limpos.") 
        except Exception as e:
            messagebox.showerror("Erro ao Limpar Dados", f"Ocorreu um erro ao tentar limpar todos os dados:\n{e}")
            print(f"ERRO DETALHADO em clear_all_data: {e}\n{traceback.format_exc()}")


    def save_data_to_json(self, filepath: str) -> bool:
        """Salva os dados da sessão atual (LCI, unidades, transformidades) em um arquivo JSON."""
        try:
            data_to_save = {
                "lci_data": self.lci_df.to_dict(orient="split"), # 'split' preserva bem a estrutura do DataFrame.
                "lci_units": self.lci_units,
                "transformities": self.transformities
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4) # indent=4 para formatação legível.
            messagebox.showinfo("Sessão Salva", f"Dados da sessão salvos com sucesso em:\n{filepath}")
            return True
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Sessão", f"Não foi possível salvar os dados da sessão.\nDetalhes: {e}")
            print(f"ERRO DETALHADO em save_data_to_json: {e}\n{traceback.format_exc()}")
            return False

    def load_data_from_json(self, filepath: str) -> bool:
        """Carrega dados de uma sessão a partir de um arquivo JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            lci_dict = loaded_data.get("lci_data")
            if lci_dict and 'data' in lci_dict and 'index' in lci_dict and 'columns' in lci_dict:
                # Reconstrói o DataFrame.
                self.lci_df = pd.DataFrame(lci_dict['data'], index=lci_dict['index'], columns=lci_dict['columns'])
                # Converte colunas para numérico, tratando erros como NaN.
                for col in self.lci_df.columns:
                    self.lci_df[col] = pd.to_numeric(self.lci_df[col], errors='coerce') 
            else:
                self.lci_df = pd.DataFrame(dtype=float) # Se os dados LCI estiverem malformados, cria um novo.
            
            self.lci_units = loaded_data.get("lci_units", {})
            self.transformities = loaded_data.get("transformities", {})
            print(f"DEBUG DataManager: Dados carregados de '{filepath}'. DataFrame LCI atual:\n{self.lci_df.to_string()}\n")
            messagebox.showinfo("Sessão Carregada", f"Dados da sessão carregados com sucesso de:\n{filepath}")
            return True
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Sessão", f"Não foi possível carregar os dados da sessão.\nVerifique o arquivo ou se ele é compatível.\nDetalhes: {e}")
            print(f"ERRO DETALHADO em load_data_from_json: {e}\n{traceback.format_exc()}")
            return False

class EmergyCalculator:
    """
    Classe responsável por realizar os cálculos de emergia
    utilizando os dados fornecidos pelo DataManager.
    """
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.results = None # Armazena os resultados do último cálculo executado.

    def _get_required_transformities(self, input_flow_names: list[str], parameters: dict) -> tuple[dict | None, str]:
        """
        Obtém as transformidades necessárias para o cálculo, priorizando valores
        fornecidos manualmente nos parâmetros da simulação em detrimento dos
        valores armazenados na tabela de transformidades.

        Args:
            input_flow_names: Lista dos nomes dos fluxos de entrada para os quais as transformidades são necessárias.
            parameters: Dicionário de parâmetros da simulação, que pode conter transformidades manuais.

        Returns:
            Uma tupla contendo:
            - Um dicionário com as transformidades finais a serem usadas (ou None em caso de erro crítico).
            - Uma string com mensagens de log/aviso sobre o processo de obtenção das transformidades.
        """
        final_tf = {} 
        missing_tf_info = [] 
        errors = [] 
        log_messages = [] 

        for fn in input_flow_names:
            # Define a chave esperada para uma transformidade manual nos parâmetros.
            param_key = f"transformity_{fn.replace(' ', '_').replace('.', '_')}" 
            
            if param_key in parameters: # Verifica se uma transformidade manual foi fornecida.
                try:
                    final_tf[fn] = float(parameters[param_key])
                    log_messages.append(f"Utilizando transformidade manual para '{fn}': {final_tf[fn]:.2e}")
                except ValueError:
                    errors.append(f"Valor de transformidade manual para '{fn}' ('{parameters[param_key]}') é inválido. Requer valor numérico.")
            else: # Se não houver manual, busca na tabela do DataManager.
                tf_value_from_manager = self.data_manager.get_transformity_value(fn)
                if tf_value_from_manager is not None:
                    final_tf[fn] = tf_value_from_manager
                    log_messages.append(f"Utilizando transformidade da tabela para '{fn}': {final_tf[fn]:.2e}")
                else:
                    missing_tf_info.append(fn) # Se não encontrar em nenhum lugar.
        
        if errors: # Se ocorreram erros na conversão de transformidades manuais.
            messagebox.showerror("Erro nos Parâmetros de Transformidade", "\n".join(errors))
            return None, "\n".join(errors)
        
        if missing_tf_info: # Se faltarem transformidades para fluxos.
            msg = (f"Transformidades não encontradas para os seguintes fluxos: {', '.join(missing_tf_info)}.\n"
                   "Forneça-as na aba 'Gerenciamento de Dados' ou manualmente na seção 'Parâmetros Adicionais' da simulação.")
            messagebox.showerror("Transformidades Faltando", msg) # Considerado erro crítico para cálculo de emergia.
            return None, msg

        if not final_tf and input_flow_names: # Se há fluxos, mas nenhuma transformidade foi aplicada.
            warn_msg = "Nenhuma transformidade foi aplicada (nem da tabela, nem manual). Resultados de emergia podem ser zero."
            log_messages.append(f"AVISO: {warn_msg}")
        
        return final_tf, "\n".join(log_messages)

    def _calculate_total_emergy_logic(self, parameters: dict, calc_summary_msg: list[str]) -> bool:
        """Lida com a lógica para o cálculo de TOTAL_EMERGY."""
        lci_matrix = self.data_manager.get_lci_matrix_for_calc()
        lci_names = self.data_manager.get_lci_names_for_calc()
        input_flow_names = lci_names['rows']
        process_names = lci_names['columns']

        if not input_flow_names and not process_names:
            messagebox.showerror("Dados Insuficientes para Cálculo",
                                 "A Matriz LCI está completamente vazia. Adicione processos e fluxos antes de calcular a emergia total.")
            return False # Erro crítico, não pode prosseguir
        elif not input_flow_names and process_names:
            messagebox.showwarning("Cálculo com Fluxos Ausentes",
                                   "Existem processos definidos, mas não há fluxos de entrada na LCI. Os resultados de emergia serão zero.")
            self.results["emergy_per_input_flow_for_each_process"] = pd.DataFrame(columns=process_names, dtype=float)
            self.results["total_emergy_per_process"] = pd.Series(index=process_names, dtype=float).fillna(0)
            calc_summary_msg.append("LCI não possui fluxos de entrada. Emergias resultantes são zero.")
            return True # Estado válido, cálculo "concluído" com resultado zero.

        required_tfs, tf_log_msg = self._get_required_transformities(input_flow_names, parameters)
        if required_tfs is None: # Erro já foi exibido por _get_required_transformities
            return False 
        calc_summary_msg.append(f"Detalhes das Transformidades Utilizadas:\n{tf_log_msg}" if tf_log_msg else "Nenhuma transformidade específica foi processada.")

        tf_vector = np.array([required_tfs.get(name, 0) for name in input_flow_names])

        if input_flow_names and lci_matrix.shape[0] != len(tf_vector):
            err_msg = f"Incompatibilidade dimensional: Matriz LCI ({lci_matrix.shape[0]} fluxos) vs. Vetor de Transformidades ({len(tf_vector)} valores)."
            messagebox.showerror("Erro de Dimensão no Cálculo", err_msg)
            calc_summary_msg.append(f"ERRO: {err_msg}")
            return False

        if lci_matrix.size > 0 and tf_vector.size > 0 and lci_matrix.shape[0] > 0:
            emergy_values_per_input = lci_matrix * tf_vector[:, np.newaxis]
            total_emergy_per_process = np.sum(emergy_values_per_input, axis=0)
            
            self.results["emergy_per_input_flow_for_each_process"] = pd.DataFrame(emergy_values_per_input, index=input_flow_names, columns=process_names)
            self.results["total_emergy_per_process"] = pd.Series(total_emergy_per_process, index=process_names)
            calc_summary_msg.append("Emergia total por processo calculada com sucesso.")
            if required_tfs:
                calc_summary_msg.append("Transformidades Finais (considerando manuais e da tabela): " + str({k:f"{v:.2e}" for k,v in required_tfs.items() if v is not None}))
        else:
            calc_summary_msg.append("Cálculo de emergia total não produziu valores (LCI pode não ter fluxos, ou transformidades/valores são zero).")
            self.results["total_emergy_per_process"] = pd.Series(index=process_names if process_names else [], dtype=float).fillna(0)
            self.results["emergy_per_input_flow_for_each_process"] = pd.DataFrame(index=input_flow_names if input_flow_names else [], columns=process_names if process_names else [], dtype=float).fillna(0)
        return True

    def _calculate_direct_inputs_sum_logic(self, parameters: dict, calc_summary_msg: list[str]) -> bool:
        """Lida com a lógica para o cálculo de DIRECT_INPUTS_SUM."""
        lci_df_full = self.data_manager.get_lci_dataframe()
        process_names = lci_df_full.columns.tolist()
        input_flow_names = lci_df_full.index.tolist()

        if lci_df_full.empty or not input_flow_names:
            self.results["sum_of_direct_inputs_per_process"] = pd.Series(index=process_names if process_names else [], dtype=float).fillna(0)
            if not input_flow_names and process_names:
                 calc_summary_msg.append("Matriz LCI não possui fluxos de entrada. A soma dos inputs diretos é zero.")
            elif lci_df_full.empty: # Cobre o caso de não ter nem fluxos nem processos
                 calc_summary_msg.append("Matriz LCI está completamente vazia. A soma dos inputs diretos é zero.")
            else: # Caso de não ter fluxos mas talvez processos (já coberto acima)
                 calc_summary_msg.append("Matriz LCI não contém fluxos de entrada. A soma dos inputs diretos é zero.")
        else:
            lci_matrix_values = self.data_manager.get_lci_matrix_for_calc()
            sum_of_inputs_per_process = np.sum(lci_matrix_values, axis=0)
            self.results["sum_of_direct_inputs_per_process"] = pd.Series(sum_of_inputs_per_process, index=process_names)
            calc_summary_msg.append("Soma dos inputs diretos por processo calculada.")
        return True

    def _calculate_emergy_indices_logic(self, parameters: dict, calc_summary_msg: list[str]) -> bool:
        """Lida com a lógica para o cálculo de EMERGY_INDICES."""
        param_names_map = {'R': "Renovável (R)", 'N': "Não Renovável (N)", 'F': "Comprada (F)"}
        components = {}
        
        for key, display_name in param_names_map.items():
            value_str = parameters.get(key)
            if value_str is None or str(value_str).strip() == "":
                messagebox.showerror("Parâmetro Ausente para Índices", f"O valor para '{display_name}' é obrigatório para o cálculo de índices emergéticos.")
                return False
            try:
                components[key] = float(value_str)
                if components[key] < 0:
                    messagebox.showerror("Valor Inválido para Índices", f"O valor para '{display_name}' ({value_str}) deve ser um número não negativo.")
                    return False
            except ValueError:
                messagebox.showerror("Valor Inválido para Índices", f"O valor para '{display_name}' ('{value_str}') deve ser numérico.")
                return False
        
        R, N, F_ = components['R'], components['N'], components['F']
        
        Y_str = parameters.get('Y')
        Y_ = None
        if Y_str is not None and str(Y_str).strip() != "":
            try:
                Y_ = float(Y_str)
                if Y_ < 0:
                    messagebox.showerror("Valor Inválido para Yield (Y)", f"O valor para 'Yield (Y)' ({Y_str}) deve ser um número não negativo.")
                    return False
                calc_summary_msg.append(f"Yield (Y) fornecido pelo usuário: {Y_:.2e}")
            except ValueError:
                messagebox.showerror("Valor Inválido para Yield (Y)", f"O valor para 'Yield (Y)' ('{Y_str}') deve ser numérico.")
                return False
        else:
            Y_ = R + N + F_
            calc_summary_msg.append(f"Yield (Y) calculado (R+N+F): {Y_:.2e}")

        calc_summary_msg.append(f"Valores de entrada para Índices: R={R:.2e}, N={N:.2e}, F={F_:.2e}, Y={Y_:.2e}")

        eyr = (Y_ / F_) if F_ != 0 else (float('inf') if Y_ > 0 else float('nan'))
        elr = ((N + F_) / R) if R != 0 else (float('inf') if (N + F_) > 0 else 0.0)
        esi = float('nan')
        if elr != 0 and not (pd.isna(eyr) or pd.isna(elr) or elr == float('inf')):
            esi = eyr / elr
        elif elr == 0 and eyr > 0 and not pd.isna(eyr): # Caso especial para ESI infinito.
            esi = float('inf')

        self.results.update({
            "EYR (Emergy Yield Ratio)": f"{eyr:.2e}", 
            "ELR (Environmental Loading Ratio)": f"{elr:.2e}", 
            "ESI (Emergy Sustainability Index)": f"{esi:.2e}"
        })
        calc_summary_msg.append(f"EYR: {eyr:.2e}")
        calc_summary_msg.append(f"ELR: {elr:.2e}")
        calc_summary_msg.append(f"ESI: {esi:.2e}")
        calc_summary_msg.append("\nInterpretações Gerais (sujeitas ao contexto do sistema analisado):"
                                "\n- EYR (Taxa de Rendimento Emergético): Valores altos (>2-5) geralmente indicam maior contribuição líquida à economia."
                                "\n- ELR (Taxa de Carga Ambiental): Valores baixos (<2-3) geralmente indicam menor estresse ambiental relativo à emergia renovável utilizada."
                                "\n- ESI (Índice de Sustentabilidade Emergética): Valores altos (>5-10) geralmente indicam maior potencial de sustentabilidade a longo prazo.")
        return True

    def calculate_emergy(self, parameters: dict | None = None) -> bool:
        """
        Executa o tipo de cálculo de emergia especificado, utilizando os dados
        e parâmetros fornecidos.

        Args:
            parameters: Dicionário contendo o tipo de cálculo e outros parâmetros relevantes.

        Returns:
            True se o cálculo for bem-sucedido (mesmo que com avisos), False em caso de erro crítico.
        """
        if parameters is None:
            parameters = {}
        
        calc_type_enum = parameters.get("calculation_type_enum")
        if not isinstance(calc_type_enum, CalculationType): # Validação do tipo de cálculo.
            messagebox.showerror("Erro Interno de Cálculo", "Tipo de cálculo inválido ou não especificado.")
            return False
        
        calc_type_display_name = CalculationType.get_display_names_map().get(calc_type_enum, "Desconhecido")
        calc_summary_msg = [f"Tipo de cálculo selecionado: {calc_type_display_name}"]
        self.results = {} # Reseta os resultados anteriores.

        print(f"\n--- Iniciando Cálculo Emergético: {calc_type_enum.name} ({calc_type_display_name}) ---")
        print(f"Parâmetros de entrada para o cálculo: {parameters}")
        
        calculation_successful = False
        try: # Bloco principal de tentativa para os cálculos.
            if calc_type_enum == CalculationType.TOTAL_EMERGY:
                calculation_successful = self._calculate_total_emergy_logic(parameters, calc_summary_msg)
            elif calc_type_enum == CalculationType.DIRECT_INPUTS_SUM:
                calculation_successful = self._calculate_direct_inputs_sum_logic(parameters, calc_summary_msg)
            elif calc_type_enum == CalculationType.EMERGY_INDICES:
                calculation_successful = self._calculate_emergy_indices_logic(parameters, calc_summary_msg)
            else: 
                calc_summary_msg.append(f"Tipo de cálculo '{calc_type_enum.name}' não implementado.")
                messagebox.showwarning("Funcionalidade Não Implementada", f"O tipo de cálculo '{calc_type_display_name}' não está completamente implementado.")
                calculation_successful = False # Explicitamente falso pois não implementado

            # Armazena o sumário do cálculo nos resultados.
            self.results["calculation_summary"] = "\n".join(calc_summary_msg)
            print("\n".join(calc_summary_msg)) 
            print("--- Fim do Cálculo ---")
            return calculation_successful # Retorna o status da lógica específica do cálculo

        except Exception as e: # Captura qualquer outra exceção não prevista durante os cálculos.
            error_details = traceback.format_exc()
            messagebox.showerror("Erro Inesperado Durante o Cálculo", f"Um erro inesperado ocorreu durante o cálculo '{calc_type_display_name}':\n{e}\n\nConsulte o console para detalhes técnicos.")
            print(f"ERRO CRÍTICO DETALHADO em calculate_emergy ({calc_type_display_name}): {e}\n{error_details}")
            self.results["calculation_summary"] = f"ERRO DURANTE O CÁLCULO: {e}\nConsulte o console para detalhes técnicos." 
            return False


    def get_results(self) -> dict | None:
        """Retorna os resultados do último cálculo executado."""
        return self.results

# --- Classes dos Frames da Interface Gráfica (Abas) ---
class DataManagementFrame(ttk.Frame):
    """
    Frame da interface gráfica para a aba "Gerenciamento de Dados".
    Permite ao usuário interagir com a Matriz LCI e a Tabela de Transformidades.
    """
    def __init__(self, parent_notebook: ttk.Notebook, controller): 
        super().__init__(parent_notebook, style="TFrame")
        self.controller = controller # Referência à instância principal da aplicação (Application).

        # --- Configuração do Canvas e Scrollbar para rolagem da aba ---
        self.canvas = tk.Canvas(self, bg=COLOR_BACKGROUND_DEEP_SPACE, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Quantum.Vertical.TScrollbar")
        
        # Frame interno que efetivamente rolará dentro do canvas.
        # Utiliza layout de grid para centralizar o 'content_holder_frame'.
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame") 
        self.scrollable_frame.grid_columnconfigure(0, weight=1) # Coluna esquerda expansível (espaçador).
        self.scrollable_frame.grid_columnconfigure(1, weight=0) # Coluna central para o conteúdo (não expansível horizontalmente).
        self.scrollable_frame.grid_columnconfigure(2, weight=1) # Coluna direita expansível (espaçador).

        # Frame que conterá todos os widgets da aba, centralizado no 'scrollable_frame'.
        self.content_holder_frame = ttk.Frame(self.scrollable_frame, style="TFrame")
        self.content_holder_frame.grid(row=0, column=1, sticky="ns") # Centralizado e estica verticalmente.

        # Associações de eventos para o funcionamento correto da rolagem.
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="scrollable_frame_window")
        self.canvas.bind("<Configure>", self._on_canvas_configure) # Para ajustar a largura do frame rolável.
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Posicionamento do canvas e da scrollbar.
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20,0), pady=20)
        self.scrollbar.pack(side="right", fill="y", padx=(0,20), pady=20)

        # Alias para o frame que contém os widgets da aba.
        content_pane = self.content_holder_frame

        # --- Instruções para o Usuário ---
        instr_label = ttk.Label(content_pane, 
                                text="Nesta seção, são gerenciados os dados de entrada para a análise emergética: a Matriz de Inventário do Ciclo de Vida (LCI) e a Tabela de Transformidades (UEVs).\n"
                                     "Siga os botões numerados para inserir dados na LCI. As transformidades podem ser adicionadas ou editadas a qualquer momento.",
                                style="Instruction.TLabel", justify="left")
        instr_label.pack(pady=(0,20), padx=10, fill="x")

        # --- Controles Gerais: Salvar e Carregar Sessão ---
        general_controls_frame = ttk.Frame(content_pane, padding=(0,0,0,15))
        general_controls_frame.pack(fill="x", padx=10)
        
        btn_save_data = ttk.Button(general_controls_frame, text="Salvar Dados da Sessão", command=self.save_session_data, width=25, style="TButton")
        btn_save_data.pack(side="left", padx=(0,10), pady=5)
        Tooltip(btn_save_data, "Salva todos os dados LCI e Transformidades inseridos em um arquivo JSON para carregamento posterior.", app_font_body=self.controller.APP_FONT_BODY)
        
        btn_load_data = ttk.Button(general_controls_frame, text="Carregar Dados da Sessão", command=self.load_session_data, width=25, style="TButton")
        btn_load_data.pack(side="left", padx=10, pady=5)
        Tooltip(btn_load_data, "Carrega dados LCI e Transformidades de um arquivo JSON salvo anteriormente.", app_font_body=self.controller.APP_FONT_BODY)

        # --- Seção da Matriz LCI ---
        lci_lf = ttk.LabelFrame(content_pane, text="Matriz LCI (Fluxos de Entrada vs. Processos/Produtos)", padding=(20,15))
        lci_lf.pack(pady=10, padx=10, fill="x", expand=False) # fill="x" para ocupar a largura, expand=False para não alargar desnecessariamente.
        
        # Botões de controle da LCI (Adicionar Processo, Fluxo, Definir Valor).
        lci_controls_top_frame = ttk.Frame(lci_lf, padding=(0,0,0,10))
        lci_controls_top_frame.pack(fill="x")
        
        self.btn_add_lci_process = ttk.Button(lci_controls_top_frame, text="1. Novo Processo (Coluna)", command=self.add_lci_process_dialog, width=25)
        self.btn_add_lci_process.pack(side="left", padx=(0,10), pady=5)
        Tooltip(self.btn_add_lci_process, "Adiciona as colunas da matriz LCI (processos ou produtos finais do sistema).", app_font_body=self.controller.APP_FONT_BODY)
        
        self.btn_add_lci_flow = ttk.Button(lci_controls_top_frame, text="2. Novo Fluxo (Linha)", command=self.add_lci_flow_dialog, width=22, state="normal") 
        self.btn_add_lci_flow.pack(side="left", padx=10, pady=5)
        Tooltip(self.btn_add_lci_flow, "Adiciona os fluxos de entrada (linhas da LCI) para cada processo.", app_font_body=self.controller.APP_FONT_BODY)
        
        self.btn_set_lci_val = ttk.Button(lci_controls_top_frame, text="3. Definir Valor LCI", command=self.set_lci_value_dialog, width=20, state="normal") 
        self.btn_set_lci_val.pack(side="left", padx=10, pady=5)
        Tooltip(self.btn_set_lci_val, "Preenche os valores na matriz LCI (intersecção de fluxo e processo).", app_font_body=self.controller.APP_FONT_BODY)
        
        # Frame para a tabela LCI (Treeview) e suas barras de rolagem.
        lci_tree_frame = ttk.Frame(lci_lf)
        lci_tree_frame.pack(fill="both", expand=True, pady=5) 
        self.lci_treeview = ttk.Treeview(lci_tree_frame, style="Treeview", height=10) # Altura da tabela em número de linhas.
        
        # Barras de rolagem para a tabela LCI.
        self.lci_v_scroll = ttk.Scrollbar(lci_tree_frame, orient="vertical", command=self.lci_treeview.yview, style="Quantum.Vertical.TScrollbar")
        self.lci_h_scroll = ttk.Scrollbar(lci_tree_frame, orient="horizontal", command=self.lci_treeview.xview, style="Quantum.Horizontal.TScrollbar")
        self.lci_treeview.configure(yscrollcommand=self.lci_v_scroll.set, xscrollcommand=self.lci_h_scroll.set)
        
        self.lci_v_scroll.pack(side="right", fill="y")
        self.lci_h_scroll.pack(side="bottom", fill="x")
        self.lci_treeview.pack(fill="both", expand=True)
        
        # Botões para remover itens da LCI.
        lci_remove_controls_frame = ttk.Frame(lci_lf, padding=(0,10,0,0))
        lci_remove_controls_frame.pack(fill="x")
        
        self.btn_remove_lci_flow = ttk.Button(lci_remove_controls_frame, text="Remover Fluxo (Linha)", command=self.remove_lci_flow_dialog, width=25, state="normal") 
        self.btn_remove_lci_flow.pack(side="left", padx=(0,10), pady=5)
        Tooltip(self.btn_remove_lci_flow, "Remove um fluxo de entrada (linha) selecionado da LCI.", app_font_body=self.controller.APP_FONT_BODY)
        
        self.btn_remove_lci_process = ttk.Button(lci_remove_controls_frame, text="Remover Processo (Coluna)", command=self.remove_lci_process_dialog, width=25, state="normal") 
        self.btn_remove_lci_process.pack(side="left", padx=10, pady=5)
        Tooltip(self.btn_remove_lci_process, "Remove um processo/produto (coluna) selecionado da LCI.", app_font_body=self.controller.APP_FONT_BODY)

        # --- Seção da Tabela de Transformidades (UEVs) ---
        trans_lf = ttk.LabelFrame(content_pane, text="Tabela de Transformidades (UEVs)", padding=(20,15))
        trans_lf.pack(pady=20, padx=10, fill="x", expand=False) 
        
        trans_instr_label = ttk.Label(trans_lf, text="Insira os valores de transformidade para cada fluxo de entrada da LCI que representa um recurso primário ou um input externo com UEV conhecido.", style="Instruction.TLabel", justify="left")
        trans_instr_label.pack(pady=(0,10), fill="x")
        
        # Botões para manipular a tabela de transformidades.
        trans_controls_frame = ttk.Frame(trans_lf, padding=(0,0,0,10))
        trans_controls_frame.pack(fill="x")
        
        btn_add_trans = ttk.Button(trans_controls_frame, text="Adicionar/Editar Transformidade", command=self.add_edit_transformity_dialog, width=30)
        btn_add_trans.pack(side="left", padx=(0,10), pady=5)
        Tooltip(btn_add_trans, "Adiciona uma nova transformidade (Nome do Fluxo, Valor e Unidade) ou edita uma entrada existente.", app_font_body=self.controller.APP_FONT_BODY)
        
        btn_remove_trans = ttk.Button(trans_controls_frame, text="Remover Transformidade", command=self.remove_transformity_dialog, width=30)
        btn_remove_trans.pack(side="left", padx=10, pady=5)
        Tooltip(btn_remove_trans, "Remove uma transformidade da tabela, selecionada pelo nome do fluxo.", app_font_body=self.controller.APP_FONT_BODY)
        
        # Frame para a tabela (Treeview) das transformidades.
        trans_tree_frame = ttk.Frame(trans_lf)
        trans_tree_frame.pack(fill="both", expand=True, pady=5) 
        self.transformity_treeview = ttk.Treeview(trans_tree_frame, columns=("flow_name", "value", "unit"), show="headings", style="Treeview", height=7)
        
        # Configuração dos cabeçalhos e colunas da tabela de transformidades.
        self.transformity_treeview.heading("flow_name", text="Nome do Fluxo/Recurso")
        self.transformity_treeview.heading("value", text="Valor Transformidade")
        self.transformity_treeview.heading("unit", text="Unidade (sej/...)")
        self.transformity_treeview.column("flow_name", width=300, anchor="w", minwidth=200)
        self.transformity_treeview.column("value", width=200, anchor="e", minwidth=120) # 'e' para alinhamento à direita (east).
        self.transformity_treeview.column("unit", width=150, anchor="w", minwidth=100)
        
        # Barra de rolagem para a tabela de transformidades.
        self.trans_v_scroll = ttk.Scrollbar(trans_tree_frame, orient="vertical", command=self.transformity_treeview.yview, style="Quantum.Vertical.TScrollbar")
        self.transformity_treeview.configure(yscrollcommand=self.trans_v_scroll.set)
        self.trans_v_scroll.pack(side="right", fill="y")
        self.transformity_treeview.pack(fill="both", expand=True)
        
        # --- Botão de Limpeza Geral ---
        clear_all_button = ttk.Button(content_pane, text="Limpar Todos os Dados Manuais", command=self.clear_all_manual_data_dialog, style="Primary.TButton", width=35)
        clear_all_button.pack(pady=(25,10), padx=10)
        Tooltip(clear_all_button, "ATENÇÃO: Remove TODOS os dados de LCI e Transformidades inseridos. Esta ação não pode ser desfeita.", app_font_body=self.controller.APP_FONT_BODY)
        
        # Inicializa a exibição das tabelas.
        self.refresh_lci_display()
        self.refresh_transformity_display()

    def _on_canvas_configure(self, event):
        """
        Chamado quando o widget Canvas é redimensionado.
        Ajusta a largura do 'scrollable_frame' para corresponder à largura do Canvas
        e reconfigura a região de rolagem ('scrollregion').
        """
        canvas_width = event.width
        self.canvas.itemconfig("scrollable_frame_window", width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def _prompt_for_name_and_unit(self, title: str, name_prompt: str, unit_prompt_base: str, initial_name: str = "", initial_unit: str = "") -> tuple[str | None, str | None]:
        """
        Função auxiliar para solicitar nome e unidade ao usuário através de diálogos.
        Retorna uma tupla (nome, unidade) ou (None, None) se o usuário cancelar.
        """
        name = simpledialog.askstring(title, name_prompt, parent=self, initialvalue=initial_name)
        if not name: # Se o usuário cancelou ou não inseriu nome.
            return None, None
        
        unit_prompt = f"{unit_prompt_base} '{name}' (opcional):" # Pergunta pela unidade.
        unit = simpledialog.askstring(title, unit_prompt, parent=self, initialvalue=initial_unit)
        # Se o usuário cancelar a unidade, 'unit' será None; trata como string vazia.
        return name, unit if unit is not None else ""


    def save_session_data(self):
        """Abre um diálogo para o usuário salvar os dados da sessão atual."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", # Extensão padrão do arquivo.
            filetypes=[("Arquivos de Sessão JSON", "*.json"), ("Todos os Arquivos", "*.*")], # Filtros de tipo de arquivo.
            title="Salvar Dados da Sessão Como...", # Título da janela de diálogo.
            initialdir=DATA_DIR, # Diretório inicial sugerido.
            initialfile=f"sessao_emergia_{datetime.now().strftime('%Y%m%d_%H%M')}.json" # Sugestão de nome de arquivo com data/hora.
        )
        if filepath: # Se o usuário selecionou um caminho e nome de arquivo.
            self.controller.data_manager.save_data_to_json(filepath) # Chama o DataManager para salvar.

    def load_session_data(self):
        """Abre um diálogo para o usuário carregar dados de uma sessão salva."""
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Arquivos de Sessão JSON", "*.json"), ("Todos os Arquivos", "*.*")],
            title="Carregar Dados da Sessão de...",
            initialdir=DATA_DIR
        )
        if filepath: # Se o usuário selecionou um arquivo.
            if self.controller.data_manager.load_data_from_json(filepath): # Chama o DataManager para carregar.
                self.controller.update_all_displays() # Se carregou com sucesso, atualiza todas as exibições da UI.

    def add_lci_flow_dialog(self):
        """Inicia o diálogo para adicionar um novo fluxo LCI."""
        name, unit = self._prompt_for_name_and_unit(
            "Novo Fluxo de Entrada na LCI",
            "Nome do novo fluxo de entrada (linha da LCI):\n(Ex: Energia Solar, Combustível, Água)",
            "Unidade para o fluxo"
        )
        if name: # Se um nome foi fornecido.
            if self.controller.data_manager.add_lci_input_flow(name, unit): # Tenta adicionar.
                self.refresh_lci_display() # Atualiza a tabela LCI na tela.
                self.controller.update_simulation_status() # Informa a aba de simulação sobre a mudança nos dados.

    def add_lci_process_dialog(self):
        """Inicia o diálogo para adicionar um novo processo LCI."""
        name, unit = self._prompt_for_name_and_unit(
            "Novo Processo/Produto na LCI",
            "Nome do novo processo/produto (coluna da LCI):\n(Ex: Produção de Aço, Eletricidade Gerada)",
            "Unidade para o processo/produto"
        )
        if name:
            if self.controller.data_manager.add_lci_process_column(name, unit):
                self.refresh_lci_display()
                self.controller.update_simulation_status()

    def set_lci_value_dialog(self):
        """Inicia o diálogo para o usuário definir um valor na matriz LCI."""
        flow = simpledialog.askstring("Definir Valor LCI", "Nome do Fluxo de Entrada (Linha) para o qual deseja definir um valor:", parent=self)
        if not flow: return # Usuário cancelou.
        process = simpledialog.askstring("Definir Valor LCI", f"Nome do Processo/Produto (Coluna) para o fluxo '{flow}':", parent=self)
        if not process: return # Usuário cancelou.
        
        value_str = None # Para armazenar a entrada válida.
        while True: # Loop para garantir entrada numérica.
            input_value_str = simpledialog.askstring("Definir Valor LCI", f"Insira o valor numérico para LCI na célula [{flow} -> {process}]:", parent=self)
            if input_value_str is None: # Usuário cancelou o diálogo do valor.
                return 
            try:
                float(input_value_str) # Tenta converter para float para validar.
                value_str = input_value_str # Armazena a string válida se a conversão for bem-sucedida.
                break # Sai do loop se o valor for numérico.
            except ValueError:
                messagebox.showerror("Entrada Inválida", f"O valor '{input_value_str}' não é um número válido. Por favor, insira um valor numérico.", parent=self)
        
        # Se chegou aqui, value_str contém uma string que pode ser convertida para float.
        if self.controller.data_manager.set_lci_value(flow, process, value_str):
            self.refresh_lci_display()
            self.controller.update_simulation_status()

    def remove_lci_flow_dialog(self):
        """Inicia o diálogo para remover um fluxo LCI."""
        name = simpledialog.askstring("Remover Fluxo de Entrada", "Nome do fluxo de entrada (linha) que deseja remover:", parent=self)
        if name:
            if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o fluxo '{name}' da LCI? Esta ação não pode ser desfeita.", icon='warning', parent=self):
                if self.controller.data_manager.remove_lci_input_flow(name):
                    self.refresh_lci_display()
                    self.controller.update_simulation_status()

    def remove_lci_process_dialog(self):
        """Inicia o diálogo para remover um processo LCI."""
        name = simpledialog.askstring("Remover Processo/Produto", "Nome do processo/produto (coluna) que deseja remover:", parent=self)
        if name:
            if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o processo '{name}' da LCI? Isso removerá toda a coluna e os valores associados.", icon='warning', parent=self):
                if self.controller.data_manager.remove_lci_process_column(name):
                    self.refresh_lci_display()
                    self.controller.update_simulation_status()

    def add_edit_transformity_dialog(self):
        """Inicia o diálogo para adicionar ou editar uma transformidade."""
        flow_name = simpledialog.askstring("Adicionar/Editar Transformidade", 
                                           "Nome do Fluxo/Recurso para a transformidade:\n(Idealmente, um nome de fluxo já existente na LCI)", 
                                           parent=self)
        if not flow_name: return # Usuário cancelou.

        current_data = self.controller.data_manager.get_transformity_with_unit(flow_name)
        # Define valores iniciais para os campos do diálogo.
        initial_val_str = str(current_data['value']) if current_data and current_data.get('value') is not None else ""
        initial_unit_str = current_data['unit'] if current_data and current_data.get('unit') is not None else "sej/unidade_original"
        
        prompt_val = f"Valor da Transformidade para '{flow_name}':"
        if current_data and current_data.get('value') is not None: 
            prompt_val += f"\n(Valor atual: {current_data['value']:.2e})" # Mostra o valor atual formatado.
        
        value_str = None
        temp_val_str = initial_val_str # Usado para manter o valor entre tentativas no loop.
        while True: # Loop para garantir entrada numérica.
            value_str_input = simpledialog.askstring("Valor da Transformidade", prompt_val, parent=self, initialvalue=temp_val_str) 
            if value_str_input is None: return # Usuário cancelou.
            try:
                float(value_str_input) # Tenta converter.
                value_str = value_str_input # Armazena a string válida.
                break 
            except ValueError:
                messagebox.showerror("Entrada Inválida", f"O valor '{value_str_input}' não é um número válido. Por favor, insira um valor numérico.", parent=self)
                temp_val_str = value_str_input # Mantém o valor inválido para o usuário corrigir na próxima tentativa.


        prompt_unit = f"Unidade da Transformidade para '{flow_name}' (ex: sej/kg, sej/MJ):"
        if current_data and current_data.get('unit') is not None: 
            prompt_unit += f"\n(Unidade atual: {current_data['unit']})"
        
        unit_str = simpledialog.askstring("Unidade da Transformidade", prompt_unit, parent=self, initialvalue=initial_unit_str)
        if unit_str is None: unit_str = initial_unit_str # Se cancelar, mantém a unidade anterior ou o padrão.

        if self.controller.data_manager.add_transformity(flow_name, value_str, unit_str):
            self.refresh_transformity_display()
            self.controller.update_simulation_status()

    def remove_transformity_dialog(self):
        """Inicia o diálogo para remover uma transformidade."""
        name = simpledialog.askstring("Remover Transformidade", "Nome do fluxo/recurso da transformidade que deseja remover:", parent=self)
        if name:
            if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover a transformidade para '{name}'?", icon='question', parent=self):
                if self.controller.data_manager.remove_transformity(name):
                    self.refresh_transformity_display()
                    self.controller.update_simulation_status()

    def clear_all_manual_data_dialog(self):
        """Solicita confirmação antes de limpar todos os dados manuais."""
        if messagebox.askyesno("Confirmar Limpeza Total de Dados", 
                               "ATENÇÃO!\n\nVocê tem certeza que deseja apagar TODOS os dados de LCI e Transformidades inseridos manualmente?\n\nEsta ação não poderá ser desfeita.", 
                               icon='warning', parent=self): # Ícone de aviso para maior ênfase.
            self.controller.data_manager.clear_all_data()
            self.refresh_lci_display()
            self.refresh_transformity_display()
            messagebox.showinfo("Dados Limpos", "Todos os dados manuais foram removidos com sucesso.", parent=self)
            self.controller.update_simulation_status() 

    def refresh_lci_display(self):
        """Atualiza a exibição da tabela LCI (Treeview) com os dados atuais do DataManager."""
        print("DEBUG DataManagementFrame: Iniciando refresh_lci_display()")
        try:
            # Limpa todos os itens existentes no Treeview.
            for i in self.lci_treeview.get_children():
                self.lci_treeview.delete(i)
            
            df = self.controller.data_manager.get_lci_dataframe() # Obtém os dados LCI atuais.
            print(f"DEBUG DataManagementFrame: DataFrame para Treeview LCI:\n{df.to_string()}\nÍndice: {list(df.index)}\nColunas: {list(df.columns)}")
            
            # Configura o cabeçalho da primeira coluna (onde os nomes dos fluxos são exibidos).
            self.lci_treeview.heading("#0", text="Fluxo Entrada ↓ | Processo/Produto →")
            self.lci_treeview.column("#0", width=250, anchor="w", minwidth=150, stretch=tk.NO)

            # Configura as colunas do Treeview baseadas nas colunas do DataFrame.
            if not df.columns.empty:
                self.lci_treeview["columns"] = list(df.columns)
                for col_name_raw in df.columns:
                    col_name = str(col_name_raw) 
                    unit = self.controller.data_manager.get_lci_unit(col_name)
                    col_display_name = f"{col_name}\n({unit})" if unit else col_name
                    self.lci_treeview.heading(col_name, text=col_display_name, anchor="center")
                    self.lci_treeview.column(col_name, width=120, anchor="e", minwidth=80) 
            else:
                self.lci_treeview["columns"] = [] # Limpa as colunas do Treeview se o DataFrame não tiver colunas.

            # Adiciona as linhas (fluxos) ao Treeview.
            if not df.index.empty:
                for index_name_raw, row_data in df.iterrows():
                    index_name = str(index_name_raw) 
                    unit = self.controller.data_manager.get_lci_unit(index_name)
                    row_display_name = f"{index_name} ({unit})" if unit else index_name
                    
                    formatted_values = []
                    if not df.columns.empty: # Formata os valores das células apenas se houver colunas.
                        for v in row_data:
                            if pd.isna(v):
                                formatted_values.append("-") # Representa NaN como "-".
                            elif isinstance(v, (float, np.number)):
                                if v == 0:
                                    formatted_values.append("0") 
                                else: # Formatação condicional para números.
                                    formatted_values.append(f"{v:.2e}" if abs(v) > 1e5 or (abs(v) < 1e-2 and v!=0) else f"{v:,.2f}")
                            else:
                                formatted_values.append(str(v)) # Converte outros tipos para string.
                    
                    self.lci_treeview.insert("", "end", text=row_display_name, values=formatted_values, iid=index_name)
            
            # Exibe uma mensagem placeholder se a LCI estiver completamente vazia.
            if df.index.empty and df.columns.empty:
                print("DEBUG DataManagementFrame: DataFrame LCI totalmente vazio. Exibindo placeholder.")
                if not self.lci_treeview.get_children(): # Adiciona apenas se o Treeview estiver realmente vazio.
                    self.lci_treeview.insert("", "end", text="Matriz LCI vazia. Adicione Processos e Fluxos.", iid="empty_lci_placeholder")
            elif df.index.empty and not df.columns.empty: # Se há processos (colunas) mas não fluxos (linhas).
                print("DEBUG DataManagementFrame: LCI com processos, mas sem fluxos. Exibindo placeholder de linhas.")
                if not self.lci_treeview.get_children():
                    self.lci_treeview.insert("", "end", text="Adicione fluxos de entrada para os processos existentes.", iid="empty_lci_rows_placeholder")
            # Se há fluxos mas não processos, os nomes dos fluxos já são mostrados na coluna #0.

            print("DEBUG DataManagementFrame: Exibição da LCI atualizada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro ao Atualizar Tabela LCI", f"Ocorreu um erro ao tentar atualizar a exibição da LCI:\n{e}")
            print(f"ERRO DETALHADO em refresh_lci_display: {e}\n{traceback.format_exc()}")


    def refresh_transformity_display(self):
        """Atualiza a exibição da tabela de transformidades (Treeview)."""
        try:
            # Limpa os itens existentes.
            for i in self.transformity_treeview.get_children():
                self.transformity_treeview.delete(i)
                
            transformities = self.controller.data_manager.get_all_transformities() # Obtém os dados.
            if not transformities: # Se não houver transformidades.
                self.transformity_treeview.insert("", "end", values=("Nenhuma transformidade inserida.", "", ""), iid="empty_trans_placeholder")
                return

            # Adiciona cada transformidade à tabela, ordenada pelo nome do fluxo.
            for flow_name_raw, data in sorted(transformities.items()):
                flow_name = str(flow_name_raw)
                value = data.get('value')
                unit = data.get('unit', 'sej/unidade_original') # Unidade padrão se não especificada.
                
                value_display = ""
                if isinstance(value, (float, np.number)):
                    value_display = f"{value:.2e}" if value != 0 else "0" # Formata o valor.
                elif value is not None:
                    value_display = str(value)

                self.transformity_treeview.insert("", "end", values=(flow_name, value_display, unit), iid=flow_name)
        except Exception as e:
            messagebox.showerror("Erro ao Atualizar Tabela de Transformidades", f"Falha ao atualizar a exibição das transformidades:\n{e}")
            print(f"ERRO DETALHADO em refresh_transformity_display: {e}\n{traceback.format_exc()}")


class SimulationFrame(ttk.Frame):
    """
    Frame da interface gráfica para a aba "Simulação Emergética".
    Permite ao usuário selecionar o tipo de cálculo, inserir parâmetros
    e executar a simulação.
    """
    def __init__(self, parent_notebook: ttk.Notebook, controller):
        super().__init__(parent_notebook, padding=(25,20), style="TFrame") 
        self.controller = controller

        title_label = ttk.Label(self, text="Simulação e Parâmetros de Cálculo", style="Title.TLabel")
        title_label.pack(pady=(0,25), anchor="center")

        instr_label = ttk.Label(self, text="Selecione o tipo de análise desejado, forneça os parâmetros necessários e clique em 'Executar Cálculo'.", style="Instruction.TLabel", justify="center")
        instr_label.pack(pady=(0,15), fill="x")

        # Label para exibir o status da prontidão para cálculo.
        self.status_label = ttk.Label(self, text="Status: Carregando informações...", style="Status.TLabel", justify="center")
        self.status_label.pack(pady=10, padx=10, fill="x")

        # --- Seção 1: Seleção do Tipo de Análise ---
        calc_type_lf = ttk.LabelFrame(self, text="1. Selecione o Tipo de Análise Emergética", padding=(20,15))
        calc_type_lf.pack(pady=15, padx=0, fill="x")
        
        self.calculation_type_var = tk.StringVar() # Variável Tkinter para o Combobox.
        self.calc_type_options_map = CalculationType.get_display_names_map() # Mapeamento de Enums para nomes de exibição.
        
        combo_frame = ttk.Frame(calc_type_lf) # Frame para agrupar Combobox e ícone de ajuda.
        combo_frame.pack(pady=5)

        self.calc_type_combo = ttk.Combobox(combo_frame, textvariable=self.calculation_type_var, 
                                            values=CalculationType.get_all_display_names(), 
                                            state="readonly", width=40, # "readonly" para forçar seleção das opções.
                                            font=(self.controller.APP_FONT_BODY, FONT_SIZE_NORMAL), 
                                            style="TCombobox")
        self.calc_type_combo.pack(side="left", padx=(0,10))
        self.calc_type_combo.set(self.calc_type_options_map[CalculationType.get_default()]) # Define o valor padrão.
        self.calc_type_combo.bind("<<ComboboxSelected>>", self.on_calc_type_change) # Evento ao selecionar item.
        
        calc_type_help = ttk.Label(combo_frame, text="(?)", style="Help.TLabel", cursor="hand2") # Ícone de ajuda.
        calc_type_help.pack(side="left")
        Tooltip(calc_type_help, 
                ("Selecione o método de cálculo desejado:\n"
                 "- Emergia Total por Processo: Utiliza dados LCI e transformidades para o cálculo completo.\n"
                 "- Soma dos Inputs Diretos: Agrega as quantidades físicas da LCI por processo.\n"
                 "- Índices Emergéticos: Calcula EYR, ELR e ESI com base nos inputs R, N, F e Y."),
                app_font_body=self.controller.APP_FONT_BODY)

        # --- Seção 2: Parâmetros para Índices Emergéticos ---
        # Este frame é exibido condicionalmente.
        self.indices_params_frame = ttk.LabelFrame(self, text="2. Parâmetros para Índices Emergéticos (R, N, F, Y)", padding=(20,15))
        
        self.param_entries_indices = {} # Dicionário para armazenar os widgets Entry (R, N, F, Y).
        indices_tooltips = {
            "R": "Emergia Renovável Local (R), em sej. Exemplo: 1.2E15",
            "N": "Emergia Não-Renovável Local (N), em sej. Exemplo: 5.0E14",
            "F": "Emergia Comprada de Fontes Externas (F), em sej. Exemplo: 2.5E14",
            "Y": "Emergia Total do Produto/Sistema (Yield - Y), em sej (opcional).\nSe omitido, será calculado como Y = R + N + F."
        }
        grid_frame_indices = ttk.Frame(self.indices_params_frame) # Frame para layout em grade.
        grid_frame_indices.pack(fill="x", expand=True, pady=5)

        for i, param_key in enumerate(["R", "N", "F", "Y"]): # Cria os campos de entrada.
            col_idx = i % 2  
            row_idx = i // 2 
            
            param_frame = ttk.Frame(grid_frame_indices, padding=(5,3)) # Frame para cada par Label/Entry/Help.
            
            ttk.Label(param_frame, text=f"{param_key}:", width=4, font=(self.controller.APP_FONT_BODY, FONT_SIZE_NORMAL, "bold")).pack(side="left")
            entry = ttk.Entry(param_frame, width=25, font=(self.controller.APP_FONT_BODY, FONT_SIZE_NORMAL))
            entry.pack(side="left", padx=(0,5), expand=True, fill="x")
            self.param_entries_indices[param_key] = entry # Armazena a referência ao Entry.
            
            help_label = ttk.Label(param_frame, text="(?)", style="Help.TLabel", cursor="hand2")
            help_label.pack(side="left")
            Tooltip(help_label, indices_tooltips[param_key], app_font_body=self.controller.APP_FONT_BODY)
            
            param_frame.grid(row=row_idx, column=col_idx, padx=10, pady=8, sticky="ew") # Posiciona na grade.
        
        grid_frame_indices.columnconfigure((0,1), weight=1) # Permite que as colunas da grade se expandam.

        # --- Seção 3: Parâmetros Adicionais (Opcional) ---
        # Para transformidades manuais que sobrescrevem a tabela, etc.
        self.gen_param_lf = ttk.LabelFrame(self, text="3. Parâmetros Adicionais (Ex: Transformidades Manuais)", padding=(20,15))
        self.gen_param_lf.pack(pady=15, padx=0, fill="x") # Sempre visível.
        
        self.param_entry_general = ttk.Entry(self.gen_param_lf, width=70, font=(self.controller.APP_FONT_BODY, FONT_SIZE_NORMAL))
        self.param_entry_general.pack(pady=10, padx=5, fill="x")
        self.param_entry_general.insert(0, "Ex: transformity_NomeDoFluxo=1.0E6; transformity_OutroFluxo=2.5E5") # Texto de exemplo.
        Tooltip(self.param_entry_general, 
                ("Forneça transformidades manuais para fluxos específicos (ex: transformity_EnergiaSolar=1.0; transformity_CombustivelXPTO=6.6E4).\n"
                 "Estes valores têm precedência sobre os da tabela de transformidades.\n"
                 "Use ';' para separar múltiplos parâmetros. Nomes de fluxos devem corresponder aos da LCI (substitua espaços e pontos por '_')."),
                app_font_body=self.controller.APP_FONT_BODY)

        # --- Botões de Ação ---
        action_buttons_frame = ttk.Frame(self, padding=(0,25)) # Frame para os botões principais.
        action_buttons_frame.pack(pady=(15,0)) 
        
        run_button = ttk.Button(action_buttons_frame, text="Executar Cálculo", command=self.run_simulation, style="Primary.TButton", width=28)
        run_button.pack(side="left", padx=(0,10))
        Tooltip(run_button, "Inicia o cálculo emergético com os dados e parâmetros configurados.", app_font_body=self.controller.APP_FONT_BODY)
        
        # Botão para exibir a janela de ajuda sobre os tipos de cálculo.
        calc_types_button = ttk.Button(self, text="Ajuda: Tipos de Cálculos e Parâmetros", command=self.controller.show_calculation_types_window, width=50)
        calc_types_button.pack(pady=15)

        # Inicializa o estado da UI (status e visibilidade dos campos de índice).
        self.update_status_display()
        self.on_calc_type_change() # Chamado para configurar a visibilidade inicial dos campos.

    def on_calc_type_change(self, event=None):
        """
        Chamado quando o tipo de cálculo é alterado no Combobox.
        Controla a visibilidade do frame de parâmetros para Índices Emergéticos.
        """
        selected_display_name = self.calculation_type_var.get()
        active_calc_type_enum = CalculationType.from_display_name(selected_display_name)
        
        if active_calc_type_enum == CalculationType.EMERGY_INDICES:
            # Exibe o frame de parâmetros para índices, posicionando-o antes dos parâmetros gerais.
            self.indices_params_frame.pack(pady=15, padx=0, fill="x", before=self.gen_param_lf)
        else:
            # Oculta o frame de parâmetros para índices.
            self.indices_params_frame.pack_forget() 
        
        self.update_status_display() # Atualiza a mensagem de status.

    def update_status_display(self):
        """
        Atualiza a label de status, informando o usuário sobre a disponibilidade
        de dados e a prontidão para o tipo de cálculo selecionado.
        """
        lci_df = self.controller.data_manager.lci_df
        # Verifica se há dados na LCI e na tabela de transformidades.
        lci_ok = not lci_df.empty # Considera não vazio se tiver linhas OU colunas.
        transformities_ok = bool(self.controller.data_manager.transformities)
        
        status_lci = "LCI: Dados presentes." if lci_ok else "LCI: Sem dados (acesse 'Gerenciamento de Dados')."
        status_trans = "Transformidades: Dados presentes." if transformities_ok else "Transformidades: Sem dados (acesse 'Gerenciamento de Dados')."
        
        ready_message_parts = [] # Lista para construir a mensagem de prontidão.
        selected_display_name = self.calculation_type_var.get()
        active_calc_type_enum = CalculationType.from_display_name(selected_display_name)

        # Lógica específica de prontidão para cada tipo de cálculo.
        if active_calc_type_enum == CalculationType.TOTAL_EMERGY:
            if not lci_ok or lci_df.index.empty: # Requer fluxos (linhas) para este cálculo.
                ready_message_parts.append("Requer dados LCI com fluxos de entrada.")
            if not transformities_ok and (lci_ok and not lci_df.index.empty): 
                ready_message_parts.append("AVISO: Nenhuma transformidade definida na tabela. Forneça-as manualmente ou na aba de Gerenciamento para resultados significativos.")
            elif (lci_ok and not lci_df.index.empty): # Se LCI com fluxos está OK.
                ready_message_parts.append("Pronto para calcular Emergia Total.")

        elif active_calc_type_enum == CalculationType.DIRECT_INPUTS_SUM:
            if not lci_ok or lci_df.index.empty:
                ready_message_parts.append("Requer dados LCI com fluxos de entrada.")
            else:
                ready_message_parts.append("Pronto para calcular Soma dos Inputs Diretos.")
        
        elif active_calc_type_enum == CalculationType.EMERGY_INDICES:
            # Verifica se os campos R, N, F (obrigatórios) estão preenchidos.
            missing_required_indices = []
            for k in ["R", "N", "F"]: # Y é opcional.
                if not self.param_entries_indices[k].get().strip(): # .strip() para ignorar apenas espaços.
                    missing_required_indices.append(k)
            if missing_required_indices:
                ready_message_parts.append(f"Preencha os campos obrigatórios ({', '.join(missing_required_indices)}) para o cálculo de Índices Emergéticos.")
            else:
                ready_message_parts.append("Pronto para calcular Índices Emergéticos.")
        else:
            ready_message_parts.append("Selecione um tipo de cálculo válido na lista.")

        final_ready_msg = " ".join(ready_message_parts) if ready_message_parts else "Verifique a configuração."
        self.status_label.config(text=f"{status_lci}\n{status_trans}\nStatus do Cálculo: {final_ready_msg}")

    def _parse_general_parameters(self) -> tuple[dict, list[str]]:
        """
        Analisa a string de parâmetros gerais (fornecida pelo usuário) e a converte
        em um dicionário de chave-valor.
        Formato esperado: "chave1=valor1;chave2=valor2"
        Retorna um dicionário de parâmetros e uma lista de erros de parsing, se houver.
        """
        params = {}
        errors = []
        raw_string = self.param_entry_general.get()
        
        # Ignora se for o texto de exemplo ou se estiver vazio.
        if raw_string and raw_string.lower().strip() != "ex: transformity_nomedofluxonalci=1.0e6": # Comparação com minúsculas para robustez
            pairs = raw_string.split(';') # Separa os pares por ponto e vírgula.
            for pair_str in pairs:
                pair_str = pair_str.strip()
                if not pair_str: continue # Ignora entradas vazias resultantes do split.
                
                if '=' not in pair_str: # Verifica se o formato chave=valor está presente.
                    errors.append(f"Parâmetro geral ignorado (formato 'chave=valor' esperado, '=' ausente): '{pair_str}'")
                    continue
                
                key, value_str = pair_str.split('=', 1) # Divide no primeiro '='.
                key = key.strip()
                value_str = value_str.strip()
                
                try:
                    # Tenta converter o valor para float; se falhar, mantém como string.
                    params[key] = float(value_str)
                except ValueError:
                    params[key] = value_str 
        return params, errors

    def run_simulation(self):
        """
        Coleta todos os parâmetros de simulação e invoca o EmergyCalculator
        para executar o cálculo selecionado.
        """
        selected_display_name = self.calculation_type_var.get()
        active_calc_type_enum = CalculationType.from_display_name(selected_display_name)

        if not active_calc_type_enum: # Validação do tipo de cálculo.
            messagebox.showerror("Erro Interno de Simulação", "Tipo de cálculo selecionado é inválido.")
            return

        # Validação de dados LCI (necessário para a maioria dos cálculos).
        if active_calc_type_enum != CalculationType.EMERGY_INDICES and self.controller.data_manager.lci_df.empty:
            messagebox.showwarning("Dados LCI Ausentes", 
                                   "A Matriz LCI está vazia. Insira dados na aba 'Gerenciamento de Dados' antes de prosseguir com este cálculo.")
            return

        simulation_params = {"calculation_type_enum": active_calc_type_enum} # Parâmetro base.
        
        # Processa parâmetros gerais (ex: transformidades manuais).
        general_params, gp_errors = self._parse_general_parameters()
        if gp_errors: # Informa o usuário sobre erros nos parâmetros gerais.
            messagebox.showwarning("Aviso sobre Parâmetros Adicionais", 
                                   "Alguns parâmetros adicionais foram ignorados devido a problemas de formato:\n" + "\n".join(gp_errors))
            # O cálculo prossegue, mas o usuário é notificado.
        simulation_params.update(general_params) # Adiciona os parâmetros gerais aos da simulação.

        # Coleta parâmetros específicos para Índices Emergéticos, se aplicável.
        if active_calc_type_enum == CalculationType.EMERGY_INDICES:
            missing_required_fields = False
            for key, entry_widget in self.param_entries_indices.items():
                value_s = entry_widget.get().strip()
                if value_s: # Se o campo foi preenchido.
                    try:
                        simulation_params[key] = float(value_s) # Converte para float.
                    except ValueError:
                        messagebox.showerror("Erro de Parâmetro (Índices)", 
                                             f"O valor fornecido para o índice '{key}' ('{value_s}') deve ser numérico.")
                        return # Interrompe se um valor numérico for inválido.
                elif key != 'Y': # R, N, F são obrigatórios; Y é opcional.
                    messagebox.showerror("Parâmetro Obrigatório (Índices)", 
                                         f"O campo '{key}' é obrigatório para o cálculo de Índices Emergéticos.")
                    missing_required_fields = True
            
            if missing_required_fields:
                return # Interrompe se campos obrigatórios para índices não foram preenchidos.

        # Executa o cálculo através do EmergyCalculator.
        if self.controller.emergy_calculator.calculate_emergy(parameters=simulation_params):
            # Se o cálculo for bem-sucedido (retorna True).
            messagebox.showinfo("Cálculo Concluído", 
                                f"Cálculo de '{selected_display_name}' finalizado com sucesso!\n"
                                "Os resultados estão disponíveis na aba 'Resultados e Gráficos'.")
            self.controller.update_results_display() # Atualiza a aba de resultados.
        # Se calculate_emergy() retornar False, indica um erro crítico,
        # e uma messagebox apropriada já foi exibida pelo método da calculadora.
        
        self.update_status_display() # Atualiza o status da simulação.

class ResultsFrame(ttk.Frame):
    """
    Frame da interface gráfica para a aba "Resultados e Gráficos".
    Exibe os resultados textuais detalhados e uma visualização gráfica
    das contribuições de emergia.
    """
    def __init__(self, parent_notebook: ttk.Notebook, controller):
        super().__init__(parent_notebook, padding=(25,20), style="TFrame")
        self.controller = controller
        self.fig_agg = None # Referência para o canvas do Matplotlib, para limpeza posterior.

        # Frame principal para dividir a aba em duas colunas (texto e gráfico).
        main_results_frame = ttk.Frame(self) 
        main_results_frame.pack(fill=tk.BOTH, expand=True)

        # --- Coluna da Esquerda: Resultados Textuais ---
        text_results_lf = ttk.LabelFrame(main_results_frame, text="Resultados Detalhados (Texto)", padding=(20,15))
        text_results_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,15)) # padx para espaçamento.

        # Frame para o título da seção de texto e o botão de exportar.
        top_text_frame = ttk.Frame(text_results_lf, padding=(0,0,0,15)) 
        top_text_frame.pack(fill="x")
        
        ttk.Label(top_text_frame, text="Relatório do Cálculo Emergético", style="Header.TLabel", 
                  font=(self.controller.APP_FONT_TITLES, FONT_SIZE_LARGE, "bold")).pack(side="left", anchor="w")
        
        self.export_button = ttk.Button(top_text_frame, text="Exportar Texto", command=self.export_results_dialog, style="Primary.TButton", width=18)
        self.export_button.pack(side="right")
        Tooltip(self.export_button, "Salva os resultados textuais exibidos em um arquivo de texto (.txt).", app_font_body=self.controller.APP_FONT_BODY)

        # Widget Text para exibir os resultados.
        self.results_text_widget = tk.Text(text_results_lf, height=20, width=60, wrap="word", state="disabled", 
                                           relief="flat", borderwidth=1, 
                                           font=("Courier New", FONT_SIZE_XSMALL), # Fonte monoespaçada para melhor alinhamento de tabelas.
                                           bg=COLOR_BACKGROUND_PANEL, fg=COLOR_TEXT_PRIMARY, 
                                           padx=15, pady=15, # Padding interno.
                                           selectbackground=COLOR_ACCENT_CYAN_ELECTRIC, 
                                           selectforeground=COLOR_TEXT_ON_ACCENT,
                                           insertbackground=COLOR_ACCENT_CYAN_ELECTRIC) 
        self.results_text_widget.configure(highlightthickness=1, highlightbackground=COLOR_BORDER_ACTIVE) # Borda sutil.
        
        # Scrollbar para o widget Text.
        self.results_scroll = ttk.Scrollbar(text_results_lf, orient="vertical", command=self.results_text_widget.yview, style="Quantum.Vertical.TScrollbar")
        self.results_text_widget.config(yscrollcommand=self.results_scroll.set)
        
        self.results_scroll.pack(side="right", fill="y")
        self.results_text_widget.pack(expand=True, fill="both")

        # --- Coluna da Direita: Visualização Gráfica ---
        chart_lf = ttk.LabelFrame(main_results_frame, text="Visualização Gráfica (Contribuições de Emergia)", padding=(20,15))
        chart_lf.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15,0)) 

        # Frame para o seletor de processo para o gráfico.
        chart_selector_frame = ttk.Frame(chart_lf)
        chart_selector_frame.pack(fill="x", pady=(0,10)) 

        ttk.Label(chart_selector_frame, text="Visualizar gráfico para o Processo/Produto:", 
                  font=(self.controller.APP_FONT_BODY, FONT_SIZE_XSMALL), 
                  foreground=COLOR_TEXT_SECONDARY).pack(side="left", padx=(0,10), pady=(0,5))

        self.chart_data_selector_var = tk.StringVar() # Variável Tkinter para o Combobox.
        self.chart_data_selector = ttk.Combobox(chart_selector_frame, textvariable=self.chart_data_selector_var, 
                                                state="readonly", width=35, 
                                                font=(self.controller.APP_FONT_BODY, FONT_SIZE_SMALL), 
                                                style="TCombobox")
        self.chart_data_selector.pack(side="left", pady=(0,5))
        self.chart_data_selector.bind("<<ComboboxSelected>>", self.update_pie_chart_from_event) # Evento ao selecionar.
        Tooltip(self.chart_data_selector, 
                "Selecione um processo/produto para visualizar o gráfico de pizza com a contribuição de emergia de cada fluxo de entrada.\n(Disponível após cálculo de 'Emergia Total por Processo').", 
                app_font_body=self.controller.APP_FONT_BODY)
        
        # Frame onde o gráfico Matplotlib será incorporado.
        self.chart_display_frame = ttk.Frame(chart_lf, style="Glass.TFrame") # Estilo "Glass" para o fundo.
        self.chart_display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Inicializa a exibição (vazia ou com mensagem padrão).
        self.display_results_and_chart(None)


    def display_results_and_chart(self, results_data: dict | None):
        """
        Exibe os resultados textuais no widget Text e atualiza o seletor
        e o gráfico de pizza com base nos dados fornecidos.
        """
        self.results_text_widget.config(state="normal") # Habilita edição para inserir texto.
        self.results_text_widget.delete("1.0", tk.END)  # Limpa o conteúdo anterior.

        current_results_to_display = results_data.copy() if results_data else {} # Cria uma cópia para evitar modificar o original.

        if current_results_to_display:
            # Extrai e exibe o sumário do cálculo.
            summary = current_results_to_display.pop("calculation_summary", "Sumário do cálculo não disponível.")
            self.results_text_widget.insert(tk.END, "--- Sumário do Cálculo Realizado ---\n", "tag_header_results")
            self.results_text_widget.insert(tk.END, summary + "\n\n", "tag_summary_text_results")

            # Exibe os resultados detalhados restantes.
            if current_results_to_display: 
                self.results_text_widget.insert(tk.END, "--- Detalhes dos Resultados Numéricos ---\n\n", "tag_header_results")
                for key, value in current_results_to_display.items():
                    # Formata o nome da chave para exibição.
                    display_key = key.replace('_', ' ').title()
                    self.results_text_widget.insert(tk.END, f"== {display_key} ==\n", "tag_subheader_results")
                    
                    # Formata o valor para exibição (trata DataFrames/Series Pandas de forma especial).
                    if isinstance(value, (pd.Series, pd.DataFrame)):
                        try:
                            # Função para formatar números dentro do DataFrame/Series.
                            def custom_float_formatter(x):
                                if isinstance(x, (float, np.number)):
                                    if pd.isna(x): return "-"
                                    if x == 0: return "0"
                                    # Usa notação científica para números muito grandes ou pequenos, senão decimal.
                                    return f"{x:.3e}" if abs(x) > 1e6 or (abs(x) < 1e-3 and x!=0) else f"{x:,.3f}"
                                return str(x)

                            if isinstance(value, pd.DataFrame):
                                # Aplica o formatador apenas às colunas numéricas.
                                num_cols = value.select_dtypes(include=np.number).columns
                                formatters_dict = {col: custom_float_formatter for col in num_cols}
                                value_str = value.to_string(formatters=formatters_dict)
                            else: # pd.Series
                                value_str = value.apply(custom_float_formatter).to_string()
                        except Exception as e_format: # Fallback se a formatação falhar.
                            print(f"Alerta: Falha ao formatar resultado '{key}': {e_format}")
                            value_str = value.to_string()
                    else:
                        value_str = str(value)
                    self.results_text_widget.insert(tk.END, value_str + "\n\n")
            elif not summary.startswith("Sumário do cálculo não disponível"): 
                self.results_text_widget.insert(tk.END, "Nenhum resultado detalhado adicional para este cálculo.")
        else: # Se não houver resultados.
            self.results_text_widget.insert(tk.END, "Nenhum resultado para exibir no momento.\n"
                                                    "Execute um cálculo na aba 'Simulação Emergética'.")

        # Configuração das tags de estilo para o texto inserido.
        self.results_text_widget.tag_configure("tag_header_results", 
                                               font=(self.controller.APP_FONT_TITLES, FONT_SIZE_MEDIUM, "bold"), 
                                               foreground=COLOR_ACCENT_CYAN_ELECTRIC, 
                                               spacing1=12, spacing3=12, underline=True) 
        self.results_text_widget.tag_configure("tag_subheader_results", 
                                               font=("Courier New", FONT_SIZE_NORMAL, "bold"), 
                                               foreground=COLOR_ACCENT_CYAN_ELECTRIC, 
                                               spacing1=10, spacing3=5)
        self.results_text_widget.tag_configure("tag_summary_text_results", 
                                               font=(self.controller.APP_FONT_BODY, FONT_SIZE_SMALL), 
                                               lmargin1=15, lmargin2=15, # Indentação para o sumário.
                                               foreground=COLOR_TEXT_PRIMARY)
        
        self.results_text_widget.config(state="disabled") # Bloqueia a edição do texto novamente.

        # Atualiza o seletor de dados para o gráfico e o próprio gráfico.
        self.populate_chart_selector(results_data if results_data else {})
        self.update_pie_chart(original_results_data=results_data if results_data else {})


    def populate_chart_selector(self, results_data: dict):
        """Popula o Combobox de seleção de processo para o gráfico de pizza."""
        options = ["Nenhum"] # Opção padrão.
        # Adiciona processos à lista de opções se o resultado de "total_emergy_per_process" existir.
        if (results_data and 
            "total_emergy_per_process" in results_data and 
            isinstance(results_data["total_emergy_per_process"], pd.Series) and 
            not results_data["total_emergy_per_process"].empty):
            
            options.extend(results_data["total_emergy_per_process"].index.tolist()) # Adiciona os nomes dos processos.
        
        self.chart_data_selector['values'] = options # Atualiza as opções do Combobox.
        if len(options) > 1: # Se houver processos além de "Nenhum".
            self.chart_data_selector.set(options[1]) # Seleciona o primeiro processo real da lista.
        else:
            self.chart_data_selector.set(options[0]) # Mantém "Nenhum" selecionado.

    def update_pie_chart_from_event(self, event=None):
        """Chamado pelo evento <<ComboboxSelected>> do seletor de processo para atualizar o gráfico."""
        # Os resultados atuais já devem estar armazenados no EmergyCalculator.
        self.update_pie_chart() 

    def update_pie_chart(self, original_results_data: dict | None = None):
        """Atualiza ou cria o gráfico de pizza de contribuições de emergia."""
        # Limpa o gráfico anterior, se existir.
        if self.fig_agg:
            self.fig_agg.get_tk_widget().destroy()
            self.fig_agg = None
        for widget in self.chart_display_frame.winfo_children(): # Limpa o frame do gráfico.
            widget.destroy()

        # Obtém os resultados atuais.
        current_results = original_results_data
        if current_results is None: # Se não foram passados, obtém do calculator.
            current_results = self.controller.emergy_calculator.get_results() if self.controller.emergy_calculator else {}
        
        if not current_results: # Se não há resultados.
            ttk.Label(self.chart_display_frame, text="Não há dados de resultados para gerar o gráfico.", 
                      style="Status.TLabel", background=COLOR_BACKGROUND_GLASS_EFFECT, justify="center").pack(padx=10, pady=10, expand=True)
            return

        selected_process_for_chart = self.chart_data_selector_var.get() # Processo selecionado pelo usuário.

        # Verifica se os dados necessários para o gráfico estão presentes e válidos.
        required_key = "emergy_per_input_flow_for_each_process" # Chave dos dados de contribuição.
        if (not selected_process_for_chart or selected_process_for_chart == "Nenhum" or
            required_key not in current_results or
            not isinstance(current_results[required_key], pd.DataFrame) or # Deve ser um DataFrame.
            selected_process_for_chart not in current_results[required_key].columns): # O processo deve ser uma coluna.
            
            ttk.Label(self.chart_display_frame, 
                      text="Selecione um processo válido para visualizar o gráfico de contribuições.\n(Disponível após cálculo de 'Emergia Total por Processo').", 
                      style="Status.TLabel", background=COLOR_BACKGROUND_GLASS_EFFECT, justify="center").pack(padx=10, pady=10, expand=True)
            return

        df_contributions_all_processes = current_results[required_key]
        # Filtra dados para o processo selecionado e remove valores zero ou negativos (ou muito pequenos).
        data_for_selected_process_chart = df_contributions_all_processes[selected_process_for_chart][df_contributions_all_processes[selected_process_for_chart] > 1e-9] 

        if data_for_selected_process_chart.empty: # Se não há dados significativos para o gráfico.
            ttk.Label(self.chart_display_frame, 
                      text=f"Não há contribuições de emergia significativas (>0)\npara o processo '{selected_process_for_chart}'.", 
                      style="Status.TLabel", background=COLOR_BACKGROUND_GLASS_EFFECT, justify="center").pack(padx=10, pady=10, expand=True)
            return

        labels = data_for_selected_process_chart.index # Nomes dos fluxos (rótulos das fatias).
        sizes = data_for_selected_process_chart.values  # Valores de emergia (tamanhos das fatias).

        # Criação da figura e do eixo Matplotlib.
        fig = Figure(figsize=(5.5, 4.5), dpi=100, facecolor=COLOR_BACKGROUND_GLASS_EFFECT) 
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLOR_BACKGROUND_GLASS_EFFECT) # Cor de fundo do eixo.

        # Define a paleta de cores para o gráfico de pizza.
        try:
            cmap = plt.get_cmap('viridis') # Tenta usar um colormap vibrante.
            pie_colors = cmap(np.linspace(0.1, 0.9, len(labels))) # Seleciona cores espaçadas do colormap.
        except: # Fallback para cores definidas manualmente se o colormap falhar.
            pie_colors = [COLOR_ACCENT_CYAN_ELECTRIC, COLOR_ACCENT_MAGENTA_NEON, "#FFD700", "#32CD32", "#FF6347", "#8A2BE2"]
            pie_colors = pie_colors[:len(labels)] # Garante o número correto de cores.

        # Define as propriedades de fonte para os textos do gráfico.
        font_props_title = FontProperties(family=self.controller.APP_FONT_TITLES, size=FONT_SIZE_NORMAL -1)
        font_props_autotext = FontProperties(family=self.controller.APP_FONT_BODY, size=FONT_SIZE_XSMALL -1, weight="bold")
        font_props_legend = FontProperties(family=self.controller.APP_FONT_BODY, size=FONT_SIZE_XXSMALL) 
        font_props_legend_title = FontProperties(family=self.controller.APP_FONT_BODY, size=FONT_SIZE_XSMALL, weight='bold') 

        # Desenha o gráfico de pizza.
        wedges, texts, autotexts = ax.pie(sizes, 
                                          labels=None, # Rótulos serão exibidos na legenda.
                                          autopct='%1.1f%%', # Formato da porcentagem nas fatias.
                                          startangle=140,    # Ângulo inicial da primeira fatia.
                                          colors=pie_colors,
                                          pctdistance=0.85,  # Distância do texto percentual do centro.
                                          wedgeprops={'edgecolor': COLOR_BACKGROUND_DEEP_SPACE, 'linewidth': 1.5}) # Borda das fatias.

        # Configura a cor e fonte dos textos de porcentagem.
        for autotext_obj in autotexts:
            autotext_obj.set_color(COLOR_BACKGROUND_DEEP_SPACE) 
            autotext_obj.set_fontproperties(font_props_autotext)
        
        ax.set_title(f"Contribuição de Emergia para\n'{selected_process_for_chart}'", 
                     color=COLOR_ACCENT_CYAN_ELECTRIC, fontproperties=font_props_title)
        
        # Adiciona legenda se houver um número razoável de fatias (para não poluir o gráfico).
        if len(labels) <= 7: 
            legend = ax.legend(wedges, labels, 
                               title="Fluxos de Entrada", 
                               loc="center left", 
                               bbox_to_anchor=(1.05, 0.5), # Posiciona a legenda à direita do gráfico.
                               prop=font_props_legend,
                               facecolor=COLOR_BACKGROUND_PANEL_LIGHTER, 
                               labelcolor=COLOR_TEXT_PRIMARY, 
                               edgecolor=COLOR_BORDER_SUBTLE,
                               title_fontproperties=font_props_legend_title)
            if legend: # Configura a cor do título da legenda.
                plt.setp(legend.get_title(), color=COLOR_ACCENT_CYAN_ELECTRIC)


        fig.tight_layout(pad=2.0) # Ajusta o layout para evitar sobreposições.

        # Integra o canvas Matplotlib na interface Tkinter.
        canvas = FigureCanvasTkAgg(fig, master=self.chart_display_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg=COLOR_BACKGROUND_GLASS_EFFECT) # Garante que o widget do canvas tenha o fundo correto.
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        self.fig_agg = canvas # Armazena a referência ao canvas para limpeza posterior.

    def export_results_dialog(self):
        """Abre um diálogo para o usuário salvar os resultados textuais em um arquivo."""
        content_to_export = self.results_text_widget.get("1.0", tk.END).strip() # Obtém todo o texto do widget.
        if not content_to_export or content_to_export.startswith("Nenhum resultado para exibir"):
            messagebox.showinfo("Nada para Exportar", "Não há resultados textuais para serem exportados no momento.", parent=self)
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Gera um timestamp para o nome do arquivo.
        default_filename = f"Resultados_Calculo_Emergia_{timestamp}.txt"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
            title="Salvar Relatório de Resultados Como...",
            initialfile=default_filename,
            initialdir=DATA_DIR 
        )
        
        if filepath: # Se o usuário selecionou um caminho e nome de arquivo.
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Relatório da Calculadora de Emergia Quântica\n")
                    f.write(f"Exportado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*70 + "\n\n") # Linha separadora.
                    f.write(content_to_export)
                messagebox.showinfo("Exportação Concluída", f"Relatório de resultados salvo com sucesso em:\n{filepath}", parent=self)
            except Exception as e:
                messagebox.showerror("Erro ao Exportar Arquivo", f"Não foi possível salvar o arquivo de resultados.\nDetalhes: {e}", parent=self)
                print(f"ERRO DETALHADO em export_results_dialog: {e}\n{traceback.format_exc()}")

# --- Classe Principal da Aplicação ---
class Application(tk.Tk):
    """
    Classe principal da aplicação Tkinter.
    Responsável por inicializar a janela principal, configurar estilos,
    criar as abas de navegação e gerenciar a comunicação entre os
    diferentes componentes da interface.
    """
    def __init__(self, data_manager: DataManager, emergy_calculator: EmergyCalculator):
        super().__init__() # Inicializa a classe base Tk.

        self.data_manager = data_manager # Instância do gerenciador de dados.
        self.emergy_calculator = emergy_calculator # Instância da calculadora de emergia.

        # Determina as famílias de fonte a serem usadas, com fallbacks.
        self.APP_FONT_TITLES = self._get_font_family(FONT_FAMILY_TITLES, FONT_FAMILY_FALLBACK_SANS, FONT_FAMILY_FALLBACK_GENERIC)
        self.APP_FONT_BODY = self._get_font_family(FONT_FAMILY_BODY, FONT_FAMILY_FALLBACK_SANS, FONT_FAMILY_FALLBACK_GENERIC)
        print(f"Info: Fonte de Títulos configurada: {self.APP_FONT_TITLES}")
        print(f"Info: Fonte de Corpo configurada: {self.APP_FONT_BODY}")

        # Configurações da janela principal.
        self.title(WINDOW_TITLE) 
        self.geometry(WINDOW_GEOMETRY) 
        self.configure(bg=COLOR_BACKGROUND_DEEP_SPACE) 

        # Tenta maximizar a janela na inicialização.
        try:
            self.state('zoomed') 
        except tk.TclError:
            # Tentativas de fallback para diferentes sistemas operacionais.
            if os.name == 'nt': # Windows
                try:
                    self.wm_state('zoomed') 
                except tk.TclError:
                    print("Alerta: Falha ao maximizar janela via 'wm_state'. Tentando 'attributes'.")
                    try: self.attributes('-zoomed', True)
                    except tk.TclError: print("Alerta: Falha ao maximizar janela via 'attributes'.")
            elif os.name == 'posix': # Linux/macOS
                try: 
                    self.attributes('-zoomed', True) 
                except tk.TclError:
                    print("Alerta: Falha ao maximizar janela via 'state(\"zoomed\")' ou 'attributes(\"-zoomed\", True)'. A janela pode não iniciar maximizada.")
            else: 
                print("Alerta: Não foi possível determinar o método para maximizar a janela neste sistema operacional.")


        self.style = ttk.Style(self) # Objeto para gerenciar estilos ttk.
        self._configure_styles() # Aplica os estilos customizados.

        self.frames = {} # Dicionário para armazenar referências às abas (frames).
        self._create_tabs() # Cria as abas da aplicação.

    def _get_font_family(self, preferred_font: str, fallback1: str, fallback2: str) -> str:
        """
        Tenta carregar a fonte preferida. Se não disponível, tenta o primeiro fallback,
        e então o segundo fallback. Retorna o nome da família de fonte que foi carregada com sucesso.
        """
        try:
            tkFont.Font(family=preferred_font).actual() # Verifica se a fonte existe.
            return preferred_font
        except tk.TclError:
            print(f"Alerta: Fonte '{preferred_font}' não encontrada. Tentando fallback '{fallback1}'.")
            try:
                tkFont.Font(family=fallback1).actual()
                return fallback1
            except tk.TclError:
                print(f"Alerta: Fonte de fallback '{fallback1}' não encontrada. Utilizando fallback genérico '{fallback2}'.")
                return fallback2 # Retorna o fallback mais genérico se os outros falharem.

    def _configure_styles(self):
        """Configura todos os estilos ttk para a aplicação, definindo a aparência dos widgets."""
        self.style.theme_use('clam') # Tema base que permite maior customização.

        # Configuração de estilo base para todos os widgets ttk.
        self.style.configure(".", 
                             background=COLOR_BACKGROUND_DEEP_SPACE, 
                             foreground=COLOR_TEXT_PRIMARY, 
                             font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL),
                             borderwidth=0, 
                             focuscolor=COLOR_ACCENT_CYAN_ELECTRIC) # Cor do anel de foco.

        # Estilos específicos para diferentes tipos de widgets.
        self.style.configure("TFrame", background=COLOR_BACKGROUND_DEEP_SPACE)
        self.style.configure("TLabel", background=COLOR_BACKGROUND_DEEP_SPACE, foreground=COLOR_TEXT_PRIMARY, font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL))
        
        self.style.configure("Title.TLabel", font=(self.APP_FONT_TITLES, FONT_SIZE_XXLARGE, "bold"), foreground=COLOR_ACCENT_CYAN_ELECTRIC, padding=(0, 15, 0, 25)) 
        self.style.configure("Header.TLabel", font=(self.APP_FONT_TITLES, FONT_SIZE_XLARGE, "bold"), foreground=COLOR_ACCENT_CYAN_ELECTRIC)
        self.style.configure("Help.TLabel", foreground=COLOR_ACCENT_CYAN_ELECTRIC, font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL, "italic"))
        self.style.configure("Instruction.TLabel", font=(self.APP_FONT_BODY, FONT_SIZE_SMALL), foreground=COLOR_TEXT_SECONDARY, wraplength=750, padding=(0,5,0,10)) 
        self.style.configure("Status.TLabel", font=(self.APP_FONT_BODY, FONT_SIZE_SMALL), foreground=COLOR_TEXT_SECONDARY, wraplength=850, padding=8)

        # Estilo para botões ttk.Button.
        self.style.configure("TButton", 
                             font=(self.APP_FONT_BODY, FONT_SIZE_MEDIUM), 
                             padding=(12, 8), 
                             borderwidth=2, 
                             relief="flat", 
                             background=COLOR_BACKGROUND_PANEL, 
                             foreground=COLOR_ACCENT_CYAN_ELECTRIC,
                             bordercolor=COLOR_BORDER_BUTTON_LIGHT) 
        self.style.map("TButton", # Define aparência para diferentes estados do botão.
                       background=[('active', COLOR_ACCENT_CYAN_ELECTRIC), ('pressed', COLOR_ACCENT_CYAN_ELECTRIC), ('hover', COLOR_BACKGROUND_PANEL_LIGHTER)],
                       foreground=[('active', COLOR_TEXT_ON_ACCENT), ('pressed', COLOR_TEXT_ON_ACCENT), ('hover', COLOR_ACCENT_CYAN_ELECTRIC)],
                       bordercolor=[('active', COLOR_ACCENT_CYAN_ELECTRIC), ('focus', COLOR_ACCENT_CYAN_ELECTRIC), ('hover', COLOR_ACCENT_CYAN_ELECTRIC)],
                       relief=[('hover', 'raised'), ('pressed', 'sunken'), ('!pressed', 'flat')])

        # Estilo para botões primários (com maior destaque).
        self.style.configure("Primary.TButton", 
                             font=(self.APP_FONT_BODY, FONT_SIZE_MEDIUM, "bold"), 
                             background=COLOR_ACCENT_CYAN_ELECTRIC, 
                             foreground=COLOR_TEXT_ON_ACCENT,
                             borderwidth=2,
                             bordercolor=COLOR_BORDER_BUTTON_LIGHT, 
                             relief="flat")
        self.style.map("Primary.TButton",
                       background=[('hover', "#0FB8DA"), ('active', "#0DA5C3"), ('pressed', '#0BA0B8')], # Leves variações de cor para interação.
                       bordercolor=[('hover', COLOR_BORDER_BUTTON_LIGHT), ('active', COLOR_BORDER_BUTTON_LIGHT), ('focus', COLOR_BORDER_BUTTON_LIGHT)],
                       relief=[('hover', 'raised'), ('pressed', 'sunken'), ('!pressed', 'flat')])

        # Estilo para o widget Notebook (abas).
        self.style.configure("TNotebook", background=COLOR_BACKGROUND_DEEP_SPACE, borderwidth=0, tabposition='nw') # 'nw' para abas no topo à esquerda.
        self.style.configure("TNotebook.Tab", 
                             font=(self.APP_FONT_BODY, FONT_SIZE_MEDIUM, "bold"), 
                             padding=[18, 10], # Padding horizontal e vertical da aba.
                             background=COLOR_BACKGROUND_PANEL, 
                             foreground=COLOR_TEXT_SECONDARY,
                             borderwidth=0)
        self.style.map("TNotebook.Tab", # Aparência da aba selecionada ou sob o cursor.
                       background=[('selected', COLOR_BACKGROUND_GLASS_EFFECT), ('active', COLOR_BACKGROUND_PANEL_LIGHTER)], 
                       foreground=[('selected', COLOR_ACCENT_CYAN_ELECTRIC), ('active', COLOR_TEXT_PRIMARY)],
                       bordercolor=[('selected', COLOR_ACCENT_CYAN_ELECTRIC)], 
                       lightcolor=[('selected', COLOR_BACKGROUND_GLASS_EFFECT)], 
                       darkcolor=[('selected', COLOR_BACKGROUND_GLASS_EFFECT)])


        # Estilo para Comboboxes.
        self.style.configure("TCombobox", 
                             font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL), 
                             padding=8, 
                             fieldbackground=COLOR_BACKGROUND_PANEL, # Fundo do campo de texto.
                             foreground=COLOR_TEXT_PRIMARY, 
                             bordercolor=COLOR_BORDER_SUBTLE,
                             arrowcolor=COLOR_ACCENT_CYAN_ELECTRIC, # Cor da seta dropdown.
                             selectbackground=COLOR_BACKGROUND_PANEL, # Fundo da lista dropdown.
                             selectforeground=COLOR_ACCENT_CYAN_ELECTRIC) # Cor do item selecionado na lista.
        self.style.map('TCombobox', 
                       fieldbackground=[('readonly', COLOR_BACKGROUND_PANEL), ('focus', COLOR_BACKGROUND_PANEL_LIGHTER)],
                       foreground=[('readonly', COLOR_TEXT_PRIMARY)],
                       bordercolor=[('focus', COLOR_ACCENT_CYAN_ELECTRIC)])
        # Estilização da Listbox interna do Combobox (requer option_add).
        self.option_add('*TCombobox*Listbox.background', COLOR_BACKGROUND_PANEL_LIGHTER)
        self.option_add('*TCombobox*Listbox.foreground', COLOR_TEXT_PRIMARY)
        self.option_add('*TCombobox*Listbox.selectBackground', COLOR_ACCENT_CYAN_ELECTRIC)
        self.option_add('*TCombobox*Listbox.selectForeground', COLOR_TEXT_ON_ACCENT)
        self.option_add('*TCombobox*Listbox.font', (self.APP_FONT_BODY, FONT_SIZE_SMALL))


        # Estilo para Treeviews (tabelas).
        self.style.configure("Treeview", 
                             font=(self.APP_FONT_BODY, FONT_SIZE_SMALL), 
                             rowheight=30, # Altura de cada linha.
                             background=COLOR_BACKGROUND_PANEL, 
                             fieldbackground=COLOR_BACKGROUND_PANEL, # Fundo das células.
                             foreground=COLOR_TEXT_PRIMARY,
                             borderwidth=1, relief="solid", bordercolor=COLOR_BORDER_SUBTLE)
        self.style.map("Treeview", # Aparência da linha selecionada.
                       background=[('selected', COLOR_ACCENT_CYAN_ELECTRIC)],
                       foreground=[('selected', COLOR_TEXT_ON_ACCENT)])
        
        self.style.configure("Treeview.Heading", # Cabeçalho da tabela.
                             font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL, "bold"), 
                             background=COLOR_ACCENT_CYAN_ELECTRIC, 
                             foreground=COLOR_TEXT_ON_ACCENT,
                             padding=10, relief="flat")
        self.style.map("Treeview.Heading", background=[('active', "#0DA5C3")]) # Hover no cabeçalho.

        # Estilo para LabelFrames (frames com título).
        self.style.configure("TLabelFrame", 
                             background=COLOR_BACKGROUND_DEEP_SPACE, 
                             bordercolor=COLOR_BORDER_SUBTLE, 
                             font=(self.APP_FONT_TITLES, FONT_SIZE_LARGE), 
                             padding=15, relief="groove", borderwidth=1)
        self.style.configure("TLabelFrame.Label", # Texto do título do LabelFrame.
                             background=COLOR_BACKGROUND_DEEP_SPACE, 
                             foreground=COLOR_ACCENT_CYAN_ELECTRIC, 
                             font=(self.APP_FONT_TITLES, FONT_SIZE_LARGE, "bold"),
                             padding=(0,0,10,5)) # Padding abaixo do título.

        # Estilo para campos de entrada de texto (TEntry).
        self.style.configure("TEntry", 
                             font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL), 
                             padding=10, relief="flat", 
                             fieldbackground=COLOR_BACKGROUND_PANEL, 
                             foreground=COLOR_TEXT_PRIMARY,
                             borderwidth=1, bordercolor=COLOR_BORDER_SUBTLE,
                             insertcolor=COLOR_ACCENT_CYAN_ELECTRIC) # Cor do cursor de texto.
        self.style.map("TEntry", 
                       bordercolor=[('focus', COLOR_ACCENT_CYAN_ELECTRIC)], 
                       fieldbackground=[('focus', COLOR_BACKGROUND_PANEL_LIGHTER)])

        # Estilos para as Tooltips.
        self.style.configure("Tooltip.TFrame", background=COLOR_TOOLTIP_BG, bordercolor=COLOR_ACCENT_CYAN_ELECTRIC, borderwidth=1)
        self.style.configure("Tooltip.TLabel", background=COLOR_TOOLTIP_BG, foreground=COLOR_TOOLTIP_TEXT, font=(self.APP_FONT_BODY, FONT_SIZE_XSMALL))

        # Estilos para as Scrollbars.
        self.style.configure("Quantum.Vertical.TScrollbar", 
                             troughcolor=COLOR_BACKGROUND_PANEL, # Cor do "trilho" da scrollbar.
                             bordercolor=COLOR_BORDER_SUBTLE, 
                             background=COLOR_ACCENT_CYAN_ELECTRIC, # Cor da barra de rolagem em si.
                             arrowcolor=COLOR_BACKGROUND_DEEP_SPACE) # Cor das setas.
        self.style.configure("Quantum.Horizontal.TScrollbar", 
                             troughcolor=COLOR_BACKGROUND_PANEL, 
                             bordercolor=COLOR_BORDER_SUBTLE, 
                             background=COLOR_ACCENT_CYAN_ELECTRIC, 
                             arrowcolor=COLOR_BACKGROUND_DEEP_SPACE)
        
        # Estilo "Glass" para Frames, usado para fundos com efeito translúcido.
        self.style.configure("Glass.TFrame", 
                             background=COLOR_BACKGROUND_GLASS_EFFECT, 
                             bordercolor=COLOR_BORDER_SUBTLE, 
                             borderwidth=1)
        
        # Estilo para o Frame do cabeçalho na janela de ajuda.
        self.style.configure("HeaderFrame.TFrame", background=COLOR_BACKGROUND_DEEP_SPACE)


    def _create_tabs(self):
        """Cria o widget Notebook e adiciona as abas (Frames) da aplicação."""
        # Container principal para o Notebook, com padding ao redor.
        container = ttk.Frame(self, padding=20) 
        container.pack(fill=tk.BOTH, expand=True) # Ocupa todo o espaço disponível na janela.

        notebook = ttk.Notebook(container, style="TNotebook") # Cria o widget de abas.
        
        # Define as classes de Frame para cada aba e o texto que aparecerá na aba.
        tab_definitions = [
            ("Gerenciamento de Dados", DataManagementFrame),
            ("Simulação Emergética", SimulationFrame),
            ("Resultados e Gráficos", ResultsFrame)
        ]

        for tab_name, FrameClass in tab_definitions:
            # Cria uma instância da classe do Frame da aba, passando 'self' (Application) como controller.
            frame_instance = FrameClass(notebook, self) 
            notebook.add(frame_instance, text=tab_name, padding=15) # Adiciona a aba ao Notebook.
            self.frames[FrameClass] = frame_instance # Armazena a referência à instância da aba.
            
        notebook.pack(expand=True, fill=tk.BOTH, pady=(15,0)) # pady para espaçamento acima do notebook.

    # --- Métodos de Callback e Atualização da UI ---
    # Funções chamadas por outras partes do código para manter a interface sincronizada.

    def update_results_display(self):
        """Solicita à aba de Resultados que atualize sua exibição com os dados mais recentes."""
        if ResultsFrame in self.frames: # Verifica se a aba de resultados existe.
            self.frames[ResultsFrame].display_results_and_chart(self.emergy_calculator.get_results())

    def update_data_management_displays(self):
        """Solicita à aba de Gerenciamento de Dados que atualize suas tabelas (LCI e Transformidades)."""
        if DataManagementFrame in self.frames:
            self.frames[DataManagementFrame].refresh_lci_display()
            self.frames[DataManagementFrame].refresh_transformity_display()
    
    def update_simulation_status(self):
        """Solicita à aba de Simulação que atualize sua mensagem de status."""
        if SimulationFrame in self.frames:
            self.frames[SimulationFrame].update_status_display()

    def update_all_displays(self):
        """
        Função utilitária para atualizar todas as partes relevantes da interface.
        Útil, por exemplo, após carregar dados de uma sessão.
        """
        self.update_data_management_displays()
        self.update_simulation_status()
        # Limpa os resultados anteriores para evitar confusão com dados de uma sessão antiga.
        if self.emergy_calculator: self.emergy_calculator.results = None 
        self.update_results_display() 


    def show_calculation_types_window(self):
        """
        Exibe uma janela Toplevel (secundária) com informações de ajuda
        sobre os diferentes tipos de cálculos suportados pela aplicação.
        """
        help_window = tk.Toplevel(self) # Cria a nova janela.
        help_window.title("Ajuda: Tipos de Cálculos e Parâmetros Requeridos")
        help_window.geometry("950x780") # Define o tamanho da janela de ajuda.
        help_window.transient(self) # Mantém a janela de ajuda sobre a janela principal.
        help_window.grab_set()      # Bloqueia interação com a janela principal enquanto a ajuda estiver aberta.
        help_window.configure(bg=COLOR_BACKGROUND_PANEL) # Cor de fundo da janela de ajuda.

        # Frame para o cabeçalho da janela de ajuda.
        header_frame = ttk.Frame(help_window, style="HeaderFrame.TFrame", padding=15)
        header_frame.pack(fill="x", pady=(10,0))
        
        main_label = ttk.Label(header_frame, text="Tipos de Cálculos e Parâmetros Requeridos", 
                               style="Header.TLabel", background=COLOR_BACKGROUND_DEEP_SPACE) 
        main_label.pack(pady=(10,5))

        # Texto introdutório com informações gerais.
        info_text_content = (
            "A seguir, são detalhados os tipos de cálculo suportados pela aplicação e os respectivos parâmetros necessários.\n"
            "Os dados de Inventário do Ciclo de Vida (LCI) e Transformidades (UEVs) são gerenciados na aba 'Gerenciamento de Dados'.\n"
            "Parâmetros adicionais, como transformidades manuais que sobrescrevem os valores da tabela, podem ser inseridos no campo 'Parâmetros Adicionais' na aba 'Simulação Emergética'.\n"
            "Para o cálculo de 'Índices Emergéticos', utilize os campos dedicados R, N, F e Y (opcional) na aba de Simulação."
        )
        info_label = ttk.Label(help_window, text=info_text_content, justify="left", wraplength=850, 
                               font=(self.APP_FONT_BODY, FONT_SIZE_SMALL), 
                               background=COLOR_BACKGROUND_PANEL, foreground=COLOR_TEXT_SECONDARY)
        info_label.pack(pady=(5,20), padx=20)

        # Lista com os exemplos de cada tipo de cálculo.
        calculation_examples_data = [
            ("1. Soma dos Inputs Diretos por Processo", 
             f"Tipo de Cálculo (selecionar na Simulação): '{CalculationType.get_display_names_map()[CalculationType.DIRECT_INPUTS_SUM]}'\n"
             "Descrição: Realiza a soma das quantidades físicas (ex: kg, MJ) de todos os fluxos de entrada listados na Matriz LCI para cada processo ou produto final. Não utiliza valores de transformidade.\n"
             "Parâmetros Necessários: Matriz LCI devidamente preenchida."),
            
            ("2. Cálculo da Emergia Total por Processo", 
             f"Tipo de Cálculo (selecionar na Simulação): '{CalculationType.get_display_names_map()[CalculationType.TOTAL_EMERGY]}'\n"
             "Descrição: Calcula a emergia total (em sej) para cada processo/produto. Este cálculo multiplica cada fluxo de entrada da LCI pela sua respectiva transformidade (UEV) e, em seguida, soma os resultados por processo.\n"
             "Parâmetros Necessários:\n"
             "  - Matriz LCI preenchida.\n"
             "  - Tabela de Transformidades preenchida (na aba 'Gerenciamento de Dados') para os fluxos de entrada relevantes.\n"
             "  - Opcional: Transformidades manuais podem ser fornecidas no campo 'Parâmetros Adicionais' (ex: transformity_EnergiaSolar=1.0E0; transformity_CombustivelX=6.6E4). Estes valores têm precedência sobre os da tabela."),
            
            ("3. Cálculo de Índices Emergéticos (EYR, ELR, ESI)", 
             f"Tipo de Cálculo (selecionar na Simulação): '{CalculationType.get_display_names_map()[CalculationType.EMERGY_INDICES]}'\n"
             "Descrição: Calcula os principais índices de avaliação emergética:\n"
             "  - EYR (Emergy Yield Ratio): Taxa de Rendimento Emergético.\n"
             "  - ELR (Environmental Loading Ratio): Taxa de Carga Ambiental.\n"
             "  - ESI (Emergy Sustainability Index): Índice de Sustentabilidade Emergética.\n"
             "Parâmetros Necessários (a serem fornecidos nos campos dedicados na aba 'Simulação Emergética'):\n"
             "  - R: Emergia Renovável Local (em sej).\n"
             "  - N: Emergia Não-Renovável Local (em sej).\n"
             "  - F: Emergia Comprada de Fontes Externas (em sej).\n"
             "  - Y (Opcional): Emergia Total do Produto/Sistema (Yield, em sej). Se não fornecido, será calculado como Y = R + N + F.")
        ]

        # Frame para o texto de ajuda com barra de rolagem.
        text_display_frame = ttk.Frame(help_window, padding=(15,10), style="Glass.TFrame") 
        text_display_frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        help_text_widget = tk.Text(text_display_frame, wrap="word", 
                                   font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL), 
                                   relief="flat", borderwidth=0, spacing1=10, spacing3=10,
                                   bg=COLOR_BACKGROUND_GLASS_EFFECT, fg=COLOR_TEXT_PRIMARY, 
                                   padx=15, pady=15,
                                   selectbackground=COLOR_ACCENT_CYAN_ELECTRIC, 
                                   selectforeground=COLOR_TEXT_ON_ACCENT,
                                   insertbackground=COLOR_ACCENT_CYAN_ELECTRIC)
        
        scrollbar = ttk.Scrollbar(text_display_frame, orient="vertical", command=help_text_widget.yview, style="Quantum.Vertical.TScrollbar")
        help_text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        help_text_widget.pack(side="left", fill="both", expand=True)

        # Configuração de tags de estilo para o texto da ajuda.
        help_text_widget.tag_configure("tag_help_title", 
                                       font=(self.APP_FONT_TITLES, FONT_SIZE_MEDIUM, "bold"), 
                                       foreground=COLOR_ACCENT_CYAN_ELECTRIC, 
                                       spacing1=12, spacing3=5) # Espaçamento antes e depois do título.
        help_text_widget.tag_configure("tag_help_description", 
                                       lmargin1=20, lmargin2=20, # Indentação para a descrição.
                                       font=(self.APP_FONT_BODY, FONT_SIZE_NORMAL), 
                                       foreground=COLOR_TEXT_PRIMARY,
                                       spacing3=15) # Espaçamento após a descrição.

        # Adiciona os exemplos de cálculo à caixa de texto.
        for title, description in calculation_examples_data:
            help_text_widget.insert(tk.END, title + "\n", "tag_help_title")
            help_text_widget.insert(tk.END, f"{description}\n\n", "tag_help_description")
        
        help_text_widget.config(state="disabled") # Bloqueia a edição do texto.

        # Botão para fechar a janela de ajuda.
        close_button = ttk.Button(help_window, text="Fechar Janela de Ajuda", command=help_window.destroy, style="Primary.TButton", width=20)
        close_button.pack(pady=25)


# --- Ponto de Entrada da Aplicação ---
# Este bloco é executado apenas quando o script é rodado diretamente.
if __name__ == "__main__":
    # Envolve a inicialização da aplicação em um bloco try-except
    # para capturar erros críticos que possam ocorrer antes que o
    # hook global de exceções esteja totalmente operacional.
    try:
        # Cria as instâncias dos componentes principais da aplicação.
        data_mgr = DataManager() # Gerenciador de dados.
        emergy_calc = EmergyCalculator(data_mgr) # Calculadora de emergia.
        
        app = Application(data_manager=data_mgr, emergy_calculator=emergy_calc) # Janela principal da aplicação.
        app.mainloop() # Inicia o loop de eventos do Tkinter, mantendo a janela ativa.
    except Exception as e_main:
        # Tratamento de último recurso para erros fatais na inicialização.
        print("--- ERRO CRÍTICO NA INICIALIZAÇÃO DA APLICAÇÃO ---")
        traceback.print_exc() # Imprime o traceback completo no console.
        # Tenta exibir uma messagebox, se o Tkinter estiver minimamente funcional.
        try:
            root_temp = tk.Tk() # Cria uma janela raiz temporária.
            root_temp.withdraw() # Oculta a janela raiz temporária.
            messagebox.showerror("Erro Fatal na Inicialização", 
                                 f"A aplicação encontrou um erro crítico durante a inicialização e não pode continuar.\n\n"
                                 f"Erro: {e_main}\n\n"
                                 "Consulte o console para obter detalhes técnicos completos.")
            if root_temp.winfo_exists(): # Verifica se a janela temporária foi criada.
                root_temp.destroy() # Destrói a janela após exibir a mensagem.
        except:
            # Se a exibição da messagebox também falhar, o erro já foi impresso no console.
            pass