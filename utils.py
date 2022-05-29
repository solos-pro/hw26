import json
from pprint import pprint

def bookmark_read():
    with open('data/bookmarks.json') as fp:
        bookmarks = json.load(fp)
    return bookmarks

def bookmark_write(post):
    bookmarks = bookmark_read()

    if post not in bookmarks:
        bookmarks.append(post)
    else:
        bookmarks.remove(post)

    with open('data/bookmarks.json', 'w', encoding='utf-8') as file:
        json.dump(bookmarks, file, ensure_ascii=False, indent=4, sort_keys=True)

def get_bookmarked_posts(posts):
    bookmarks = bookmark_read()
    bookmarked_posts = []
    if bookmarks:
        for bookmark in bookmarks:
            for post in posts:
                if post["pk"] == bookmark:
                    bookmarked_posts.append(post)
    return bookmarked_posts

def load_comment():
    with open('data/comments.json') as fp:
        comments = json.load(fp)
    return comments

def write_comment(comments, name, comment, postid):
    new_pk = 1
    for element in comments:
        if element["pk"] >= new_pk:
            new_pk = element["pk"] + 1

    new_comment = {
        "commenter_name": name,
        "comment": comment,
        "post_id": postid,
        "pk": new_pk
    }
    comments.append(new_comment)

    with open('data/comments.json', 'w', encoding='utf-8') as file:
        json.dump(comments, file, ensure_ascii=False, indent=4, sort_keys=True)
    return 0


def load_data():
    with open('data/data.json') as fp:
        posts = json.load(fp)

    with open('data/comments.json') as fp:
        comments = json.load(fp)

    posts = prepare_posts(posts, comments)

    with open('data/bookmarks.json') as fp:
        bookmark = json.load(fp)

    return posts, comments, bookmark



def prepare_posts(posts, comments):
    for i, post in enumerate(posts):
        pk = post.get('pk')
        post_comments = []
        for comment in comments:
            if comment.get('post_id') == pk:
                post_comments.append(comment)
            posts[i]['comment_count'] = len(post_comments)

        posts[i]['content'] = tegify_content(posts[i]['content'])
    return posts


def tegify_content(content):
    words = content.split(" ")
    for i, word in enumerate(words):
        if word.startswith("#"):
            tag = word.replace("#", "")
            link = f"<a href=/tag/{tag}>{word}</a>"
            words[i] = link
    return " ".join(words)

def search_func(posts, search_query):
    searched_posts = []
    if search_query:
        for post in posts:
            if search_query in post["content"]:
                # post["content"] = post["content"][:50]
                searched_posts.append(post)
    return searched_posts


def user_posts_func(posts, username):
    user_posts = []
    for post_ in posts:
        if post_["poster_name"] == username:
            post_["content"] = post_["content"]#[:50]
            user_posts.append(post_)
    return user_posts

def post_comment_func(comments, postid=1):
    post_comments = []
    for post_comment in comments:
        if post_comment['post_id'] == postid:
            post_comments.append(post_comment)
    return post_comments

def tag_func(posts, tag_word):
    tag_posts = []
    for post in posts:
        if ("#" + tag_word) in post['content']:
            tag_posts.append(post)
    return tag_posts

