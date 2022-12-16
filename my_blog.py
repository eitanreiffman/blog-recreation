class Blog:
    def __init__(self):
        self.users = set()
        self.posts = []
        self.current_user = None

    def _get_post_from_id(self, post_id):
        for post in self.posts:
            if post.id == int(post_id):
                return post
    
    def create_user(self):
        username = input("Please choose a username: ")
        if username in {u.username for u in self.users}:
            print(f"User with username {username} already exists.")
        else:
            password = input("Please choose a password: ")
            new_user = User(username, password)
            self.users.add(new_user)
            print(f"{new_user} has been created!")

    def log_user_in(self):
        username = input("What is your username? ")
        password = input("What is your password? ")
        for user in self.users:
            if user.username == username and user.check_password(password):
                self.current_user = user
                print(f"{user} has been logged in!")
                break
        else:
            print("The username or password you entered is incorrect")

    def log_user_out(self):
        self.current_user = None
        print("You have successfully logged out!")

    def create_post(self):
        if self.current_user is not None:
            title = input("Enter the title of your post: ")
            body = input("Enter the full body of your post: ")
            new_post = Post(title, body, self.current_user)
            self.posts.append(new_post)
            print(f"Your post, {new_post.title}, has successfully been created!")
        else:
            print("You must be logged in to create a new post.")

    def view_posts(self):
        if self.posts:
            for post in self.posts:
                print(post)
        else:
            print("There are currently no posts in this blog to show.")

    def view_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            print(post)
        else:
            print(f"Post with ID {post_id} doesn't exist")

    def edit_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:        
            if self.current_user is not None and self.current_user == post.author:
                print(post)
                edit_part = input("Do you want to edit the title, body, both, or exit? ")
                while edit_part not in {'title', 'body', 'both', 'exit'}:
                    edit_part = input("Invalid option. Please try again.")
                if edit_part == "exit":
                    return
                if edit_part == "both":
                    new_title = input("Please enter your new desired title: ")
                    new_body = input("Please enter your new desired body: ")
                    post.update(title = new_title, body = new_body)
                elif edit_part == 'title':
                    new_title = input("Please enter your new title: ")
                    post.update(title = new_title)
                elif edit_part == 'body':
                    new_body = input("Please enter your new body: ")
                    post.update(body = new_body)
                print(f"Your post, {post.title}, has been updated.")
            if self.current_user is not None and self.current_user != post.author:
                print("You aren't authorized to make a change to this post.")
            else:
                print("You must be logged in to perform this action.")
        else:
            print(f"Post with the ID {post_id} doesn't exist.")

    def delete_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            if self.current_user is not None and self.current_user == post.author:
                self.posts.remove(post)
                print(f"{post.title} has been removed")
            elif self.current_user is not None and self.current_user != post.author:
                print("You aren't authorized to delete this post.")
            else:
                print("You must be logged in to perform this action.")
        else:
            print(f"Post with the ID number {post_id} does not exist.")

class User:
    id_counter = 1

    def __init__(self, username, password):
        self.username = username
        self.password = password[::-2]
        self.id = User.id_counter
        User.id_counter += 1

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User: {self.id}|{self.username}>"

    def check_password(self, password_guess):
        return self.password == password_guess[::-2]

class Post:
    id_counter = 1

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author
        self.id = Post.id_counter
        Post.id_counter += 1

    def __str__(self):
        formatted_post = f"""
        {self.id}. {self.title.title()}
            by {self.author}
        {self.body}
        """
        return formatted_post

    def __repr__(self):
        return f"<Post: {self.id}|{self.title}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def run_blog():
    
    my_blog = Blog()
    
    while True:
        if my_blog.current_user is None:
            print("1. Sign Up\n2. Log In\n3. View All Posts\n4. View a Post\n5. Quit")
            do_now = input("Which of these actions do you want to do? ")
            while do_now not in {'1', '2', '3', '4', '5'}:
                do_now = input("Invalid option. Please choose 1, 2, 3, 4, or 5: ")
            if do_now == '5':
                print("Thanks for checking out the blog. Goodbye!")
                break
            elif do_now == '4':
                post_id = input("Type the ID of the post you would like to view: ")
                my_blog.view_post(post_id)
            elif do_now == '3':
                my_blog.view_posts()
            elif do_now == '2':
                my_blog.log_user_in()
            elif do_now == '1':
                my_blog.create_user()
        else:
            print("1. Log Out\n2. Create New Post\n3. View All Posts\n4. View a Post\n5. Edit a Post\n6. Delete a Post")
            do_now = input("Which of these actions would you like to do now? ")
            while do_now not in {'1', '2', '3', '4', '5', '6'}:
                do_now = input("Invalid option. Please choose 1, 2, 3, 4, 5, or 6: ")
            if do_now == '1':
                my_blog.log_user_out()
            elif do_now == '2':
                my_blog.create_post()
            elif do_now == '3':
                my_blog.view_posts()
            elif do_now == '4':
                post_id = input("What is the ID number of the post you'd like to view? ")
                my_blog.view_post(post_id)
            elif do_now == '5':
                post_id = input("What is the ID number of the post you'd like to edit? ")
                my_blog.edit_post(post_id)
            elif do_now == '6':
                post_id = input("What is the ID number of the post you'd like to delete? ")
                my_blog.delete_post(post_id)

run_blog()

