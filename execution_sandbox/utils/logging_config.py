import logging
import os
from typing import Optional


def setup_logging(log_file: Optional[str] = None, level: int = logging.DEBUG):
    """Configure logging to display logs to both console and file (if specified).

    Args:
        log_file: Optional path to log file. If None, only console logging is enabled.
        level: Logging level to use. Defaults to DEBUG.
    """
    # Create logs directory if logging to file
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),  # Console handler
            *(
                [] if not log_file else [logging.FileHandler(log_file)]
            ),  # File handler if log_file specified
        ],
    )

    # Create a logger for flow traversal specifically
    flow_logger = logging.getLogger("flow.traversal")
    flow_logger.setLevel(level)


def log_node_execution(logger: logging.Logger, node_name: str, phase: str, data: any):
    """Log node execution details.

    Args:
        logger: Logger instance to use
        node_name: Name of the node being executed
        phase: Execution phase (prep, exec, post)
        data: Data being processed in this phase
    """
    logger.debug(f"Node: {node_name} | Phase: {phase} | Data: {data}")


def log_flow_transition(
    logger: logging.Logger, from_node: str, to_node: str, action: str
):
    """Log flow transitions between nodes.

    Args:
        logger: Logger instance to use
        from_node: Source node name
        to_node: Target node name
        action: Action triggering the transition
    """
    logger.info(f"Flow Transition: {from_node} --({action})--> {to_node}")
