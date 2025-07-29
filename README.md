# Juego de piedra papel o tijera con Hiwonder uHandPi

## Instrucciones

1. Clonar el repositorio:
```sh
    git clone https://github.com/OssianGH/rps.git
    cd rps
```
2. Encender la mano, conectarse al wifi de la misma y copiar el archivo del servidor de la mano:
```sh
    scp hand_server.py pi@192.168.149.1:/home/pi/uHand_Pi
```
3. Copiar los archivos de las acciones de la mano
```sh
    scp 21_reset.d6a pi@192.168.149.1:/home/pi/uHand_Pi/ActionGropus
    scp 22_rock.d6a pi@192.168.149.1:/home/pi/uHand_Pi/ActionGropus
    scp 23_sissors.d6a pi@192.168.149.1:/home/pi/uHand_Pi/ActionGropus
    scp 24_paper.d6a pi@192.168.149.1:/home/pi/uHand_Pi/ActionGropus
```
4. Ir al directorio del servidor local:
```sh
    cd rps_game_remote
    python -m venv venv
    source venv/bin/activate  # En Windows usar `venv\Scripts\activate`
```
5. Crear un entorno virtual:
```sh
    cd rps_game_remote
    python -m venv venv
    source venv/bin/activate  # En Windows usar `venv\Scripts\activate`
```
6. Instalar las dependencias requeridas:
```sh
    pip install flask pillow numpy tensorflow requests flask-cors
```
7. Ejecutar el servidor local:
```sh
    flask run
```
8. En otra terminal, ejecutar el servidor de la mano:
```sh
    ssh pi@192.168.149.1 (contraseña: Raspberry)
    cd /home/pi/uHand_Pi/
    python3 hand_server.py
```
