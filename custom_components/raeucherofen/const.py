"""Constants for the Rayucherofen integration."""

DOMAIN = "raeucherofen"
CONF_HOST = "host"

# Update interval
UPDATE_INTERVAL = 10 # seconds

# Programs Mapping (must match enum in .ino)
PROGRAM_MAPPING = {
    0: "Keines",
    1: "Trocknen",
    2: "Kalträuchern",
    3: "Heißräuchern",
    4: "Kochen",
    5: "Dämpfen",
    6: "Krakauer",
    7: "Individuell",
    8: "Abkühlen"
}

REVERSE_PROGRAM_MAPPING = {v: k for k, v in PROGRAM_MAPPING.items()}
