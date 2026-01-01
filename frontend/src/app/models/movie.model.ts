export interface Genre {
  id: number;
  name: string;
  description?: string;
}

export interface Director {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  photo_url?: string;
  nationality?: string;
}

export interface Actor {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  photo_url?: string;
  nationality?: string;
}

export interface Review {
  id: number;
  movie_id: number;
  reviewer_name: string;
  rating: number;
  comment?: string;
  created_at?: string;
}

export interface Movie {
  id: number;
  title: string;
  release_year: number;
  description?: string;
  poster_url?: string;
  rating?: number;
  runtime_minutes?: number;
  director?: Director;
  genres: Genre[];
  actors?: Actor[];
  reviews?: Review[];
}

export interface MovieCreate {
  title: string;
  release_year: number;
  description?: string;
  poster_url?: string;
  rating?: number;
  runtime_minutes?: number;
  director_id?: number;
  genre_ids: number[];
  actor_ids: number[];
}

export interface ActorWithMovies extends Actor {
  movies: Movie[];
}

export interface DirectorWithMovies extends Director {
  movies: Movie[];
}

export interface FilterOptions {
  genre_id?: number;
  director_id?: number;
  release_year?: number;
  actor_id?: number;
}
