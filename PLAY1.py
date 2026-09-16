import time, os, psutil, random, gc
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

LINKS = [
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849857P5tcdclw5vm1xt26e5k6&balance=0&currency=USD&userid=12792790&isMobile=false",
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849874Pml2svzg5s1q1hkplx7l&balance=0&currency=USD&userid=12792807&isMobile=false",
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849881P2ycg9r0f5sc0v6vxsu1&balance=0&currency=USD&userid=12792814&isMobile=false",
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849892P692a6toh6wt4a7e48gg&balance=0&currency=USD&userid=12792825&isMobile=false",
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849898Pzswtvmb4i3qrzwgfxx6&balance=0&currency=USD&userid=12792831&isMobile=false",
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849907P2eew5cz5cxqosw7f485&balance=0&currency=USD&userid=12792840&isMobile=false",
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=SPRIBE&lan=es&partnerid=8&token=0P12849916Pf0q1a0zdltx9pgqlxoe&balance=0&currency=USD&userid=12792849&isMobile=false"
]

PLANTILLA_BASE = "Quieres Ganar Mas de 2 mil en 45 minutoｓ Escribeme al Whatsapp⚡ ✅𝐎𝟗𝟔𝟖𝟖𝟑𝟐𝟑𝟎𝟎✅⚓𝚃𝙴L𝙴𝙶𝚁AM😚✅𝙰𝚅𝙸𝙰𝚃𝙾𝚁𝙿𝙺𝙰✅Sin 𝙿agos adelantadoss⚓⚡⛳⛺➕➗VAR_3"
EMOJIS_POOL = list("😎😷😋😍😘😝😉😙🤓🔥💧👸😏🤑🤗👊✊👍💥👌👈👇👆👉👅👄🤘💏🙆💆💙💜💛💚👑🎩🙋💃🐽💗💌🤖🐺🐶💎🐦🐤🐥🐞🦄🐠🦀🦁🐼🐴🐒🐵➗🌹🌻🍄💐🌵🐩💵🎁💰")

historial_enviados = set()

def generar_mensaje_unico():
    global historial_enviados
    if len(historial_enviados) >= 10000: 
        historial_enviados.clear()
        
    for _ in range(5000):
        e1 = random.choice(EMOJIS_POOL)
        e2 = random.choice(EMOJIS_POOL)
        e3 = random.choice(EMOJIS_POOL)
        ultimos_tres = e1 + e2 + e3
        
        msg_final = PLANTILLA_BASE.replace("VAR_3", ultimos_tres)
        
        if msg_final not in historial_enviados:
            historial_enviados.add(msg_final)
            return msg_final
            
    return PLANTILLA_BASE.replace("VAR_3", "🔥💧👸")

def limpiar_especifico(pid):
    try:
        p = psutil.Process(pid)
        for hijo in p.children(recursive=True): hijo.kill()
        p.kill()
    except: pass
    gc.collect()

def iniciar():
    opt = Options()
    opt.add_argument("-headless")
    opt.set_preference("browser.cache.disk.enable", False)
    opt.set_preference("browser.cache.memory.enable", False)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=opt)
    try: driver.set_window_size(1920, 1080)
    except: pass
    return driver

def buscar_campo_texto(dr):
    try:
        caja = dr.find_elements(By.TAG_NAME, "textarea")
        if not caja: caja = dr.find_elements(By.CSS_SELECTOR, "input[type='text'], [contenteditable='true'], .chat-input, .message-input")
        if caja: return caja[0]
        iframes = dr.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            try:
                dr.switch_to.frame(frame)
                caja = dr.find_elements(By.TAG_NAME, "textarea")
                if not caja: caja = dr.find_elements(By.CSS_SELECTOR, "input[type='text'], [contenteditable='true'], .chat-input, .message-input")
                if caja: return caja[0]
                sub_caja = buscar_campo_texto(dr)
                if sub_caja: return sub_caja
                dr.switch_to.parent_frame()
            except:
                try: dr.switch_to.default_content()
                except: pass
    except: pass
    return None

def abrir_y_verificar_tags_todos(dr):
    print("⏳ [LITHIUMS1 - HEADLESS] Abriendo y preparando todos los chats en segundo plano...")
    handles = []
    for i, url in enumerate(LINKS):
        if i == 0:
            dr.get(url)
        else:
            dr.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(0.5)
        
        pestanas = dr.window_handles
        current_handle = pestanas[-1]
        handles.append(current_handle)
        dr.switch_to.window(current_handle)
        
        listo = False; intentos = 0
        while not listo and intentos < 12:
            dr.switch_to.default_content()
            if buscar_campo_texto(dr):
                listo = True
                break
            time.sleep(1); intentos += 1
        time.sleep(1)
    
    dr.switch_to.default_content()
    return handles

def disparar_con_protocolo_seguro(dr, handle, idx, msg):
    try:
        dr.switch_to.window(handle)
        dr.switch_to.default_content()
        target = buscar_campo_texto(dr)
        
        if target:
            try: target.click()
            except: pass
            
            try:
                target.send_keys(Keys.CONTROL + "a")
                target.send_keys(Keys.BACKSPACE)
            except: pass
            
            target.send_keys(msg)
            
            val_actual = target.get_attribute("value") or target.text
            if not val_actual or len(val_actual) < 10:
                dr.execute_script("arguments[0].value = arguments[1];", target, msg)
            
            target.send_keys(Keys.ENTER)
            return True
    except:
        pass
    finally:
        try: dr.switch_to.default_content()
        except: pass
    return False

def run():
    dr = iniciar()
    pid = dr.service.process.pid
    total_disparos_global = 0
    MAX_DISPAROS_CICLO = 1200
    
    try:
        handles = abrir_y_verificar_tags_todos(dr)
        num_tags = len(handles)
        
        proximo_disparo_por_tag = {i: 0.0 for i in range(num_tags)}
        
        print(f"\n🚀 [LITHIUMS1 ACTIONS] INICIANDO RACHAS INTELIGENTES ({num_tags} chats activos)...")
        
        while total_disparos_global < MAX_DISPAROS_CICLO:
            ahora = time.time()
            disparo_realizado_en_iteracion = False
            
            for idx in range(num_tags):
                if total_disparos_global >= MAX_DISPAROS_CICLO:
                    break
                
                if ahora >= proximo_disparo_por_tag[idx]:
                    msg = generar_mensaje_unico()
                    
                    if disparar_con_protocolo_seguro(dr, handles[idx], idx, msg):
                        total_disparos_global += 1
                        disparo_realizado_en_iteracion = True
                        print(f"    ⚡ [LITHIUMS1] Chat #{idx+1} enviado | Total ciclo: {total_disparos_global}/{MAX_DISPAROS_CICLO}")
                        
                        proximo_disparo_por_tag[idx] = time.time() + 5.0
            
            if not disparo_realizado_en_iteracion:
                time.sleep(0.1)
        
        print(f"\n🎯 [LITHIUMS1] META DE {MAX_DISPAROS_CICLO} ALCANZADA.")
        
    except Exception as e:
        print(f"⚠️ [LITHIUMS1] Error en ejecución: {e}")
    finally:
        try: dr.quit()
        except: pass
        limpiar_especifico(pid)
        historial_enviados.clear()
        gc.collect()
        print("🔄 [LITHIUMS1] Ciclo finalizado correctamente en GitHub Actions.\n")

if __name__ == "__main__": 
    run()
