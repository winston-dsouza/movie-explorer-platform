import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { ActorWithMovies } from '../../models/movie.model';

@Component({
  selector: 'app-actor-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './actor-detail.component.html',
  styleUrls: ['./actor-detail.component.css']
})
export class ActorDetailComponent implements OnInit {
  actor: ActorWithMovies | null = null;
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
      this.loadActor(+id);
    }
  }

  loadActor(id: number): void {
    this.loading = true;
    this.error = null;
    
    this.movieService.getActor(id).subscribe({
      next: (actor) => {
        this.actor = actor;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load actor details';
        this.loading = false;
        console.error('Error loading actor:', err);
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/actors']);
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
}
