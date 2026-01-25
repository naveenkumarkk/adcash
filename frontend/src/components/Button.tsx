import type { ButtonInterface } from "../types"
import styles from './Button.module.css'

export const Button = ({ text, filled, type, href, icon: Icon }: ButtonInterface) => {
    const filledClass = filled ? styles.filled : ""

    return (
        <a href={href} className={`${styles.btn} ${styles[type]} ${filledClass}`}>
            {Icon && <Icon className={styles.icon} />}
            <span>{text}</span>
        </a>
    )
}
