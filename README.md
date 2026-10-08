# WebGuard – Automated Website Testing & Monitoring Dashboard

WebGuard is a Python-based website testing and monitoring tool designed to automate the process of checking website functionality, performance, and reliability. It combines **Selenium, Python, HTML, CSS, JavaScript, and GitHub Actions** to provide an interactive dashboard for viewing website test results.

The project aims to reduce the need for manual website testing by automatically performing essential checks and generating detailed reports.

## Key Features

- **Automated Website Testing:** Uses Python and Selenium to launch a browser and test websites automatically.
- **Website Availability Checks:** Verifies whether a website is accessible and retrieves its HTTP response status.
- **Performance Monitoring:** Measures website page navigation time to help identify slow-loading pages.
- **Broken Link Detection:** Scans webpages for links that return errors.
- **Automated Screenshots:** Captures screenshots of tested websites for visual inspection.
- **Interactive Dashboard:** Displays website status, performance metrics, test results, and testing history through a modern web interface.
- **Test Reports:** Generates structured results to help identify website issues.
- **GitHub Actions Integration:** Executes automated website tests through GitHub Actions without requiring a dedicated server.
- **Free Hosting:** Uses GitHub Pages to host the dashboard publicly.

## How It Works

Users access the WebGuard dashboard and select a website to test. The website testing process is initiated through GitHub Actions, where Python and Selenium perform automated checks using a browser.

Once testing is complete, the results are saved and published to the dashboard, allowing users to review website availability, loading performance, broken links, and screenshots.

> **Note:** GitHub Pages hosts the static dashboard; it does not run Python or Selenium directly. Website scans are executed through GitHub Actions, and results are published for display on the dashboard.

## Technologies Used

| Component | Technologies |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Browser automation | Python, Selenium |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |

## Project Objective

The primary objective of WebGuard is to demonstrate how browser automation, website testing, and CI/CD workflows can be combined to build a practical quality assurance tool.

The project highlights skills in **Python programming, Selenium automation, web development, software testing, GitHub Actions, and DevOps practices**, while providing a foundation for more advanced website monitoring capabilities.
