import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FavoritesService {
  private readonly STORAGE_KEY = 'movie_favorites';
  private readonly WATCH_LATER_KEY = 'watch_later';
  
  private favoritesSubject = new BehaviorSubject<number[]>(this.loadFavorites());
  private watchLaterSubject = new BehaviorSubject<number[]>(this.loadWatchLater());
  
  favorites$ = this.favoritesSubject.asObservable();
  watchLater$ = this.watchLaterSubject.asObservable();

  constructor() {}

  private loadFavorites(): number[] {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  }

  private loadWatchLater(): number[] {
    const stored = localStorage.getItem(this.WATCH_LATER_KEY);
    return stored ? JSON.parse(stored) : [];
  }

  private saveFavorites(favorites: number[]): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
    this.favoritesSubject.next(favorites);
  }

  private saveWatchLater(watchLater: number[]): void {
    localStorage.setItem(this.WATCH_LATER_KEY, JSON.stringify(watchLater));
    this.watchLaterSubject.next(watchLater);
  }

  isFavorite(movieId: number): boolean {
    return this.favoritesSubject.value.includes(movieId);
  }

  isWatchLater(movieId: number): boolean {
    return this.watchLaterSubject.value.includes(movieId);
  }

  toggleFavorite(movieId: number): void {
    const currentFavorites = this.favoritesSubject.value;
    const index = currentFavorites.indexOf(movieId);
    
    if (index > -1) {
      currentFavorites.splice(index, 1);
    } else {
      currentFavorites.push(movieId);
    }
    
    this.saveFavorites(currentFavorites);
  }

  toggleWatchLater(movieId: number): void {
    const currentWatchLater = this.watchLaterSubject.value;
    const index = currentWatchLater.indexOf(movieId);
    
    if (index > -1) {
      currentWatchLater.splice(index, 1);
    } else {
      currentWatchLater.push(movieId);
    }
    
    this.saveWatchLater(currentWatchLater);
  }

  getFavoriteIds(): number[] {
    return this.favoritesSubject.value;
  }

  getWatchLaterIds(): number[] {
    return this.watchLaterSubject.value;
  }

  clearFavorites(): void {
    this.saveFavorites([]);
  }

  clearWatchLater(): void {
    this.saveWatchLater([]);
  }

  addFavorite(movieId: number): void {
    const currentFavorites = this.favoritesSubject.value;
    if (!currentFavorites.includes(movieId)) {
      currentFavorites.push(movieId);
      this.saveFavorites(currentFavorites);
    }
  }

  removeFavorite(movieId: number): void {
    const currentFavorites = this.favoritesSubject.value;
    const index = currentFavorites.indexOf(movieId);
    if (index > -1) {
      currentFavorites.splice(index, 1);
      this.saveFavorites(currentFavorites);
    }
  }

  addToWatchLater(movieId: number): void {
    const currentWatchLater = this.watchLaterSubject.value;
    if (!currentWatchLater.includes(movieId)) {
      currentWatchLater.push(movieId);
      this.saveWatchLater(currentWatchLater);
    }
  }

  removeFromWatchLater(movieId: number): void {
    const currentWatchLater = this.watchLaterSubject.value;
    const index = currentWatchLater.indexOf(movieId);
    if (index > -1) {
      currentWatchLater.splice(index, 1);
      this.saveWatchLater(currentWatchLater);
    }
  }
}
