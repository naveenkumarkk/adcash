export interface BadgeInterface {
  text: string
  filled?: boolean
}
export interface Category {
  name: string
}
export interface Country {
  id: number
  code: string
}

export interface Influencer{
    id: string
    name: string
}
export interface Offer {
  id: number
  title: string
  description: string
  image_url?: string
  categories: Category[]
  payout_type: string
  amount: string
}
export interface CardInterface {
  title: string
  body: string
  category_badges?: { text: string; filled: boolean }[]
  payoutType?: string
  amount?: string
  image?: string
  indicator: string | boolean
}