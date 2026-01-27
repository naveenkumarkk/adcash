import type { BadgeProps } from "../types/index";
import styles from "./Badge.module.css";

export function Badge({ text, filled = false }: BadgeProps) {
  const filledClass = filled ? styles.filled : "";
  
  return (
    <small className={`${styles.badge} ${filledClass}`}>
      {text}
    </small>
  );
}