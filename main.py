import asyncio
import threading
from flask import Flask
from shared_client import start_client
import importlib
import os
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

async def flask_runner():
    threading.Thread(target=run_flask, daemon=True).start()

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            func = getattr(module, f"run_{plugin}_plugin", None)
            if callable(func):
                print(f"🚀 Running {plugin} plugin...")
                if asyncio.iscoroutinefunction(func):
                    await func()
                else:
                    func()
            else:
                print(f"⚠️ No valid 'run_{plugin}_plugin' function in {plugin}.py")
        except Exception as e:
            print(f"❌ Error loading plugin '{plugin}': {e}")

async def main():
    await load_and_run_plugins()
    await flask_runner()
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Unhandled error: {e}")
        sys.exit(1)
