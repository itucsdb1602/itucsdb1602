# Ozgun

## users
* init - GET /users/init to init users, users_block and user_friends table then redirect to home (you can use GET /users/destroy for the opposite). Use links on register or login page to do this
* register - GET /register to get registration page (links to this page on the navigation when user isn't logged in). POST /register to register user then redirect to home (CREATE)
* login - GET /login to get login page (links to this page on the navigation when user isn't logged in). POST /login to login which then redirect to home
* logout - GET /logout to logout then redirect to home (Links for logout is under username dropdown after user logged in)
* list - GET /users for list of all users rendered html (Links to this page on the navigation as "users") (READ)
* settings - GET /settings to get settings page of current user (Links for settings is under username dropdown after user logged in). POST /settings to update current user and redirect to /settings (UPDATE)
* delete account - links to deleting user is in /settings page. GET /delete to logout and delete current user then redirect to home (DELETE)

## users_friend
* get friendship status - On users page friendship status of each user shown as Friend or Close Friend (READ)
* add friend - GET /users/{user-id}/friend to friend a user  (CREATE)
* make close friend - GET /users/{user-id/closer to update friendship to close friend (UPDATE)
* unfriend - GET /users/{user-id}/unfriend to unfriend a user (DELETE)

## users_block
* get block status - On users page block status of each user shown as Blocked or Flagged as Inappropriate (READ)
* block - GET /users/{user-id}/block to block a user (CREATE)
* flag - GET /users/{user-id}/flag to flag user inappropriate which update users_block table  (UPDATE)
* unblock - GET /users/{user-id}/unblock to unblock a user (DELETE)
