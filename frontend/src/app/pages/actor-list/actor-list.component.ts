import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MovieService } from '../../services/movie.service';
import { Actor } from '../../models/movie.model';

@Component({
  selector: 'app-actor-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="container py-4">
      <h1 class="mb-4">Actors</h1>
      
      <div class="mb-4">
        <input 
          type="text" 
          class="form-control" 
          placeholder="Search actors..." 
          [(ngModel)]="searchQuery"
          (keyup.enter)="onSearch()">
      </div>

      <div *ngIf="loading" class="text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div class="row g-4" *ngIf="!loading">
        <div *ngFor="let actor of actors" class="col-md-6 col-lg-4">
          <div class="card actor-card h-100">
            <div class="card-body text-center">
              <img 
                [src]="actor.photo_url || getDefaultImage()" 
                class="rounded-circle mb-3" 
                width="120" 
                height="120"
                style="object-fit: cover;"
                [alt]="actor.name">
              <h5 class="card-title">{{ actor.name }}</h5>
              <p class="card-text text-muted" *ngIf="actor.nationality">
                <i class="bi bi-geo-alt me-1"></i>{{ actor.nationality }}
              </p>
              <a [routerLink]="['/actors', actor.id]" class="btn btn-primary btn-sm">
                View Profile
              </a>
            </div>
          </div>
        </div>
      </div>

      <div *ngIf="!loading && actors.length === 0" class="text-center py-5">
        <p class="text-muted">No actors found</p>
      </div>
    </div>
  `
})
export class ActorListComponent implements OnInit {
  actors: Actor[] = [];
  loading = false;
  searchQuery = '';

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.loadActors();
  }

  loadActors(): void {
    this.loading = true;
    if (this.searchQuery) {
      this.movieService.searchActors(this.searchQuery).subscribe({
        next: (actors) => {
          this.actors = actors;
          this.loading = false;
        },
        error: () => this.loading = false
      });
    } else {
      this.movieService.getActors().subscribe({
        next: (actors) => {
          this.actors = actors;
          this.loading = false;
        },
        error: () => this.loading = false
      });
    }
  }

  onSearch(): void {
    this.loadActors();
  }

  getDefaultImage(): string {
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120"%3E%3Crect width="120" height="120" fill="%23dee2e6"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="12" fill="%236c757d"%3ENo Photo%3C/text%3E%3C/svg%3E';
  }
}
