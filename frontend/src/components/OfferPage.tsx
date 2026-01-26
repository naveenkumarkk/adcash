import { useEffect, useState, type FormEvent } from "react"
import { Card } from "./Card"
import type { Offer, Country } from "../types"

export const OffersPage: React.FC = () => {
    const [offers, setOffers] = useState<Offer[]>([])
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)
    const [searchInput, setSearchInput] = useState<string>("")
    const [query, setQuery] = useState<string>("")
    const [page, setPage] = useState<number>(1)
    const [totalPages, setTotalPages] = useState<number>(1)
    const [countries, setCountries] = useState<Country[]>([])
    const [selectedCountry, setSelectedCountry] = useState<string>("")

    const fetchCountries = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/country/all")
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
            const data = await res.json()
            const normalizedCountries = Array.isArray(data) ? data : (data?.items || [])
            setCountries(normalizedCountries)
            
            // Find and select GLB country
            const glbCountry = normalizedCountries.find((c: Country) => c.code === "GLB")
            if (glbCountry) {
                setSelectedCountry(String(glbCountry.id))
            }
        } catch (err: any) {
            console.error("Fetch countries error:", err)
        }
    }

    const fetchOffers = async (currentQuery: string = "", targetPage: number = 1, countryId: string = "") => {
        setLoading(true)
        setError(null)
        const normalizeOffers = (payload: unknown): Offer[] => {
            if (Array.isArray(payload)) return payload
            if (payload && typeof payload === "object") {
                const maybeItems = (payload as { items?: unknown }).items
                if (Array.isArray(maybeItems)) return maybeItems
            }
            return []
        }
        try {
            const url = new URL("http://localhost:8000/api/offers/all")
            if (currentQuery) {
                url.searchParams.set("title", currentQuery)
            }
            if (countryId) {
                url.searchParams.set("country", countryId)
            }
            url.searchParams.set("page", String(targetPage))
            url.searchParams.set("size", "12")
            const res = await fetch(url)
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
            const data = await res.json()
            const items = normalizeOffers(data)
            const metaPages = typeof data === "object" && data && typeof (data as { pages?: unknown }).pages === "number"
                ? Math.max(1, (data as { pages: number }).pages)
                : 1
            setTotalPages(metaPages)
            setOffers(items)
        } catch (err: any) {
            console.error("Fetch error:", err)
            setError(err.message || "Unknown error")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchCountries()
    }, [])

    useEffect(() => {
        fetchOffers(query, page, selectedCountry)
    }, [query, page, selectedCountry])

    const handleSearch = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        setPage(1)
        setQuery(searchInput.trim())
    }

    return (
        <div className="offers-page">
            <form className="offers-search" onSubmit={handleSearch}>
                <input
                    className="search-input"
                    type="text"
                    placeholder="Search offers by title..."
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                />
                <select
                    className="country-select"
                    value={selectedCountry}
                    onChange={(e) => {
                        setSelectedCountry(e.target.value)
                        setPage(1)
                    }}
                >
                    {countries.map((country) => (
                        <option key={country.id} value={String(country.id)}>
                            {country.code}
                        </option>
                    ))}
                </select>
                <button className="search-button" type="submit" disabled={loading}>
                    Search
                </button>
            </form>

            {loading && <div>Loading offers...</div>}
            {error && <div>Error: {error}</div>}
            {!loading && !error && !offers.length && <div>No offers available</div>}

            <div className="card-container">
                {offers?.map((offer) => (
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
                    />
                ))}
            </div>

            <div className="offers-pagination">
                <button
                    type="button"
                    className="page-button"
                    onClick={() => setPage((prev) => Math.max(1, prev - 1))}
                    disabled={loading || page <= 1}
                >
                    Previous
                </button>
                <span className="page-indicator">Page {page} of {totalPages}</span>
                <button
                    type="button"
                    className="page-button"
                    onClick={() => setPage((prev) => Math.min(totalPages, prev + 1))}
                    disabled={loading || page >= totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    )
}
