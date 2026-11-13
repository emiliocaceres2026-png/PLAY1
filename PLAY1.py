import time, os, json, psutil, gc
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

# =========================================================================
# CONFIGURACIÓN DE ARCHIVOS Y REGLAS DE TIEMPO
# =========================================================================
ESTADO_FILE = "estado_ecuabet.json"
MAX_DISPAROS_CICLO = 1200  # Purga optimizada cada 1200 disparos
COOLDOWN_POR_TAG = 5.0

# =========================================================================
# CONFIGURACIÓN DE ENLACES / TOKENS
# =========================================================================
LINKS = [
    # Chat / Tag 1
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=undefined&lan=es&partnerid=8&token=0P3501298Pekhpe0ithgteoe3q2nz8&balance=0&currency=USD&userid=3406564&isMobile=false"
]

LINKS = [link for link in LINKS if link and not link.startswith("AQUI_TU_")]

# =========================================================================
# BLOQUE 1 - SECUENCIA EXACTA (128 TEXTOS DE TELEGRAM)
# =========================================================================
BLOQUE_1_TEXTOS = [
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😄😍😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😄😍😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😜😄😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😄😍😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😙😜😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😘😙😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😍😃😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑🙂🔥",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😄😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😍😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😜😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😗😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😉😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🔥😎😌",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😌",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🤑😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💛😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💛😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💛😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💛😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😚",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😳",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😉",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💜😎😁",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😚",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😳",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😉",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💚😎😁",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😚",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😳",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😉",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💙😎😁",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎🎁😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😚",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😳",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😉",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👸😎😁",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😌",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😚",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😳",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😉",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎👑😎😁",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😄",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😍",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😃",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😘",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😝",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😀",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😚",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😛",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😊",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😗",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😉",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😙",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎💵😎😁"
]

# =========================================================================
# BLOQUE 2 - TEXTOS CON NÚMEROS Y EMOJIS PROPORCIONADOS (SIN REPETIR)
# =========================================================================
EMOJIS_BLOQUE_2 = [
    "🌀", "🌁", "🌂", "🌃", "🌄", "🌅", "🌆", "🌇", "🌈", "🌉", 
    "🌊", "🌋", "🌌", "🌍", "🌎", "🌏", "🌐", "🌑", "🌒", "🌓", 
    "🌔", "🌕", "🌖", "🌗", "🌘", "🌙", "🌚", "🌛", "🌜", "🌝", 
    "🌞", "🌟", "🌠", "🌭", "🌮", "🌯", "🌰", "🌱", "🌲", "🌳", 
    "🌴", "🌵", "🌶", "🌷", "🌸", "🌹", "🌺", "🌻", "🌼", "🌽", 
    "🌾", "🌿", "🍀", "🍁", "🍂", "🍃", "🍄", "🍅", "🍆", "🍇", 
    "🍈", "🍉", "🍊", "🍋", "🍌", "🍍", "🍎", "🍏", "🍐", "🍑", 
    "🍒", "🍓", "🍔", "🍕", "🍖", "🍗", "🍘", "🍙", "🍚", "🍛", 
    "🍜", "🍝", "🍞", "🍟", "🍠", "🍡", "🍢", "🍣", "🍤", "🍥", 
    "🍦", "🍧", "🍨", "🍩", "🍪", "🍫", "🍬", "🍭", "🍮", "🍯", 
    "🍰", "🍱", "🍲", "🍳", "🍴", "🍵", "🍶", "🍷", "🍸", "🍹", 
    "🍺", "🍻", "🍼", "🍽", "🍾", "🍿", "🎀", "🎁", "🎂", "🎃", 
    "🎄", "🎅", "🎆", "🎇", "🎈", "🎉", "🎊", "🎋", "🎌", "🎍", 
    "🎎", "🎏", "🎐", "🎑", "🎒", "🎲", "🎳", "🎴", "🎵", "🎶", 
    "🎷", "🎸", "🎹", "🎺", "🎻", "🎼", "🎽", "🎾", "🎿", "🏀", 
    "🏁", "🏂", "🏃", "🏄", "🏅", "🏆", "🏇", "🏈", "🏉", "🏊", 
    "🏋", "🏌", "👈", "👉", "👊", "👋", "👌", "👍", "👎", "👏", 
    "👐", "👑", "👒", "👓", "👔", "👕", "👖", "👗", "👘", "👙", 
    "👚", "👛", "👜", "👝", "👞", "👟", "👠", "👡", "👢", "👣", 
    "👤", "👥", "👦", "👧", "👨", "👩", "👪", "👫", "👬", "👭", 
    "👮", "👯", "👰", "👱", "👲", "👳", "👴", "👵", "👶", "👷", 
    "👸", "👹", "👺", "👻", "👼", "👽", "👾", "👿", "💀", "💁", 
    "💂", "💃", "💄", "💅", "💆", "💇", "💈", "💉", "💊", "💋", 
    "💌", "💍", "💎", "💏", "💐", "💑", "💒", "💓", "💔", "💕", 
    "💖", "💗", "💘", "💙", "💚", "💛", "💜", "💝", "💞", "💟", 
    "💠", "💡", "💢", "💣", "💤", "💥", "💦", "💧", "💨", "📙", 
    "📚", "📛", "📜", "📝", "📞", "📟", "📠", "📡", "📢", "📣", 
    "📤", "📥", "📦", "📧", "📨", "📩", "📪", "📫", "📬", "📭", 
    "📮", "📯", "📰", "📱", "📲", "📳", "📴", "📵"
]

