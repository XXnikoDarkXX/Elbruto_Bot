# 🥊 ElBruto Bot

Bot automático para gestionar y combatir con tus personajes de **ElBruto**.  
Permite registrar brutos a torneos, luchar automáticamente y resolver subidas de nivel, enviando notificaciones a través de Telegram.

---

## ✨ Características

- ✅ Registro automático en torneos (opcional).
- ⚔️ Combates automáticos (6 u 8 por día según habilidades).
- 📈 Detección de subida de nivel antes y durante combates.
- 🤖 Elección automática de recompensas según reglas personalizadas.
- 📩 Notificaciones detalladas en Telegram.
- ⛔ Pausa automática si la subida requiere revisión manual.

---

## 📦 Requisitos

- Python **3.8** o superior
- Cuenta de Telegram y un bot creado con [@BotFather](https://t.me/BotFather)
- Token de API y Chat ID de Telegram
- Dependencias indicadas en `requirements.txt`

---

## ⚙️ Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/usuario/ElBruto_Bot.git
   cd ElBruto_Bot




2. **Crea un entorno virtual e instala las dependencias:**
```bash
  python -m venv venv
  source venv/bin/activate   # En Linux/Mac
  venv\Scripts\activate      # En Windows
  pip install -r requirements.txt
```

3. **Configura las variables de entorno creando un archivo .env:**
Configura las variables de entorno creando un archivo .env:
```bash
  TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
  TELEGRAM_CHAT_ID=7194420980
```

---
## ▶️ Uso
**Para ejecutar el bot:**
```bash
python main.py
```
El bot:
1. Comprueba si hay subida de nivel pendiente.
2. Registra al bruto en torneo si está activado.
3. Lucha contra los oponentes disponibles.
4. Resuelve subidas de nivel durante combates si ocurren.
5. Detiene los combates si es necesaria revisión manual.

---

## 📂 Estructura del proyecto
ElBruto_Bot/
├── core/
│ └── utils.py
├── modules/
│ ├── brute.py
│ ├── brute_manager.py
│ ├── brute_logic.py
│ ├── telegram_notifier.py
├── .env
├── requirements.txt
├── main.py
└── README.md

---

## 📬 Notificaciones de Telegram

El bot envía mensajes con:
- Información detallada del bruto.
- Subida de nivel con recompensas.
- Combates realizados, victorias y derrotas.
- Avisos de revisión manual.

**Ejemplo de notificación:**
```bash
- 👤 Usuario: TuNombre
- 🎉 ¡Subida de Nivel! 🎉
- Nombre: Brutazo
- Nivel: 5
- ...
- 🎁 Recompensas disponibles:

    - Opción 1: strength +2

    - Opción 2: agility +1
```

---

## 🛠 Personalización

- **Reglas de elección de recompensa:** en `brute_manager.py` dentro del método `elegir_recompensa`.
- **Formato de mensajes:** en `telegram_notifier.py`.
- **Número de combates diarios:** se define según habilidades en `brute_logic.py`.

---

## 🐞 Solución de problemas

| Error | Posible causa | Solución |
|-------|---------------|----------|
| `401 Unauthorized` | El token de Telegram es incorrecto | Verifica `TELEGRAM_BOT_TOKEN` en `.env` |
| `Can't parse entities` | Error de formato en MarkdownV2 | Escapa texto dinámico con `escape_markdown_v2()` |
| No envía mensajes | Chat ID incorrecto o bot no iniciado | Envía un mensaje al bot desde Telegram y usa el Chat ID correcto |
