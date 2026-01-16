import discord
from datetime import datetime
import os
import csv
import re

TOKEN = "MTQ2MTgzODU1NDAxMDIyMjY5NA.Gd4ODF.lL4Sczl577VvaEWBBHT37SVfW-1otCPOZr11ws"
CANAL_FACTURAS_ID = 1461115604151828691
CSV_FILE = "facturas.csv"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def extraer_dato(texto, campo):
    patron = rf"{campo}:\s*(.+)"
    resultado = re.search(patron, texto, re.IGNORECASE)
    return resultado.group(1).strip() if resultado else ""

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CANAL_FACTURAS_ID:
        return

    contenido = message.content

    if "Plantilla de Facturación" not in contenido:
        return

    try:
        servicio = extraer_dato(contenido, "Servicio Ofrecido")
        vehiculo = extraer_dato(contenido, "Vehículo")
        costo = extraer_dato(contenido, "Costo de Servicio")
        usuario = extraer_dato(contenido, "Usuario al que se le cobro")
        imagen = extraer_dato(contenido, "Imagen del Vehículo")

        costo = float(costo)

        file_exists = os.path.exists(CSV_FILE)

        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "Fecha",
                    "Servicio",
                    "Vehiculo",
                    "Costo",
                    "Usuario",
                    "Imagen"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                servicio,
                vehiculo,
                costo,
                usuario,
                imagen
            ])

        await message.channel.send("✅ Factura registrada correctamente")

    except Exception as e:
        await message.channel.send(
            "❌ Error al procesar la factura. Revisa el formato."
        )
        print(e)

client.run(TOKEN)
