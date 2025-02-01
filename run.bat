start powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$env:TERM='xterm-256color'; & '%~dp0image-upscaler\Scripts\Activate.ps1'; python '%~dp0image-upscaler.py'"
