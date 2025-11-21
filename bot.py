# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import logging
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_CHAT_ID = "851133567"

KEYWORDS = [
    "ابي حل", "أبي حل", "ابغى حل", "أبغى حل", "حل واجب", "حلول",
    "مشروع تخرج", "مشروع التخرج", "بحث"hi, "بحوث", "مساعدة بحث",
    "برزنتيشن", "عرض تقديمي", "بوربوينت", "presentation",
    "واجب", "مكلف", "تكليف", "مهمه", "مهمة"
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    message = update.message
    message_text = message.text.lower()
    if any(keyword in message_text for keyword in KEYWORDS):
        logger.info(f"تم العثور على كلمة مفتاحية في مجموعة '{message.chat.title}'")
        user = message.from_user
        chat = message.chat
        forward_text = (
            f"🔔 **تنبيه بطلب جديد** 🔔\n\n"
            f"**👤 المرسل:** {user.first_name} {user.last_name or ''}\n"
            f"**🏷️ اسم المستخدم:** @{user.username or 'غير متوفر'}\n"
            f"**👥 المجموعة:** {chat.title}\n\n"
            f"**📝 نص الرسالة الأصلي:**\n"
            f"----------------------------------\n"
            f"{message.text}\n"
            f"----------------------------------"
        )
        try:
            await context.bot.send_message(
                chat_id=YOUR_CHAT_ID,
                text=forward_text,
                parse_mode='Markdown'
            )
            logger.info(f"تم إرسال التنبيه بنجاح إلى {YOUR_CHAT_ID}")
        except Exception as e:
            logger.error(f"فشل إرسال الرسالة: {e}")

def main():
    if not BOT_TOKEN:
        logger.error("خطأ: لم يتم العثور على متغير البيئة BOT_TOKEN.")
        return
        
    logger.info("جارٍ إنشاء تطبيق البوت...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS, message_handler))
    logger.info("البوت جاهز الآن وسيبدأ بالاستماع للرسائل...")
    application.run_polling()

if __name__ == "__main__":
    main()
