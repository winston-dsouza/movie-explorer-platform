/**
 * Unit tests for FavoritesService.
 * Tests localStorage operations, favorites and watch later management.
 */

import { TestBed } from '@angular/core/testing';
import { FavoritesService } from './favorites.service';

describe('FavoritesService', () => {
  let service: FavoritesService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [FavoritesService]
    });
    service = TestBed.inject(FavoritesService);
    // Clear localStorage before each test
    localStorage.clear();
    jest.clearAllMocks();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('Favorites Management', () => {
    it('should add movie to favorites', () => {
      service.addFavorite(1);
      expect(service.isFavorite(1)).toBe(true);
    });

    it('should remove movie from favorites', () => {
      service.addFavorite(1);
      service.removeFavorite(1);
      expect(service.isFavorite(1)).toBe(false);
    });

    it('should toggle favorite status', () => {
      service.toggleFavorite(1);
      expect(service.isFavorite(1)).toBe(true);
      
      service.toggleFavorite(1);
      expect(service.isFavorite(1)).toBe(false);
    });

    it('should get all favorites', () => {
      service.addFavorite(1);
      service.addFavorite(2);
      service.addFavorite(3);

      const favorites = service.getFavoriteIds();
      expect(favorites.length).toBe(3);
      expect(favorites).toContain(1);
      expect(favorites).toContain(2);
      expect(favorites).toContain(3);
    });

    it('should return empty array when no favorites', () => {
      const favorites = service.getFavoriteIds();
      expect(favorites).toEqual([]);
    });

    it('should not add duplicate favorites', () => {
      service.addFavorite(1);
      service.addFavorite(1);
      
      const favorites = service.getFavoriteIds();
      expect(favorites.length).toBe(1);
    });

    it('should persist favorites in localStorage', () => {
      service.addFavorite(1);
      
      // Create new service instance to test persistence
      const newService = new FavoritesService();
      expect(newService.isFavorite(1)).toBe(true);
    });
  });

  describe('Watch Later Management', () => {
    it('should add movie to watch later', () => {
      service.addToWatchLater(1);
      expect(service.isWatchLater(1)).toBe(true);
    });

    it('should remove movie from watch later', () => {
      service.addToWatchLater(1);
      service.removeFromWatchLater(1);
      expect(service.isWatchLater(1)).toBe(false);
    });

    it('should toggle watch later status', () => {
      service.toggleWatchLater(1);
      expect(service.isWatchLater(1)).toBe(true);
      
      service.toggleWatchLater(1);
      expect(service.isWatchLater(1)).toBe(false);
    });

    it('should get all watch later movies', () => {
      service.addToWatchLater(1);
      service.addToWatchLater(2);

      const watchLater = service.getWatchLaterIds();
      expect(watchLater.length).toBe(2);
      expect(watchLater).toContain(1);
      expect(watchLater).toContain(2);
    });

    it('should return empty array when no watch later movies', () => {
      const watchLater = service.getWatchLaterIds();
      expect(watchLater).toEqual([]);
    });

    it('should not add duplicate watch later movies', () => {
      service.addToWatchLater(1);
      service.addToWatchLater(1);
      
      const watchLater = service.getWatchLaterIds();
      expect(watchLater.length).toBe(1);
    });

    it('should persist watch later in localStorage', () => {
      service.addToWatchLater(1);
      
      // Create new service instance to test persistence
      const newService = new FavoritesService();
      expect(newService.isWatchLater(1)).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    it('should handle invalid movie IDs gracefully', () => {
      service.addFavorite(-1);
      service.addFavorite(0);
      
      expect(service.isFavorite(-1)).toBe(true);
      expect(service.isFavorite(0)).toBe(true);
    });

    it('should handle removing non-existent favorite', () => {
      expect(() => service.removeFavorite(999)).not.toThrow();
      expect(service.isFavorite(999)).toBe(false);
    });

    it('should handle corrupted localStorage data', () => {
      localStorage.setItem('favorites', 'invalid json');
      
      const newService = new FavoritesService();
      expect(newService.getFavoriteIds()).toEqual([]);
    });

    it('should maintain separate favorites and watch later lists', () => {
      service.addFavorite(1);
      service.addToWatchLater(1);

      expect(service.isFavorite(1)).toBe(true);
      expect(service.isWatchLater(1)).toBe(true);

      service.removeFavorite(1);
      expect(service.isFavorite(1)).toBe(false);
      expect(service.isWatchLater(1)).toBe(true);
    });
  });
});
