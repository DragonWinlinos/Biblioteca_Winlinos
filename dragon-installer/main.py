import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
import subprocess

# --- 1. Logo/Mascote Gerada por Código (Minimalista) ---
# Usaremos um widget DrawingArea para desenhar a logo do dragão/mascote
# de forma programática, sem arquivos de imagem.

class DragonLogo(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_size_request(200, 100)
        self.connect("draw", self.on_draw)

    def on_draw(self, widget, cr):
        # Cor de fundo (preto ou transparente)
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.paint()

        # Cor do Dragão (Verde Esmeralda)
        cr.set_source_rgb(0.0, 0.8, 0.0)
        cr.set_line_width(5)

        # Desenho Abstrato do Dragão (Exemplo: um "D" estilizado com chifres/asas)
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        center_x = width / 2
        center_y = height / 2

        # Corpo/Base (Um arco forte - a "asa" ou "corpo" do dragão)
        cr.arc(center_x, center_y, 40, 0, 3.14159 * 2)
        cr.stroke()

        # Cabeça/Chifre (Dois triângulos simples)
        cr.move_to(center_x + 40, center_y)
        cr.line_to(center_x + 60, center_y - 20)
        cr.line_to(center_x + 80, center_y)
        cr.stroke()

        cr.move_to(center_x - 40, center_y)
        cr.line_to(center_x - 60, center_y - 20)
        cr.line_to(center_x - 80, center_y)
        cr.stroke()

        # Texto (Nome do Sistema)
        cr.select_font_face("Sans", Gtk.cairo.FONT_SLANT_NORMAL, Gtk.cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(18)
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.move_to(center_x - 70, center_y + 40)
        cr.show_text("Dragon Winlinos")

        return False

# --- 2. Janela Principal do Instalador (DI) ---

class DragonInstaller(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Dragon Winlinos Installer")
        self.set_border_width(10)
        self.set_default_size(600, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Stack para gerenciar as páginas (Boas-Vindas, Wi-Fi, Instalação)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        # Container principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Adicionar o seletor de páginas (para debug, pode ser removido no final)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
        vbox.pack_start(stack_switcher, False, False, 0)

        vbox.pack_start(self.stack, True, True, 0)

        # --- Páginas ---
        self.create_welcome_page()
        self.create_wifi_page()
        self.create_install_page()

        # --- Menu de Controle (Logo Clicável) ---
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Dragon Installer"
        self.set_titlebar(self.header)

        # Botão de Logo (Mascote)
        self.logo_button = Gtk.Button()
        self.logo_button.add(DragonLogo())
        self.logo_button.connect("clicked", self.on_logo_clicked)
        self.header.pack_start(self.logo_button, False, False, 0)

        # Menu de Desligamento/Reinicialização
        self.control_menu = Gtk.Menu()
        self.shutdown_item = Gtk.MenuItem.new_with_label("Desligar Completamente")
        self.reboot_item = Gtk.MenuItem.new_with_label("Reiniciar Completamente")
        self.shutdown_item.connect("activate", self.on_shutdown_clicked)
        self.reboot_item.connect("activate", self.on_reboot_clicked)
        self.control_menu.append(self.shutdown_item)
        self.control_menu.append(self.reboot_item)
        self.control_menu.show_all()

    def create_welcome_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(20)

        logo = DragonLogo()
        vbox.pack_start(logo, False, False, 0)

        label = Gtk.Label("Bem-vindo ao Dragon Winlinos Netinstall.\n\nEste processo irá baixar e instalar o sistema operacional completo. É necessária uma conexão com a internet.")
        vbox.pack_start(label, False, False, 0)

        next_button = Gtk.Button.new_with_label("Próximo: Conectar ao Wi-Fi")
        next_button.connect("clicked", lambda w: self.stack.set_visible_child_name("wifi"))
        vbox.pack_end(next_button, False, False, 0)

        self.stack.add_named(vbox, "welcome")

    def create_wifi_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(20)

        label = Gtk.Label("2. Conexão Wi-Fi (Manual)")
        vbox.pack_start(label, False, False, 0)

        # Campo SSID
        ssid_label = Gtk.Label("Nome da Rede (SSID):")
        self.ssid_entry = Gtk.Entry()
        vbox.pack_start(ssid_label, False, False, 0)
        vbox.pack_start(self.ssid_entry, False, False, 0)

        # Campo Senha
        pass_label = Gtk.Label("Senha:")
        self.pass_entry = Gtk.Entry()
        self.pass_entry.set_visibility(False)
        vbox.pack_start(pass_label, False, False, 0)
        vbox.pack_start(self.pass_entry, False, False, 0)

        # Botão Conectar
        connect_button = Gtk.Button.new_with_label("Conectar e Verificar")
        connect_button.connect("clicked", self.on_connect_clicked)
        vbox.pack_start(connect_button, False, False, 0)

        self.status_label = Gtk.Label("")
        vbox.pack_start(self.status_label, False, False, 0)

        self.stack.add_named(vbox, "wifi")

    def create_install_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(20)

        label = Gtk.Label("3. Instalação (Netinstall)")
        vbox.pack_start(label, False, False, 0)

        self.progress_bar = Gtk.ProgressBar()
        vbox.pack_start(self.progress_bar, False, False, 0)

        self.install_log = Gtk.TextView()
        self.install_log.set_editable(False)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.install_log)
        vbox.pack_start(scrolled_window, True, True, 0)

        self.stack.add_named(vbox, "install")

    # --- Lógica de Controle ---

    def on_logo_clicked(self, button):
        # Exibe o menu de controle ao clicar na logo
        self.control_menu.popup_at_widget(button, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None)

    def on_shutdown_clicked(self, widget):
        # Comando para desligamento completo (sem suspensão)
        print("Desligamento completo solicitado.")
        subprocess.run(["shutdown", "-h", "now"])
        Gtk.main_quit()

    def on_reboot_clicked(self, widget):
        # Comando para reinicialização completa
        print("Reinicialização completa solicitada.")
        subprocess.run(["reboot"])
        Gtk.main_quit()

    def on_connect_clicked(self, button):
        ssid = self.ssid_entry.get_text()
        password = self.pass_entry.get_text()

        if not ssid:
            self.status_label.set_text("Erro: Digite o nome da rede (SSID).")
            return

        self.status_label.set_text(f"Tentando conectar a {ssid}...")
        
        # --- Lógica de Conexão Wi-Fi (Simulação no ambiente Live) ---
        # Em um ambiente real, usaríamos nmcli ou wpa_supplicant.
        # Aqui, simulamos a execução do comando.
        
        try:
            # Comando de exemplo para wpa_supplicant (requer configuração prévia)
            # Exemplo: subprocess.run(["wpa_cli", "set_network", "0", "ssid", f'"{ssid}"'])
            
            # Simulação de sucesso
            GLib.timeout_add_seconds(2, self.on_connect_success)
            
        except Exception as e:
            self.status_label.set_text(f"Erro de conexão: {e}")

    def on_connect_success(self):
        self.status_label.set_text("Conexão bem-sucedida! Clique em Próximo para continuar.")
        # Avançar para a próxima fase (Particionamento)
        # self.stack.set_visible_child_name("partitioning")
        return False # Retorna False para não repetir o timeout

# --- 3. Inicialização ---

if __name__ == "__main__":
    win = DragonInstaller()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
