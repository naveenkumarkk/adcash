/**
 * Custom React Hooks
 * Reusable hooks for data fetching and state management
 */

import { useState, useEffect } from "react";
import { fetchCountries, fetchInfluencers, fetchOffers } from "../services/api.service";
import { DEFAULTS, PAGINATION } from "../config/constants";
import type { Country, Influencer, Offer } from "../types";

/**
 * Hook to fetch and manage countries
 */
export function useCountries() {
  const [countries, setCountries] = useState<Country[]>([]);
  const [selectedCountryId, setSelectedCountryId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadCountries() {
      try {
        setIsLoading(true);
        const data = await fetchCountries();
        
        if (isMounted) {
          setCountries(data);

          // Auto-select global country if available
          const globalCountry = data.find((c) => c.code === DEFAULTS.COUNTRY_CODE);
          if (globalCountry) {
            setSelectedCountryId(String(globalCountry.id));
          }
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to fetch countries");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadCountries();

    return () => {
      isMounted = false;
    };
  }, []);

  return {
    countries,
    selectedCountryId,
    setSelectedCountryId,
    isLoading,
    error,
  };
}

/**
 * Hook to fetch and manage influencers
 */
export function useInfluencers() {
  const [influencers, setInfluencers] = useState<Influencer[]>([]);
  const [selectedInfluencerId, setSelectedInfluencerId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadInfluencers() {
      try {
        setIsLoading(true);
        const data = await fetchInfluencers();
        
        if (isMounted) {
          setInfluencers(data);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to fetch influencers");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadInfluencers();

    return () => {
      isMounted = false;
    };
  }, []);

  return {
    influencers,
    selectedInfluencerId,
    setSelectedInfluencerId,
    isLoading,
    error,
  };
}

/**
 * Hook to fetch and manage offers with pagination and filters
 */
export function useOffers(
  searchQuery: string,
  countryId: string,
  influencerId: string,
  page: number
) {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadOffers() {
      try {
        setIsLoading(true);
        setError(null);

        const response = await fetchOffers({
          title: searchQuery,
          countryId,
          influencerId,
          page,
          size: PAGINATION.DEFAULT_PAGE_SIZE,
        });

        if (isMounted) {
          setOffers(response.items);
          setTotalPages(response.pages);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to fetch offers");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadOffers();

    return () => {
      isMounted = false;
    };
  }, [searchQuery, countryId, influencerId, page]);

  return {
    offers,
    totalPages,
    isLoading,
    error,
  };
}
