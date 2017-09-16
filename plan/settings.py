import appdirs
import plan


DATA_PATH = appdirs.user_data_dir(plan.__package__, plan.__author__)
LOG_PATH = appdirs.user_log_dir(plan.__package__, plan.__author__)
TICK_RATE = 60  # Default tick rate for Reporter in seconds.
