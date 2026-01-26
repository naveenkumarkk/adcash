/**
 * Badge Component
 * Displays a badge with optional filled state
 */

import type { BadgeProps } from "../types";
import styles from "./Badge.module.css";

export function Badge({ text, filled = false }: BadgeProps) {
  const filledClass = filled ? styles.filled : "";
  
  return (
    <small className={`${styles.badge} ${filledClass}`}>
      {text}
    </small>
  );
}