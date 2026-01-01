import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { DirectorWithMovies } from '../../models/movie.model';

@Component({
  selector: 'app-director-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './director-detail.component.html',
  styleUrls: ['./director-detail.component.css']
})
export class DirectorDetailComponent implements OnInit {
  director: DirectorWithMovies | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadDirector(+id);
    }
  }

  loadDirector(id: number): void {
    this.loading = true;
    this.error = null;
    
    this.movieService.getDirector(id).subscribe({
      next: (director) => {
        this.director = director;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load director details';
        this.loading = false;
        console.error('Error loading director:', err);
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/directors']);
  }

  calculateAge(birthDate: string | undefined): number | null {
    if (!birthDate) return null;
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  }

  getAverageRating(): number | null {
    if (!this.director?.movies || this.director.movies.length === 0) return null;
    const moviesWithRating = this.director.movies.filter(m => m.rating);
    if (moviesWithRating.length === 0) return null;
    const sum = moviesWithRating.reduce((acc, movie) => acc + (movie.rating || 0), 0);
    return Math.round((sum / moviesWithRating.length) * 10) / 10;
  }
}
