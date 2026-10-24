import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from db import init_db, obtener_disponibles

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    productos = obtener_disponibles()

    if not productos:
        await update.message.reply_text(
            "😔 No hay productos disponibles en este momento. Vuelve más tarde."
        )
        return

    teclado = []
    for prod_id, nombre, precio in productos:
        teclado.append([
            InlineKeyboardButton(
                f"{nombre} — ${precio}",
                callback_data=f"comprar_{prod_id}"
            )
        ])

    await update.message.reply_text(
        "🛒 *Productos disponibles:*\n\nElige el que quieras comprar:",
        reply_markup=InlineKeyboardMarkup(teclado),
        parse_mode="Markdown"
    )

async def seleccionar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    prod_id = int(query.data.split("_")[1])

    await query.edit_message_text(
        f"Elegiste el producto ID {prod_id}.\n"
        f"Aquí irá el flujo de pago (lo agregamos al final)."
    )

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(seleccionar_producto, pattern=r"^comprar_\d+$"))
    print("Bot corriendo...")
    app.run_polling()
