import threading
import uvicorn
import logging
import os
from pystyle import Colors, Colorate, Center
from logger import info, warn, fail, success, debug

# ====================
# Logging Suppression
# ====================
logging.getLogger("discord.gateway").setLevel(logging.ERROR)
logging.getLogger("discord.client").setLevel(logging.ERROR)
logging.getLogger("discord.http").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("websockets").setLevel(logging.ERROR)
logging.getLogger("websockets.client").setLevel(logging.ERROR)
logging.getLogger("uvicorn.error").setLevel(logging.ERROR)
logging.getLogger("uvicorn.access").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.ERROR)

class CustomUvicornHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        
        if record.name == "uvicorn.access" and " - \"" in log_message and "HTTP/" in log_message:
            debug(log_message)
        elif record.levelno >= logging.ERROR:
            fail(log_message)
        elif record.levelno >= logging.WARNING:
            warn(log_message)
        elif record.levelno >= logging.INFO:
            info(log_message)
        else:
            info(log_message)

def configure_uvicorn_logging():
    custom_handler = CustomUvicornHandler()
    formatter = logging.Formatter('%(message)s')
    custom_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    loggers = [
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
    ]
    
    for logger in loggers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.addHandler(custom_handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


# ✅ No more config.yaml used
def start_discord_bot():
    from bot import start_bot
    start_bot()  # let bot.py manage the token, not config.yaml


banner = """
██████╗  ██████╗  ██████╗ ███████╗████████╗    ██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██║   ██║███████╗   ██║       ██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║██║   ██║╚════██║   ██║       ██╔══██╗██║   ██║   ██║   
██████╔╝╚██████╔╝╚██████╔╝███████║   ██║       ██████╔╝╚██████╔╝   ██║   
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝   
     API BOOST PANEL                          - Ð00M.py                          

"""

def main():
    print(Center.XCenter(Colorate.Vertical(color=Colors.purple_to_blue, text=banner), spaces=15))


    configure_uvicorn_logging()

    # ✅ Start Discord bot (bot.py handles the token)
    bot_thread = threading.Thread(target=start_discord_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # ✅ ALWAYS launch API from api.py, no config.yaml
    from api import app
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info", log_config=None)


if __name__ == "__main__":
    clear_console()
    main()
