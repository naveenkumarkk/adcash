/**
 * OffersGrid Component
 * Displays a grid of offer cards
 */

import { Card } from "./Card";
import { categoriesToBadges, getPayoutIndicator } from "../lib/utils";
import type { Offer } from "../types/index";

interface OffersGridProps {
  offers: Offer[];
}

export function OffersGrid({ offers }: OffersGridProps) {
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
          indicator={getPayoutIndicator(offer.payout_type)}
          categoryBadges={categoriesToBadges(offer.categories)}
        />
      ))}
    </div>
  );
}
