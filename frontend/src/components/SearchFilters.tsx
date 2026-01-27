import type { FormEvent } from "react";
import { ARIA_LABELS, DEFAULTS } from "../config/constants";
import type { Country, Influencer } from "../types/index";

interface SearchFiltersProps {
  searchInput: string;
  onSearchInputChange: (value: string) => void;
  onSearchSubmit: (event: FormEvent<HTMLFormElement>) => void;
  countries: Country[];
  selectedCountryId: string;
  onCountryChange: (countryId: string) => void;
  influencers: Influencer[];
  selectedInfluencerId: string;
  onInfluencerChange: (influencerId: string) => void;
  isLoading: boolean;
}

export function SearchFilters({
  searchInput,
  onSearchInputChange,
  onSearchSubmit,
  countries,
  selectedCountryId,
  onCountryChange,
  influencers,
  selectedInfluencerId,
  onInfluencerChange,
  isLoading,
}: SearchFiltersProps) {
  return (
    <form className="offers-search" onSubmit={onSearchSubmit}>
      <input
        className="search-input"
        type="text"
        placeholder="Search offers by title..."
        value={searchInput}
        onChange={(e) => onSearchInputChange(e.target.value)}
        aria-label={ARIA_LABELS.SEARCH_INPUT}
      />

      <select
        className="country-select"
        value={selectedCountryId}
        onChange={(e) => onCountryChange(e.target.value)}
        aria-label={ARIA_LABELS.COUNTRY_FILTER}
      >
        <option value="">All Countries</option>
        {countries.map((country) => (
          <option key={country.id} value={String(country.id)}>
            {country.code}
          </option>
        ))}
      </select>

      <select
        className="influencer-select"
        value={selectedInfluencerId}
        onChange={(e) => onInfluencerChange(e.target.value)}
        aria-label={ARIA_LABELS.INFLUENCER_FILTER}
      >
        <option value="">{DEFAULTS.EMPTY_OPTION_TEXT}</option>
        {influencers.map((influencer) => (
          <option key={influencer.id} value={String(influencer.id)}>
            {influencer.name}
          </option>
        ))}
      </select>

      <button className="search-button" type="submit" disabled={isLoading}>
        Search
      </button>
    </form>
  );
}
