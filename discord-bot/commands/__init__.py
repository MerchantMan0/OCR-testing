from .docscan import handle_docscan
from .doctr import handle_doctr
from .help import handle_help
from .memory import handle_free
from .pipeline_cmd import handle_pipeline
from .transform_cmd import handle_transform

COMMANDS = {
    "!docscan": handle_docscan,
    "!doctr": handle_doctr,
    "!transform": handle_transform,
    "!fullscan": handle_pipeline,
    "!memory": handle_free,
    "!help": handle_help,
}
