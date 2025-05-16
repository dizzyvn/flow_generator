import streamlit as st

from flow import create_flow
from main import shared
from utils.shared_monitor import SharedMonitor

# Initialize session state for storing execution history and current node buffer
if "execution_history" not in st.session_state:
    st.session_state.execution_history = []
if "_current_node_buffer" not in st.session_state:
    st.session_state._current_node_buffer = None
if "input_fields" not in st.session_state:
    st.session_state.input_fields = {
        key: value for key, value in shared.items() if value is not None
    }
if "needs_update" not in st.session_state:
    st.session_state.needs_update = False


def flush_node_buffer():
    buf = st.session_state._current_node_buffer
    if buf and (buf.get("prep") or buf.get("exec") or buf.get("post")):
        st.session_state.execution_history.append(buf)
    st.session_state._current_node_buffer = None


def on_shared_change(key, old_value, new_value):
    print(f"on_shared_change: {key}, {old_value}, {new_value}")
    if key == "current_node":
        # New node started, flush previous node buffer
        flush_node_buffer()
        st.session_state._current_node_buffer = {
            "node": new_value,
            "prep": None,
            "exec": None,
            "post": None,
            "status": None,
        }
        st.session_state.needs_update = True
    elif key == "node_executions":
        buf = st.session_state._current_node_buffer
        if buf is not None:
            if new_value.get("prep_output") is not None:
                buf["prep"] = new_value["prep_output"]
            if new_value.get("exec_output") is not None:
                buf["exec"] = new_value["exec_output"]
            if new_value.get("post_output") is not None:
                buf["post"] = new_value["post_output"]
            buf["status"] = new_value["status"]
            st.session_state.needs_update = True


def main():
    st.title("Flow Execution Monitor")

    # Sidebar for input
    with st.sidebar:
        st.header("Input")
        from main import shared

        for key, value in st.session_state.input_fields.items():
            st.text_input(key, value)

        if st.button("Run Flow"):
            # Clear previous execution history and buffer
            st.session_state.execution_history = []
            st.session_state._current_node_buffer = None
            st.session_state.needs_update = False

            # Initialize the shared store with the query
            shared = SharedMonitor({key: value for key, value in shared.items()})

            # Add callback to monitor changes
            shared.add_callback(on_shared_change)

            # Create and run the flow
            flow = create_flow()
            flow.run(shared)

            flush_node_buffer()

            # Add final state to history
            st.session_state.execution_history.append(
                {
                    "type": "final_state",
                    "content": {
                        "execution_path": shared["execution_path"],
                        "results": {
                            k: v
                            for k, v in shared.items()
                            if k
                            not in [
                                "current_node",
                                "execution_path",
                                "node_results",
                                "execution_status",
                            ]
                        },
                    },
                }
            )
            st.session_state.needs_update = True

    # If we need an update, trigger a rerun
    if st.session_state.needs_update:
        st.session_state.needs_update = False
        st.rerun()


if __name__ == "__main__":
    main()
