import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FavoritesService } from '@app/services/favorites.service';
import { MovieService } from '@app/services/movie.service';
import { Movie } from '@app/models/movie.model';

@Component({
  selector: 'app-watch-later',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './watch-later.component.html',
  styleUrls: ['./watch-later.component.css']
})
export class WatchLaterComponent implements OnInit {
  watchLaterMovies: Movie[] = [];
  loading = false;
  error = '';
  Math = Math;

  constructor(
    private favoritesService: FavoritesService,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    this.loadWatchLaterMovies();
  }

  loadWatchLaterMovies(): void {
    this.loading = true;
    this.error = '';
    
    const watchLaterIds = this.favoritesService.getWatchLaterIds();
    
    if (watchLaterIds.length === 0) {
      this.watchLaterMovies = [];
      this.loading = false;
      return;
    }

    // Load movie details for each watch later item
    const moviePromises = watchLaterIds.map((id: number) => 
      this.movieService.getMovie(id).toPromise()
    );

    Promise.all(moviePromises)
      .then(movies => {
        this.watchLaterMovies = movies.filter((movie: Movie | undefined) => movie !== undefined) as Movie[];
        this.loading = false;
      })
      .catch(err => {
        this.error = 'Failed to load watch later movies';
        this.loading = false;
        console.error(err);
      });
  }

  removeFromWatchLater(movieId: number): void {
    this.favoritesService.removeFromWatchLater(movieId);
    this.watchLaterMovies = this.watchLaterMovies.filter(movie => movie.id !== movieId);
  }

  addToFavorites(movieId: number): void {
    this.favoritesService.addFavorite(movieId);
  }

  isInFavorites(movieId: number): boolean {
    return this.favoritesService.isFavorite(movieId);
  }

  markAsWatched(movieId: number): void {
    this.removeFromWatchLater(movieId);
    // Optionally, you could track watched movies separately
  }

  getRatingStars(rating: number): string[] {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push('bi-star-fill');
    }
    if (hasHalfStar) {
      stars.push('bi-star-half');
    }
    for (let i = stars.length; i < 5; i++) {
      stars.push('bi-star');
    }
    
    return stars;
  }

  getTotalRuntime(): number {
    return this.watchLaterMovies.reduce((total, movie) => total + (movie.runtime_minutes || 0), 0);
  }

  formatRuntime(minutes: number): string {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  }

  getDefaultPoster(): string {
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="450" viewBox="0 0 300 450"%3E%3Crect width="300" height="450" fill="%23dee2e6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="20" fill="%236c757d"%3ENo Poster%3C/text%3E%3C/svg%3E';
  }
}
