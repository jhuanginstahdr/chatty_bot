from app.local.demo import multithreaded_demo

if __name__ == "__main__":
    import logging

    # Create a file handler and set the level to save all messages
    file_handler = logging.FileHandler('latency.log')
    file_handler.setLevel(logging.INFO)

    # Create a console handler and set the level to display messages of INFO level and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set the format for the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logging.basicConfig(handlers=[file_handler, console_handler])

    # runs the demo app
    multithreaded_demo()

    logging.info('App has exited')