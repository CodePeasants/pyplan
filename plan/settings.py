import appdirs
import plan


DATA_PATH = appdirs.user_data_dir(plan.__package__, plan.__author__)
LOG_PATH = appdirs.user_log_dir(plan.__package__, plan.__author__)
TICK_RATE = 60  # Default tick rate for Reporter in seconds.
TIME_ZONE = 'UTC'  # Interchange time zone everything is converted to internally.
ID_KEY = '__id__'  # Key used to store hash ID for objects, for serialization & deserialization.
TYPE_KEY = '__type__'  # Key used to store class type name, for serialization & deserialization.
