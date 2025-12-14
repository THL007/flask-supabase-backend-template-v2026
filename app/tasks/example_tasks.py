"""Example Celery tasks."""
from app.extensions import celery
from app.extensions import supabase_client
from flask import current_app


@celery.task(name="tasks.example_task")
def example_task(data: dict):
    """Example async task."""
    try:
        # Access Flask app context
        with current_app.app_context():
            current_app.logger.info(f"Processing task with data: {data}")
            
            # Example: Process data, send email, etc.
            # This is where you'd put your async logic
            
            return {"status": "completed", "data": data}
    except Exception as e:
        current_app.logger.error(f"Task failed: {e}")
        raise


@celery.task(name="tasks.process_blog_post")
def process_blog_post(post_id: str):
    """Process a blog post asynchronously (e.g., generate preview, index for search)."""
    try:
        with current_app.app_context():
            client = supabase_client.get_client()
            
            # Example: Fetch post, process it, update it
            response = client.table("blog_posts").select("*").eq("id", post_id).single().execute()
            
            if response.data:
                # Process the post (e.g., generate preview, extract tags, etc.)
                current_app.logger.info(f"Processing blog post: {post_id}")
                
                # Update post with processed data
                # client.table("blog_posts").update({"processed": True}).eq("id", post_id).execute()
                
                return {"status": "completed", "post_id": post_id}
            else:
                raise Exception(f"Post not found: {post_id}")
    except Exception as e:
        current_app.logger.error(f"Failed to process blog post: {e}")
        raise

