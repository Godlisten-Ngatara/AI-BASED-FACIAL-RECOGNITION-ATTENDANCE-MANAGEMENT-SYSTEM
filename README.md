# AI-BASED-FACIAL-RECOGNITION-ATTENDANCE-MANAGEMENT-SYSTEM - Collaboration Guide

This project involves building a facial recognition system using IP cameras. The project is divided into four key modules: Frontend, Backend, Facial Recognition, and Camera Integration.

## Getting Started

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/Godlisten-Ngatara/AI-BASED-FACIAL-RECOGNITION-ATTENDANCE-MANAGEMENT-SYSTEM.git
cd AI-BASED-FACIAL-RECOGNITION-ATTENDANCE-MANAGEMENT-SYSTEM
```
## Development Setup

Python Version: Ensure you're using Python 3.6 or higher.

Setting Up the Environment: Create a virtual environment:

```bash
python -m venv venv
```
### Activate the Virtual Environment

On Windows
```bash
.\venv\Scripts\activate
```

On macOS/Linux
```bash
source venv/bin/activate
```

### Install Dependencies: Install the required libraries
```bash
pip install -r requirements.txt
```

## Branching Strategy
We follow a Gitflow branching model. Here's how it works:

1. Main Branch: The stable production version of the project. Never push directly to main.

2. Develop Branch: The primary development branch. Always pull the latest changes from develop before starting your work.

3. Feature Branches: For each new feature or bug fix, create a new branch from develop.
- Naming: `feature/feature-name`

4. Release Branches: Once a set of features is ready for release, create a release branch from develop.
- Naming: `release/release-name`

5. Hotfix Branches: For urgent fixes, create a branch from main.
- Naming: `hotfix/issue-name`

### Commands to Manage Branches

To create a new branch from `develop`:

```bash
git checkout -b feature/feature-name
```
To switch to an existing branch:

```bash
git checkout feature/feature-name
```


