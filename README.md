# Event-Management-System
![Python](https://img.shields.io/badge/Python-3.11.4-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative)


## **Project Overview**

> Event Management System allows users to create events, register as attendees, and submit feedback on events. The system support user authentication, event management, attendee registration, and feedback collection.

## ✨ **Features**

1. **User**: Users of the system, who can create events, register for events, and submit feedback.
2. **Event**: Events created by users. Each event is owned by a single user.
3. **Registration**: Represents a user's registration to an event. Links users to events they are attending.
4. **Feedback**: Feedback submitted by attendees for events they attended.
5. **Tag**: Represents tags that can be associated with events, allowing for categorization and searchability of events.

## 💾 Installation

### 📂 Clone the Repository

```bash
git clone https://github.com/MaximPyanin/Event-Management-System.git
cd Event-Management-System
```
### 🔐 Set Up Environment Variables
Create a .env file in the root directory of the project and add the following environment variables:

- SENDGRID_API_KEY=your_sendgrid_api_key
- ACCOUNT_SID=your_account_sid
- AUTH_TOKEN=your_auth_token
- SENDER_PHONE=your_sender_phone
- SENDER_EMAIL=your_sender_email
- POSTGRES_URI=your_postgres_uri
- PAPERTRAIL_HOST=your_papertrail_host
- PAPERTRAIL_PORT=your_papertrail_port
- DOMAIN=your_domain
- PUBLIC_KEY=your_public_key
- ADMIN_PASSWORD=your_admin_password
- DASHBOARD_DOMAIN=your_dashboard_domain
- DASHBOARD_AUTH=your_dashboard_auth
- POSTGRES_PASSWORD=your_postgres_password
- EMAIL=your_email
- CERT_RESOLVER=your_cert_resolver
- PRIVATE_KEY=yout_private_key

Install Dependencies
```bash
poetry install
```

### Docker Setup
Build and Run Docker Containers
```bash
docker compose pull
docker compose up -d  --build
```
This command will build the Docker images and start the containers for the application and RabbitMQ.

### 🔧 Usage
Run the Application
To start the application, use the following command:

```bash
docker compose up -d --build
```

### 🧪 Running Tests
To run tests, use the following command:

```bash
poetry run pytest tests
```

### 📚 Documentation
The project's API documentation can be accessed via the FastAPI interactive docs once the application is running at /docs


### 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

### 📄   License
This project is licensed under the MIT License - see the LICENSE file for details.
