import os
import logging
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN_API = os.getenv('TELEGRAM_TOKEN')
BOT_USERNAME: Final = "@Yunoball_bot"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Anime database with genres and descriptions
ANIME_DATA = {
    "Action": {
        "Attack on Titan": "A masterpiece of storytelling with incredible world-building. The plot twists are mind-blowing and the animation quality is top-tier. Themes of freedom, humanity, and sacrifice make this a must-watch. The character development is phenomenal, especially Eren's transformation throughout the series.",
        
        "Demon Slayer": "Visually stunning with breathtaking animation, especially the fight scenes. The story follows Tanjiro's journey to save his sister, showcasing themes of family bonds and determination. While the plot is straightforward, the emotional depth and character relationships make it incredibly engaging.",
        
        "Jujutsu Kaisen": "Modern shounen at its finest with a perfect balance of humor, action, and character development. The power system is well-explained and creative. Gojo Satoru alone makes this worth watching - he's the perfect mentor figure with incredible depth.",
        
        "One Piece": "The ultimate adventure anime with unparalleled world-building spanning over two decades. Oda's storytelling genius shines through complex plots that pay off after hundreds of episodes. The themes of friendship, dreams, and freedom are beautifully woven throughout.",
    },
    
    "Romance": {
        "Your Name": "A beautiful tale that perfectly blends romance with supernatural elements. Makoto Shinkai's animation is absolutely gorgeous, and the emotional payoff is incredible. The way it handles themes of connection, fate, and love across time and space is masterful.",
        
        "Toradora!": "One of the best romantic comedies in anime. The character development is exceptional, especially how Taiga and Ryuuji grow together. It perfectly balances comedy with genuine emotional moments, and the Christmas episodes are absolutely perfect.",
        
        "Kaguya-sama: Love is War": "Brilliant comedy that turns the simple concept of confession into psychological warfare. The characters are incredibly well-written, and the humor is consistently clever. It's both hilarious and surprisingly touching when it wants to be.",
        
        "Weathering With You": "Another Shinkai masterpiece with stunning visuals and a touching story about love and sacrifice. The weather animation is phenomenal, and the emotional core about choosing personal happiness over duty resonates deeply.",
    },
    
    "Horror": {
        "Another": "A psychological horror masterpiece that creates genuine tension and dread. The mystery elements are well-crafted, and the atmosphere is consistently unsettling. The deaths are creative and the plot twist is satisfying without feeling cheap.",
        
        "Parasyte": "Brilliant blend of horror, action, and philosophical themes about humanity. The body horror is genuinely disturbing, but the character development of Shinichi and his relationship with Migi is fascinating. It asks deep questions about what makes us human.",
        
        "Tokyo Ghoul": "Dark and brutal exploration of identity and belonging. The first season is exceptional with great character development and world-building. Kaneki's transformation from innocent student to ghoul is both tragic and compelling.",
        
        "Hell Girl": "Atmospheric horror that focuses on human nature's dark side. Each episode is like a morality tale, exploring themes of revenge and justice. The repetitive format works well for the horror atmosphere it creates.",
    },
    
    "Comedy": {
        "One Punch Man": "Perfect parody of superhero tropes with incredible animation. Saitama's existential crisis about being too powerful is both hilarious and surprisingly deep. The supporting cast is fantastic, and the action scenes are spectacular.",
        
        "Konosuba": "Hilarious parody of isekai anime with fantastic character dynamics. Every main character is flawed in the best possible way, leading to constant comedy gold. Kazuma's reactions to his useless party members never get old.",
        
        "Gintama": "The king of comedy anime with perfect timing and incredible range. It can make you laugh until you cry, then immediately hit you with serious emotional moments. The parodies and references are brilliant, though you need knowledge of other anime to fully appreciate it.",
        
        "Nichijou": "Absurdist comedy at its finest with incredible animation quality. The random humor and over-the-top reactions to mundane situations are hilarious. It's pure joy in animated form.",
    },
    
    "Drama": {
        "A Silent Voice": "Powerful exploration of bullying, redemption, and forgiveness. The character development is incredible, and it handles heavy themes with sensitivity. The animation perfectly complements the emotional storytelling.",
        
        "Your Lie in April": "Emotionally devastating story about music, love, and dealing with trauma. The classical music performances are beautifully animated, and the character relationships feel genuine. Prepare for tears.",
        
        "Violet Evergarden": "Visually stunning with incredible attention to detail. Violet's journey to understand human emotions is beautifully told. Each episode is like a small masterpiece, and the themes of love, loss, and human connection are perfectly executed.",
        
        "Clannad: After Story": "The gold standard for emotional anime. The first part builds up the characters and relationships, while After Story delivers some of the most powerful emotional moments in anime history. It's a beautiful meditation on family, love, and life.",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    keyboard = []
    
    for genre in ANIME_DATA.keys():
        keyboard.append([InlineKeyboardButton(genre, callback_data=f"genre_{genre}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🍥 Welcome to the Anime Recommendation Bot! 🍥\n\n"
        "Choose a genre to explore both peak and mid animes...your choice can either make or maime you boi:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("genre_"):
        genre = data.replace("genre_", "")
        keyboard = []
        
        for anime in ANIME_DATA[genre].keys():
            keyboard.append([InlineKeyboardButton(anime, callback_data=f"anime_{genre}_{anime}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Genres", callback_data="back_to_genres")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📺 {genre} Anime Recommendations:\n\n"
            f"Pick a card and find out which pokemon you get! :",
            reply_markup=reply_markup
        )
    
    elif data.startswith("anime_"):
        parts = data.replace("anime_", "").split("_", 1)
        genre = parts[0]
        anime = parts[1]
        
        description = ANIME_DATA[genre][anime]
        
        keyboard = [
            [InlineKeyboardButton(f"🔙 Back to {genre}", callback_data=f"genre_{genre}")],
            [InlineKeyboardButton("🏠 Back to Genres", callback_data="back_to_genres")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🎬 {anime}\n\n"
            f"📝 JUDGEMENT!:\n{description}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif data == "back_to_genres":
        keyboard = []
        for genre in ANIME_DATA.keys():
            keyboard.append([InlineKeyboardButton(genre, callback_data=f"genre_{genre}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🍥 Welcome to the Anime Recommendation Bot! 🍥\n\n"
        "Choose a genre to explore both peak and mid animes...your choice can either make or maime you boi:",
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 Bot Help🍜

Commands:
• /start - Start the bot and see genre options
• /help - Show this help message

How to use:
1. Use /start to see available genres
2. Click on a genre to see anime recommendations
3. Click on an anime title to read my detailed opinion
4. Use the back buttons to navigate

Features:
• Multiple anime genres (Action, Romance, Horror, Comedy, Drama)
• Detailed opinions and reviews for each anime
• Easy navigation with inline keyboards

Enjoy discovering new anime! 🍥
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main() -> None:
    # Create the Application
    application = Application.builder().token(TOKEN_API).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Let your fate begin...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':

    main()
