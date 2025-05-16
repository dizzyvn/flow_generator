from typing import Any, Callable, Dict, Optional


class SharedMonitor:
    """A wrapper around a dictionary that notifies of changes to the shared state."""

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        self._data = initial_data or {}
        self._callbacks = []
        # Initialize execution tracking
        self._data.update(
            {
                "current_node": None,
                "execution_path": [],
                "node_executions": {},
            }
        )

    def add_callback(self, callback: Callable[[str, Any, Any], None]):
        """Add a callback function that will be called when a value changes.

        The callback should have the signature: callback(key, old_value, new_value)
        """
        self._callbacks.append(callback)

    def _notify(self, key: str, old_value: Any, new_value: Any):
        """Notify all callbacks of a change."""
        for callback in self._callbacks:
            try:
                callback(key, old_value, new_value)
            except Exception:
                pass

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any):
        old_value = self._data.get(key)
        self._data[key] = value
        if old_value != value:
            self._notify(key, old_value, value)

    def __delitem__(self, key: str):
        old_value = self._data[key]
        del self._data[key]
        self._notify(key, old_value, None)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def update(self, other: Dict[str, Any]):
        """Update multiple values at once."""
        for key, value in other.items():
            self[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def __repr__(self) -> str:
        return f"SharedMonitor({self._data})"

    def track_node_execution(self, node_name, status, p, e, r):
        """Track node execution in the shared state."""
        self["current_node"] = node_name
        self["execution_path"].append(f"{node_name} ({status})")
        self["node_executions"] = {
            "status": status,
            "prep_output": p,
            "exec_output": e,
            "post_output": r,
        }
