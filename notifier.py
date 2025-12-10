#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Notificaciones
Envía alertas por Email y WhatsApp
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

logger = logging.getLogger(__name__)


def send_email_notification(to_email, products):
    """
    Envía notificación por email
    """
    try:
        from_email = os.getenv('GMAIL_USER')
        app_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not from_email or not app_password or not to_email:
            logger.error("Credenciales de email incompletas")
            return False
        
        # Crear mensaje HTML
        html_body = generate_email_html(products)
        
        # Configurar email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[RETAIL ARBITRAGE] {len(products)} Productos Aprobados - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = from_email
        msg['To'] = to_email
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Enviar
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password.replace(' ', ''))
            server.sendmail(from_email, to_email, msg.as_string())
        
        logger.info(f"✅ Email enviado a {to_email}")
        return True
    
    except Exception as e:
        logger.error(f"✗ Error enviando email: {e}")
        return False


def send_whatsapp_notification(phone, products):
    """
    Envía una notificación por WhatsApp a un número mediante la API de CallMeBot.
    
    Genera el texto del mensaje a partir de `products`, construye la URL de CallMeBot (incluyendo la clave API desde la variable de entorno `CALLMEBOT_APIKEY`) y realiza una petición HTTP GET para enviar el mensaje.
    
    Parameters:
        phone (str): Número de teléfono destino en formato internacional (incluye código de país).
        products (list): Lista de diccionarios con datos de los productos que se incluirán en el mensaje.
    
    Returns:
        `true` si la petición recibió un HTTP 200 y el envío se considera exitoso, `false` en caso contrario.
    """
    try:
        if not phone or not products:
            logger.error("Teléfono o productos no válidos")
            return False
        
        # Crear mensaje
        message = generate_whatsapp_message(products)
        
        # Enviar vía CallMeBot
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={message}&apikey={os.getenv('CALLMEBOT_APIKEY')}"
        response = requests.get(url)

        if response.status_code == 200:
            logger.info(f"✅ WhatsApp enviado a {phone}")
            return True
        else:
            logger.error(f"✗ Error enviando WhatsApp: {response.text}")
            return False

    except Exception as e:
        logger.error(f"✗ Error enviando WhatsApp: {e}")
        return False


def generate_email_html(products):
    """
    Genera el cuerpo HTML del email
    """
    product_rows = ""
    total_savings = sum(p.get('regular_price', 0) - p.get('price', 0) for p in products)
    
    for p in products:
        product_rows += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{p.get('name', 'N/A')}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{p.get('store', 'N/A')}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">${p.get('price', 0):.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; color: red;">{p.get('discount', 0):.1f}%</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{p.get('roi', 0):.1f}%</td>
        </tr>
        """
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>🛒 Retail Arbitrage Bot - Productos Aprobados</h2>
        <p>Se encontraron <strong>{len(products)}</strong> productos que cumplen los criterios de rentabilidad.</p>
        
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #21808d; color: white;">
                    <th style="padding: 10px; text-align: left;">Producto</th>
                    <th style="padding: 10px; text-align: left;">Tienda</th>
                    <th style="padding: 10px; text-align: left;">Precio</th>
                    <th style="padding: 10px; text-align: left;">Descuento</th>
                    <th style="padding: 10px; text-align: left;">ROI</th>
                </tr>
            </thead>
            <tbody>
                {product_rows}
            </tbody>
        </table>
        
        <p style="margin-top: 20px;">
            <strong>Ahorro Total Potencial:</strong> ${total_savings:.2f}<br>
            <strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
        
        <p style="color: #999; font-size: 12px; margin-top: 30px;">
            <em>Este es un mensaje automático del Retail Arbitrage Bot. No responder a este email.</em>
        </p>
    </body>
    </html>
    """
    
    return html


def generate_whatsapp_message(products):
    """
    Genera el mensaje para WhatsApp
    """
    best_product = max(products, key=lambda x: x.get('roi', 0))
    total_savings = sum(p.get('regular_price', 0) - p.get('price', 0) for p in products)
    
    message = f"""
🛒 *RETAIL ARBITRAGE BOT*

🏆 *Mejores Oportunidades del Día*

✅ Productos encontrados: {len(products)}
🨋 Mejor ROI: {best_product.get('roi', 0):.1f}%
💵 Ahorro total: ${total_savings:.2f}

🔗 Revisa el email para más detalles

_Bot Automatizado_
    """
    
    return message