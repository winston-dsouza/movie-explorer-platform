import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/movies', pathMatch: 'full' },
  { 
    path: 'movies', 
    loadComponent: () => import('./pages/movie-list/movie-list.component').then(m => m.MovieListComponent)
  },
  { 
    path: 'movies/:id', 
    loadComponent: () => import('./pages/movie-detail/movie-detail.component').then(m => m.MovieDetailComponent)
  },
  { 
    path: 'actors', 
    loadComponent: () => import('./pages/actor-list/actor-list.component').then(m => m.ActorListComponent)
  },
  { 
    path: 'actors/:id', 
    loadComponent: () => import('./pages/actor-detail/actor-detail.component').then(m => m.ActorDetailComponent)
  },
  { 
    path: 'directors', 
    loadComponent: () => import('./pages/director-list/director-list.component').then(m => m.DirectorListComponent)
  },
  { 
    path: 'directors/:id', 
    loadComponent: () => import('./pages/director-detail/director-detail.component').then(m => m.DirectorDetailComponent)
  },
  { 
    path: 'favorites',
    loadComponent: () => import('./pages/favorites/favorites.component').then(m => m.FavoritesComponent)
  },
  { 
    path: 'watch-later', 
    loadComponent: () => import('./pages/watch-later/watch-later.component').then(m => m.WatchLaterComponent)
  },
  { path: '**', redirectTo: '/movies' }
];
