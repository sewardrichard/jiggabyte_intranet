import asyncio
from core.scraper import search_google_maps

async def main():
    try:
        res = await search_google_maps("Fintech", "Harare, Zimbabwe", print)
        print("Success:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Required for Windows Playwright async
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
