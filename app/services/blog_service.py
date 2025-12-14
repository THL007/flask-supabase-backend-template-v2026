"""Blog service for managing Markdown-backed content."""
import markdown
from typing import List, Dict, Optional
from supabase import Client


class BlogService:
    """Service for blog operations."""
    
    def __init__(self, supabase: Client):
        """Initialize blog service."""
        self.supabase = supabase
        self.table = "blog_posts"
        self.bucket = "blog-content"
    
    def list_posts(self, limit: int = 10, offset: int = 0) -> List[Dict]:
        """List all blog posts."""
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("published", True)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .offset(offset)\
                .execute()
            
            posts = []
            for post in response.data:
                posts.append(self._format_post(post))
            
            return posts
        except Exception as e:
            raise Exception(f"Failed to list posts: {str(e)}")
    
    def get_post_by_slug(self, slug: str) -> Optional[Dict]:
        """Get a blog post by slug."""
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("slug", slug)\
                .eq("published", True)\
                .single()\
                .execute()
            
            if not response.data:
                return None
            
            post = self._format_post(response.data)
            
            # Fetch markdown content from storage if needed
            if post.get("content_storage_path"):
                content = self._fetch_content_from_storage(post["content_storage_path"])
                if content:
                    post["html_content"] = self._render_markdown(content)
            
            return post
        except Exception as e:
            raise Exception(f"Failed to get post: {str(e)}")
    
    def _format_post(self, post: Dict) -> Dict:
        """Format post data."""
        return {
            "id": post.get("id"),
            "title": post.get("title"),
            "slug": post.get("slug"),
            "excerpt": post.get("excerpt"),
            "author": post.get("author"),
            "created_at": post.get("created_at"),
            "updated_at": post.get("updated_at"),
            "tags": post.get("tags", []),
            "content_storage_path": post.get("content_storage_path"),
            "content": post.get("content"),  # Inline content if stored in table
        }
    
    def _fetch_content_from_storage(self, path: str) -> Optional[str]:
        """Fetch markdown content from Supabase Storage."""
        try:
            response = self.supabase.storage.from_(self.bucket).download(path)
            return response.decode("utf-8")
        except Exception:
            return None
    
    def _render_markdown(self, markdown_content: str) -> str:
        """Render markdown to HTML."""
        md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
        return md.convert(markdown_content)

