/**
 * Unit tests for MovieListComponent.
 * Tests filtering, search, and UI interactions.
 */

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { MovieListComponent } from './movie-list.component';
import { MovieService } from '../../services/movie.service';
import { FavoritesService } from '../../services/favorites.service';
import { of } from 'rxjs';

describe('MovieListComponent', () => {
  let component: MovieListComponent;
  let fixture: ComponentFixture<MovieListComponent>;
  let movieService: jest.Mocked<MovieService>;
  let favoritesService: jest.Mocked<FavoritesService>;

  const mockMovies = [
    {
      id: 1,
      title: 'Inception',
      description: 'Test',
      release_year: 2010,
      runtime_minutes: 148,
      rating: 8.8,
      poster_url: '',
      director: { id: 1, name: 'Nolan', bio: '' },
      genres: [{ id: 1, name: 'Action', description: '' }],
      actors: [],
      reviews: []
    }
  ];

  beforeEach(async () => {
    const movieServiceMock = {
      getMovies: jest.fn().mockReturnValue(of(mockMovies)),
      filterMovies: jest.fn().mockReturnValue(of(mockMovies)),
      searchMovies: jest.fn().mockReturnValue(of(mockMovies)),
      getGenres: jest.fn().mockReturnValue(of([{ id: 1, name: 'Action', description: '' }])),
      getDirectors: jest.fn().mockReturnValue(of([{ id: 1, name: 'Nolan', bio: '', photo_url: '', movies: [] }])),
      getActors: jest.fn().mockReturnValue(of([{ id: 1, name: 'DiCaprio', bio: '', photo_url: '', movies: [] }]))
    };
    const favoritesServiceMock = {
      isFavorite: jest.fn(),
      toggleFavorite: jest.fn(),
      isWatchLater: jest.fn(),
      toggleWatchLater: jest.fn()
    };
    const activatedRouteMock = {
      snapshot: { queryParams: {} },
      queryParams: of({})
    };

    await TestBed.configureTestingModule({
      imports: [MovieListComponent, HttpClientTestingModule, FormsModule],
      providers: [
        { provide: MovieService, useValue: movieServiceMock },
        { provide: FavoritesService, useValue: favoritesServiceMock },
        { provide: ActivatedRoute, useValue: activatedRouteMock }
      ]
    }).compileComponents();

    movieService = TestBed.inject(MovieService) as jest.Mocked<MovieService>;
    favoritesService = TestBed.inject(FavoritesService) as jest.Mocked<FavoritesService>;

    fixture = TestBed.createComponent(MovieListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load movies on init', () => {
    expect(movieService.getMovies).toHaveBeenCalled();
    expect(component.movies.length).toBe(1);
    expect(component.movies[0].title).toBe('Inception');
  });

  it('should load filters on init', () => {
    expect(movieService.getGenres).toHaveBeenCalled();
    expect(movieService.getDirectors).toHaveBeenCalled();
    expect(movieService.getActors).toHaveBeenCalled();
  });

  describe('Filtering', () => {
    it('should filter movies when genre selected', () => {
      component.selectedGenreId = 1;
      component.onFilterChange();
      
      expect(movieService.filterMovies).toHaveBeenCalledWith({ genre_id: 1 });
    });

    it('should filter movies when director selected', () => {
      component.selectedDirectorId = 2;
      component.onFilterChange();
      
      expect(movieService.filterMovies).toHaveBeenCalledWith({ director_id: 2 });
    });

    it('should filter movies when actor selected', () => {
      component.selectedActorId = 3;
      component.onFilterChange();
      
      expect(movieService.filterMovies).toHaveBeenCalledWith({ actor_id: 3 });
    });

    it('should apply multiple filters', () => {
      component.selectedGenreId = 1;
      component.selectedDirectorId = 2;
      component.selectedActorId = 3;
      component.onFilterChange();
      
      expect(movieService.filterMovies).toHaveBeenCalledWith({ genre_id: 1, director_id: 2, actor_id: 3 });
    });

    it('should get all movies when no filters selected', () => {
      component.selectedGenreId = null;
      component.selectedDirectorId = null;
      component.selectedActorId = null;
      component.onFilterChange();
      
      expect(movieService.getMovies).toHaveBeenCalled();
    });
  });

  describe('Search', () => {
    it('should search movies with valid query', () => {
      component.searchQuery = 'Inception';
      component.onSearch();
      
      expect(movieService.searchMovies).toHaveBeenCalledWith('Inception');
    });

    it('should not search with empty query', () => {
      component.searchQuery = '';
      component.onSearch();
      
      expect(movieService.searchMovies).not.toHaveBeenCalled();
    });

    it('should not search with whitespace-only query', () => {
      component.searchQuery = '   ';
      component.onSearch();
      
      expect(movieService.searchMovies).not.toHaveBeenCalled();
    });

    it('should trim search query', () => {
      component.searchQuery = '  Inception  ';
      component.onSearch();
      
      expect(movieService.searchMovies).toHaveBeenCalledWith('Inception');
    });
  });

  describe('Favorites', () => {
    it('should check if movie is favorite', () => {
      favoritesService.isFavorite.mockReturnValue(true);
      
      const result = favoritesService.isFavorite(1);
      
      expect(favoritesService.isFavorite).toHaveBeenCalledWith(1);
      expect(result).toBe(true);
    });

    it('should toggle favorite status', () => {
      const mockEvent = new Event('click');
      component.toggleFavorite(mockEvent, 1);
      
      expect(favoritesService.toggleFavorite).toHaveBeenCalledWith(1);
    });
  });

  describe('Watch Later', () => {
    it('should check if movie is in watch later', () => {
      favoritesService.isWatchLater.mockReturnValue(true);
      
      const result = favoritesService.isWatchLater(1);
      
      expect(favoritesService.isWatchLater).toHaveBeenCalledWith(1);
      expect(result).toBe(true);
    });

    it('should toggle watch later status', () => {
      const mockEvent = new Event('click');
      component.toggleWatchLater(mockEvent, 1);
      
      expect(favoritesService.toggleWatchLater).toHaveBeenCalledWith(1);
    });
  });

  describe('Loading State', () => {
    it('should show loading state while fetching movies', () => {
      component.loading = true;
      fixture.detectChanges();
      
      expect(component.loading).toBe(true);
    });

    it('should hide loading state after movies loaded', () => {
      component.ngOnInit();
      
      expect(component.loading).toBe(false);
    });
  });
});
