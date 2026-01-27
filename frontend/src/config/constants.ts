
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  TIMEOUT: 30000, // 30 seconds
} as const;

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 12,
  DEFAULT_PAGE: 1,
} as const;

export const DEFAULTS = {
  COUNTRY_CODE: "GLB",
  EMPTY_OPTION_TEXT: "---",
} as const;

export const STATUS_MESSAGES = {
  LOADING: "Loading offers...",
  NO_OFFERS: "No offers available",
  ERROR_PREFIX: "Error: ",
} as const;

export const ARIA_LABELS = {
  SEARCH_INPUT: "Search offers",
  COUNTRY_FILTER: "Filter by country",
  INFLUENCER_FILTER: "Filter by Influencer",
  PREVIOUS_PAGE: "Previous page",
  NEXT_PAGE: "Next page",
} as const;
