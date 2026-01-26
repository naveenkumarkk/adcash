/**
 * Utility Functions
 * Reusable helper functions for the application
 */

import type { BadgeData, Category } from "../types";

/**
 * Convert categories to badge data
 */
export function categoriesToBadges(categories: Category[]): BadgeData[] {
  return categories.map((cat) => ({
    text: cat.name,
    filled: true,
  }));
}

/**
 * Determine payout indicator text
 */
export function getPayoutIndicator(payoutType: string): string | false {
  return payoutType === "CUSTOM" ? "custom" : false;
}

/**
 * Safely clamp a value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

/**
 * Format error message for display
 */
export function formatErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === "string") {
    return error;
  }
  return "An unknown error occurred";
}
