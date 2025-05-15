import copy
import logging
import time
import warnings

logger = logging.getLogger(__name__)


class BaseNode:
    def __init__(self):
        self.params, self.successors = {}, {}

    def set_params(self, params):
        self.params = params

    def next(self, node, action="default"):
        if action in self.successors:
            warnings.warn(f"Overwriting successor for action '{action}'")
        self.successors[action] = node
        return node

    def prep(self, shared):
        pass

    def exec(self, prep_res):
        pass

    def post(self, shared, prep_res, exec_res):
        pass

    def _exec(self, prep_res):
        return self.exec(prep_res)

    def _run(self, shared):
        p = self.prep(shared)
        e = self._exec(p)
        result = self.post(shared, p, e)
        return result

    def run(self, shared):
        if self.successors:
            warnings.warn("Node won't run successors. Use Flow.")
        return self._run(shared)

    def __rshift__(self, other):
        return self.next(other)

    def __sub__(self, action):
        if isinstance(action, str):
            return _ConditionalTransition(self, action)
        raise TypeError("Action must be a string")


class _ConditionalTransition:
    def __init__(self, src, action):
        self.src, self.action = src, action

    def __rshift__(self, tgt):
        return self.src.next(tgt, self.action)


class Node(BaseNode):
    def __init__(self, max_retries=1, wait=0):
        super().__init__()
        self.max_retries, self.wait = max_retries, wait

    def exec_fallback(self, prep_res, exc):
        raise exc

    def _exec(self, prep_res):
        time.sleep(1)
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res, e)
                if self.wait > 0:
                    time.sleep(self.wait)

    def _run(self, shared):
        # Track node execution start
        logger = logging.getLogger(f"{self.__class__.__name__}")

        try:
            # Run the node
            if hasattr(shared, "track_node_execution"):
                shared.track_node_execution(
                    self.__class__.__name__, "started", None, None, None
                )
            logger.info("Started")
            p = self.prep(shared)
            if hasattr(shared, "track_node_execution"):
                shared.track_node_execution(
                    self.__class__.__name__, "prep", p, None, None
                )
            logger.info("Input: %s", p)
            e = self._exec(p)
            logger.info("Output: %s", e)
            if hasattr(shared, "track_node_execution"):
                shared.track_node_execution(self.__class__.__name__, "exec", p, e, None)
            r = self.post(shared, p, e)
            logger.info("Routing: %s", r)
            if hasattr(shared, "track_node_execution"):
                shared.track_node_execution(self.__class__.__name__, "post", p, e, r)
            return r

        except Exception as e:
            # Track failure
            if hasattr(shared, "track_node_execution"):
                shared.track_node_execution(
                    self.__class__.__name__, "error", str(e), None, None
                )
            raise e


class BatchNode(Node):
    def _exec(self, items):
        return [super(BatchNode, self)._exec(i) for i in (items or [])]


class Flow(BaseNode):
    def __init__(self, start=None):
        super().__init__()
        self.start_node = start

    def start(self, start):
        self.start_node = start
        return start

    def get_next_node(self, curr, action):
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors:
            warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def _orch(self, shared, params=None):
        curr, p, last_action = (
            copy.copy(self.start_node),
            (params or {**self.params}),
            None,
        )
        while curr:
            curr.set_params(p)
            last_action = curr._run(shared)
            curr = copy.copy(self.get_next_node(curr, last_action))
        return last_action

    def _run(self, shared):
        p = self.prep(shared)
        o = self._orch(shared)
        return self.post(shared, p, o)

    def post(self, shared, prep_res, exec_res):
        return exec_res


class BatchFlow(Flow):
    def _run(self, shared):
        pr = self.prep(shared) or []
        for bp in pr:
            self._orch(shared, {**self.params, **bp})
        return self.post(shared, pr, None)
