/**
 * API Service Layer
 * Handles all HTTP requests and API communication
 */

import { API_CONFIG } from "../config/constants";
import type { Country, Influencer, Offer, PaginatedResponse } from "../types";

/**
 * Base fetch wrapper with error handling
 */
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error);
    throw error;
  }
}

/**
 * Fetch all countries
 */
export async function fetchCountries(): Promise<Country[]> {
  const data = await apiFetch<Country[] | { items: Country[] }>("/country/all");
  return Array.isArray(data) ? data : data?.items || [];
}

/**
 * Fetch all influencers
 */
export async function fetchInfluencers(): Promise<Influencer[]> {
  const data = await apiFetch<Influencer[] | { items: Influencer[] }>("/influencer/all");
  return Array.isArray(data) ? data : data?.items || [];
}

/**
 * Fetch offers with filters
 */
export async function fetchOffers(params: {
  title?: string;
  countryId?: string;
  influencerId?: string;
  page?: number;
  size?: number;
}): Promise<PaginatedResponse<Offer>> {
  const searchParams = new URLSearchParams();
  
  if (params.title) searchParams.set("title", params.title);
  if (params.countryId) searchParams.set("country", params.countryId);
  if (params.influencerId) searchParams.set("influencer_id", params.influencerId);
  if (params.page) searchParams.set("page", String(params.page));
  if (params.size) searchParams.set("size", String(params.size));

  const endpoint = `/offers/all?${searchParams.toString()}`;
  const data = await apiFetch<any>(endpoint);

  // Normalize response
  const items = Array.isArray(data) ? data : data?.items || [];
  const pages = typeof data === "object" && data ? (data as any).pages : 1;

  return {
    items,
    pages: Math.max(1, pages),
    total: items.length,
    page: params.page || 1,
    size: params.size || 12,
  };
}
