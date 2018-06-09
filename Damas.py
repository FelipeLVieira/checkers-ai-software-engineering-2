#!/usr/bin/env python3
try:
    import pygame
except:
    print("Erro: este aplicativo precisa da biblioteca externa `pygame' para ser executado.\nPor favor, instale-a antes de executar este programa.")
    sys.exit(1)
import sys
import os
sys.path.append(os.path.abspath("src"))
os.chdir(os.path.abspath("src"))
import Title
Title.main()