BLOQUE_2_TEXTOS = [
    f"15 Quieres ganar mas de 4 m1l2nes en 45 minutos pide 1nf0 {emoji} 𝟶𝟿𝟼 𝟾𝟾𝟹 𝟸𝟹 𝟶0 o al tlg aviatorpka sin cobros adelantados"
    for emoji in EMOJIS_BLOQUE_2
]

TOTAL_TEXTOS_B1 = len(BLOQUE_1_TEXTOS)
TOTAL_TEXTOS_B2 = len(BLOQUE_2_TEXTOS)

# =========================================================================
# GESTIÓN DE ESTADO PERSISTENTE DUAL EN DISCO
# =========================================================================
def cargar_estado():
    if os.path.exists(ESTADO_FILE):
        try:
            with open(ESTADO_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return (
                    data.get("indice_b1", 0), 
                    data.get("indice_b2", 0), 
                    data.get("disparo_global", 0)
                )
        except:
            pass
    return 0, 0, 0

def guardar_estado(indice_b1, indice_b2, disparo_global):
    try:
        with open(ESTADO_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "indice_b1": indice_b1, 
                "indice_b2": indice_b2, 
                "disparo_global": disparo_global
            }, f, ensure_ascii=False)
    except:
        pass

# =========================================================================
# LIMPIEZA DE PROCESOS Y NAVEGADOR
# =========================================================================
def limpiar_procesos_navegador(pid):
    try:
        p = psutil.Process(pid)
        for hijo in p.children(recursive=True):
            hijo.kill()
        p.kill()
    except:
        pass
    gc.collect()

def iniciar():
    opt = Options()
    # MODO HEADLESS ACTIVADO PARA AHORRAR CPU Y RAM
    opt.add_argument("--headless")
    
    opt.set_preference("browser.cache.disk.enable", False)
    opt.set_preference("browser.cache.memory.enable", False)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=opt)
    try:
        driver.set_window_size(1366, 768)
    except:
        pass
    return driver

# =========================================================================
# DETECCIÓN DE ELEMENTOS Y SISTEMA ANTI-RESTRICCIÓN DE SALDO
# =========================================================================
def buscar_campo_texto(dr):
    try:
        caja = dr.find_elements(By.TAG_NAME, "textarea")
        if not caja:
            caja = dr.find_elements(By.CSS_SELECTOR, "input[type='text'], [contenteditable='true'], .chat-input, .message-input")
        if caja:
            return caja[0]
            
        iframes = dr.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            try:
                dr.switch_to.frame(frame)
                caja = dr.find_elements(By.TAG_NAME, "textarea")
                if not caja:
                    caja = dr.find_elements(By.CSS_SELECTOR, "input[type='text'], [contenteditable='true'], .chat-input, .message-input")
                if caja:
                    return caja[0]
                sub_caja = buscar_campo_texto(dr)
                if sub_caja:
                    return sub_caja
                dr.switch_to.parent_frame()
            except:
                try:
                    dr.switch_to.default_content()
                except:
                    pass
    except:
        pass
    return None

