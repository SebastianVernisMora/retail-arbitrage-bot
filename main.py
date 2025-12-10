#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retail Arbitrage Bot - Kivy UI
"""

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.logger import Logger
import threading

from backend import run_search_and_analyze

class RetailArbitrageApp(App):

    def build(self):
        """
        Construye y configura la interfaz principal de la aplicación Kivy.
        
        Configura el título y el color de fondo de la ventana, crea el layout raíz y los controles de la UI:
        - etiqueta de título,
        - sección de configuración con campos de texto para búsqueda, tiendas, descuento mínimo y precio máximo (prellenados desde variables de entorno si están disponibles),
        - botón para iniciar la búsqueda,
        - área de salida de logs dentro de un ScrollView.
        Además redirige stdout y stderr hacia el widget de logs.
        
        Returns:
        	layout_raiz (BoxLayout): El contenedor raíz que agrupa todos los widgets de la interfaz.
        """
        self.title = 'Retail Arbitrage Bot'
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        title_label = Label(text='Retail Arbitrage Bot', font_size='24sp', bold=True, size_hint_y=None, height=50)
        layout.add_widget(title_label)

        # --- Configuration ---
        config_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=200)

        config_layout.add_widget(Label(text='Search Query:', halign='right'))
        self.search_query = TextInput(text=os.getenv('SEARCH_QUERY', 'sidra,rompope'), multiline=False)
        config_layout.add_widget(self.search_query)

        config_layout.add_widget(Label(text='Stores:', halign='right'))
        self.stores = TextInput(text=os.getenv('STORES', 'walmart,liverpool'), multiline=False)
        config_layout.add_widget(self.stores)

        config_layout.add_widget(Label(text='Min Discount (%):', halign='right'))
        self.min_discount = TextInput(text=os.getenv('MIN_DISCOUNT', '30'), multiline=False)
        config_layout.add_widget(self.min_discount)

        config_layout.add_widget(Label(text='Max Price:', halign='right'))
        self.max_price = TextInput(text=os.getenv('MAX_PRICE', '500'), multiline=False)
        config_layout.add_widget(self.max_price)

        layout.add_widget(config_layout)

        # --- Controls ---
        self.run_button = Button(text='Run Search', on_press=self.run_search_thread, size_hint_y=None, height=50)
        layout.add_widget(self.run_button)

        # --- Log Output ---
        self.log_output = TextInput(text='Logs will appear here...\n', readonly=True, background_color=(0,0,0,1), foreground_color=(1,1,1,1))
        log_scroll = ScrollView(size_hint=(1, 1))
        log_scroll.add_widget(self.log_output)
        layout.add_widget(log_scroll)

        # Redirect stdout to log output
        sys.stdout = self
        sys.stderr = self

        return layout

    def write(self, s):
        """
        Añade texto al área de registro de la interfaz y sitúa el cursor al final del contenido.
        
        Parameters:
            s (str): Texto a añadir al log; puede contener saltos de línea y fragmentos parciales de salida.
        """
        self.log_output.text += s
        self.log_output.cursor = (0, len(self.log_output.text))

    def flush(self):
        """
        No realiza ninguna acción; existe para cumplir la interfaz de objeto de archivo requerida al redirigir stdout/stderr a la aplicación.
        
        Se mantiene como método vacío para satisfacer la expectativa de que el objeto log tenga un método `flush`.
        """
        pass

    def run_search_thread(self, instance):
        """
        Inicia la búsqueda en un hilo de fondo y prepara la interfaz de usuario para la ejecución.
        
        Deshabilita el botón de ejecución, reinicia el área de log con un mensaje inicial y arranca un hilo separado que invoca `run_search`.
        
        Parameters:
        	instance: el objeto que disparó el evento (por ejemplo, el botón pulsado). No se utiliza dentro de la función.
        """
        self.run_button.disabled = True
        self.log_output.text = "Starting search...\n"
        threading.Thread(target=self.run_search).start()

    def run_search(self):
        """
        Ejecuta la búsqueda y el análisis usando los valores actuales de la interfaz y registra el resultado en la salida de log.
        
        Actualiza las variables de entorno (SEARCH_QUERY, STORES, MIN_DISCOUNT, MAX_PRICE) con los valores presentes en los campos de la UI, invoca backend.run_search_and_analyze(), añade el resultado al área de log y, si ocurre una excepción, registra el mensaje de error. Siempre vuelve a habilitar el botón de ejecución al finalizar.
        """
        try:
            # Update environment variables from UI
            os.environ['SEARCH_QUERY'] = self.search_query.text
            os.environ['STORES'] = self.stores.text
            os.environ['MIN_DISCOUNT'] = self.min_discount.text
            os.environ['MAX_PRICE'] = self.max_price.text

            result = run_search_and_analyze()
            self.log_output.text += f"Search finished: {result}\n"
        except Exception as e:
            self.log_output.text += f"Error: {e}\n"
        finally:
            self.run_button.disabled = False


if __name__ == '__main__':
    RetailArbitrageApp().run()