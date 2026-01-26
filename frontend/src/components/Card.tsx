/**
 * Card Component
 * Displays an offer card with details and badges
 */

import type { CardProps, BadgeData } from "../types";
import { Badge } from "./Badge";
import styles from "./Card.module.css";

export function Card({
  title,
  body,
  image,
  categoryBadges,
  payoutType,
  amount,
  indicator,
}: CardProps) {
  return (
    <article className={`stack-sm ${styles.card}`}>
      {indicator && <small className={styles.indicator}>{indicator}</small>}
      
      {image && <img src={image} alt={title} className={styles.image} />}
      
      <h3 className={styles.title}>{title}</h3>
      <p className={styles.body}>{body}</p>

      {payoutType && (
        <small className={styles.subtitle}>
          <strong>Payout Type:</strong> <Badge text={payoutType} />
        </small>
      )}

      {amount && (
        <small className={styles.subtitle}>
          <strong>Amount:</strong> {amount}
        </small>
      )}

      {categoryBadges && categoryBadges.length > 0 && (
        <div className={styles.badgeRow}>
          {categoryBadges.map((badge: BadgeData, index: number) => (
            <Badge key={index} text={badge.text} filled={badge.filled} />
          ))}
        </div>
      )}
    </article>
  );
}