def verificar_chat_listo_y_estable(dr, handle):
    try:
        dr.switch_to.window(handle)
        dr.switch_to.default_content()

        # 1. Verificar si hay restricción de saldo activa en pantalla (<app-chat-message-restriction>)
        try:
            restriccion = dr.find_elements(By.CSS_SELECTOR, "app-chat-message-restriction")
            if restriccion and restriccion[0].is_displayed():
                return False, None # Se considera no estable/restringido para evitar disparar
        except:
            pass

        # 2. Palabras clave de bloqueo o desconexión
        textos_bloqueo = ["reconectando", "reconnecting", "connecting...", "sin conexión", "esperando conexión", "error de red"]
        try:
            body_text = dr.find_element(By.TAG_NAME, "body").text.lower()
            if any(t in body_text for t in textos_bloqueo):
                return False, None
        except:
            pass

        target = buscar_campo_texto(dr)
        if target and target.is_displayed() and target.is_enabled():
            return True, target
    except:
        pass
    return False, None

def abrir_y_verificar_tags_todos(dr):
    print(f"⏳ [ECUABET] Abriendo y preparando {len(LINKS)} pestañas en modo Headless...")
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
        
        listo = False
        intentos = 0
        while not listo and intentos < 20:
            estable, _ = verificar_chat_listo_y_estable(dr, current_handle)
            if estable:
                listo = True
                break
            time.sleep(1)
            intentos += 1
        time.sleep(1)
    
    dr.switch_to.default_content()
    return handles

def disparar_con_protocolo_seguro(dr, handle, msg):
    try:
        # Verificación previa de estabilidad y restricción de saldo (< 5 USD)
        estable, target = verificar_chat_listo_y_estable(dr, handle)
        if not estable or target is None:
            try:
                dr.switch_to.window(handle)
                dr.switch_to.default_content()
                restriccion = dr.find_elements(By.CSS_SELECTOR, "app-chat-message-restriction")
                if restriccion:
                    print("    🛡️ [ANTI-RESTRICCIÓN] Saldo inferior a 5 USD detectado. Bot en modo espera (ignorando turno hasta que recargues)...")
                else:
                    # Si la red falló, intentamos cerrar el chat con el botón para proteger
                    btn_chat = dr.find_element(By.CSS_SELECTOR, "button.btn.btn-circl.header__btn-chat")
                    if btn_chat.is_displayed():
                        btn_chat.click()
                        print("    🛡️ [ANTI-CAÍDAS] Red inestable detectada: Chat cerrado temporalmente.")
            except:
                pass
            return False

        try:
            target.click()
        except:
            pass
        
        try:
            target.send_keys(Keys.CONTROL + "a")
            target.send_keys(Keys.BACKSPACE)
        except:
            pass
        
        target.send_keys(msg)
        
        val_actual = target.get_attribute("value") or target.text
        if not val_actual or len(val_actual) < 10:
            dr.execute_script("arguments[0].value = arguments[1];", target, msg)
        
        target.send_keys(Keys.ENTER)
        
        # Verificación posterior instantánea: ¿Apareció la restricción justo al enviar?
        time.sleep(0.5)
        restriccion_post = dr.find_elements(By.CSS_SELECTOR, "app-chat-message-restriction")
        if restriccion_post and restriccion_post[0].is_displayed():
            print("    ⚠️ [ALERTA] Restricción de saldo activada tras el envío. Pausando disparos.")
            return False

        return True
    except:
        pass
    finally:
        try:
            dr.switch_to.default_content()
        except:
            pass
    return False

