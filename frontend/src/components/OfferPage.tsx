import { useEffect, useState } from "react"
import { Card } from "./Card"
import type { Offer } from "../types"

export const OffersPage: React.FC = () => {
    const [offers, setOffers] = useState<Offer[]>([])
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)
    useEffect(() => {
        const fetchOffers = async () => {
            try {
                const res = await fetch("http://localhost:8000/api/offers/all")
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)

                const data: Offer[] = await res.json()
                console.log("Fetched offers:", data) 
                setOffers(data)
            } catch (err: any) {
                console.error("Fetch error:", err)
                setError(err.message || "Unknown error")
            } finally {
                setLoading(false)
            }
        }

        fetchOffers()
    }, [])

    if (loading) return <div>Loading offers...</div>
    if (!offers.length) return <div>No offers available</div>

    return (
        <div className="card-container">
            {offers.map((offer) => (
                <Card
                    key={offer.id}
                    title={offer.title}
                    body={offer.description}
                    image={offer.image_url}
                    payoutType={offer.payout_type}
                    amount={offer.amount}
                    category_badges={[
                        ...offer.categories.map(cat => ({ text: cat.name, filled: true }))
                    ]}
                    // indicator={offer.payout_type}
        
                />
            ))}
        </div>
    )
}
