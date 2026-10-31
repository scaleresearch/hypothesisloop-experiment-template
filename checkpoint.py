"""How a job keeps what it must not lose across a stop: files under its own prefix of the
platform's object store, $HYPOTHESISLOOP_DATA_URI.

    import checkpoint
    if checkpoint.restore("state.pt"):       # a job started again finds its last save here
        state = torch.load("state.pt")
    for step in ...:
        ...
        if step % 500 == 0 or checkpoint.stopping():
            torch.save(state, "state.pt")
            checkpoint.save("state.pt")
        if checkpoint.stopping():
            sys.exit(143)

A job the platform starts again (a retry, a burst job preempted, a machine taken back) keeps its
id and so its prefix, while its disk starts empty. Save at a steady pace: a machine taken back
gives no warning. When the platform stops a job it sends SIGTERM and gives it the job spec's
checkpoint_grace_seconds: importing this module makes SIGTERM set stopping() instead of ending
the process, so the loop saves once more and exits 143, as SIGTERM would have: a job that was
stopped did not complete.
"""

import os
import signal
from urllib.parse import urlparse

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

_stopping = False


def _on_term(signum, frame) -> None:
    global _stopping
    _stopping = True


signal.signal(signal.SIGTERM, _on_term)


def stopping() -> bool:
    """True once the platform has said the job is being stopped."""
    return _stopping


def save(path: str, name: str | None = None) -> None:
    """Uploads the file at path as name, its base name by default, replacing an earlier save."""
    bucket, key = _where(name or os.path.basename(path))
    _client().upload_file(path, bucket, key)


def restore(path: str, name: str | None = None) -> bool:
    """Downloads the save of name, its base name by default, to path. False when there is none."""
    bucket, key = _where(name or os.path.basename(path))
    try:
        _client().download_file(bucket, key, path)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchKey"):
            return False
        raise
    return True


def _where(name: str) -> tuple[str, str]:
    uri = os.environ.get("HYPOTHESISLOOP_DATA_URI")
    if not uri:
        raise RuntimeError("checkpoint: $HYPOTHESISLOOP_DATA_URI is not set, so this process is no job of "
                           "the platform and has no prefix to save to: the platform sets it in a job")
    parsed = urlparse(uri)
    return parsed.netloc, parsed.path.lstrip("/") + "checkpoints/" + name


def _client():
    return boto3.client("s3", config=Config(s3={"addressing_style": "path"}))
