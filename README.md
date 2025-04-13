# Moon Agent Tracker

This is a microservices-based system for MoonInsurance to track agent performance and sales activities.

## Microservices

- **Agent Service**: Handles agent records and their assigned products.
- **Integration Service**: Receives data from the core sales system.
- **Notification Service**: Sends alerts when sales targets are achieved.

## Tech Stack

- Python (FastAPI / Flask)
- MySQL (AWS RDS)
- Docker
- AWS (ECR, EKS, CodePipeline, etc.)
