import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { FavoritesService } from '../../services/favorites.service';
import { Movie, Genre, Director, Actor, FilterOptions } from '../../models/movie.model';

@Component({
  selector: 'app-movie-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './movie-list.component.html',
  styleUrls: ['./movie-list.component.css']
})
export class MovieListComponent implements OnInit {
  movies: Movie[] = [];
  genres: Genre[] = [];
  directors: Director[] = [];
  actors: Actor[] = [];
  loading = false;
  error: string | null = null;
  
  searchQuery = '';
  selectedGenreId: number | null = null;
  selectedDirectorId: number | null = null;
  selectedActorId: number | null = null;
  selectedYear: number | null = null;
  
  years: number[] = [];

  constructor(
    private movieService: MovieService,
    public favoritesService: FavoritesService
  ) {
    // Generate years from 1900 to current year
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 1900; year--) {
      this.years.push(year);
    }
  }

  ngOnInit(): void {
    this.loadMovies();
    this.loadFilters();
  }

  loadMovies(): void {
    this.loading = true;
    this.error = null;
    
    // Trim search query and check if it has meaningful content
    const trimmedQuery = this.searchQuery.trim();
    
    if (trimmedQuery) {
      this.movieService.searchMovies(trimmedQuery).subscribe({
        next: (movies) => {
          this.movies = movies;
          this.loading = false;
        },
        error: (error) => {
          this.error = 'Failed to search movies';
          this.loading = false;
          console.error('Error searching movies:', error);
        }
      });
    } else if (this.hasActiveFilters()) {
      const filters: FilterOptions = {};
      if (this.selectedGenreId) filters.genre_id = this.selectedGenreId;
      if (this.selectedDirectorId) filters.director_id = this.selectedDirectorId;
      if (this.selectedActorId) filters.actor_id = this.selectedActorId;
      if (this.selectedYear) filters.release_year = this.selectedYear;
      
      this.movieService.filterMovies(filters).subscribe({
        next: (movies) => {
          this.movies = movies;
          this.loading = false;
        },
        error: (error) => {
          this.error = 'Failed to filter movies';
          this.loading = false;
          console.error('Error filtering movies:', error);
        }
      });
    } else {
      this.movieService.getMovies().subscribe({
        next: (movies) => {
          this.movies = movies;
          this.loading = false;
        },
        error: (error) => {
          this.error = 'Failed to load movies';
          this.loading = false;
          console.error('Error loading movies:', error);
        }
      });
    }
  }

  loadFilters(): void {
    // Load genres
    this.movieService.getGenres().subscribe({
      next: (genres) => this.genres = genres,
      error: (error) => console.error('Error loading genres:', error)
    });
    
    // Load directors
    this.movieService.getDirectors().subscribe({
      next: (directors) => this.directors = directors,
      error: (error) => console.error('Error loading directors:', error)
    });
    
    // Load actors
    this.movieService.getActors().subscribe({
      next: (actors) => this.actors = actors,
      error: (error) => console.error('Error loading actors:', error)
    });
  }

  hasActiveFilters(): boolean {
    return !!(this.selectedGenreId || this.selectedDirectorId || this.selectedActorId || this.selectedYear);
  }

  onSearch(): void {
    // Only search if there's actual content
    const trimmedQuery = this.searchQuery.trim();
    if (!trimmedQuery && !this.hasActiveFilters()) {
      // If search is empty and no filters, just load all movies
      this.loadMovies();
      return;
    }
    
    if (trimmedQuery.length > 0) {
      this.loadMovies();
    }
  }

  onFilterChange(): void {
    this.searchQuery = ''; // Clear search when using filters
    this.loadMovies();
  }

  clearFilters(): void {
    this.searchQuery = '';
    this.selectedGenreId = null;
    this.selectedDirectorId = null;
    this.selectedActorId = null;
    this.selectedYear = null;
    this.loadMovies();
  }

  toggleFavorite(event: Event, movieId: number): void {
    event.stopPropagation();
    event.preventDefault();
    this.favoritesService.toggleFavorite(movieId);
  }

  toggleWatchLater(event: Event, movieId: number): void {
    event.stopPropagation();
    event.preventDefault();
    this.favoritesService.toggleWatchLater(movieId);
  }

  getDefaultPoster(): string {
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="450" viewBox="0 0 300 450"%3E%3Crect width="300" height="450" fill="%23dee2e6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="20" fill="%236c757d"%3ENo Poster%3C/text%3E%3C/svg%3E';
  }
}
