from .docscan import handle_docscan
from .doctr import handle_doctr
from .help import handle_help
from .memory import handle_free

COMMANDS = {
    "!docscan": handle_docscan,
    "!doctr": handle_doctr,
    "!memory": handle_free,
    "!help": handle_help,
}
