/**
 * Pagination Component
 * Handles page navigation controls
 */

import { ARIA_LABELS } from "../config/constants";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPreviousPage: () => void;
  onNextPage: () => void;
  isLoading: boolean;
}

export function Pagination({
  currentPage,
  totalPages,
  onPreviousPage,
  onNextPage,
  isLoading,
}: PaginationProps) {
  return (
    <div className="offers-pagination">
      <button
        type="button"
        className="page-button"
        onClick={onPreviousPage}
        disabled={isLoading || currentPage <= 1}
        aria-label={ARIA_LABELS.PREVIOUS_PAGE}
      >
        Previous
      </button>

      <span className="page-indicator">
        Page {currentPage} of {totalPages}
      </span>

      <button
        type="button"
        className="page-button"
        onClick={onNextPage}
        disabled={isLoading || currentPage >= totalPages}
        aria-label={ARIA_LABELS.NEXT_PAGE}
      >
        Next
      </button>
    </div>
  );
}
