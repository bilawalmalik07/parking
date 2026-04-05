# PostgreSQL Parking Management System

A Python-based Command Line Interface (CLI) application for managing a parking lot with a 50-slot capacity. This project integrates a local Python backend with a cloud-hosted Neon (PostgreSQL) database.

Click the button below to run this app instantly in your browser:
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/bilawalmalik07/parking)

> [!IMPORTANT]
> **Setup Instructions:**
>
> 1. Once the Codespace opens, **click on `main.py`** in the file explorer.
> 2. **Wait 20-30 seconds** for the terminal to finish installing all requirements (database drivers and environment tools)
> 3. Once the terminal is ready, run the app by typing: python main.py

## Features

- **Real-time Slot Tracking**: Uses SQL `COUNT` to track active parked cars.
- **Automated Billing**: Calculates fees based on $5 per 2-hour blocks using `math.ceil`.
- **Persistent Storage**: All tickets, entry times, and payments are stored in a PostgreSQL database.
