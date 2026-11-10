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
MAX_DISPAROS_CICLO = 1200  # <--- Límite ajustado a 1200 disparos por ciclo
COOLDOWN_POR_TAG = 5.0

# =========================================================================
# CONFIGURACIÓN DE ENLACES / TOKENS
# =========================================================================
LINKS = [
    # Chat / Tag 1
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=undefined&lan=es&partnerid=8&token=0P2660662Patst910sitki1p9qe1i6&balance=0&currency=USD&userid=2528761&isMobile=false"
]

LINKS = [link for link in LINKS if link and not link.startswith("AQUI_TU_")]

# =========================================================================
# BLOQUE 1 - SECUENCIA EXACTA
# =========================================================================
BLOQUE_1_TEXTOS = [
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😄😍😜",
    "Quieres ganar mas de 19OO in 45 minuts sin tener perdidas scribeme seguro abajo les dejo tlg ⚓AVIATORPKA⚓ estamos Disponibles🔥ven te esperamos💎😍😄😜",
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

        try:
            restriccion = dr.find_elements(By.CSS_SELECTOR, "app-chat-message-restriction")
            if restriccion and restriccion[0].is_displayed():
                return False, None
        except:
            pass

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
        estable, target = verificar_chat_listo_y_estable(dr, handle)
        if not estable or target is None:
            try:
                dr.switch_to.window(handle)
                dr.switch_to.default_content()
                restriccion = dr.find_elements(By.CSS_SELECTOR, "app-chat-message-restriction")
                if restriccion:
                    print("    🛡️ [ANTI-RESTRICCIÓN] Saldo inferior a 5 USD detectado. Bot en modo espera (ignorando turno hasta que recargues)...")
                else:
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
        if not val_actual or len(val_actual) < 5:
            dr.execute_script("arguments[0].value = arguments[1];", target, msg)
        
        target.send_keys(Keys.ENTER)
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
# CICLO PRINCIPAL DE EJECUCIÓN
# =========================================================================
def run():
    indice_b1, indice_b2, disparo_global = cargar_estado()
    dr = iniciar()
    pid = dr.service.process.pid

    try:
        handles = abrir_y_verificar_tags_todos(dr)
        if not handles:
            print("⚠️ [ERROR] No se pudo abrir ningún enlace.")
            return

        print(f"\n🚀 [ECUABET ACTIONS] INICIANDO SECUENCIA DUAL (Disparos previos registrados: {disparo_global})...")

        while disparo_global < MAX_DISPAROS_CICLO:
            if disparo_global % 2 == 0:
                msg = BLOQUE_1_TEXTOS[indice_b1]
                bloque_activo = "Bloque 1"
                indice_b1 = (indice_b1 + 1) % TOTAL_TEXTOS_B1
            else:
                msg = BLOQUE_2_TEXTOS[indice_b2]
                bloque_activo = "Bloque 2"
                indice_b2 = (indice_b2 + 1) % TOTAL_TEXTOS_B2

            enviado = False
            for idx, handle in enumerate(handles):
                if disparar_con_protocolo_seguro(dr, handle, msg):
                    disparo_global += 1
                    enviado = True
                    print(f"    ⚡ [{bloque_activo}] Chat #{idx+1} enviado | Total global: {disparo_global}/{MAX_DISPAROS_CICLO}")
                    guardar_estado(indice_b1, indice_b2, disparo_global)
                    break
            
            if enviado:
                time.sleep(COOLDOWN_POR_TAG)
            else:
                time.sleep(2.0)

        print(f"\n🎯 [ECUABET] META DE {MAX_DISPAROS_CICLO} DISPAROS ALCANZADA.")

    except Exception as e:
        print(f"⚠️ [ECUABET] Error en ejecución: {e}")
    finally:
        try:
            dr.quit()
        except:
            pass
        limpiar_procesos_navegador(pid)
        gc.collect()
        print("🔄 [ECUABET] Ciclo finalizado correctamente en GitHub Actions.\n")

if __name__ == "__main__":
    run()
