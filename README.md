# Raeucherofen Home Assistant Integration

Custom Component for integrating the ESP32-based Smoker directly into Home Assistant.

## Installation

1. Install via HACS by adding this repository as a **Custom Repository**.
2. Restart Home Assistant.
3. Go to **Settings -> Devices & Services -> Add Integration**.
4. Search for **Smoker**.
5. Enter the IP address of your ESP32.

## Features

- Monitor Temperatures (Top, Mid, Bottom, Meat, Outside)
- Control Set Temperature and Timer
- Start/Stop Programs
- Control Fan, Flap, Smoke, Steam

## HACS Installation Fix

If you see an error about **Version**, you must create a **Release** on GitHub.

1. Push your code to GitHub.
2. Go to your repository > **Releases** > **Draft a new release**.
3. Tag version: `v1.0.0`.
4. Release title: `v1.0.0`.
5. Publish release.
6. Now try downloading in HACS again.
