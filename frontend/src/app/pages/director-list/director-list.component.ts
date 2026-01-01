import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { Director } from '../../models/movie.model';

@Component({
  selector: 'app-director-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './director-list.component.html',
  styleUrls: ['./director-list.component.css']
})
export class DirectorListComponent implements OnInit {
  directors: Director[] = [];
  filteredDirectors: Director[] = [];
  loading = true;
  error: string | null = null;
  searchTerm = '';

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.loadDirectors();
  }

  loadDirectors(): void {
    this.loading = true;
    this.error = null;
    
    this.movieService.getDirectors().subscribe({
      next: (directors) => {
        this.directors = directors;
        this.filteredDirectors = directors;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load directors';
        this.loading = false;
        console.error('Error loading directors:', err);
      }
    });
  }

  searchDirectors(): void {
    if (!this.searchTerm.trim()) {
      this.filteredDirectors = this.directors;
      return;
    }

    this.loading = true;
    this.movieService.searchDirectors(this.searchTerm).subscribe({
      next: (directors) => {
        this.filteredDirectors = directors;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Search failed';
        this.loading = false;
        console.error('Search error:', err);
      }
    });
  }

  clearSearch(): void {
    this.searchTerm = '';
    this.filteredDirectors = this.directors;
  }
}
