import type { Key } from "react"
import type { CardInterface } from "../types"
import { Badge } from "./Badge"
import { Button } from "./Button"
import styles from './Card.module.css'

export const Card: React.FC<CardInterface> = ({
    title,
    body,
    image,
    category_badges,
    payoutType,
    amount,
    // indicator 
}) => {
    return (
        <article className={`stack-sm ${styles.card}`}>
            {/* {indicator && <small className={styles.indicator}>{indicator}</small>} */}
            {image && <img src={image} alt={title} className={styles.image} />}
            <h3 className={styles.title}>{title}</h3>
            <p className={styles.body}>{body}</p>
            {(payoutType) && (
                <small className={styles.subtitle}>
                    <strong>Payout Type:</strong>{" "}
                    <Badge text={payoutType}></Badge>

                </small>
            )}
            {
                (amount) && (
                    <small className={styles.subtitle}>
                        <strong>Amount:</strong>{" "}{amount}
                    </small>
                )
            }

            {category_badges && (
                <div className={styles.badgeRow}>
                    {category_badges.map((b: { text: String; filled: Boolean | undefined }, i: Key | null | undefined) => (
                        <Badge key={i} text={b.text} filled={b.filled} />
                    ))}
                </div>
            )}
        </article>
    )
}
