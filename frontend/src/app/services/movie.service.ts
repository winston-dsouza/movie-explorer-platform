/**
 * MovieService - HTTP service for Movie Explorer API
 * 
 * Provides methods to interact with the backend REST API for movies, actors,
 * directors, genres, and reviews. All methods return RxJS Observables for
 * asynchronous data handling.
 * 
 * Edge Cases Handled:
 * - Null/undefined filter values are excluded from query parameters
 * - Empty search queries are validated before API calls
 * - Pagination parameters have default values
 * - HTTP errors propagate through Observable error channel
 * 
 * @example
 * ```typescript
 * // Get all movies
 * this.movieService.getMovies().subscribe(movies => console.log(movies));
 * 
 * // Search with validation
 * if (query.trim().length > 0) {
 *   this.movieService.searchMovies(query).subscribe(...);
 * }
 * ```
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie, MovieCreate, Genre, Actor, Director, ActorWithMovies, DirectorWithMovies, FilterOptions } from '../models/movie.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // ===== Movies Endpoints =====

  /**
   * Retrieve all movies with optional pagination.
   * 
   * @param skip - Number of records to skip (default: 0)
   * @param limit - Maximum number of records to return (default: 100)
   * @returns Observable<Movie[]> - Stream of movie array
   * 
   * Edge Cases:
   * - Returns empty array if no movies exist
   * - Pagination prevents memory overflow on large datasets
   */
  getMovies(skip: number = 0, limit: number = 100): Observable<Movie[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Movie[]>(`${this.apiUrl}/movies`, { params });
  }

  /**
   * Retrieve a single movie by ID with full details.
   * 
   * @param id - Movie primary key
   * @returns Observable<Movie> - Stream with movie details including actors, genres, director, reviews
   * 
   * Edge Cases:
   * - Returns 404 error if movie doesn't exist (handled by HTTP interceptor)
   * - Invalid IDs (negative, non-numeric) handled by backend
   */
  getMovie(id: number): Observable<Movie> {
    return this.http.get<Movie>(`${this.apiUrl}/movies/${id}`);
  }

  /**
   * Filter movies by multiple criteria (genre, director, actor, year).
   * Only non-null/undefined filters are applied to the query.
   * 
   * @param filters - Object containing optional filter criteria
   * @param skip - Pagination offset
   * @param limit - Maximum results
   * @returns Observable<Movie[]> - Filtered movie list
   * 
   * Edge Cases:
   * - Null/undefined values are excluded from query parameters
   * - Multiple filters apply AND logic (must match all)
   * - Returns empty array if no matches found
   * 
   * @example
   * ```typescript
   * // Filter by genre only
   * filterMovies({ genre_id: 1, director_id: null, actor_id: null })
   * 
   * // Filter by multiple criteria
   * filterMovies({ genre_id: 1, director_id: 2, actor_id: 3 })
   * ```
   */
  filterMovies(filters: FilterOptions, skip: number = 0, limit: number = 100): Observable<Movie[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    
    // Only add defined filter values to prevent "null" string in query params
    if (filters.genre_id != null && filters.genre_id !== undefined) {
      params = params.set('genre_id', filters.genre_id.toString());
    }
    if (filters.director_id != null && filters.director_id !== undefined) {
      params = params.set('director_id', filters.director_id.toString());
    }
    if (filters.release_year != null && filters.release_year !== undefined) {
      params = params.set('release_year', filters.release_year.toString());
    }
    if (filters.actor_id != null && filters.actor_id !== undefined) {
      params = params.set('actor_id', filters.actor_id.toString());
    }
    
    return this.http.get<Movie[]>(`${this.apiUrl}/movies/filter`, { params });
  }

  /**
   * Search movies by title or description using case-insensitive partial matching.
   * 
   * @param query - Search string (should be trimmed before calling)
   * @param skip - Pagination offset
   * @param limit - Maximum results
   * @returns Observable<Movie[]> - Movies matching search query
   * 
   * Edge Cases:
   * - Empty/whitespace queries should be validated before calling this method
   * - Case-insensitive search performed by backend
   * - Returns empty array if no matches
   * - Special characters are URL-encoded automatically
   * 
   * @example
   * ```typescript
   * const query = searchInput.trim();
   * if (query.length > 0) {
   *   this.searchMovies(query).subscribe(...);
   * }
   * ```
   */
  searchMovies(query: string, skip: number = 0, limit: number = 100): Observable<Movie[]> {
    const params = new HttpParams()
      .set('q', query)
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Movie[]>(`${this.apiUrl}/movies/search`, { params });
  }

  createMovie(movie: MovieCreate): Observable<Movie> {
    return this.http.post<Movie>(`${this.apiUrl}/movies`, movie);
  }

  updateMovie(id: number, movie: Partial<MovieCreate>): Observable<Movie> {
    return this.http.put<Movie>(`${this.apiUrl}/movies/${id}`, movie);
  }

  deleteMovie(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/movies/${id}`);
  }

  // Genres endpoints
  getGenres(skip: number = 0, limit: number = 100): Observable<Genre[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Genre[]>(`${this.apiUrl}/genres`, { params });
  }

  getGenre(id: number): Observable<Genre> {
    return this.http.get<Genre>(`${this.apiUrl}/genres/${id}`);
  }

  // Actors endpoints
  getActors(skip: number = 0, limit: number = 100): Observable<Actor[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Actor[]>(`${this.apiUrl}/actors`, { params });
  }

  getActor(id: number): Observable<ActorWithMovies> {
    return this.http.get<ActorWithMovies>(`${this.apiUrl}/actors/${id}`);
  }

  searchActors(query: string, skip: number = 0, limit: number = 100): Observable<Actor[]> {
    const params = new HttpParams()
      .set('q', query)
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Actor[]>(`${this.apiUrl}/actors/search`, { params });
  }

  getActorsByGenre(genreId: number, skip: number = 0, limit: number = 100): Observable<Actor[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Actor[]>(`${this.apiUrl}/actors/by-genre/${genreId}`, { params });
  }

  // Directors endpoints
  getDirectors(skip: number = 0, limit: number = 100): Observable<Director[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Director[]>(`${this.apiUrl}/directors`, { params });
  }

  getDirector(id: number): Observable<DirectorWithMovies> {
    return this.http.get<DirectorWithMovies>(`${this.apiUrl}/directors/${id}`);
  }

  searchDirectors(query: string, skip: number = 0, limit: number = 100): Observable<Director[]> {
    const params = new HttpParams()
      .set('q', query)
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Director[]>(`${this.apiUrl}/directors/search`, { params });
  }
}
