# ReviewPlatform

## 🚀 Overview

ReviewPlatform is a user-friendly review and rating system that enables
users to explore shops and cafés, read and write reviews, and interact
through voting.

**Tech Stack:** Django · Bootstrap · jQuery · SQLite

------------------------------------------------------------------------

## 🧩 Key Features

### 🏪 Shop Management

-   View all shops with categories and locations
-   **Admin-only:** Add, update, and delete shops
-   Duplicate prevention based on *shop name + location*

### ⭐ Review & Rating System

-   Users can post detailed reviews
-   1--5 star rating system
-   AJAX-based live upvote/downvote
-   Contradictory or duplicate votes prevented
-   Displays total score (upvotes − downvotes)

### 🔍 Search & Filtering

-   Search shops by name
-   Filter by category
-   Combine search + category
-   Sorting options:
    -   ⭐ Highest Rating
    -   📝 Most Reviewed
    -   🆕 Newly Added

### 📄 Pagination

-   Shops displayed in batches of 5 for smooth browsing

### 🔐 Authentication

-   User registration
-   Login / Logout
-   Restricted interactions for unauthenticated users
-   Admin privileges for shop management

------------------------------------------------------------------------

## 📁 Project Structure (Highlighted)

    ReviewPlatform/
    ├── shops/                # Shop & review app
    ├── templates/            # HTML templates
    ├── static/               # CSS, JS, Images
    ├── ReviewPlatform/       # Django project configuration
    └── db.sqlite3            # Database

------------------------------------------------------------------------

## 🚧 Future Enhancements

-   Add user profiles
-   Implement review images
-   Google Maps integration for shop location
-   API endpoints for external integration

------------------------------------------------------------------------

## 📜 License

This project is licensed for educational and learning purposes.
