/**
 * StatusMessage Component
 * Displays loading, error, or empty state messages
 */

import { STATUS_MESSAGES } from "../config/constants";

interface StatusMessageProps {
  isLoading: boolean;
  error: string | null;
  hasOffers: boolean;
}

export function StatusMessage({ isLoading, error, hasOffers }: StatusMessageProps) {
  if (isLoading) {
    return <div className="status-message">{STATUS_MESSAGES.LOADING}</div>;
  }

  if (error) {
    return (
      <div className="status-message error">
        {STATUS_MESSAGES.ERROR_PREFIX}
        {error}
      </div>
    );
  }

  if (!hasOffers) {
    return <div className="status-message">{STATUS_MESSAGES.NO_OFFERS}</div>;
  }

  return null;
}
