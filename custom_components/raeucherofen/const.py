"""Constants for the Rayucherofen integration."""

DOMAIN = "raeucherofen"
CONF_HOST = "host"

# Update interval
UPDATE_INTERVAL = 10 # seconds

# Programs Mapping (must match enum in .ino)
PROGRAM_MAPPING = {
    0: "None",
    1: "Dry",
    2: "Cold",
    3: "Hot",
    4: "Cook",
    5: "Steam",
    6: "Krakauer",
    7: "Individual",
    8: "Cooldown"
}

REVERSE_PROGRAM_MAPPING = {v: k for k, v in PROGRAM_MAPPING.items()}
