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
        self.log_output.text += s
        self.log_output.cursor = (0, len(self.log_output.text))

    def flush(self):
        pass

    def run_search_thread(self, instance):
        self.run_button.disabled = True
        self.log_output.text = "Starting search...\n"
        threading.Thread(target=self.run_search).start()

    def run_search(self):
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
