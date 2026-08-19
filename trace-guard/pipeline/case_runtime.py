# Adapter: exposes a case content file as a segments module for tts.py/render2.py.
# Select the case with env CASE_FILE=cases/<key>.py, then SEGMENTS_MODULE=case_runtime.
import importlib.util, os
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ["CASE_FILE"])
_spec = importlib.util.spec_from_file_location("case_content", _p)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
SEGS = _mod.SEGS
CASE = _mod.CASE
SAMPLE_LAST_ID = SEGS[-1]["id"]
PAUSE_DEFAULT = 0.45
PAUSE_SLIDE_CHANGE = 0.9
PAUSE_AFTER_NUGGET = 0.7
