# PostgreSQL Parking Management System

A Python-based Command Line Interface (CLI) application for managing a parking lot with a 50-slot capacity. This project integrates a local Python backend with a cloud-hosted Neon (PostgreSQL) database.

## Features

- **Real-time Slot Tracking**: Uses SQL `COUNT` to track active parked cars.
- **Automated Billing**: Calculates fees based on $5 per 2-hour blocks using `math.ceil`.
- **Persistent Storage**: All tickets, entry times, and payments are stored in a PostgreSQL database.
