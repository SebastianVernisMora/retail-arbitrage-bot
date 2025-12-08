#!/usr/bin/env node

/**
 * Módulo de Envio de Mensajes WhatsApp
 * Utiliza whatsapp-web.js para integrar WhatsApp Web
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// Crear cliente
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Generar QR al iniciarse
client.on('qr', (qr) => {
    console.log('\n📱 Código QR generado:');
    qrcode.generate(qr, { small: true });
    console.log('\n✅ Escanea el código con WhatsApp en tu teléfono');
});

// Verificar cuando está listo
client.on('ready', () => {
    console.log('\n✅ WhatsApp Web vinculado correctamente');
    console.log('El bot está listo para enviar mensajes');
    saveStatus('connected');
});

// Manejar desconexiones
client.on('disconnected', (reason) => {
    console.log(`\n⚠️ WhatsApp desconectado: ${reason}`);
    saveStatus('disconnected');
});

// Inicializar cliente
client.initialize();

/**
 * Enviar mensaje a un número de WhatsApp
 */
async function sendMessage(phoneNumber, message) {
    try {
        // Formatear número (eliminar caracteres especiales)
        const formattedNumber = phoneNumber.replace(/\D/g, '');
        
        // Agregar código de país si es necesario
        const chatId = `${formattedNumber}@c.us`;
        
        // Enviar mensaje
        await client.sendMessage(chatId, message);
        
        console.log(`\n✅ Mensaje enviado a ${phoneNumber}`);
        return true;
    } catch (error) {
        console.error(`\n✗ Error enviando mensaje: ${error}`);
        return false;
    }
}

/**
 * Guardar estado de conexión
 */
function saveStatus(status) {
    const statusFile = '.whatsapp_status';
    fs.writeFileSync(statusFile, status);
}

/**
 * Exportar funciones para uso desde Python
 */
module.exports = {
    sendMessage,
    client
};

// Si se ejecuta directamente
if (require.main === module) {
    console.log('Módulo WhatsApp iniciado. Esperando conexión...');
    
    // Mantener el proceso activo
    process.stdin.resume();
}