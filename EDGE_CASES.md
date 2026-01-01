# Edge Cases and Error Handling Documentation

This document outlines edge cases, error handling strategies, and validation rules implemented throughout the Movie Explorer Platform.

## Table of Contents
- [Backend Edge Cases](#backend-edge-cases)
- [Frontend Edge Cases](#frontend-edge-cases)
- [Database Constraints](#database-constraints)
- [API Validation Rules](#api-validation-rules)
- [Known Limitations](#known-limitations)

---

## Backend Edge Cases

### 1. Movie CRUD Operations

#### Creating Movies
**Edge Cases:**
- **Non-existent Director ID**: Returns 404 error with message "Director not found"
- **Non-existent Genre IDs**: Returns 404 error with message "Genre not found"
- **Duplicate Title**: Allowed (no unique constraint on title)
- **Rating out of range**: Validated by Pydantic (0.0 - 10.0)
- **Negative duration**: Validated by Pydantic (must be positive integer)
- **Future release year**: Allowed (for upcoming movies)
- **Empty genre list**: Allowed (movie without genres)

**Validation Rules:**
```python
rating: float = Field(..., ge=0.0, le=10.0)  # Must be between 0 and 10
duration: int = Field(..., gt=0)              # Must be positive
release_year: int                             # No year range validation
```

**Example Error Response:**
```json
{
  "detail": "Director with id 999 not found"
}
```

#### Filtering Movies
**Edge Cases:**
- **All filters None/null**: Returns all movies (behaves like getMovies)
- **Invalid filter IDs**: Returns empty array (no error thrown)
- **Multiple filters**: Applied with AND logic (must match all criteria)
- **Genre filter with no movies**: Returns empty array
- **Actor filter without movie relationship**: Returns empty array

**Implementation:**
```python
# Filters are conditionally applied only if provided
if genre_id:
    query = query.join(Movie.genres).filter(Genre.id == genre_id)
if director_id:
    query = query.filter(Movie.director_id == director_id)
if actor_id:
    query = query.join(Movie.actors).filter(Actor.id == actor_id)
```

#### Search Movies
**Edge Cases:**
- **Empty search term**: Returns all movies (validation should be frontend)
- **Special characters**: Handled safely by SQLAlchemy parameterization
- **SQL injection attempts**: Prevented by ORM parameterization
- **Case sensitivity**: Case-insensitive using ILIKE
- **Unicode characters**: Fully supported

**SQL Injection Protection:**
```python
# SAFE: SQLAlchemy parameterizes queries
Movie.title.ilike(f"%{search_term}%")

# UNSAFE (not used):
# db.execute(f"SELECT * FROM movies WHERE title LIKE '%{search_term}%'")
```

### 2. Actor/Director Operations

#### Creating Actors
**Edge Cases:**
- **Duplicate names**: Allowed (no unique constraint)
- **Missing optional fields**: Set to None (nullable columns)
- **Birth year in future**: Allowed (no validation)
- **Negative birth year**: Allowed (for historical figures)
- **Empty bio**: Allowed (nullable field)

**Schema Definition:**
```python
class ActorCreate(BaseModel):
    name: str                      # Required
    bio: Optional[str] = None      # Optional
    birth_year: Optional[int] = None
    photo_url: Optional[str] = None
```

#### Filter Actors by Genre
**Edge Cases:**
- **Genre with no movies**: Returns empty array
- **Movies without actors**: Not included in results
- **Actor in multiple movies of same genre**: Returned once (DISTINCT query)

**Query Implementation:**
```python
db.query(Actor).join(Actor.movies).join(Movie.genres).filter(
    Genre.id == genre_id
).distinct().offset(skip).limit(limit).all()
```

### 3. Review Operations

#### Creating Reviews
**Edge Cases:**
- **Non-existent movie**: Returns 404 error
- **Duplicate reviews**: Allowed (same author can review multiple times)
- **Rating out of range**: Validated (1-10 scale)
- **Empty comment**: Allowed (nullable field)
- **Very long comments**: No length limit (database TEXT column)

**Validation:**
```python
rating: int = Field(..., ge=1, le=10)  # 1 to 10 scale
comment: Optional[str] = None           # Nullable
```

#### Deleting Reviews
**Edge Cases:**
- **Delete non-existent review**: Returns 404 error
- **Orphaned movie**: Deleting review doesn't delete movie (no cascade)
- **Movie with no reviews**: Returns empty array (not an error)

### 4. Database Seeding

**Edge Cases:**
- **Running seed multiple times**: Creates duplicate entries (no idempotency check)
- **Empty database**: Successfully creates all entities
- **Partial seed failure**: Rolled back by transaction
- **Foreign key violations**: Prevented by creating entities in correct order (directors → movies → actors → genres → relationships → reviews)

**Seed Order:**
```python
1. Directors (no dependencies)
2. Genres (no dependencies)
3. Actors (no dependencies)
4. Movies (requires director_id)
5. Movie-Genre relationships (requires movies and genres)
6. Movie-Actor relationships (requires movies and actors)
7. Reviews (requires movies)
```

---

## Frontend Edge Cases

### 1. Movie Service

#### Filter Operations
**Edge Cases:**
- **All filters null**: Query params omitted, returns all movies
- **Angular [value]="null"**: Converts to string "null" ❌ INCORRECT
- **Angular [ngValue]="null"**: Properly sends null ✅ CORRECT
- **Undefined vs null**: Both handled identically (excluded from params)

**Correct Implementation:**
```typescript
// Check for both null and undefined before adding to params
if (filters.genre_id != null && filters.genre_id !== undefined) {
  params = params.set('genre_id', filters.genre_id.toString());
}
```

**HTML Template Fix:**
```html
<!-- INCORRECT: converts to string "null" -->
<option [value]="null">All Genres</option>

<!-- CORRECT: properly handles null value -->
<option [ngValue]="null">All Genres</option>
```

#### Search Validation
**Edge Cases:**
- **Empty string**: Should not trigger API call
- **Whitespace only**: Trimmed and prevented
- **Very long queries**: No limit (backend handles pagination)
- **Special characters**: URL-encoded by HttpClient

**Validation Implementation:**
```typescript
onSearch() {
  const trimmed = this.searchQuery.trim();
  if (trimmed.length > 0) {
    this.movieService.searchMovies(trimmed).subscribe(...);
  }
}
```

### 2. Favorites Service

#### LocalStorage Operations
**Edge Cases:**
- **LocalStorage disabled**: Application breaks (no fallback)
- **LocalStorage full**: Add operation fails silently
- **Corrupted JSON**: Caught and returns empty array
- **Browser incognito mode**: Works but cleared on close
- **Multiple browser tabs**: Changes not synced between tabs

**Corruption Handling:**
```typescript
getFavorites(): number[] {
  try {
    const favorites = localStorage.getItem('favorites');
    return favorites ? JSON.parse(favorites) : [];
  } catch (error) {
    console.error('Corrupted favorites data, resetting');
    return [];
  }
}
```

#### Duplicate Prevention
**Edge Cases:**
- **Adding same movie twice**: Prevented using Set
- **Toggle rapid clicks**: Each click toggles (no debouncing)
- **Invalid movie IDs**: Allowed (no validation)

```typescript
addToFavorites(movieId: number): void {
  const favorites = new Set(this.getFavorites());
  favorites.add(movieId);  // Set prevents duplicates
  localStorage.setItem('favorites', JSON.stringify([...favorites]));
}
```

### 3. Component Edge Cases

#### Movie Detail Component
**Edge Cases:**
- **Movie not found (404)**: Shows error message
- **Missing poster image**: Shows placeholder or broken image
- **No reviews**: Shows "No reviews yet" message
- **Empty cast**: Shows empty section
- **Null director**: Defensive navigation with optional chaining

**Template Safety:**
```html
<!-- Safe navigation operator prevents errors if director is null -->
<p>Directed by: {{ movie?.director?.name }}</p>

<!-- Default text for empty arrays -->
<div *ngIf="movie?.reviews?.length === 0">
  No reviews yet.
</div>
```

#### Favorites/Watch Later Pages
**Edge Cases:**
- **Empty favorites list**: Shows "No favorites yet" message
- **Movie deleted from database**: 404 error when fetching (not handled gracefully)
- **LocalStorage out of sync**: No refresh mechanism

**Missing Feature:**
```typescript
// TODO: Handle case where favorited movie was deleted
loadFavorites() {
  const ids = this.favoritesService.getFavorites();
  ids.forEach(id => {
    this.movieService.getMovie(id).subscribe({
      next: movie => this.movies.push(movie),
      error: err => {
        // Movie was deleted - should remove from favorites
        console.warn(`Movie ${id} not found, removing from favorites`);
        this.favoritesService.removeFromFavorites(id);
      }
    });
  });
}
```

---

## Database Constraints

### SQLite Constraints
```sql
-- Primary Keys (auto-increment)
id INTEGER PRIMARY KEY AUTOINCREMENT

-- Foreign Keys
FOREIGN KEY (director_id) REFERENCES directors(id)

-- Nullable Fields
bio TEXT NULL
photo_url TEXT NULL
poster_url TEXT NULL

-- Non-Nullable Fields
name VARCHAR NOT NULL
title VARCHAR NOT NULL
release_year INTEGER NOT NULL

-- No Unique Constraints
-- Movies can have duplicate titles
-- Actors can have duplicate names
-- Reviews can have duplicate authors
```

### Many-to-Many Relationships
```python
# movie_genres association table
movie_id → movies.id (CASCADE delete)
genre_id → genres.id (CASCADE delete)

# movie_actors association table
movie_id → movies.id (CASCADE delete)
actor_id → actors.id (CASCADE delete)
```

**Cascading Behavior:**
- Deleting a movie removes its genre/actor associations
- Deleting a genre/actor removes associations but not movies
- No orphan prevention (genres can exist with no movies)

---

## API Validation Rules

### Request Validation
```python
# Pydantic automatically validates:
1. Required fields present
2. Correct data types
3. Field constraints (min/max values)
4. Email format (if EmailStr used)
5. URL format (if HttpUrl used)
```

### Response Codes
```
200 OK          - Successful GET, PUT, POST, DELETE
404 Not Found   - Resource doesn't exist
422 Unprocessable Entity - Validation error (Pydantic)
500 Internal Server Error - Unexpected backend error
```

### Query Parameter Handling
```python
# Optional parameters with defaults
skip: int = 0
limit: int = 100

# Optional filters (None if not provided)
genre_id: Optional[int] = None
director_id: Optional[int] = None

# Backend ignores None values in filtering
```

---

## Known Limitations

### 1. No Authentication
- All endpoints are public
- Anyone can create/update/delete data
- No user-specific favorites (localStorage only)

### 2. No Pagination UI
- Backend supports pagination (skip/limit)
- Frontend loads all results at once
- Could cause performance issues with 1000+ movies

### 3. No Image Validation
- poster_url and photo_url accept any string
- No verification that URLs point to valid images
- Broken image links display broken image icon

### 4. No Rate Limiting
- API can be spammed with requests
- No throttling or request limiting
- Vulnerable to DoS attacks

### 5. LocalStorage Limitations
- Favorites/watch later only stored locally
- Not synced across devices
- Cleared when browser data is cleared
- No backup or recovery

### 6. Search Limitations
- Simple substring matching only
- No fuzzy search or typo tolerance
- No search ranking or relevance scoring
- Searches both title and description (can't filter to one field)

### 7. No Soft Deletes
- Deleting a movie permanently removes it
- No trash/recycle bin
- Favorited movies can be deleted (causes 404 errors)

### 8. No Optimistic Locking
- Concurrent updates can overwrite each other
- Last write wins (no conflict detection)
- No versioning or change tracking

---

## Testing Edge Cases

### Backend Tests (pytest)
```bash
cd backend
pytest tests/

# Run specific test file
pytest tests/test_movies_api.py

# Run with coverage
pytest --cov=app tests/
```

**Test Coverage Includes:**
- ✅ Empty database queries
- ✅ Invalid foreign key references
- ✅ Search with no results
- ✅ Filtering with no matches
- ✅ Creating with missing required fields
- ✅ Updating non-existent resources
- ✅ Deleting non-existent resources
- ✅ Validation errors (rating out of range)

### Frontend Tests (Jest)
```bash
cd frontend
npm install
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:ci
```

**Test Coverage Includes:**
- ✅ Empty filter handling (all nulls)
- ✅ Empty search query validation
- ✅ LocalStorage corruption handling
- ✅ Duplicate prevention in favorites
- ✅ HTTP error responses
- ✅ Component initialization
- ✅ Service method calls

---

## Recommendations for Production

1. **Add Authentication**: Implement JWT or OAuth2
2. **Add Authorization**: Role-based access control (RBAC)
3. **Add Rate Limiting**: Prevent API abuse
4. **Add Caching**: Redis for frequently accessed data
5. **Add Image Validation**: Verify URLs and file types
6. **Add Soft Deletes**: Allow recovery of deleted data
7. **Add Server-Side Favorites**: Store in database, not localStorage
8. **Add Pagination UI**: Infinite scroll or page navigation
9. **Add Error Boundaries**: Graceful error handling in Angular
10. **Add Monitoring**: Logging, metrics, and alerting
11. **Add Input Sanitization**: Prevent XSS attacks
12. **Add CORS Configuration**: Restrict allowed origins
13. **Add Request Validation**: Additional backend validation beyond Pydantic
14. **Add Database Migrations**: Use Alembic for schema changes
15. **Add Backup Strategy**: Regular database backups

---

## Contact

For questions about edge cases or to report bugs, please open an issue on GitHub.
