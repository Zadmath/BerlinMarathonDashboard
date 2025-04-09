'''
    Contains the server to run our application.
'''
from flask_failsafe import failsafe


@failsafe
def create_app():
    '''
        Gets the underlying Flask server from our Dash app.

        Returns:
            The server to be run
    '''
    # the import is intentionally inside to work with the server failsafe
    from app import app  # pylint: disable=import-outside-toplevel
    return app.server

app = create_app()

if __name__ == "__main__":
    create_app().run(port="8050", debug=False)
    import os
    import psutil
    process = psutil.Process(os.getpid())
    print(f"Total RAM used: {process.memory_info().rss / 1024**2:.2f} MB")

