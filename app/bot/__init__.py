from .main import main as start


def _run_bot_instance():
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        print("Worker interrupted")
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()

        if pending:
            loop.run_until_complete(
                asyncio.gather(*pending, return_exceptions=True)
            )
        loop.close()



def start_in_process():
    from multiprocessing import Process

    event = Process(target=_run_bot_instance, daemon=True)
    event.start()
    return event.pid
