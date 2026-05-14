# Project Overview
VaqueroConnect is a social platform designed for UTRGV students. The goal of the project is to allow students to connect with each other through profiles, posts, following, notifications, and chat features. The platform includes a login system restricted to @utrgv.edu accounts, personalized profiles, a home feed, and interactive social features such as likes and follows.

This document outlines the full development timeline from the early prototype to Phase 1.5.

---

# Phase 1.0
## Anna:
- Created a new branch dedicated to the front-end platform (HTML/CSS design)
- Designed the Home and Navbar pages
- Created `main_home.html` to serve as the actual home page after the user logs in
- Fixed the logout system

## Melanie:
- Worked on login system and profile prototype
- Updated naming conventions
- Fixed login system
- Created `static.py` for frontend of login

---

# Phase 1.1 — Backend Update
## Anna:
**New backend features added:**
- Created a new backend branch (`back_enddesign`)
- Implemented the full Follow/Unfollow system
- Added the Follow model and database migration
- Added follow/unfollow button logic with proper redirects
- Added follower and following counts to user profiles
- Updated profile page to show:
  - Follow button
  - Follower/Following counts

## Melanie:
- Worked on frontend and backend for login/signin system
- Added a submit button with proper redirects
- Added a "must have @utrgv.edu account" restriction for signup

---

# Branch Merge Update
Both the front-end and back-end branches for Phase 1.0 and Phase 1.1 were successfully merged into the main development branch.  
This merge unified the login system, profile prototype, follow system, and updated frontend design into one stable build.

---

# Phase 1.3 — Backend New Update
## Anna:
**New backend features added:**
- Created another backend branch (`back_end1.3`)
- Implemented the post system
- Created a database model for posts
- Added a new page for users to create posts and upload/share pictures
- Posts now appear in `main_home` and profile pages
- Added post count and post showcase on the user profile
- Updated the enrolled campus selection for users
- Added the notification page
- Implemented the notification system
  - Created the model
  - Built the API
  - Added the notification page
- Integrated notifications with post likes
- Added the chat system
- Fixed bugs and organized static and other files

---

# Phase 1.4 — Front End Design
## Melanie:
- Modified the profile page design
- Added the profile user picture
- Created a new design for the login and register pages
- Modified the color themes for `main_home`, `create_post`, and chat pages

---

# Phase 1.5 — Backend and Frontend Final Touches
## Anna:
- Fixed and added backup code from a corrupted branch
- Modified and fixed bugs in the backend design
- Updated HTML pages and fixed a profile picture bug
- Fixed the notification API (Django REST Framework)