# =========================================================================
# CICLO PRINCIPAL CON PURGA CADA 1200 DISPAROS Y CERO REPETICIONES
# =========================================================================
def run():
    if not LINKS:
        print("❌ Error: No se configuraron enlaces válidos en la lista LINKS.")
        return

    indice_b1, indice_b2, contador_disparos = cargar_estado()
    
    print(f"[SISTEMA] Ecuabet / Virtualsoft Iniciado (Modo Headless 🕶️).")
    print(f"[SISTEMA] Reanudando Bloque 1 [{indice_b1 + 1}/{TOTAL_TEXTOS_B1}] | Bloque 2 [{indice_b2 + 1}/{TOTAL_TEXTOS_B2}] | Global: {contador_disparos}")
    print(f"[SISTEMA] Ciclo de purga configurado cada {MAX_DISPAROS_CICLO} disparos (Anti-Restricción de Saldo Activa).\n")

    while True:
        dr = iniciar()
        pid = dr.service.process.pid
        disparos_en_ciclo = 0

        try:
            handles = abrir_y_verificar_tags_todos(dr)
            num_tags = len(handles)
            proximo_disparo_por_tag = {i: 0.0 for i in range(num_tags)}
            idx_tag_actual = 0
            
            print(f"\n🚀 [ECUABET] CICLO EN CURSO ({num_tags} pestañas activas en segundo plano)...")

            while disparos_en_ciclo < MAX_DISPAROS_CICLO:
                ahora = time.time()
                tiempo_espera = proximo_disparo_por_tag[idx_tag_actual] - ahora
                if tiempo_espera > 0:
                    time.sleep(tiempo_espera)

                handle = handles[idx_tag_actual]

                # Comprobación de estabilidad y saldo antes de tomar el turno
                estable, _ = verificar_chat_listo_y_estable(dr, handle)
                if not estable:
                    print(f"    ⏸️ Pestaña #{idx_tag_actual + 1} restringida o en reconexión. Esperando habilitación...")
                    time.sleep(3.0)
                    continue

                # Selección secuencial y ordenada de bloques sin repetición anticipada
                if disparos_en_ciclo % 2 == 0:
                    msg = BLOQUE_1_TEXTOS[indice_b1]
                    tipo_bloque = f"B1 [{indice_b1 + 1}/{TOTAL_TEXTOS_B1}]"
                else:
                    msg = BLOQUE_2_TEXTOS[indice_b2]
                    tipo_bloque = f"B2 [{indice_b2 + 1}/{TOTAL_TEXTOS_B2}]"

                enviado = disparar_con_protocolo_seguro(dr, handle, msg)

                if enviado:
                    contador_disparos += 1
                    disparos_en_ciclo += 1
                    print(f"    ⚡ Pestaña #{idx_tag_actual + 1} -> Enviado {tipo_bloque} | Ciclo: {disparos_en_ciclo}/{MAX_DISPAROS_CICLO} | Total: {contador_disparos}")
                    
                    # Avanzar índices de forma estrictamente ordenada
                    if disparos_en_ciclo % 2 == 0:
                        indice_b1 = (indice_b1 + 1) % TOTAL_TEXTOS_B1
                    else:
                        indice_b2 = (indice_b2 + 1) % TOTAL_TEXTOS_B2

                    # Guardar progreso al instante en disco para mantener el orden exacto
                    guardar_estado(indice_b1, indice_b2, contador_disparos)

                    proximo_disparo_por_tag[idx_tag_actual] = time.time() + COOLDOWN_POR_TAG
                    idx_tag_actual = (idx_tag_actual + 1) % num_tags
                else:
                    print(f"    ⚠️ Pausa en Pestaña #{idx_tag_actual + 1} (Saldo < 5 USD o Restricción activa). Manteniendo orden en cola...")
                    time.sleep(3.0)

            # LLEGADA A LA META DE 1200 DISPAROS (PURGA DE CACHÉ / CPU)
            print(f"\n🎯 [ECUABET] META DE {MAX_DISPAROS_CICLO} DISPAROS ALCANZADA.")
            print(f"🧹 Purgando navegador headless y liberando memoria RAM y CPU...")

        except Exception as e:
            print(f"⚠️ [ECUABET] Excepción en ejecución: {e}. Reiniciando sesión sin perder índice...")
        finally:
            try:
                dr.quit()
            except:
                pass
            limpiar_procesos_navegador(pid)
            print(f"🔄 Navegador purgado con éxito. Retomando sesión limpia en orden exacto...\n")
            time.sleep(5.0)

if __name__ == "__main__":
    run()
