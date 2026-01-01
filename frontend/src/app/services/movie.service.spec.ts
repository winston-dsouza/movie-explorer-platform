/**
 * Unit tests for MovieService.
 * Tests HTTP API calls, filtering, search, and error handling.
 */

import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { MovieService } from './movie.service';
import { Movie } from '../models/movie.model';

describe('MovieService', () => {
  let service: MovieService;
  let httpMock: HttpTestingController;
  const apiUrl = 'http://localhost:8000/api';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [MovieService]
    });
    service = TestBed.inject(MovieService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getMovies', () => {
    it('should fetch all movies', () => {
      const mockMovies: Movie[] = [
        {
          id: 1,
          title: 'Inception',
          description: 'A thief who steals corporate secrets',
          release_year: 2010,
          runtime_minutes: 148,
          rating: 8.8,
          poster_url: 'https://example.com/inception.jpg',
          director: { id: 1, name: 'Christopher Nolan', bio: '' },
          genres: [],
          actors: [],
          reviews: []
        }
      ];

      service.getMovies().subscribe(movies => {
        expect(movies.length).toBe(1);
        expect(movies[0].title).toBe('Inception');
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies` && 
          request.params.get('skip') === '0' && 
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush(mockMovies);
    });

    it('should handle empty movie list', () => {
      service.getMovies().subscribe(movies => {
        expect(movies).toEqual([]);
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies` && 
          request.params.get('skip') === '0' && 
          request.params.get('limit') === '100'
      );
      req.flush([]);
    });
  });

  describe('getMovie', () => {
    it('should fetch a single movie by id', () => {
      const mockMovie: Movie = {
        id: 1,
        title: 'Inception',
        description: 'Test',
        release_year: 2010,
        runtime_minutes: 148,
        rating: 8.8,
        poster_url: '',
        director: { id: 1, name: 'Nolan', bio: '' },
        genres: [],
        actors: [],
        reviews: []
      };

      service.getMovie(1).subscribe(movie => {
        expect(movie.id).toBe(1);
        expect(movie.title).toBe('Inception');
      });

      const req = httpMock.expectOne(`${apiUrl}/movies/1`);
      expect(req.request.method).toBe('GET');
      req.flush(mockMovie);
    });
  });

  describe('filterMovies', () => {
    it('should apply genre filter', () => {
      service.filterMovies({ genre_id: 1 }).subscribe();

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/filter` && 
          request.params.get('genre_id') === '1' &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush([]);
    });

    it('should apply director filter', () => {
      service.filterMovies({ director_id: 2 }).subscribe();

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/filter` && 
          request.params.get('director_id') === '2' &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush([]);
    });

    it('should apply actor filter', () => {
      service.filterMovies({ actor_id: 3 }).subscribe();

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/filter` && 
          request.params.get('actor_id') === '3' &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush([]);
    });

    it('should apply multiple filters', () => {
      service.filterMovies({ genre_id: 1, director_id: 2, actor_id: 3 }).subscribe();

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/filter` &&
          request.params.get('genre_id') === '1' &&
          request.params.get('director_id') === '2' &&
          request.params.get('actor_id') === '3' &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush([]);
    });

    it('should not add null filters to query params', () => {
      service.filterMovies({}).subscribe();

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/filter` &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.params.keys().length).toBe(2); // skip and limit only
      req.flush([]);
    });
  });

  describe('searchMovies', () => {
    it('should search movies by query', () => {
      const mockResults: Movie[] = [
        {
          id: 1,
          title: 'Inception',
          description: '',
          release_year: 2010,
          runtime_minutes: 148,
          rating: 8.8,
          poster_url: '',
          director: { id: 1, name: 'Nolan', bio: '' },
          genres: [],
          actors: [],
          reviews: []
        }
      ];

      service.searchMovies('Inception').subscribe(movies => {
        expect(movies.length).toBe(1);
        expect(movies[0].title).toBe('Inception');
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/search` && 
          request.params.get('q') === 'Inception' &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush(mockResults);
    });

    it('should handle empty search results', () => {
      service.searchMovies('NonexistentMovie').subscribe(movies => {
        expect(movies).toEqual([]);
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/movies/search`
      );
      req.flush([]);
    });
  });

  describe('getGenres', () => {
    it('should fetch all genres', () => {
      const mockGenres = [
        { id: 1, name: 'Action', description: 'Action movies' },
        { id: 2, name: 'Drama', description: 'Drama movies' }
      ];

      service.getGenres().subscribe(genres => {
        expect(genres.length).toBe(2);
        expect(genres[0].name).toBe('Action');
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/genres` &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush(mockGenres);
    });
  });

  describe('getActors', () => {
    it('should fetch all actors', () => {
      const mockActors = [
        { id: 1, name: 'Tom Hanks', bio: '', photo_url: '', movies: [] }
      ];

      service.getActors().subscribe(actors => {
        expect(actors.length).toBe(1);
        expect(actors[0].name).toBe('Tom Hanks');
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/actors` &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush(mockActors);
    });
  });

  describe('getDirectors', () => {
    it('should fetch all directors', () => {
      const mockDirectors = [
        { id: 1, name: 'Christopher Nolan', bio: '', photo_url: '', movies: [] }
      ];

      service.getDirectors().subscribe(directors => {
        expect(directors.length).toBe(1);
        expect(directors[0].name).toBe('Christopher Nolan');
      });

      const req = httpMock.expectOne(
        request => request.url === `${apiUrl}/directors` &&
          request.params.get('skip') === '0' &&
          request.params.get('limit') === '100'
      );
      expect(req.request.method).toBe('GET');
      req.flush(mockDirectors);
    });
  });
});
