import asyncio
from streamer.streamers.flare_streamer import block_loop as flare_block_loop
from dotenv import load_dotenv

load_dotenv()

asyncio.run(flare_block_loop())