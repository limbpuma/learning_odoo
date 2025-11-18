# Odoo Docker Boilerplate

## Overview

This repository provides a boilerplate for deploying Odoo using Docker. It simplifies the setup process, allowing 
developers to quickly get started with Odoo in a containerized environment. This boilerplate includes configurations 
for Odoo, PostgreSQL, and any necessary dependencies, ensuring a smooth development and production experience.

Based on the following Github repository:
https://github.com/TrendicoGroup/odoo_docker

## Features

- **Easy Setup**: Quickly deploy Odoo with a single command.
- **Docker Compose**: Utilize Docker Compose for managing multi-container applications.
- **Customizable**: Easily modify configurations to suit your project needs.
- **Environment Variables**: Use environment variables for sensitive data and configuration settings.
- **Volume Management**: Persistent storage for Odoo and PostgreSQL data.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to set up your Odoo environment using this boilerplate:

1. **Clone the Repository**

2. **Configure Environment Variables**:

Copy `.env.example` file as `.env` in the root directory and set the necessary environment variables. 

Here’s an example:

```env
# postgresql environment variables
POSTGRES_DB=postgres
POSTGRES_PASSWORD=Password123
POSTGRES_USER=odoo
PGDATA=/var/lib/postgresql/16/data/pgdata

# odoo environment variables
HOST=postgres
USER=odoo
PASSWORD=Password123
```

3. **Build and Start the Containers**:

Use Docker Compose to build and start the containers:

```bash
docker-compose up -d
```

`-d` starts the containers as a daemon. If you want to see the logs live, don't use this flag.

4. **Access Odoo**:

Once the containers are running, you can access Odoo by navigating to `http://localhost:8069` in your web browser.

5. **Stop the Containers**:

To stop the running containers, use:

```bash
docker-compose down
```

## Directory Structure

- `docker-compose.yml`: The main configuration file for Docker Compose.
- `addons/`: Directory containing custom modules (if any).
- `enterprise/`: Directory containing enterprise modules (if any).

## Customization

You can customize the Odoo configuration by modifying the `odoo.conf` file located in the `odoo/` directory. 
Additionally, you can add custom modules by placing them in the `odoo/addons/` directory.

## Troubleshooting

**Container Fails to Start**: Check the logs for errors using:

```bash
docker-compose logs
```

**Database Connection Issues**: Ensure that the PostgreSQL service is running and 
that the credentials in the `.env` file are correct.
