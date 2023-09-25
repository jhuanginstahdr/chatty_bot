from app.local.demo import multithreaded_demo

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    # runs the demo app
    multithreaded_demo()

    logging.info('App has exited')