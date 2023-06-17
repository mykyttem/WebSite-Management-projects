# WebSite-Management-projects

WebSite created for create projects, communications for users, control projects, tasks, members, joined

---

# List functions
- Created/auth Accounts
- See my profile
- Create/settings/control project
- chat members
- joined for project

---

# Deployment



1. Clone the repository: git clone "url repository"

2. Go to the "src" project directory: cd folder "src"

3. Install dependencies: pip install -r requirements.txt

4. Makemigrations apps
    Python manage.py makemigrations "app"
    Example: 
        Python manage.py makemigrations accounts

5. Migrate: Python manage.py migrate


6. Python manage.py runserver

---
# Warning

This project has dependencies `Daphne`. Please note that these dependencies are not supported for Windows operating systems. However, they can be supported on WSL (Windows Subsystem for Linux), Linux, and macOS. If you are using Windows and these dependencies are not supported, I advise you to remove the following packages from the INSTALLED_APPS list in the settings:

`channels`
`daphne`

By removing these packages, you can ensure that your project will run without any compatibility issues in your Windows environment, however chat will not work

## Redis

For chats i users `redis`, for chat working, install packeges `redis` from requirements and start server in `dockers` OR console command `sudo service redis-server start`  