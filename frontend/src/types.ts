import type { ComponentType, SVGProps } from "react";

export interface BadgeInterface {
    text: String;
    filled?: Boolean;
}

export interface ButtonInterface {
    text: string;
    filled?: boolean;
    type: string;
    href: string;
    icon?: ComponentType<SVGProps<SVGSVGElement>>;
}
export interface Category {
  name: string
}
export interface Offer {
  id: number
  title: string
  description: string
  image_url?: string
  categories: Category[]
  payout_type: string
  amount:  string
}
export interface CardInterface {
    title: string 
    body: string 
    category_badges?: { text: string; filled: boolean }[]
    btn?: {
        text: string
        filled: boolean
        href: string
        type: "primary" | "secondary"
        
    } | undefined
    payoutType?: string
    amount?: string
    image?: string
    indicator?: string
    

}