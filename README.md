# ProSolver - Intelligent Incident Management System

## Overview

**ProSolver** is an advanced incident management system designed to streamline and automate the resolution of recurring technical issues in complex IT environments. This project was developed as part of my Bachelor's degree at the **University of Science and Technology Houari Boumediene (USTHB)** and focuses on improving efficiency in IT operations through automation and centralization.

### The Problem

Modern IT infrastructures, particularly those relying on **microservices architectures**, face frequent **synchronization failures**, **server misconfigurations**, and **system outages**. The traditional approach to incident resolution involves:

- **Manual execution of troubleshooting scripts** across multiple servers and containers.
- **High error susceptibility** due to human intervention.
- **Inefficient resource utilization**, leading to downtime and increased operational costs.
- **Slow incident resolution**, impacting service availability and user experience.

### The Solution - ProSolver

To address these challenges, **ProSolver** introduces a structured and automated approach to incident management:

- **Automated Execution**: Users can define incident resolution workflows and associate them with predefined scripts.
- **Efficient Management**: The system automatically executes the required commands across multiple servers and containers in the correct order.
- **Secure Access**: Implements **LDAP authentication** for controlled access to incident resolution processes.
- **Real-time Monitoring**: Logs and tracks all incident resolution steps to ensure transparency and accountability.

## Project Details

- **Grade**: 16.5/20
- **Supervisor**: Dr. Souad Saighi Marir
- **Completion Date**: June 2023

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Vue.js
- **Database**: MySQL
- **Containerization**: Docker & Docker Compose
- **Authentication**: LDAP Integration

## DevOps Implementation

To ensure **ProSolver** operates seamlessly, a **DevOps approach** was adopted to automate deployment, monitoring, and scaling:

- **Continuous Integration & Continuous Deployment (CI/CD)**: 
  - GitHub Actions is used to automate testing and deployment.
  - Every code push triggers unit tests and builds Docker images for deployment.

- **Containerization**:
  - The entire application runs inside **Docker containers**, ensuring consistency across environments.
  - **Docker Compose** is used to orchestrate services and manage dependencies.

- **Infrastructure as Code (IaC)**:
  - Deployment scripts automate the provisioning of servers and services.
  - Configurations are stored in version-controlled YAML files for reproducibility.

- **Monitoring & Logging**.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.12 or higher
- Node.js (for Vue.js frontend)
- MySQL
- Docker & Docker Compose

### Setup

#### Clone the Repository
```bash
git clone https://github.com/your-username/prosolver.git
cd prosolver
```

#### Backend Setup
```bash
pip install -r requirements.txt
python run.py
```

#### Database Configuration
- Create a MySQL database and update the connection settings in `config.py`.

#### Frontend Setup
```bash
cd frontend
npm install
npm run serve
```

#### Docker Deployment
```bash
docker-compose build
docker-compose up
```

## Features

- **Automated Incident Resolution** - Scripts execute seamlessly over SSH on multiple servers.
- **LDAP Authentication** - Secure access control for system users.
- **Incident Workflow Management** - Define, execute, and monitor resolution steps.
- **Centralized Logging** - Tracks all incident resolution activities for audit and transparency.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**ProSolver** transforms a tedious and error-prone manual resolution process into an **automated**, **efficient**, and **secure** system, significantly improving IT operations and ensuring better system reliability.
