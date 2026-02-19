"""Pipeline stages for the KakaoTalk consultation bot.

Each stage is a self-contained unit that can be tested in isolation.
The PipelineRunner in ``src.main`` wires them together.
"""

from src.pipeline.classify import ClassifyPipeline, ClassifyResult
from src.pipeline.receive import ReceivePipeline, ReceiveResult
from src.pipeline.respond import RespondPipeline, RespondResult
from src.pipeline.send import SendPipeline, SendResult
from src.pipeline.track import ActionTracker

__all__ = [
    "ActionTracker",
    "ClassifyPipeline",
    "ClassifyResult",
    "ReceivePipeline",
    "ReceiveResult",
    "RespondPipeline",
    "RespondResult",
    "SendPipeline",
    "SendResult",
]
