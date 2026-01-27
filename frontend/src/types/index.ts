export interface BadgeProps {
  text: string;
  filled?: boolean;
}

export interface CardProps {
  title: string;
  body: string;
  categoryBadges?: BadgeData[];
  payoutType?: string;
  amount?: string;
  image?: string;
  indicator: string | boolean;
}

export interface Category {
  id?: number;
  name: string;
}

export interface Country {
  id: number;
  code: string;
}

export interface Influencer {
  id: string;
  name: string;
}

export interface Offer {
  id: number;
  title: string;
  description: string;
  image_url?: string;
  categories: Category[];
  payout_type: string;
  amount: string;
}

export interface BadgeData {
  text: string;
  filled: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiError {
  message: string;
  status?: number;
}


export interface OfferFilters {
  title?: string;
  countryId?: string;
  influencerId?: string;
  page?: number;
  size?: number;
}
