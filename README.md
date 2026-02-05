# Mini MDN - Fleet & Device Management API

This is a technical assessment project for a Fleet Management System. It allows users to manage their fleets and devices through a secure REST API, with built-in data isolation and Docker support.

##  Features
- **User Authentication**: Secure Token-based authentication.
- **Data Isolation**: Users can only see and manage their own fleets and devices.
- **REST API**: Full CRUD operations for Fleets and Devices.
- **Filtering**: Easily filter devices by fleet using query parameters.
- **Dockerized**: Ready to deploy with Docker and Docker Compose.

---

1. **Build and start the containers:**
   ```bash
   docker compose up --build 
   ```
2. **Access the Api**
- Web API: http://localhost:8000/api/

- Admin Panel: http://localhost:8000/admin/