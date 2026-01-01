import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { FavoritesService } from '../../services/favorites.service';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './movie-detail.component.html',
  styleUrls: ['./movie-detail.component.css']
})
export class MovieDetailComponent implements OnInit {
  movie: Movie | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private movieService: MovieService,
    public favoritesService: FavoritesService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadMovie(+id);
    }
  }

  loadMovie(id: number): void {
    this.movieService.getMovie(id).subscribe({
      next: (movie) => {
        this.movie = movie;
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load movie details';
        this.loading = false;
        console.error('Error loading movie:', error);
      }
    });
  }

  toggleFavorite(): void {
    if (this.movie) {
      this.favoritesService.toggleFavorite(this.movie.id);
    }
  }

  toggleWatchLater(): void {
    if (this.movie) {
      this.favoritesService.toggleWatchLater(this.movie.id);
    }
  }

  getDefaultPoster(): string {
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600"%3E%3Crect width="400" height="600" fill="%23dee2e6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="24" fill="%236c757d"%3ENo Poster%3C/text%3E%3C/svg%3E';
  }

  getDefaultProfileImage(): string {
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150"%3E%3Crect width="150" height="150" fill="%23dee2e6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="14" fill="%236c757d"%3ENo Image%3C/text%3E%3C/svg%3E';
  }
}
