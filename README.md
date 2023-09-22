# DGTBot - Appointment Availability Checker

**DGTBot** is a Python script designed to check for the availability of appointments at the DGT website. It automates the process of searching for available appointments for various procedures at DGT offices.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Introduction

The **DGTBot** is a tool that can help you monitor the availability of appointments for different procedures at DGT offices, such as renewing your driver's license or vehicle registration. It automates the process of filling out the appointment request form and solving CAPTCHAs, making it easier for you to secure an appointment when one becomes available.

## Features

- Automated appointment availability checking.
- CAPTCHA solving using 2Captcha or Selenium Recaptcha Solver.
- Exponential backoff with jitter for retries.
- Simulated human behavior to avoid detection.
- Randomized browser settings for stealth.

## Requirements

Before you can use **DGTBot**, make sure you have the following requirements installed:

- Python 3.x
- Selenium: `pip install selenium`
- WebDriver for Chrome (ChromeDriver): [Download here](https://sites.google.com/chromium.org/driver/) and add it to your system's PATH.
- Latest User Agents: `pip install latest-user-agents`
- httpagentparser: `pip install httpagentparser`
- TwoCaptcha API key (optional, if using 2Captcha service): [Sign up here](https://2captcha.com/)
- Selenium Recaptcha Solver (optional, if using Recaptcha Solver): [Selenium Recaptcha Solver](https://pypi.org/project/selenium-recaptcha-solver/)

## Getting Started

1. Clone this repository or download the script `dgt_bot.py`.

2. Install the required Python packages mentioned in the [Requirements](#requirements) section.

3. Make sure you have Chrome installed, and download the ChromeDriver that matches your Chrome version.

4. Add the ChromeDriver executable to your system's PATH or specify its location in the script.

5. Optionally, obtain a TwoCaptcha API key if you plan to use the 2Captcha service for CAPTCHA solving.

6. Optionally, install the Selenium Recaptcha Solver if you prefer to use it for CAPTCHA solving.

## Usage

Run the `main.py` script to check for appointment availability. You can customize the script with your preferred parameters and configuration.

```bash
python main.py
```