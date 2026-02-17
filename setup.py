# setup.py
"""
Arquivo de configuração para criar executável usando PyInstaller
Instale PyInstaller primeiro: pip install pyinstaller
Para criar executável: python setup.py
"""

import PyInstaller.__main__
import os
import sys

# Nome do arquivo principal
main_script = 'main.py'

# Ícone (opcional) - você pode adicionar um arquivo .ico
icon_file = 'icon.ico' if os.path.exists('icon.ico') else None

# Configurações do PyInstaller
args = [
    main_script,
    '--name=WindowsOptimizerPro',
    '--onefile',
    '--windowed',  # Não mostra console
    '--clean',
    '--noconfirm',
]

# Adicionar ícone se existir
if icon_file:
    args.append(f'--icon={icon_file}')

# Adicionar dados adicionais
args.extend([
    '--add-data=modules;modules',  # Incluir módulos
    '--hidden-import=PySide6.QtCore',
    '--hidden-import=PySide6.QtWidgets',
    '--hidden-import=PySide6.QtGui',
])

# Executar PyInstaller
if __name__ == '__main__':
    print("📦 Criando executável do Windows Optimizer Pro...")
    PyInstaller.__main__.run(args)
    print("✅ Executável criado com sucesso na pasta 'dist'!")