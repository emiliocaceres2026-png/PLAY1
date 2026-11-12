import time
import os
import json
import psutil
import gc
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
MAX_DISPAROS_CICLO = 1200  # Cada 1200 disparos limpia CPU/RAM y reinicia navegador
COOLDOWN_POR_TAG = 5.0

# =========================================================================
# CONFIGURACIÓN DE ENLACES / TOKENS (TAC1 y TAC2)
# =========================================================================
LINKS = [
    # TAC1
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=undefined&lan=es&partnerid=8&token=0P9598545P99mrw5j96ultpseez623&balance=0¤cy=USD&userid=9526601&isMobile=false",
    # TAC2
    "https://casino.virtualsoft.tech/game/play/?gameid=203831&mode=real&provider=undefined&lan=es&partnerid=8&token=0P4724879Pafkl7fdk385zeq5ie4gh&balance=0¤cy=USD&userid=4658141&isMobile=false"
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

# Eliminar cualquier duplicado accidental manteniendo el orden exacto
BLOQUE_1_TEXTOS = list(dict.fromkeys(BLOQUE_1_TEXTOS))
BLOQUE_2_TEXTOS = list(dict.fromkeys(BLOQUE_2_TEXTOS))

# =========================================================================
# GESTIÓN DE ESTADO PERSISTENTE INDEPENDIENTE POR TAC (TAC1, TAC2, etc.)
# =========================================================================
def inicializar_estado_tacs(num_tacs):
    estado = {
        "disparo_ciclo": 0,
        "total_acumulado": 0,
        "tacs": {}
    }
    for i in range(num_tacs):
        tac_id = f"TAC{i+1}"
        estado["tacs"][tac_id] = {
            "usados_b1": [],
            "usados_b2": [],
            "turno_bloque": 1  # Alterna 1 -> 2 -> 1 en cada TAC
        }
    return estado

def cargar_estado(num_tacs):
    estado_base = inicializar_estado_tacs(num_tacs)
    if os.path.exists(ESTADO_FILE):
        try:
            with open(ESTADO_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                estado_base["disparo_ciclo"] = data.get("disparo_ciclo", 0)
                estado_base["total_acumulado"] = data.get("total_acumulado", 0)
                tacs_guardados = data.get("tacs", {})
                for tac_id in estado_base["tacs"]:
                    if tac_id in tacs_guardados:
                        estado_base["tacs"][tac_id]["usados_b1"] = tacs_guardados[tac_id].get("usados_b1", [])
                        estado_base["tacs"][tac_id]["usados_b2"] = tacs_guardados[tac_id].get("usados_b2", [])
                        estado_base["tacs"][tac_id]["turno_bloque"] = tacs_guardados[tac_id].get("turno_bloque", 1)
        except:
            pass
    return estado_base

def guardar_estado(estado):
    try:
        with open(ESTADO_FILE, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False, indent=2)
    except:
        pass

def obtener_siguiente_mensaje_tac(estado, tac_id):
    """
    Obtiene el siguiente mensaje disponible para este TAC sin repetir
    ninguno ya enviado en este mismo TAC hasta agotar el bloque completo.
    """
    info_tac = estado["tacs"][tac_id]
    bloque_num = info_tac["turno_bloque"]

    if bloque_num == 1:
        lista_completa = BLOQUE_1_TEXTOS
        clave_usados = "usados_b1"
        nombre_bloque = "Bloque 1"
    else:
        lista_completa = BLOQUE_2_TEXTOS
        clave_usados = "usados_b2"
        nombre_bloque = "Bloque 2"

    usados = info_tac[clave_usados]
    disponibles = [txt for txt in lista_completa if txt not in usados]

    # Si ya se enviaron todos los textos del bloque en este TAC, reiniciar ciclo del bloque
    if not disponibles:
        print(f"    🔄 [{tac_id} - {nombre_bloque}] Todos los textos usados. Reiniciando lista del bloque...")
        info_tac[clave_usados] = []
        disponibles = list(lista_completa)

    mensaje_elegido = disponibles[0]
    return mensaje_elegido, bloque_num, nombre_bloque

def registrar_disparo_tac(estado, tac_id, bloque_num, mensaje_enviado):
    """Registra el mensaje en el historial del TAC y alterna el bloque para su próximo turno."""
    info_tac = estado["tacs"][tac_id]
    if bloque_num == 1:
        info_tac["usados_b1"].append(mensaje_enviado)
        info_tac["turno_bloque"] = 2
    else:
        info_tac["usados_b2"].append(mensaje_enviado)
        info_tac["turno_bloque"] = 1

# =========================================================================
# LIMPIEZA PROFUNDA DE PROCESOS, CPU Y RAM
# =========================================================================
def limpiar_procesos_y_memoria(pid=None):
    print("🧹 [LIMPIEZA SISTEMA] Liberando CPU, procesos huérfanos de Firefox/GeckoDriver y memoria RAM...")
    if pid:
        try:
            p = psutil.Process(pid)
            for hijo in p.children(recursive=True):
                hijo.kill()
            p.kill()
        except:
            pass

    # Barrido adicional de cualquier proceso zombie de firefox o geckodriver en memoria
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            nombre = (proc.info['name'] or '').lower()
            if 'firefox' in nombre or 'geckodriver' in nombre:
                proc.kill()
        except:
            pass

    gc.collect()
    time.sleep(2)
    print("✅ [LIMPIEZA SISTEMA] CPU y RAM liberadas correctamente.")

def iniciar():
    opt = Options()
    opt.add_argument("--headless")
    opt.set_preference("browser.cache.disk.enable", False)
    opt.set_preference("browser.cache.memory.enable", False)
    opt.set_preference("browser.sessionhistory.max_entries", 2)
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
    print(f"⏳ [ECUABET] Abriendo y preparando {len(LINKS)} pestañas (TAC1..TAC{len(LINKS)}) en modo Headless...")
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

def disparar_con_protocolo_seguro(dr, handle, tac_id, msg):
    try:
        estable, target = verificar_chat_listo_y_estable(dr, handle)
        if not estable or target is None:
            try:
                dr.switch_to.window(handle)
                dr.switch_to.default_content()
                restriccion = dr.find_elements(By.CSS_SELECTOR, "app-chat-message-restriction")
                if restriccion:
                    print(f"    🛡️ [{tac_id} - ANTI-RESTRICCIÓN] Saldo inferior a 5 USD detectado. Saltando turno...")
                else:
                    btn_chat = dr.find_element(By.CSS_SELECTOR, "button.btn.btn-circl.header__btn-chat")
                    if btn_chat.is_displayed():
                        btn_chat.click()
                        print(f"    🛡️ [{tac_id} - ANTI-CAÍDAS] Red inestable detectada: Chat cerrado temporalmente.")
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
# CICLO PRINCIPAL CONTINUO CON REINICIO Y LIMPIEZA CADA 1200 DISPAROS
# =========================================================================
def ejecutar_ciclo_1200(estado):
    dr = iniciar()
    pid = dr.service.process.pid

    try:
        handles = abrir_y_verificar_tags_todos(dr)
        if not handles:
            print("⚠️ [ERROR] No se pudo abrir ningún enlace. Reintentando tras limpieza...")
            return

        print(f"\n🚀 [ECUABET ACTIONS] INICIANDO BLOQUE DE {MAX_DISPAROS_CICLO} DISPAROS (Ciclo actual: {estado['disparo_ciclo']}/{MAX_DISPAROS_CICLO} | Acumulado histórico: {estado['total_acumulado']})...")

        while estado["disparo_ciclo"] < MAX_DISPAROS_CICLO:
            alguno_enviado = False

            for idx, handle in enumerate(handles):
                if estado["disparo_ciclo"] >= MAX_DISPAROS_CICLO:
                    break

                tac_id = f"TAC{idx+1}"
                msg, bloque_num, nombre_bloque = obtener_siguiente_mensaje_tac(estado, tac_id)

                if disparar_con_protocolo_seguro(dr, handle, tac_id, msg):
                    registrar_disparo_tac(estado, tac_id, bloque_num, msg)
                    estado["disparo_ciclo"] += 1
                    estado["total_acumulado"] += 1
                    alguno_enviado = True

                    usados_count = len(estado["tacs"][tac_id][f"usados_b{bloque_num}"])
                    total_bloque = len(BLOQUE_1_TEXTOS) if bloque_num == 1 else len(BLOQUE_2_TEXTOS)

                    print(f"    ⚡ [{tac_id} | {nombre_bloque}] ({usados_count}/{total_bloque}) | Ciclo: {estado['disparo_ciclo']}/{MAX_DISPAROS_CICLO} | Total: {estado['total_acumulado']}")
                    guardar_estado(estado)
                    time.sleep(COOLDOWN_POR_TAG)

            if not alguno_enviado:
                time.sleep(2.0)

        print(f"\n🎯 [ECUABET] META DE {MAX_DISPAROS_CICLO} DISPAROS DEL CICLO ALCANZADA. PREPARANDO LIMPIEZA Y REINICIO...")
        # Reinicia el contador del ciclo para la siguiente vuelta manteniendo intactos los historiales usados_b1 y usados_b2
        estado["disparo_ciclo"] = 0
        guardar_estado(estado)

    except Exception as e:
        print(f"⚠️ [ECUABET] Error en ejecución: {e}")
    finally:
        try:
            dr.quit()
        except:
            pass
        limpiar_procesos_y_memoria(pid)

def run():
    if not LINKS:
        print("⚠️ [ERROR] No hay enlaces configurados en LINKS.")
        return

    # Bucle infinito controlado: corre 1200 -> limpia CPU/RAM -> vuelve a correr
    while True:
        estado = cargar_estado(len(LINKS))
        ejecutar_ciclo_1200(estado)
        print("🔄 [ECUABET] Reiniciando nueva sesión limpia en 3 segundos...\n")
        time.sleep(3)

if __name__ == "__main__":
    run()
