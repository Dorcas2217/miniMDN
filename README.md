# Mini-MDM API

This is a simplified Mobile Device Management (MDM) API built with **Django** and **Django Rest Framework (DRF)**. It allows users to manage fleets of devices with strict ownership and security rules.

## Features
- **User Management**: View user details along with their owned fleets.
- **Fleet Management**: Create and list fleets (with unique naming per user).
- **Device Management**: Full CRUD operations for devices.
- **Security**: Strict data isolation—users can only interact with their own data.
- **Filtering**: Ability to filter devices by fleet.

---

## Technical Design Decisions

### 1. Data Integrity & Constraints
To respect the requirement that "Fleets belonging to the same User must have a unique name", I implemented a `UniqueConstraint` in the `Fleet` model:
```python
constraints = [
    models.UniqueConstraint(fields=['name', 'owner'], name='unique_fleet_per_user')
]