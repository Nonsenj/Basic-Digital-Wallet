import asyncio
from backend import config, models

if __name__ == "__main__":
    settings = config.get_setting()
    models.init_db(settings)
    asyncio.run(models.recreate_table())
