import os
import sys
import logging

from gunicorn.app.base import Application
from app.asgi import application


log = logging.getLogger(__name__)


class ApplicationLoader(Application):
    """Bypasses the class `WSGIApplication."""

    def init(self, parser, opts, args):
        """Class ApplicationLoader object constructor."""
        self.cfg.set("default_proc_name", args[0])

    def load(self):
        """Load application."""
        return application


def run_wsgi(host, port, workers):
    """Run gunicorn WSGI with ASGI workers."""
    log.info("Start gunicorn WSGI with ASGI workers.")
    sys.argv = [
        "--gunicorn",
        "-w",
        workers,
        "-k",
        "uvicorn.workers.UvicornWorker",
        "-b {host}:{port}".format(
            host=host,
            port=port,
        ),
    ]
    sys.argv.append("app.asgi:application")

    ApplicationLoader().run()


if __name__ == "__main__":
    print(os.environ.get("PORT", "8000"))
    run_wsgi(
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=os.environ.get("PORT", "8000"),
        workers=os.getenv("WORKERS", "4"),
    )