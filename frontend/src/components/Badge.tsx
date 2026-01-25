
import type { BadgeInterface } from "../types"
import styles from './Badge.module.css'

export const Badge = ({ text, filled }: BadgeInterface) => {
    const filledClass = filled ? styles.filled : "";
    return (
        <small className={`${styles.badge} ${filledClass}`}>{text}</small>
    )
}