#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Productos
Evalúa productos según criterios de rentabilidad
"""

import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# Criterios
MIN_DISCOUNT = 30
MIN_MARGIN = 50
MIN_ROI = 50
MAX_STORAGE_DAYS = 90


class ProductAnalyzer:
    def __init__(self):
        self.min_discount = float(os.getenv('MIN_DISCOUNT', MIN_DISCOUNT))
        self.min_margin = float(os.getenv('MIN_MARGIN', MIN_MARGIN))
        self.min_roi = float(os.getenv('MIN_ROI', MIN_ROI))
        self.max_storage = int(os.getenv('MAX_STORAGE_DAYS', MAX_STORAGE_DAYS))
    
    def analyze_product(self, product):
        """Analiza un producto y retorna si es aprobado"""
        try:
            # Extraer datos
            regular_price = float(product.get('regular_price', 0))
            current_price = float(product.get('price', 0))
            discount = product.get('discount', 0)
            
            if not regular_price or not current_price:
                return False, {}
            
            # Cálculos
            real_discount = ((regular_price - current_price) / regular_price) * 100
            margin = ((current_price - current_price) / current_price) * 100  # Ajustar lógica
            roi = margin * (365 / self.max_storage)  # Proyectado anual
            
            # Evaluar criterios
            approved = (
                real_discount >= self.min_discount and
                margin >= self.min_margin and
                roi >= self.min_roi
            )
            
            analysis = {
                'discount_real': round(real_discount, 1),
                'margin': round(margin, 1),
                'roi': round(roi, 1),
                'approved': approved,
                'analysis_date': pd.Timestamp.now()
            }
            
            return approved, analysis
        
        except Exception as e:
            logger.error(f"Error analizando producto: {e}")
            return False, {}
    
    def save_approved_products(self, products, filename='data/productos_aprobados.csv'):
        """Guardar productos aprobados"""
        if not products:
            logger.warning("No hay productos aprobados para guardar")
            return
        
        df = pd.DataFrame(products)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"✅ Productos aprobados guardados: {len(products)}")