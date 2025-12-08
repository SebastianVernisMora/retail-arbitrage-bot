# 🚀 Guía de Instalación - Retail Arbitrage Bot

## Requisitos Previos

- Python 3.8 o superior
- Node.js 14 o superior
- Git
- Cuenta de Gmail con App Password
- Número de WhatsApp

## Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/SebastianVernisMora/retail-arbitrage-bot.git
cd retail-arbitrage-bot
```

### 2. Crear Entorno Virtual de Python

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 4. Instalar Dependencias Node.js

```bash
npm install
```

### 5. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env` con tu editor favorito:

```bash
nano .env  # O usar tu editor favorito
```

#### Obtener Gmail App Password

1. Ve a https://myaccount.google.com/apppasswords
2. Selecciona "Correo" (Mail) y "Otro"
3. Copia el código de 16 caracteres
4. Pégalo en `GMAIL_APP_PASSWORD` (sin espacios o con espacios, ambos funcionan)

#### Configuración Completa de .env

```env
# Gmail
GMAIL_USER=tu-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Notificaciones
NOTIFY_EMAIL=tu-email@gmail.com
NOTIFY_PHONE=+521234567890

# Búsqueda (separadas por comas)
SEARCH_QUERY=sidra,rompope,juguetes

# Criterios
MIN_DISCOUNT=30
MAX_PRICE=500

# Tiendas
STORES=walmart,liverpool,chedraui

# Frecuencia (horas entre búsquedas)
CHECK_INTERVAL_HOURS=6

# Criterios de rentabilidad
MIN_MARGIN=50
MIN_ROI=50
MAX_STORAGE_DAYS=90
```

### 6. Ejecutar la Aplicación

```bash
python main.py
```

La primera vez, mostrará un código QR de WhatsApp. Escanea con tu teléfono:

**WhatsApp → Dispositivos Vinculados → Vincular un Dispositivo**

## Ejecución Automática (Linux)

### Configurar como Servicio Systemd

1. Edita `retail-arbitrage.service`:

```bash
sudo nano retail-arbitrage.service
```

2. Reemplaza:
   - `tu-usuario` con tu nombre de usuario
   - `/home/tu-usuario/` con tu ruta completa

3. Copia el archivo:

```bash
sudo cp retail-arbitrage.service /etc/systemd/system/
```

4. Habilita y inicia:

```bash
sudo systemctl daemon-reload
sudo systemctl enable retail-arbitrage
sudo systemctl start retail-arbitrage
```

5. Verifica el estado:

```bash
sudo systemctl status retail-arbitrage
```

6. Ver logs:

```bash
sudo journalctl -u retail-arbitrage -f
```

## Solucionar Problemas

### Error: "ModuleNotFoundError"

```bash
pip install --upgrade -r requirements.txt
```

### Error: "No such file or directory: '.env'"

```bash
cp .env.example .env
# Luego edita .env
```

### WhatsApp no conecta

- Verifica que WhatsApp está instalado en tu teléfono
- Escanea el QR dentro de 30 segundos
- Revisa que tu conexión a internet es estable

### No llegan notificaciones de email

- Verifica credenciales en `.env`
- Revisa la carpeta de spam
- Confirma que el App Password es correcto (sin caracteres extra)

## Ver Logs

```bash
# Ver últimas líneas
tail -f retail_arbitrage.log

# Ver todo el archivo
cat retail_arbitrage.log
```

## Actualizar

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Desinstalar

```bash
# Si está como servicio
sudo systemctl stop retail-arbitrage
sudo systemctl disable retail-arbitrage
sudo rm /etc/systemd/system/retail-arbitrage.service

# Eliminar archivos
rm -rf retail-arbitrage-bot
```

## Soporte

Para reportar problemas: https://github.com/SebastianVernisMora/retail-arbitrage-bot/issues

---

Hecho con ❤️ en México