# cmsc388j-final-diary-site

**Deployment link (Heroku):** https://cmsc388j-final-project-diary.herokuapp.com/

**Premise:**

Project Diaries is a site where people can sign up to create project diaries and make diary entries on their progress until they complete the project. People will be able to see other people’s projects to feel encouraged or learn what others are working on. They can comment on other's projects to show encouragement. In a sense, this is like a social media and progress tracker to help people’s productivity.

**Description:**

This is a Flask application created for CMSC388J, using the later project code as a base to help build it. The CSS and Bootstrap used are currently directly from CMSC388J: [class repository here](https://github.com/CMSC388J/cmsc388j-spring21).

**Functionality:**

* Blueprints
* Registration and Login
  * with hashed passwords
* Database
  * MongoDB used (Atlas)
* Security
  * Talisman/CSP
  * CSRF forms
* Emails
  * Flask_Mail
