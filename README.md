# 🛒 Retail Arbitrage Bot - México

> Sistema automatizado de retail arbitrage con web scraping, análisis de productos y notificaciones por email/WhatsApp para tiendas mexicanas (Walmart, Liverpool, Chedraui, Soriana)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## ✨ Características

- 🔍 **Web Scraping Automatizado** - Monitorea múltiples tiendas retail mexicanas
- 📊 **Análisis Inteligente** - Evalúa productos según criterios de rentabilidad (ROI ≥50%, Margen ≥50%)  
- 📧 **Notificaciones Email** - Alertas HTML con productos aprobados vía Gmail
- 💬 **Notificaciones WhatsApp** - Mensajes automáticos con resumen de oportunidades
- ⏰ **Ejecución Programada** - Búsquedas automáticas cada N horas
- 📝 **Logs Completos** - Registro detallado de todas las operaciones
- 💾 **Exportación CSV** - Guarda resultados para análisis posterior

## 🚀 Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/SebastianVernisMora/retail-arbitrage-bot.git
cd retail-arbitrage-bot

# Instalar dependencias
pip install -r requirements.txt
npm install

# Configurar
cp .env.example .env
nano .env  # Editar con tus credenciales

# Ejecutar
python main.py
```

## 📋 Requisitos

- Python 3.8 o superior
- Node.js 14+ (para WhatsApp)
- Cuenta Gmail con [App Password](https://myaccount.google.com/apppasswords)
- Número de WhatsApp con WhatsApp Web

## ⚙️ Configuración

### 1. Obtener Gmail App Password

1. Ve a https://myaccount.google.com/apppasswords
2. Selecciona "Correo" y "Otro"
3. Copia el código de 16 caracteres
4. Pégalo en `.env` como `GMAIL_APP_PASSWORD`

### 2. Configurar Variables de Entorno

Edita el archivo `.env`:

```env
# Credenciales Gmail
GMAIL_USER=tu-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Destinatarios
NOTIFY_EMAIL=destinatario@gmail.com
NOTIFY_PHONE=+521234567890

# Parámetros de búsqueda
SEARCH_QUERY=sidra,rompope,luces navideñas
MIN_DISCOUNT=30
MAX_PRICE=500

# Tiendas a monitorear
STORES=walmart,liverpool,chedraui

# Frecuencia (horas)
CHECK_INTERVAL_HOURS=6
```

### 3. Vincular WhatsApp

Al ejecutar por primera vez:

```bash
python main.py
```

Se mostrará un código QR. Escanéalo con:
**WhatsApp → Dispositivos Vinculados → Vincular un Dispositivo**

## 📊 Uso

### Ejecución Manual

```bash
python main.py
```

### Ver Logs en Tiempo Real

```bash
tail -f retail_arbitrage.log
```

## 🔍 Criterios de Análisis

Los productos son aprobados si cumplen **TODOS** estos criterios:

| Criterio | Valor Mínimo |
|----------|---------------|
| Descuento real | ≥ 30% |
| Margen de ganancia | ≥ 50% |
| ROI proyectado | ≥ 50% |
| Tiempo almacenamiento | ≤ 90 días |
| Demanda histórica | Alta/Muy Alta |
| Fecha caducidad | ≥ 6 meses (si aplica) |

## 📁 Estructura del Proyecto

```
retail-arbitrage-bot/
├── main.py                    # 🎯 Script principal
├── scraper.py                 # 🕷️ Módulo de web scraping
├── analyzer.py                # 📊 Analizador de productos
├── notifier.py                # 📧 Sistema de notificaciones
├── whatsapp_sender.js         # 💬 Módulo WhatsApp (Node.js)
├── requirements.txt           # 📦 Dependencias Python
├── package.json              # 📦 Dependencias Node.js
├── .env.example              # ⚙️ Ejemplo de configuración
└── data/                     # 💾 Datos generados
    ├── productos_encontrados.csv
    └── productos_aprobados.csv
```

## 📧 Notificaciones

### Email (Gmail)
Recibirás un email HTML con:
- ✅ Resumen de productos encontrados
- 📦 Detalles de cada producto aprobado
- 💰 Cálculos de ROI y márgenes
- 🔗 Links directos a las tiendas

### WhatsApp
Mensaje con resumen ejecutivo:
- 📊 Total de productos aprobados
- 🏆 Mejor oportunidad del día  
- 💵 Ahorro total potencial

## 🛡️ Consideraciones Legales

⚠️ **IMPORTANTE**: Este software es para uso educativo y personal.

- ✅ Respeta los términos de servicio de cada sitio web
- ⏱️ Implementa delays entre requests (2-3 segundos mínimo)
- 🚫 No sobrecargues los servidores
- 🎭 Usa User-Agents realistas
- 🌐 Considera usar proxies para volúmenes altos

## 🐛 Solución de Problemas

### El scraper no encuentra productos
- ✅ Verifica que los selectores CSS están actualizados
- ⚠️ Las tiendas cambian su estructura HTML frecuentemente
- 📝 Revisa los logs para ver errores específicos

### No llegan notificaciones
- 🔑 Verifica credenciales de Gmail en `.env`
- 📱 Confirma que WhatsApp Web está conectado
- 📧 Revisa la carpeta de spam

### Error de dependencias
```bash
pip install --upgrade -r requirements.txt
npm install
```

## 📄 Licencia

[MIT License](LICENSE) - © 2025 Sebastian Vernis Mora

## 👤 Autor

**Sebastian Vernis Mora**

- 🌐 GitHub: [@SebastianVernisMora](https://github.com/SebastianVernisMora)
- 📧 Email: solucionesdigitalesdev@outlook.com
- 📍 Ubicación: México

---

<div align="center">

⭐ **Si este proyecto te fue útil, considera darle una estrella**

Made with ❤️ in México

</div>
