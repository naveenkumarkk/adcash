import type { BadgeData, Category } from "../types/index";
export function categoriesToBadges(categories: Category[]): BadgeData[] {
  return categories.map((cat) => ({
    text: cat.name,
    filled: true,
  }));
}

export function getPayoutIndicator(payoutType: string): string | false {
  return payoutType === "CUSTOM" ? "Custom" : false;
}

export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

export function formatErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === "string") {
    return error;
  }
  return "An unknown error occurred";
}
