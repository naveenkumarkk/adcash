/**
 * OffersPage Component
 * Main page for displaying and filtering offers
 */

import { useState, type FormEvent } from "react";
import { useCountries, useInfluencers, useOffers } from "../hooks/useData";
import { clamp } from "../lib/utils";
import { SearchFilters } from "./SearchFilters";
import { StatusMessage } from "./StatusMessage";
import { OffersGrid } from "./OffersGrid";
import { Pagination } from "./Pagination";
import { PAGINATION } from "../config/constants";

export const OffersPage: React.FC = () => {
  // Search state
  const [searchInput, setSearchInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [page, setPage] = useState(PAGINATION.DEFAULT_PAGE);

  // Data hooks
  const {
    countries,
    selectedCountryId,
    setSelectedCountryId,
  } = useCountries();

  const {
    influencers,
    selectedInfluencerId,
    setSelectedInfluencerId,
  } = useInfluencers();

  const {
    offers,
    totalPages,
    isLoading,
    error,
  } = useOffers(searchQuery, selectedCountryId, selectedInfluencerId, page);

  // Event handlers
  const handleSearchSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setPage(PAGINATION.DEFAULT_PAGE);
    setSearchQuery(searchInput.trim());
  };

  const handleCountryChange = (countryId: string) => {
    setSelectedCountryId(countryId);
    setPage(PAGINATION.DEFAULT_PAGE);
  };

  const handleInfluencerChange = (influencerId: string) => {
    setSelectedInfluencerId(influencerId);
    setPage(PAGINATION.DEFAULT_PAGE);
  };

  const handlePreviousPage = () => {
    setPage((prev) => clamp(prev - 1, 1, totalPages));
  };

  const handleNextPage = () => {
    setPage((prev) => clamp(prev + 1, 1, totalPages));
  };

  return (
    <div className="offers-page">
      <SearchFilters
        searchInput={searchInput}
        onSearchInputChange={setSearchInput}
        onSearchSubmit={handleSearchSubmit}
        countries={countries}
        selectedCountryId={selectedCountryId}
        onCountryChange={handleCountryChange}
        influencers={influencers}
        selectedInfluencerId={selectedInfluencerId}
        onInfluencerChange={handleInfluencerChange}
        isLoading={isLoading}
      />

      <StatusMessage
        isLoading={isLoading}
        error={error}
        hasOffers={offers.length > 0}
      />

      {!isLoading && !error && offers.length > 0 && (
        <>
          <OffersGrid offers={offers} />
          <Pagination
            currentPage={page}
            totalPages={totalPages}
            onPreviousPage={handlePreviousPage}
            onNextPage={handleNextPage}
            isLoading={isLoading}
          />
        </>
      )}
    </div>
  );
}
