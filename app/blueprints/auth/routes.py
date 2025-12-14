"""Auth routes."""
from flask import request, jsonify, session, redirect, url_for
from app.blueprints.auth import auth_bp
from app.extensions import supabase_client


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login endpoint (delegates to Supabase)."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        client = supabase_client.get_client()
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        
        if response.user:
            return jsonify({
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                },
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
            })
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Signup endpoint (delegates to Supabase)."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        client = supabase_client.get_client()
        response = client.auth.sign_up({
            "email": email,
            "password": password,
        })
        
        if response.user:
            return jsonify({
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                },
                "message": "User created successfully",
            }), 201
        else:
            return jsonify({"error": "Failed to create user"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout endpoint."""
    try:
        client = supabase_client.get_client()
        client.auth.sign_out()
        return jsonify({"message": "Logged out successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """Refresh access token."""
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    
    if not refresh_token:
        return jsonify({"error": "Refresh token required"}), 400
    
    try:
        client = supabase_client.get_client()
        response = client.auth.refresh_session(refresh_token)
        
        if response.session:
            return jsonify({
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
            })
        else:
            return jsonify({"error": "Failed to refresh token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 401

