#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retail Arbitrage Bot - Sistema Principal
Monitorea tiendas retail, analiza productos y envía notificaciones
"""

import os
import sys
import time
import logging
import schedule
from datetime import datetime
from dotenv import load_dotenv

from scraper import RetailScraper
from analyzer import ProductAnalyzer
from notifier import send_email_notification, send_whatsapp_notification

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'retail_arbitrage.log')),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_search_and_analyze():
    """Ejecuta búsqueda, análisis y notificaciones"""
    try:
        logger.info("=" * 80)
        logger.info("INICIANDO CICLO DE BÚSQUEDA Y ANÁLISIS")
        logger.info("=" * 80)
        
        # Obtener configuración
        query = os.getenv('SEARCH_QUERY', 'sidra').split(',')
        stores = os.getenv('STORES', 'walmart,liverpool').split(',')
        min_discount = int(os.getenv('MIN_DISCOUNT', '30'))
        max_price = float(os.getenv('MAX_PRICE', '500'))
        
        logger.info(f"Buscando productos: {', '.join(query)}")
        logger.info(f"Tiendas: {', '.join(stores)}")
        logger.info(f"Criterios: Descuento ≥30%, Precio ≤${max_price}")
        
        scraper = RetailScraper()
        
        # Scraping de cada tienda
        for store in stores:
            store = store.strip()
            for search_term in query:
                search_term = search_term.strip()
                logger.info(f"Scraping {store} para: {search_term}")
                
                if store == 'walmart':
                    scraper.scrape_walmart(search_term, min_discount, max_price)
                elif store == 'liverpool':
                    scraper.scrape_liverpool(search_term, min_discount, max_price)
                elif store == 'chedraui':
                    scraper.scrape_chedraui(search_term, min_discount, max_price)
                
                time.sleep(int(os.getenv('REQUEST_DELAY', '2')))
        
        # Guardar resultados
        if scraper.results:
            scraper.save_results('data/productos_encontrados.csv')
            logger.info(f"✅ Productos encontrados: {len(scraper.results)}")
        else:
            logger.warning("⚠ No se encontraron productos")
            return
        
        # Analizar productos
        logger.info("Analizando productos encontrados...")
        analyzer = ProductAnalyzer()
        approved_products = []
        
        for product in scraper.results:
            is_approved, analysis = analyzer.analyze_product(product)
            if is_approved:
                product.update(analysis)
                approved_products.append(product)
        
        logger.info(f"✅ Productos aprobados: {len(approved_products)}")
        
        # Guardar y notificar
        if approved_products:
            analyzer.save_approved_products(approved_products, 'data/productos_aprobados.csv')
            
            logger.info("Enviando notificaciones...")
            
            # Email
            if send_email_notification(os.getenv('NOTIFY_EMAIL'), approved_products):
                logger.info("✅ Email enviado")
            else:
                logger.error("✗ Error al enviar email")
            
            # WhatsApp
            if send_whatsapp_notification(os.getenv('NOTIFY_PHONE'), approved_products):
                logger.info("✅ WhatsApp enviado")
            else:
                logger.error("✗ Error al enviar WhatsApp")
        
        logger.info("=" * 80)
        logger.info("CICLO COMPLETADO")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Error en el ciclo: {e}", exc_info=True)


def main():
    """Función principal"""
    logger.info("""
    ════════════════════════════════════════
    RETAIL ARBITRAGE BOT - MÉXICO
    Sistema Automatizado de Búsqueda y Análisis
    ════════════════════════════════════════
    """)
    
    # Verificar variables de entorno
    required_vars = ['GMAIL_USER', 'GMAIL_APP_PASSWORD', 'NOTIFY_EMAIL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Variables faltantes: {', '.join(missing_vars)}")
        sys.exit(1)
    
    os.makedirs('data', exist_ok=True)
    
    # Ejecutar inmediatamente
    logger.info("Ejecutando búsqueda inicial...")
    run_search_and_analyze()
    
    # Programar ejecuciones
    interval_hours = int(os.getenv('CHECK_INTERVAL_HOURS', '6'))
    logger.info(f"Programando ejecuciones cada {interval_hours} horas")
    
    schedule.every(interval_hours).hours.do(run_search_and_analyze)
    
    logger.info("Bot ejecutándose. Presiona Ctrl+C para detener.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("\nBot detenido")
        sys.exit(0)


if __name__ == '__main__':
    main()