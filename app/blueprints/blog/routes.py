"""Blog routes."""
from flask import render_template, abort as flask_abort, request, jsonify
from app.blueprints.blog import blog_bp
from app.services.blog_service import BlogService
from app.extensions import supabase_client


@blog_bp.route("/")
def index():
    """List all blog posts."""
    try:
        blog_service = BlogService(supabase_client.get_client())
        posts = blog_service.list_posts()
        return render_template("blog/index.html", posts=posts)
    except Exception as e:
        current_app.logger.error(f"Error listing blog posts: {e}")
        flask_abort(500)


@blog_bp.route("/<slug>")
def post(slug):
    """Display a single blog post."""
    try:
        blog_service = BlogService(supabase_client.get_client())
        post_data = blog_service.get_post_by_slug(slug)
        
        if not post_data:
            flask_abort(404)
        
        return render_template("blog/post.html", post=post_data)
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Error fetching blog post: {e}")
        flask_abort(500)


@blog_bp.route("/api/posts")
def api_list_posts():
    """API endpoint to list blog posts."""
    try:
        blog_service = BlogService(supabase_client.get_client())
        posts = blog_service.list_posts()
        return jsonify(posts)
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Error listing blog posts: {e}")
        return jsonify({"error": "Failed to fetch posts"}), 500


@blog_bp.route("/api/posts/<slug>")
def api_get_post(slug):
    """API endpoint to get a single blog post."""
    try:
        blog_service = BlogService(supabase_client.get_client())
        post_data = blog_service.get_post_by_slug(slug)
        
        if not post_data:
            return jsonify({"error": "Post not found"}), 404
        
        return jsonify(post_data)
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Error fetching blog post: {e}")
        return jsonify({"error": "Failed to fetch post"}), 500

