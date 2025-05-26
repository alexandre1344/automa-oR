from datetime import datetime, timedelta  # Modificar esta linha para incluir timedelta
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  # Add this import
import threading
import time
from PIL import Image, ImageTk
import os
from contas import GerenciadorContas
from updater import Updater
from version import VERSION

class SEAPPoliciaPenalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação RAS")
        # Adjust window size to better fit content
        self.root.geometry("650x750")  # Changed from 750x850
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        
        # Cores do tema
        self.cor_fundo = '#000000'
        self.cor_destaque = '#FFD700'
        self.cor_texto = '#FFFFFF'
        self.cor_secundaria = '#1A1A1A'
        self.cor_input = '#333333'
        self.cor_texto_input = '#FFD700'
        
        # Initialize variables first
        self.driver = None
        self.auto_close = tk.BooleanVar(value=False)
        self.gerenciador_contas = GerenciadorContas()
        
        # Then configure and create UI elements
        self.configurar_estilos()
        self.carregar_logo()
        self.criar_cabecalho()
        self.criar_formulario()
        self.criar_controles()
        self.criar_rodape()

        # Adicionar verificação de atualizações
        self.check_for_updates()
        
    def check_for_updates(self):
        updater = Updater()
        has_update, new_version = updater.check_for_updates()
        
        if has_update:
            if messagebox.askyesno("Atualização Disponível", 
                                 f"Nova versão {new_version} disponível!\nDeseja atualizar agora?"):
                self.atualizar_status("Baixando atualização...", 0)
                if updater.download_update(new_version):
                    messagebox.showinfo("Sucesso", 
                                      "Atualização baixada com sucesso!\nO programa será reiniciado.")
                    self.reiniciar_aplicacao()
                else:
                    messagebox.showerror("Erro", 
                                       "Erro ao baixar atualização.\nTente novamente mais tarde.")
    
    def reiniciar_aplicacao(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilo geral
        self.style.configure('.', background=self.cor_fundo, foreground=self.cor_texto)
        
        # Estilo dos inputs (Entry)
        self.style.configure('Gold.TEntry',
                           fieldbackground=self.cor_input,
                           foreground=self.cor_texto_input,
                           bordercolor=self.cor_destaque,
                           lightcolor=self.cor_destaque,
                           darkcolor=self.cor_destaque,
                           insertcolor=self.cor_destaque,
                           padding=5)
        self.style.map('Gold.TEntry',
                      fieldbackground=[('readonly', self.cor_input)],
                      bordercolor=[('active', self.cor_destaque), ('focus', self.cor_destaque)])
        
        # Estilo dos Combobox
        self.style.configure('Gold.TCombobox',
                           fieldbackground=self.cor_input,
                           foreground=self.cor_texto_input,
                           background=self.cor_input,
                           arrowcolor=self.cor_destaque,
                           bordercolor=self.cor_destaque,
                           lightcolor=self.cor_destaque,
                           darkcolor=self.cor_destaque,
                           padding=5)
        self.style.map('Gold.TCombobox',
                     fieldbackground=[('readonly', self.cor_input)],
                     background=[('readonly', self.cor_input)],
                     bordercolor=[('active', self.cor_destaque), ('focus', self.cor_destaque)])
        
        # Botões
        self.style.configure('Gold.TButton',
                           font=('Arial', 10, 'bold'),
                           background=self.cor_fundo,
                           foreground=self.cor_destaque,
                           bordercolor=self.cor_destaque,
                           borderwidth=2,
                           padding=8,
                           relief='raised')
        self.style.map('Gold.TButton',
                     foreground=[('active', '#FFFFFF'), ('disabled', '#7F7F7F')],
                     background=[('active', '#333333')])
        
        # Barra de progresso
        self.style.configure("Gold.Horizontal.TProgressbar",
                           troughcolor=self.cor_secundaria,
                           background=self.cor_destaque,
                           bordercolor=self.cor_destaque,
                           lightcolor=self.cor_destaque,
                           darkcolor=self.cor_destaque,
                           thickness=10)
        
        # Estilo para entradas com erro
        self.style.configure('Error.TEntry',
                           fieldbackground='#FFE4E1',
                           foreground='red')

    def carregar_logo(self):
        try:
            # Substitua pelo caminho da sua logo
            img = Image.new('RGB', (180, 60), color='black')
            self.logo_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            self.logo_image = None

    def criar_cabecalho(self):
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(pady=10, fill='x')
        
        if self.logo_image:
            logo_label = ttk.Label(header_frame, image=self.logo_image, background=self.cor_fundo)
            logo_label.pack(pady=5)
        
        title_frame = ttk.Frame(header_frame, style='TFrame')
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="Sistema de Automação", 
                             font=('Arial', 18, 'bold'), 
                             bg=self.cor_fundo, fg=self.cor_destaque)
        title_label.pack()
        
        sub_label = tk.Label(title_frame, text="Alexandre-dev RJ", 
                           font=('Arial', 8), 
                           bg=self.cor_fundo, fg=self.cor_texto)
        sub_label.pack(pady=5)
        
        separator = ttk.Separator(self.root, orient='horizontal', style='Gold.TSeparator')
        separator.pack(fill='x', padx=20, pady=5)

    def criar_formulario(self):
        form_frame = ttk.Frame(self.root, style='TFrame')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Conta Salva (novo campo)
        ttk.Label(form_frame, text="Conta Salva:", style='TLabel').grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.conta_combo = ttk.Combobox(form_frame, 
                                      values=[""] + self.gerenciador_contas.obter_contas(),
                                      state='readonly',
                                      style='Gold.TCombobox',
                                      font=('Arial', 10))
        self.conta_combo.grid(row=0, column=1, padx=5, pady=10, sticky='ew')
        self.conta_combo.bind('<<ComboboxSelected>>', self.carregar_conta_salva)
        
        # Botões de gerenciamento de conta
        conta_buttons_frame = ttk.Frame(form_frame, style='TFrame')
        conta_buttons_frame.grid(row=0, column=2, padx=5, pady=10)
        
        ttk.Button(conta_buttons_frame,
                  text="Salvar Atual",
                  command=self.salvar_conta_atual,
                  style='Gold.TButton').pack(side='left', padx=2)
        
        ttk.Button(conta_buttons_frame,
                  text="Remover",
                  command=self.remover_conta_atual,
                  style='Gold.TButton').pack(side='left', padx=2)

        # Dicionário de estilos para labels
        label_style = {'font': ('Arial', 10, 'bold'), 'background': self.cor_fundo, 'foreground': self.cor_destaque}
        
        # Tipo de Acesso
        ttk.Label(form_frame, text="Tipo de Acesso:", style='TLabel').grid(row=1, column=0, padx=5, pady=10, sticky='e')
        self.tipo_acesso = ttk.Combobox(form_frame, 
                                      values=["ID Funcional", "CPF"], 
                                      state='readonly',
                                      style='Gold.TCombobox',
                                      font=('Arial', 10))
        self.tipo_acesso.grid(row=1, column=1, padx=5, pady=10, sticky='ew')
        self.tipo_acesso.current(0)
        
        # ID Funcional
        ttk.Label(form_frame, text="ID Funcional:", style='TLabel').grid(row=2, column=0, padx=5, pady=10, sticky='e')
        self.id_entry = ttk.Entry(form_frame, 
                                style='Gold.TEntry',
                                font=('Arial', 10))
        self.id_entry.grid(row=2, column=1, padx=5, pady=10, sticky='ew')
        
        
        # Senha
        ttk.Label(form_frame, text="Senha:", style='TLabel').grid(row=3, column=0, padx=5, pady=10, sticky='e')
        self.senha_entry = ttk.Entry(form_frame, 
                                   style='Gold.TEntry',
                                   show="*",
                                   font=('Arial', 10))
        self.senha_entry.grid(row=3, column=1, padx=5, pady=10, sticky='ew')
        
        
        # Checkbox para mostrar/ocultar senha
        self.mostrar_senha = tk.BooleanVar()
        self.mostrar_senha_check = ttk.Checkbutton(form_frame,
                                              text="Mostrar senha",
                                              variable=self.mostrar_senha,
                                              command=self.toggle_senha,
                                              style='Gold.TCheckbutton')
        self.mostrar_senha_check.grid(row=3, column=2, padx=5, pady=10, sticky='w')
        
        # Unidade
        ttk.Label(form_frame, text="Unidade:", style='TLabel').grid(row=4, column=0, padx=5, pady=10, sticky='e')
        self.unidade = ttk.Combobox(form_frame, 
                                  values=self.carregar_unidades(), 
                                  state='readonly',
                                  style='Gold.TCombobox',
                                  font=('Arial', 10))
        self.unidade.grid(row=4, column=1, padx=5, pady=10, sticky='ew')
        self.unidade.current(0)  # Changed from 58 to 0 since we only have 2 items (0 or 1)
        
        # Data
        ttk.Label(form_frame, text="Data (AAAA-MM-DD):", style='TLabel').grid(row=5, column=0, padx=5, pady=10, sticky='e')
        self.data_entry = ttk.Entry(form_frame, 
                                  style='Gold.TEntry',
                                  font=('Arial', 10))
        self.data_entry.grid(row=5, column=1, padx=5, pady=10, sticky='ew')
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default date
        
        # Validação da data
        def validar_data(event=None):
            data = self.data_entry.get()
            if self.validar_data(data):
                self.data_entry.configure(style='Gold.TEntry')
            else:
                self.data_entry.configure(style='Error.TEntry')
                
        self.data_entry.bind('<FocusOut>', validar_data)
        
        # Turno
        ttk.Label(form_frame, text="Turno:", style='TLabel').grid(row=6, column=0, padx=5, pady=10, sticky='e')
        self.turno_var = tk.StringVar(value="08:00:00")
        self.turno_combo = ttk.Combobox(
            form_frame,
            textvariable=self.turno_var,
            values=["08:00:00", "20:00:00"],
            state='readonly',
            style='Gold.TCombobox',
            font=('Arial', 10)
        )
        self.turno_combo.grid(row=6, column=1, padx=5, pady=10, sticky='ew')

        # Opções
        options_frame = ttk.Frame(form_frame, style='TFrame')
        options_frame.grid(row=7, column=0, columnspan=2, pady=15)

        ttk.Checkbutton(options_frame, 
                       text="Fechar navegador automaticamente", 
                       variable=self.auto_close,
                       style='Gold.TCheckbutton').pack(anchor='w')

    def carregar_unidades(self):
        return [
            "PRESÍDIO INSPETOR JOSÉ ANTÔNIO DA COSTA BARROS",
            "SEGURANÇA PRESENTE"
        ]

    def criar_controles(self):
        control_frame = ttk.Frame(self.root, style='TFrame')
        control_frame.pack(pady=20, fill='x', padx=40)
        
        # Create a frame for buttons
        button_frame = ttk.Frame(control_frame, style='TFrame')
        button_frame.pack(pady=10, fill='x')
        
        # Add buttons side by side
        self.run_button = ttk.Button(button_frame, 
                                   text="EXECUTAR AUTOMAÇÃO", 
                                   command=self.iniciar_automacao,
                                   style='Gold.TButton')
        self.run_button.pack(side='left', pady=10, padx=5, expand=True, fill='x')
        
        self.restart_button = ttk.Button(button_frame,
                                       text="REINICIAR AUTOMAÇÃO",
                                       command=self.reiniciar_automacao,
                                       style='Gold.TButton')
        self.restart_button.pack(side='left', pady=10, padx=5, expand=True, fill='x')
        
        self.repeat_button = ttk.Button(button_frame, 
                                      text="REPETIR INSCRIÇÃO", 
                                      command=self.repetir_inscricao,
                                      state='disabled',
                                      style='Gold.TButton')
        self.repeat_button.pack(side='left', pady=10, padx=5, expand=True, fill='x')
        
        self.stop_button = ttk.Button(control_frame, 
                                    text="PARAR", 
                                    state='disabled',
                                    command=self.parar_automacao,
                                    style='Gold.TButton')
        self.stop_button.pack(pady=5, ipadx=20, ipady=5, fill='x')
        
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para executar")
        status_label = tk.Label(control_frame, 
                              textvariable=self.status_var, 
                              font=('Arial', 9), 
                              bg=self.cor_fundo, 
                              fg=self.cor_destaque)
        status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(control_frame, 
                                      orient='horizontal', 
                                      mode='determinate', 
                                      style="Gold.Horizontal.TProgressbar")
        self.progress.pack(pady=5, fill='x')

    def criar_rodape(self):
        footer_frame = ttk.Frame(self.root, style='TFrame')
        footer_frame.pack(side='bottom', pady=10, fill='x')
        
        separator = ttk.Separator(footer_frame, orient='horizontal', style='Gold.TSeparator')
        separator.pack(fill='x', padx=20, pady=5)
        
        creditos_frame = ttk.Frame(footer_frame, style='TFrame')
        creditos_frame.pack(fill='x')
        
        creditos = tk.Label(creditos_frame, 
                          text="© 2024 Alexandre-dev RJ | Versão 2.0", 
                          font=('Arial', 8), 
                          bg=self.cor_fundo, 
                          fg=self.cor_destaque)
        creditos.pack(side='right', padx=10)

    def iniciar_automacao(self):
        if not self.validar_campos():
            return
        
        # Atualiza a conta atual se estiver selecionada
        nome_conta = self.conta_combo.get()
        if nome_conta:
            dados = {
                'tipo_acesso': self.tipo_acesso.get(),
                'id': self.id_entry.get(),
                'senha': self.senha_entry.get(),
                'unidade': self.unidade.get(),
                'data': self.data_entry.get(),
                'turno': self.turno_var.get()  # Adicionar turno
            }
            self.gerenciador_contas.salvar_conta(nome_conta, dados)
            self.atualizar_lista_contas()
            
        self.run_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("Iniciando automação...")
        self.progress['value'] = 0
        
        # Executar em thread separada
        threading.Thread(target=self.executar_automacao, daemon=True).start()

    def validar_campos(self):
        if not self.id_entry.get():
            messagebox.showwarning("Validação", "Por favor, informe o ID Funcional!")
            return False
        if not self.senha_entry.get():
            messagebox.showwarning("Validação", "Por favor, informe a senha!")
            return False
        
        # Validate date format
        data = self.data_entry.get()
        if not self.validar_data(data):
            messagebox.showwarning("Validação", "Data inválida! Use o formato AAAA-MM-DD")
            return False
        
        return True

    def validar_data(self, data):
        """Valida se a data existe no calendário"""
        try:
            from calendar import monthrange
            data_obj = datetime.strptime(data, "%Y-%m-%d")
            
            # Verificar se o dia existe naquele mês
            _, last_day = monthrange(data_obj.year, data_obj.month)
            
            if data_obj.day > last_day:
                return False
                
            # Não permitir datas passadas
            if data_obj.date() < datetime.now().date():
                return False
                
            return True
        except ValueError:
            return False

    def executar_automacao(self):
        try:
            self.atualizar_status("Configurando navegador...", 10)
            servico = Service(ChromeDriverManager().install())
            chrome_options = webdriver.ChromeOptions()
            
            if self.auto_close.get():
                chrome_options.add_argument("--headless")
            
            self.driver = webdriver.Chrome(service=servico, options=chrome_options)
            
            # Passo 1: Acessar o site
            self.atualizar_status("Acessando o SEAP RJ...", 20)
            self.driver.get("https://www.seapsistema.rj.gov.br/")
            
            # Passo 2: Selecionar tipo de acesso
            self.atualizar_status("Selecionando tipo de acesso...", 30)
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ddlTipoAcesso"]'))
            )
            dropdown.click()
            
            # Defines the XPath based on the selected access type
            tipo_acesso_xpath = {
                "ID Funcional": '/html/body/main/form/div[3]/div/div[1]/div[1]/div[1]/div/select/option[3]',
                "CPF": '//*[@id="ddlTipoAcesso"]/option[2]'
            }
            
            selected_type = self.tipo_acesso.get()
            type_xpath = tipo_acesso_xpath[selected_type]
            
            option = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, type_xpath))
            )
            option.click()
            
            # Passo 3: Preencher ID Funcional ou CPF
            self.atualizar_status("Preenchendo credenciais...", 40)
            login_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="txtLogin"]'))
            )
            login_field.send_keys(self.id_entry.get())
            
            # Passo 4: Preencher senha
            self.atualizar_status("Preenchendo senha...", 50)
            senha_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/main/form/div[3]/div/div[1]/div[2]/div[1]/div/div/div/input'))
            )
            senha_field.send_keys(self.senha_entry.get())
            
            # Passo 5: Clicar no campo do CAPTCHA
            self.atualizar_status("Clicando no campo do CAPTCHA...", 55)
            captcha_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/main/form/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/input'))
            )
            captcha_input.click()
            
            # Create WebDriverWait with 10 minutes timeout
            wait = WebDriverWait(self.driver, 600)  # 600 seconds = 10 minutes
            
            # Passo 6: Clicar em entrar
            self.atualizar_status("Aguardando carregamento (pode demorar até 10 minutos)...", 60)
            entrar_button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/div/div/div/div[1]/div[2]/a'))
            )
            entrar_button.click()

            # Passo 6: Selecionar unidade
            self.atualizar_status("Aguardando carregamento da unidade (pode demorar até 10 minutos)...", 70)  # Era 80, agora 70
            unidade_dropdown = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select'))
            )
            unidade_dropdown.click()
            
            # Defines the XPath based on the selected unit
            unidade_xpath = {
                "PRESÍDIO INSPETOR JOSÉ ANTÔNIO DA COSTA BARROS": '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select/option[59]',
                "SEGURANÇA PRESENTE": '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select/option[70]'
            }
            
            # Seleciona a opção correta baseada na unidade escolhida
            selected_unit = self.unidade.get()
            unit_xpath = unidade_xpath[selected_unit]
            
            unidade_option = wait.until(
                EC.presence_of_element_located((By.XPATH, unit_xpath))
            )
            unidade_option.click()

            time.sleep(0.5) # Wait for the dropdown to be ready

            # Select date using visible text
            select_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[3]/div/div/select'))
            )

            # Create Select object
            select = Select(select_element)

            # Get date from entry and format it
            try:
                data_input = self.data_entry.get()  # Already in YYYY-MM-DD format
                
                # Find and select the date
                options = select_element.find_elements(By.TAG_NAME, "option")
                date_found = False
                
                for option in options:
                    if data_input in option.text:  # Look for YYYY-MM-DD format directly
                        option.click()
                        date_found = True
                        self.repeat_button.config(state='normal')  # Habilita o botão após selecionar a data
                        self.atualizar_status(f"Data {data_input} selecionada com sucesso", 85)
                        break
                        
                if not date_found:
                    self.repeat_button.config(state='disabled')  # Desabilita se a data não for encontrada
                    raise Exception(f"Data {data_input} não disponível")
                    
            except ValueError:
                self.repeat_button.config(state='disabled')
                raise Exception("Formato de data inválido. Use AAAA-MM-DD")
            except Exception as e:
                self.repeat_button.config(state='disabled')
                raise Exception(f"Erro ao selecionar data: {str(e)}")
            
            time.sleep(0.2)  # Small delay to ensure element is properly in view
            # Wait for the second CAPTCHA input and click it
            try:
                segundo_captcha_input = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[4]/div[1]/div/div/input'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", segundo_captcha_input)
                time.sleep(0.5)  # Small delay to ensure element is properly in view
                segundo_captcha_input.click()
                self.atualizar_status("Clicando no segundo CAPTCHA...", 90)
            except Exception as e:
                print(f"Erro ao clicar no segundo CAPTCHA: {str(e)}")
                raise

            # Tentar clicar no botão "Eu Vou"
            self.clicar_botao_eu_vou(self.turno_var.get())
            
            # Conclusão
            self.atualizar_status("Automação concluída com sucesso!", 100, "green")
            self.repeat_button.config(state='normal')
            self.restart_button.config(state='normal')  # Enable restart button
            
            if not self.auto_close.get():
                self.atualizar_status("Sucesso", "Automação concluída!\nO navegador permanecerá aberto.")
            
        except Exception as e:
            self.atualizar_status(f"Erro: {str(e)}", 0, "red")
            messagebox.showerror("Erro", f"Ocorreu um erro durante a automação:\n{str(e)}")
        finally:
            self.finalizar_automacao()

    def parar_automacao(self):
        if messagebox.askyesno("Confirmar", "Deseja realmente interromper a automação?"):
            self.atualizar_status("Automação interrompida pelo usuário", 0, "orange")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.finalizar_automacao()

    def atualizar_status(self, mensagem, progresso=None, cor=None):
        self.root.after(0, lambda: self.status_var.set(mensagem))
        if progresso is not None:
            def update_progress():
                self.progress['value'] = progresso
            self.root.after(0, update_progress)
        if cor == "green":
            self.root.after(0, lambda: self.status_var.set(mensagem))
        elif cor == "red":
            self.root.after(0, lambda: self.status_var.set(mensagem))
        elif cor == "orange":
            self.root.after(0, lambda: self.status_var.set(mensagem))

    def finalizar_automacao(self):
        try:
            if self.auto_close.get() and self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Erro ao fechar navegador: {e}")
        finally:
            self.root.after(0, lambda: self.run_button.config(state='normal'))
            self.root.after(0, lambda: self.stop_button.config(state='disabled'))

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.root.destroy()

    def toggle_senha(self):
        """Alterna a visibilidade da senha"""
        if self.mostrar_senha.get():
            self.senha_entry.config(show="")
        else:
            self.senha_entry.config(show="*")

    def carregar_conta_salva(self, event=None):
        nome_conta = self.conta_combo.get()
        if nome_conta:
            dados = self.gerenciador_contas.obter_dados_conta(nome_conta)
            if dados:
                self.tipo_acesso.set(dados.get('tipo_acesso', ''))
                self.id_entry.delete(0, 'end')
                self.id_entry.insert(0, dados.get('id', ''))
                self.senha_entry.delete(0, 'end')
                self.senha_entry.insert(0, dados.get('senha', ''))
                self.unidade.set(dados.get('unidade', ''))
                self.data_entry.delete(0, 'end')
                self.data_entry.insert(0, dados.get('data', '2025-04-20'))
                self.turno_var.set(dados.get('turno', '08:00:00'))  # Adicionar turno

    def salvar_conta_atual(self):
        nome = simpledialog.askstring("Salvar Conta", "Digite um nome para esta conta:")
        if nome:
            if not all([self.id_entry.get(), self.senha_entry.get(), self.unidade.get(), self.data_entry.get()]):
                messagebox.showerror("Erro", "Preencha todos os campos antes de salvar!")
                return
            dados = {
                'tipo_acesso': self.tipo_acesso.get(),
                'id': self.id_entry.get(),
                'senha': self.senha_entry.get(),
                'unidade': self.unidade.get(),
                'data': self.data_entry.get(),
                'turno': self.turno_var.get()  # Adicionar turno
            }
            self.gerenciador_contas.salvar_conta(nome, dados)
            self.atualizar_lista_contas()
            messagebox.showinfo("Sucesso", "Conta salva com sucesso!")

    def remover_conta_atual(self):
        nome = self.conta_combo.get()
        if nome and messagebox.askyesno("Confirmar", f"Deseja remover a conta {nome}?"):
            self.gerenciador_contas.remover_conta(nome)
            self.atualizar_lista_contas()
            self.conta_combo.set('')
            messagebox.showinfo("Sucesso", "Conta removida com sucesso!")

    def atualizar_lista_contas(self):
        self.conta_combo['values'] = [""] + self.gerenciador_contas.obter_contas()

    def repetir_inscricao(self):
        try:
            if not self.driver:
                messagebox.showerror("Erro", "Navegador não está aberto!")
                return
            
            # Incrementar data respeitando o calendário
            try:
                from calendar import monthrange
                current_date = datetime.strptime(self.data_entry.get(), "%Y-%m-%d")
                
                # Pegar o último dia do mês atual
                _, last_day = monthrange(current_date.year, current_date.month)
                
                # Se estamos no último dia do mês
                if current_date.day == last_day:
                    # Se for dezembro, vamos para janeiro do próximo ano
                    if current_date.month == 12:
                        next_date = datetime(current_date.year + 1, 1, 1)
                    else:
                        # Senão, vamos para o dia 1 do próximo mês
                        next_date = datetime(current_date.year, current_date.month + 1, 1)
                else:
                    # Se não for último dia do mês, só adiciona um dia
                    next_date = current_date + timedelta(days=1)
                
                # Atualizar campo de data
                self.data_entry.delete(0, tk.END)
                self.data_entry.insert(0, next_date.strftime("%Y-%m-%d"))
                
                # Atualiza a conta atual se estiver selecionada
                nome_conta = self.conta_combo.get()
                if nome_conta:
                    dados = {
                        'tipo_acesso': self.tipo_acesso.get(),
                        'id': self.id_entry.get(),
                        'senha': self.senha_entry.get(),
                        'unidade': self.unidade.get(),
                        'data': self.data_entry.get(),
                        'turno': self.turno_var.get()  # Adicionar turno
                    }
                    self.gerenciador_contas.salvar_conta(nome_conta, dados)
                    
            except ValueError as e:
                raise Exception(f"Erro ao incrementar data: {str(e)}")
                
            wait = WebDriverWait(self.driver, 600)  # 600 seconds = 10 minutes

            # Click enter button
            self.atualizar_status("Realizando login...", 60)
            entrar_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/div/div/div/div[1]/div[2]/a'))
            )
            entrar_button.click()

            # Click new inscription
            self.atualizar_status("Tentando clicar em Nova Inscrição...", 70)
            max_tentativas = 10  # Número máximo de tentativas
            for tentativa in range(max_tentativas):
                try:
                    # Tenta encontrar e clicar no botão Nova Inscrição
                    inscricao_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[6]/div/div/div/input'))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", inscricao_button)
                    inscricao_button.click()
                    
                    # Verifica se o dropdown de unidade apareceu
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select'))
                        )
                        # Se chegou aqui, o dropdown apareceu
                        self.atualizar_status("Nova Inscrição realizada com sucesso", 75)
                        break
                    except:
                        # Se o dropdown não apareceu, continua tentando
                        self.atualizar_status(f"Tentativa {tentativa + 1} de clicar em Nova Inscrição...", 70)
                        continue
                        
                except Exception as e:
                    if tentativa == max_tentativas - 1:  # Se for a última tentativa
                        raise Exception(f"Erro ao clicar em Nova Inscrição após {max_tentativas} tentativas: {str(e)}")
                    time.sleep(0.1)  # Espera 1 segundo antes da próxima tentativa
            
            # Select unit
            self.atualizar_status("Selecionando unidade...", 80)
            unidade_dropdown = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select'))
            )
            unidade_dropdown.click()
            
            # Get unit xpath
            unidade_xpath = {
                "PRESÍDIO INSPETOR JOSÉ ANTÔNIO DA COSTA BARROS": '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select/option[59]',
                "SEGURANÇA PRESENTE": '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select/option[70]'
            }
            
            selected_unit = self.unidade.get()
            unit_xpath = unidade_xpath[selected_unit]
            
            unidade_option = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, unit_xpath))
            )
            unidade_option.click()

            time.sleep(0.5) # Wait for the dropdown to be ready

            # Select date using visible text
            select_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[3]/div/div/select'))
            )

            # Find and select the new date
            options = select_element.find_elements(By.TAG_NAME, "option")
            date_found = False
            next_date_str = next_date.strftime("%Y-%m-%d")
            
            for option in options:
                if next_date_str in option.text:
                    option.click()
                    date_found = True
                    self.atualizar_status(f"Selecionada próxima data: {next_date_str}", 85)
                    break
                    
            if not date_found:
                raise Exception(f"Data {next_date_str} não disponível")
            
            time.sleep(0.2)  # Small delay to ensure element is properly in view
            # Wait for the second CAPTCHA input and click it
            try:
                segundo_captcha_input = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[4]/div[1]/div/div/input'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", segundo_captcha_input)
                time.sleep(0.5)  # Small delay to ensure element is properly in view
                segundo_captcha_input.click()
                self.atualizar_status("Clicando no segundo CAPTCHA...", 90)
            except Exception as e:
                print(f"Erro ao clicar no segundo CAPTCHA: {str(e)}")
                raise
            # Conclusion
            self.atualizar_status("Inscrição repetida com sucesso!", 100, "green")
            
        except Exception as e:
            self.atualizar_status(f"Erro: {str(e)}", 0, "red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao repetir a inscrição:\n{str(e)}")
        finally:
            self.run_button.config(state='normal')
            self.repeat_button.config(state='normal')
            self.stop_button.config(state='disabled')

    def reiniciar_automacao(self):
        try:
            if not self.driver:
                messagebox.showerror("Erro", "Navegador não está aberto!")
                return
                
            if messagebox.askyesno("Confirmar", "Deseja reiniciar a automação?\nIsso irá interromper qualquer processo em andamento."):
                self.run_button.config(state='disabled')
                self.restart_button.config(state='disabled')
                self.repeat_button.config(state='disabled')
                self.stop_button.config(state='normal')
                
                self.atualizar_status("Reiniciando automação...", 30)
                
                # Navigate back to login page
                self.driver.get("https://www.seapsistema.rj.gov.br/")
                
                # Passo 2: Selecionar tipo de acesso
            self.atualizar_status("Selecionando tipo de acesso...", 30)
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ddlTipoAcesso"]'))
            )
            dropdown.click()
            
            wait = WebDriverWait(self.driver, 600)  # 600 seconds = 10 minutes

            # Define o XPath baseado no tipo de acesso selecionado
            tipo_acesso_xpath = {
                "ID Funcional": '/html/body/main/form/div[3]/div/div[1]/div[1]/div[1]/div/select/option[3]',
                "CPF": '//*[@id="ddlTipoAcesso"]/option[2]'
            }
            
            selected_type = self.tipo_acesso.get()
            type_xpath = tipo_acesso_xpath[selected_type]
            
            option = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, type_xpath))
            )
            option.click()
            
            # Passo 3: Preencher ID Funcional ou CPF
            self.atualizar_status("Preenchendo credenciais...", 40)
            login_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="txtLogin"]'))
            )
            login_field.send_keys(self.id_entry.get())
            
            # Passo 4: Preencher senha
            self.atualizar_status("Preenchendo senha...", 50)
            senha_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/main/form/div[3]/div/div[1]/div[2]/div[1]/div/div/div/input'))
            )
            senha_field.send_keys(self.senha_entry.get())
            
            # Passo 5: Clicar no campo do CAPTCHA
            self.atualizar_status("Clicando no campo do CAPTCHA...", 55)
            captcha_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/main/form/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/input'))
            )
            captcha_input.click()
            
            # Create WebDriverWait with 10 minutes timeout
            wait = WebDriverWait(self.driver, 600)  # 600 seconds = 10 minutes
            
            # Passo 6: Clicar em entrar
            self.atualizar_status("Aguardando carregamento (pode demorar até 10 minutos)...", 60)
            entrar_button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[6]/div/div/div/div[1]/div[2]/a'))
            )
            entrar_button.click()

            # Passo 6: Selecionar unidade
            self.atualizar_status("Aguardando carregamento da unidade (pode demorar até 10 minutos)...", 70)  # Era 80, agora 70
            unidade_dropdown = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select'))
            )
            unidade_dropdown.click()
            
            # Define o XPath baseado na unidade selecionada
            unidade_xpath = {
                "PRESÍDIO INSPETOR JOSÉ ANTÔNIO DA COSTA BARROS": '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select/option[59]',
                "SEGURANÇA PRESENTE": '/html/body/form/div[5]/div[2]/div[1]/div[2]/div/div/select/option[70]'
            }
            
            # Seleciona a opção correta baseada na unidade escolhida
            selected_unit = self.unidade.get()
            unit_xpath = unidade_xpath[selected_unit]
            
            unidade_option = wait.until(
                EC.presence_of_element_located((By.XPATH, unit_xpath))
            )
            unidade_option.click()

            time.sleep(0.5) # Wait for the dropdown to be ready

            # Select date using visible text
            select_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[3]/div/div/select'))
            )

            # Create Select object
            select = Select(select_element)

            # Get date from entry and format it
            try:
                data_input = self.data_entry.get()  # Already in YYYY-MM-DD format
                
                # Find and select the date
                options = select_element.find_elements(By.TAG_NAME, "option")
                date_found = False
                
                for option in options:
                    if data_input in option.text:  # Look for YYYY-MM-DD format directly
                        option.click()
                        date_found = True
                        self.repeat_button.config(state='normal')  # Habilita o botão após selecionar a data
                        self.atualizar_status(f"Data {data_input} selecionada com sucesso", 85)
                        break
                        
                if not date_found:
                    self.repeat_button.config(state='disabled')  # Desabilita se a data não for encontrada
                    raise Exception(f"Data {data_input} não disponível")
                    
            except ValueError:
                self.repeat_button.config(state='disabled')
                raise Exception("Formato de data inválido. Use AAAA-MM-DD")
            except Exception as e:
                self.repeat_button.config(state='disabled')
                raise Exception(f"Erro ao selecionar data: {str(e)}")
            
            time.sleep(0.2)  # Small delay to ensure element is properly in view
            # Wait for the second CAPTCHA input and click it
            try:
                segundo_captcha_input = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[5]/div[2]/div[1]/div[4]/div[1]/div/div/input'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", segundo_captcha_input)
                time.sleep(0.5)  # Small delay to ensure element is properly in view
                segundo_captcha_input.click()
                self.atualizar_status("Clicando no segundo CAPTCHA...", 90)
            except Exception as e:
                print(f"Erro ao clicar no segundo CAPTCHA: {str(e)}")
                raise
                
            self.repeat_button.config(state='normal')
            self.restart_button.config(state='normal')
                
        except Exception as e:
            self.atualizar_status(f"Erro ao reiniciar: {str(e)}", 0, "red")
            messagebox.showerror("Erro", f"Erro ao reiniciar automação:\n{str(e)}")
        finally:
            # Only enable other buttons if there's an error
            if self.status_var.get().startswith("Erro"):
                self.run_button.config(state='normal')
                self.repeat_button.config(state='normal')
                self.stop_button.config(state='disabled')

    def clicar_botao_eu_vou(self, turno):
        """Clica no botão 'Eu Vou' do horário especificado"""
        try:
            self.atualizar_status("Aguardando botão 'Eu Vou' aparecer...", 95)
            wait = WebDriverWait(self.driver, 30)
            
            # Aguarda a tabela carregar
            linhas = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//tbody//tr")))
            encontrou = False
            
            for linha in linhas:
                if turno in linha.text:
                    try:
                        botao_eu_vou = linha.find_element(By.XPATH, ".//a[span[contains(text(), 'Eu Vou')]]")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_eu_vou)
                        time.sleep(0.5)
                        botao_eu_vou.click()
                        encontrou = True
                        self.atualizar_status(f'Botão "Eu Vou" do turno {turno} clicado com sucesso!', 100, "green")
                        break
                    except Exception as e:
                        print(f'Botão "Eu Vou" não encontrado na linha do turno {turno}: {e}')
                        
            if not encontrou:
                self.atualizar_status(f'Nenhuma vaga do turno {turno} encontrada.', 100, "orange")
                
        except Exception as e:
            self.atualizar_status(f"Erro ao clicar no botão 'Eu Vou': {e}", 0, "red")
            raise

if __name__ == "__main__":
    root = tk.Tk()
    app = SEAPPoliciaPenalApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()