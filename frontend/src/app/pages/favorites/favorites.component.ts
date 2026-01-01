import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FavoritesService } from '@app/services/favorites.service';
import { MovieService } from '@app/services/movie.service';
import { Movie } from '@app/models/movie.model';

@Component({
  selector: 'app-favorites',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.css']
})
export class FavoritesComponent implements OnInit {
  favoriteMovies: Movie[] = [];
  loading = false;
  error = '';

  constructor(
    private favoritesService: FavoritesService,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    this.loadFavoriteMovies();
  }

  loadFavoriteMovies(): void {
    this.loading = true;
    this.error = '';
    
    const favoriteIds = this.favoritesService.getFavoriteIds();
    
    if (favoriteIds.length === 0) {
      this.favoriteMovies = [];
      this.loading = false;
      return;
    }

    // Load movie details for each favorite
    const moviePromises = favoriteIds.map((id: number) => 
      this.movieService.getMovie(id).toPromise()
    );

    Promise.all(moviePromises)
      .then(movies => {
        this.favoriteMovies = movies.filter((movie: Movie | undefined) => movie !== undefined) as Movie[];
        this.loading = false;
      })
      .catch(err => {
        this.error = 'Failed to load favorite movies';
        this.loading = false;
        console.error(err);
      });
  }

  removeFromFavorites(movieId: number): void {
    this.favoritesService.removeFavorite(movieId);
    this.favoriteMovies = this.favoriteMovies.filter(movie => movie.id !== movieId);
  }

  addToWatchLater(movieId: number): void {
    this.favoritesService.addToWatchLater(movieId);
  }

  isInWatchLater(movieId: number): boolean {
    return this.favoritesService.isWatchLater(movieId);
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

  getDefaultPoster(): string {
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="450" viewBox="0 0 300 450"%3E%3Crect width="300" height="450" fill="%23dee2e6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="20" fill="%236c757d"%3ENo Poster%3C/text%3E%3C/svg%3E';
  }
}
