# BermbaliBlog
#### Video Demo: https://www.youtube.com/watch?v=VsvsPlv11vQ
#### Description:

Welcome to BermbaliBlog, a web application inspired by my village Bermbal in the Dakahlia governorate of Egypt. This blog platform allows users to register, log in, create posts, and browse posts created by others. The goal is to provide a place for community discussions and sharing of ideas, much like the traditional gathering spots in a village.

### Project Inspiration and Acknowledgements

I gained significant inspiration from the distribution code of the finance problem from Problem Set 9, especially in implementing the login, logout, and registration functionalities. Special thanks to the CS50 staff for their foundational work, particularly the helpers.py file which was directly adapted from the problem set.

Additionally, I utilized Bootstrap to style the web application, and I must acknowledge the assistance of ChatGPT in helping me integrate and customize Bootstrap components effectively, as well as for its help with other details of the project.


### Project Files

1. **app.py**: This is the main application file that contains the Flask application and the various routes that handle user requests. It includes routes for user registration, login, logout, creating posts, and viewing posts. The file also handles database interactions and session management.

2. **templates/layout.html**: This is the base HTML file that includes the common structure for all pages. It uses Bootstrap for styling and includes a navigation bar that adjusts based on the user's authentication status.

3. **templates/apology.html**: This template is used to display error messages to users. It shows a humorous image along with the error message.

4. **templates/create_post.html**: This template provides a form for users to create new blog posts. Users can add a title, body text, and optionally upload an image.

5. **templates/index.html**: This is the homepage template that lists the latest blog posts. Each post is displayed with a title, snippet of the body, and a link to read more.

6. **templates/login.html**: This template contains the login form for users to access their accounts.

7. **templates/post.html**: This template displays a single blog post in full, including the title, image (if any), body text, and metadata about the post.

8. **templates/register.html**: This template contains the registration form for new users.

9. **templates/user.html**: This template shows all posts created by a specific user.

10. **static/styles.cs  s**: This file contains custom CSS styles for the application, providing additional styling beyond the default Bootstrap classes.

11. **static/BermbaliBlog_favicon.png**: The favicon for the website, representing a village-like scene to symbolize the community aspect of the blog.

12. **helpers.py**: Contains utility functions used across the application, such as rendering apology messages and requiring login for certain routes.

13. **blog.db**: This is the SQLite database file that stores user and post information. It includes two main tables: users and posts. The users table stores user credentials and the posts table stores blog posts along with references to the users who created them. 

14. **static/images**: This directory contains the images uploaded by users as part of their blog posts. Each image is stored with a unique path to prevent conflicts and ensure they can be properly linked to their respective posts.

15. **requirements.txt**: This file lists all the dependencies required to run the BermbaliBlog application. To install these dependencies, use the command pip install -r requirements.txt. 

### Design Choices

- **User Authentication**: I used Flask sessions to manage user login states, allowing users to register, log in, and log out securely. The decision to use sessions was influenced by the need for a straightforward yet effective way to maintain user sessions.
  
- **Bootstrap Integration**: To create a responsive and visually appealing design, I integrated Bootstrap into the project. This choice was made to leverage its pre-designed components and grid system, ensuring the site looks good on various devices.

- **Database Management**: SQLite was chosen as the database for its simplicity and ease of use with Flask. It stores user information, blog posts, and session data.

- **Error Handling**: Custom error pages were created using the apology.html template to provide a better user experience in case of errors.

### Challenges and Considerations

- **Image Handling**: Allowing users to upload images with their posts required careful handling to ensure the server's security and the proper display of images.
  
- **Pagination**: Implementing pagination for the blog posts list was necessary to handle large numbers of posts efficiently without overwhelming the user with too much information at once.

- **User Experience**: Ensuring the site is intuitive and easy to navigate was a key focus. This involved designing a clean layout, clear navigation, and informative feedback for user actions.

### Conclusion

BermbaliBlog is a testament to the power of community and shared knowledge. By providing a platform for users to share their thoughts and ideas, it aims to foster a sense of connection and dialogue. I hope you find it both useful and enjoyable to use. 

Thank you for exploring BermbaliBlog. If you have any questions or feedback, feel free to reach out.
