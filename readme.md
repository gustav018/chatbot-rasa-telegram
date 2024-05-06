# Asistente de Telegram con Rasa y Python

Este es un proyecto para crear un asistente de Telegram utilizando Rasa como motor de procesamiento de lenguaje natural.

## Configuración del Entorno

1. Crea un entorno virtual con Conda:

    ```bash
    conda create -n asistente python=3.10
    ```

2. Activa el entorno virtual:

    ```bash
    conda activate asistente
    ```

3. Actualiza pip:

    ```bash
    python -m pip uninstall pip
    python -m ensurepip
    python -m pip install -U pip
    ```

4. Instala las dependencias necesarias:

    ```bash
    pip install python-telegram-bot==13.7
    pip install python-dotenv
    pip install rasa
    ```

## Obtención del Token de Telegram

Para obtener el token de Telegram, sigue estos pasos:

1. Dirígete a [https://t.me/BotFather](https://t.me/BotFather) en tu navegador ![BotFather](img/BotFather.png)

2. Envía el mensaje `/newbot` para crear un nuevo bot.

3. Sigue las instrucciones de BotFather para configurar tu nuevo bot y obtener el token de acceso.

4. Copia el token generado por BotFather.

5. Abre el archivo `.env` en la raíz de tu proyecto y pega el token en la variable `TELEGRAM_API_TOKEN`, de esta manera:

    ```
    TELEGRAM_API_TOKEN=your_telegram_api_token
    ```



## Inicialización y Entrenamiento del Proyecto Rasa

1. Este repositorio ya contiene los archivos de un proyecto Rasa básico. Solo necesitas dirigirte a la carpeta `rasa_chatbot`.

2. Si deseas entrenar el modelo con los archivos existentes en el repositorio, simplemente escribe el siguiente comando para entrenar el modelo:

    ```bash
    rasa train
    ```

3. Si quieres iniciar un proyecto nuevo en Rasa, ejecuta el siguiente comando:

    ```bash
    rasa init
    ```

## Ejecución del Asistente

1. En una terminal, ejecuta el script `python telegram_rasa.py` para iniciar el asistente de Telegram.



## Interacción Interactiva con Rasa (Opcional)

Una vez dentro de la carpeta de tu proyecto Rasa, puedes iniciar una sesión interactiva de Rasa con el siguiente comando:

```bash
rasa shell
