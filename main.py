# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client
import importlib
import os
import sys

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
                print(f"⚠️  No valid 'run_{plugin}_plugin' function found in {plugin}.py")
        except Exception as e:
            print(f"❌ Error loading plugin '{plugin}': {e}")

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("🔄 Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Unhandled error: {e}")
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass
