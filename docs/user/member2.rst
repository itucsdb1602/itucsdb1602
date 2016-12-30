Parts Implemented by Göktürk GÖK
================================

The parts that i have implemented are the *Complaint*, *Comments* and *pLikes(Post Likes)* pages and functionalities related to users.

Complaints
----------

The complaint table can be operated via click on "COMPLAINT BOX" on the home page. Only users who logged-in can do Complaint operations and display via click on the post owner's box on posts and comments.
If the complaint is evaluated then it can be updated via clicking to yellow update button on complaint in "COMPLAINT BOX".

Complaint button below the user name.

   .. image:: images/gokturk/complaint_button.png
      :scale: 50 %
      :alt: Complaint button.

Here on the left side when logged-off, and right side when the user log-in COMPLAINT BOX is seen.

   .. image:: images/gokturk/complaint_box_before_login.png
      :scale: 50 %
      :alt: Complaint Box appears only the user who logged-in on home page.

   .. image:: images/gokturk/complaint_box_login.png
      :scale: 50 %
      :alt: Complaint Box is invisible when logged-off.

Add Complaint
^^^^^^^^^^^^^

To add a new complaint on a post, you need to click on the button near the name of the post owner .Also click the *-* button.

   .. image:: images/gokturk/complaint_add_post.png
      :scale: 100 %
      :alt: Add complaint on a post.
      ******************************
To add a new complaint about a comment the user wants to complain is shown as clicking the user's near side of the comment owner's name.

   .. image:: images/gokturk/complaint_add_comment.png
      :scale: 100 %
      :alt: Add complaint on a comment.

      ******************************

   .. image:: images/gokturk/complaint_add_comment2.png
      :scale: 100 %
      :alt: Add complaint on a post.

Added complaint is displayed like this.

   .. image:: images/gokturk/complaint_added.png
      :scale: 100 %
      :alt: Added complaint display on a complaint box.
      ******************************
   .. image:: images/gokturk/complaint_display.png
      :scale: 100 %
      :alt: Added complaint display on a complaint box.



As a result, the new complaint you entered will be added to the database and the new list will be shown to you.




Delete Complaint
^^^^^^^^^^^^^^^^

To delete a complaint, click the red delete button near of the complaint. Then press the *Red Delete* button.

   .. image:: images/gokturk/complaint_delete.png
      :scale: 100 %
      :alt: Deleting demonstration
      ******************************
   .. image:: images/gokturk/complaint_display.png
      :scale: 100 %
      :alt: Complaints display on a complaint box.
      ******************************
   .. image:: images/gokturk/complaint_deleted.png
      :scale: 100 %
      :alt: After delete operation demonstration


Then, the entry will be removed from the database and the resulting list will be displayed.

Update Complaint
^^^^^^^^^^^^^^^^

To update the information of a *complaint*, click the yellow update button which would like to update then it makes change as it is evaluated as status 1. After that, click the *Yellow Update* button and watch it happen.

   .. image:: images/gokturk/complaint_update.png
      :scale: 100 %
      :alt: Updating demonstration
      ******************************
Then this button directs the user to the related comment/post for changing. And when it is changed, then complaint's is_done will changed as 1.

   .. image:: images/gokturk/complaint_update_to_comment.png
      :scale: 100 %
      :alt: Updating demonstration

   .. image:: images/gokturk/complaint_updated.png
         :scale: 100 %
         :alt: Updating demonstration

Information in the entry will be updated and shown back.

   .. note:: Update operation changes the status of the complaint like the social media style.


Search Complaint
^^^^^^^^^^^^^^^^

To search the information of a complaint.

   .. image:: images/gokturk/complaint_display.png
      :scale: 100 %
      :alt: selecting demonstration



Information in the entry will be selected and displayed.



Comments
--------

The comments table can be displayed under the posts which is commented. Also number of comments are displayed under the post as number of comments display-button.
Only users who logged-in can add, update and delete the comment.

   .. note:: Update and delete operations can be done on only the comments which is added by the user logged-in.

   .. image:: images/gokturk/complaint_image.png
      :scale: 100 %
      :alt: Complaint Box appears only the user who logged-in on home page.

Add Comment
^^^^^^^^^^^

To add a new commment on a post, user can add a comment via Add Comment under all the comments.

   .. image:: images/gokturk/comment_add.png
      :scale: 100 %
      :alt: Add comment on a post.

Added comment is shown.

   .. image:: images/gokturk/comment_added.png
      :scale: 100 %
      :alt: Added comment under the post.

Added comment is displayed under the related post.

   .. image:: images/gokturk/comment_displayed.png
      :scale: 100 %
      :alt: Added comment under the post.


As a result, the new comment which the user entered will be added to the database and the new list will be shown to user.




Delete Comment
^^^^^^^^^^^^^^

To delete a comment, click the red delete button near of the comment. Then press the *Red Delete* button.

Comment list before deletion under the post.

   .. image:: images/gokturk/comment_displayed.png
         :scale: 100 %
         :alt: Comment Display.

Red delete button on a comment
   .. image:: images/gokturk/comment_delete_button.png
      :scale: 100 %
      :alt: Red Delete Button.

Listing comments after delete the post.

   .. image:: images/gokturk/comment_deleted.png
      :scale: 100 %
      :alt: After deletion listing the all comments.


Then, the entry will be removed from the database and the resulting list will be displayed.

   .. note:: Delete operation is available only to the comments which is added by the current user.

Update Comment
^^^^^^^^^^^^^^

To update the information of a *comment*, click the yellow update button which user would like to update via *yellow update button* then updating a comment will be done and listed under the post.


Before updating a comment

   .. image:: images/gokturk/comment_before_update.png
      :scale: 100 %
      :alt: Before updating.

   .. image:: images/gokturk/comment_update_button.png
      :scale: 100 %
      :alt: Update button

Then this button directs the user to the related comment for changing. And when it is updated, then comments are listed as up-to-date under the post.

   .. image:: images/gokturk/comment_update_page.png
      :scale: 100 %
      :alt: Update a comment.

   .. image:: images/gokturk/comment_updated_display.png
         :scale: 100 %
         :alt: Updated comment is listed under the post.

Information in the entry will be updated and shown back.

   .. note:: Update operation available only to the comments which is added by the current user as it seems.


Listing Comments
^^^^^^^^^^^^^^^^

Listing all the comments under a post.

   .. image:: images/gokturk/comment_updated_display.png
      :scale: 100 %
      :alt: listing demonstration



Information in the entry will be selected,listed and shown back.


pLikes(Post Like)
-----------------

To be able to like a post user can reach the user buttons on the posts on home page.

   .. image:: images/gokturk/plikes_page.png
      :scale: 100 %
      :alt: Home page display with the like buttons.


 .. note:: If the user wants to like posts, first login the website.

Like a post
^^^^^^^^^^^


   .. image:: images/gokturk/plikes_before.png
      :scale: 100 %
      :alt: Like post

To like the post, user can hit the green thumb-up button.

   .. image:: images/gokturk/plikes_after.png
      :scale: 100 %
      :alt: Like post


Consequently,if you like the post,it will be added to the database.


Unlike a post
^^^^^^^^^^^^^

   .. image:: images/gokturk/plikes_after.png
      :scale: 100 %
      :alt: unLike post

To unlike the post, user can hit the green thumb-up button which is already liked.

   .. image:: images/gokturk/plikes_before.png
      :scale: 100 %
      :alt: unLike post

Consequently,if you unlike the post,it will be delete from the database.






