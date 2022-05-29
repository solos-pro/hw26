from flask import Flask, request, render_template, url_for
from utils import *


posts, comments, bookmarks = load_data()
app = Flask(__name__, static_url_path='/static')


@app.route("/",)
def page_index():
    bookmarks = bookmark_read()
    return render_template("index.html", posts=posts, num=len(bookmarks))


@app.route("/search/")
def search_page():
    search_query = request.args.get("word")
    searched_posts = search_func(posts, search_query)
    return render_template("search.html", posts=searched_posts[:9], num=len(searched_posts))    # цифра - количество постов

@app.route("/tag/<tagword>/")
def tag_pages(tagword):
    tag_posts = tag_func(posts, tagword)
    print(tag_posts[0]['pic'])
    return render_template("tag.html", posts=tag_posts, tagword=tagword)


@app.route("/user_feed/<username>/")
def user_feed(username):
    user_posts = user_posts_func(posts, username)
    return render_template("user-feed.html", posts=user_posts)


@app.route("/posts/<int:postid>/", methods=["GET", "POST"])
def post(postid):
    _, comments, _ = load_data()
    post_comments = post_comment_func(comments, postid)

    if request.method == "POST":
        trigger = request.form.get("bookmark")
        if (trigger == "change"):
            bookmark_write(postid)

        else:
            name = request.form.get("commenter_name")
            comment = request.form.get("comment")

            if(name and comment):
                write_comment(comments, name, comment, postid)

    return render_template("post.html", posts=posts[postid-1], comments=post_comments)



@app.route("/bookmarks/", )
def bookmarks():
    bookmarked_posts = get_bookmarked_posts(posts)
    return render_template("bookmarks.html", posts=bookmarked_posts)


if __name__ == "__main__":
    app.run(debug=True)

