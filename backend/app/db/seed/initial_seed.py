from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Country, Influencers, Categories, Offer, OfferCategories, InfluencerCustomPayouts

async def seed_initial_data(session: AsyncSession):
    countries = [
        {"name": "Global", "code": "GLB","cpa_amount":40},
        {"name": "United States", "code": "US","cpa_amount":60},
        {"name": "Germany", "code": "DE","cpa_amount":30},
        {"name": "Estonia", "code": "EST","cpa_amount":40},
    ]
    for country in countries:
        result = await session.execute(select(Country).where(Country.code == country["code"]))
        existing = result.scalar_one_or_none()
        if not existing:
            session.add(Country(**country))
    influencers = [
        {"name": "Tech Influencer 1"},
        {"name": "Tech Influencer 2"},
        {"name": "Finance Influencer 1"},
        {"name": "Finance Influencer 2"},
        {"name": "Food Influencer 1"},
        {"name": "Food Influencer 2"},
    ]
    for inf in influencers:
        result = await session.execute(select(Influencers).where(Influencers.name == inf['name']))
        existing = result.scalar_one_or_none()
        if not existing:
            session.add(Influencers(**inf))
    categories = [
        {"name": "Gaming"},
        {"name": "Tech"},
        {"name": "Health"},
        {"name": "Nutrition"},
        {"name": "Fashion"},
        {"name": "Finance"},
    ]
    for cat in categories:
        result = await session.execute(select(Categories).where(Categories.name == cat['name']))
        existing = result.scalar_one_or_none()
        if not existing:
            session.add(Categories(**cat))

    await session.flush()  

    offers = [
        {"title":"Tech Promotion Offer1","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Tech"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA","influencer_list":[{"influencer":"Tech Influencer 1","custom_amount":60},{"influencer":"Tech Influencer 2","custom_amount":100}]},
        {"title":"Tech Promotion Offer2","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Tech"],"country":"GLB","fixed_amount":20,"cpa_amount":0,"payout_type":"FIXED"},
        {"title":"Tech Promotion Offer3","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Tech"],"country":"Germany","fixed_amount":10,"cpa_amount":30,"payout_type":"CPA_FIXED"},
        {"title":"Tech Promotion Offer4","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Tech"],"country":"GLB","fixed_amount":20,"cpa_amount":0,"payout_type":"FIXED"},
        {"title":"Tech Promotion Offer5","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Tech"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA"},
        {"title":"Food Promotion Offer1","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Health","Nutrition"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA"},
        {"title":"Food Promotion Offer2","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Health","Nutrition"],"country":"GLB","fixed_amount":10,"cpa_amount":0,"payout_type":"FIXED"},
        {"title":"Food Promotion Offer3","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Health","Nutrition"],"country":"Germany","fixed_amount":0,"cpa_amount":30,"payout_type":"CPA","influencer_list":[{"influencer":"Food Influencer 1","custom_amount":60},{"influencer":"Food Influencer 2","custom_amount":100}]},
        {"title":"Food Promotion Offer4","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Health","Nutrition"],"country":"GLB","fixed_amount":10,"cpa_amount":20,"payout_type":"CPA_FIXED"},
        {"title":"Food Promotion Offer5","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Health","Nutrition"],"country":"GLB","fixed_amount":20,"cpa_amount":0,"payout_type":"FIXED","influencer_list":[{"influencer":"Food Influencer 3","custom_amount":60},{"influencer":"Food Influencer 4","custom_amount":100}]},
        {"title":"Fashion Promotion Offer1","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Fashion"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA"},
        {"title":"Fashion Promotion Offer2","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Fashion"],"country":"GLB","fixed_amount":20,"cpa_amount":0,"payout_type":"FIXED"},
        {"title":"Fashion Promotion Offer3","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Fashion"],"country":"Germany","fixed_amount":10,"cpa_amount":30,"payout_type":"CPA_FIXED"},
        {"title":"Fashion Promotion Offer4","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Fashion"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA"},
        {"title":"Fashion Promotion Offer5","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Fashion"],"country":"GLB","fixed_amount":10,"cpa_amount":0,"payout_type":"FIXED"},
        {"title":"Finance Promotion Offer1","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Finance"],"country":"GLB","fixed_amount":10,"cpa_amount":20,"payout_type":"CPA_FIXED"},
        {"title":"Finance Promotion Offer2","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Finance"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA"},
        {"title":"Finance Promotion Offer3","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Finance"],"country":"Germany","fixed_amount":10,"cpa_amount":0,"payout_type":"FIXED","influencer_list":[{"influencer":"Finance Influencer 1","custom_amount":60},{"influencer":"Finance Influencer 2","custom_amount":100}]},
        {"title":"Finance Promotion Offer4","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Finance"],"country":"GLB","fixed_amount":10,"cpa_amount":20,"payout_type":"CPA_FIXED","influencer_list":[{"influencer":"Finance Influencer 3","custom_amount":60},{"influencer":"Finance Influencer 4","custom_amount":100}]},
        {"title":"Finance Promotion Offer5","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Finance"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA"},
        {"title":"Gaming Promotion Offer1","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Gaming","Tech"],"country":"GLB","fixed_amount":30,"cpa_amount":0,"payout_type":"FIXED","influencer_list":[{"influencer":"Tech Influencer 1","custom_amount":60},{"influencer":"Tech Influencer 2","custom_amount":100}]},
        {"title":"Gaming Promotion Offer2","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Gaming","Tech"],"country":"Germany","fixed_amount":0,"cpa_amount":30,"payout_type":"CPA"},
        {"title":"Gaming Promotion Offer3","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Gaming","Tech"],"country":"GLB","fixed_amount":10,"cpa_amount":20,"payout_type":"CPA_FIXED"},
        {"title":"Gaming Promotion Offer4","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Gaming","Tech"],"country":"GLB","fixed_amount":0,"cpa_amount":20,"payout_type":"CPA","influencer_list":[{"influencer":"Tech Influencer 3","custom_amount":60},{"influencer":"Tech Influencer 4","custom_amount":100}]},
        {"title":"Gaming Promotion Offer5","image_url":"https://picsum.photos/id/237/200/300","description":"Lorel Ipsum","categories":["Gaming","Tech"],"country":"GLB","fixed_amount":20,"cpa_amount":0,"payout_type":"FIXED"}
    ]

    image_id = 1
    for off in offers:
        img_url = off['image_url'].replace("id",str(image_id))
        image_id+=1
        result = await session.execute(select(Offer).where(Offer.title == off['title']))
        offer = result.scalar_one_or_none()
        if not offer:
            offer = Offer(title=off['title'], image_url=img_url,description=off['description'],cpa_amount=off['cpa_amount'],fixed_amount=off['fixed_amount'],payout_type=off['payout_type'])
            session.add(offer)
            await session.flush()

        for cat_name in off['categories']:
            cat_query = await session.execute(select(Categories).where(Categories.name == cat_name))
            category = cat_query.scalar_one_or_none()
            if category:
                oc_query = await session.execute(
                    select(OfferCategories)
                    .where(OfferCategories.offer_id == offer.id)
                    .where(OfferCategories.category_id == category.id)
                )
                if not oc_query.scalar_one_or_none():
                    session.add(OfferCategories(offer_id=offer.id, category_id=category.id))

        country_query = await session.execute(select(Country).where(Country.code == off["country"]))
        country = country_query.scalar_one_or_none()

        if "influencer_list" in off and off["influencer_list"]:
            for influencer_info in off["influencer_list"]:
                inf_query = await session.execute(select(Influencers).where(Influencers.name == influencer_info["influencer"]))
                influencer = inf_query.scalar_one_or_none()
                if influencer:
                    icp_query = await session.execute(
                        select(InfluencerCustomPayouts)
                        .where(InfluencerCustomPayouts.offer_id == offer.id)
                        .where(InfluencerCustomPayouts.influencer_id == influencer.id)
                    )
                    if not icp_query.scalar_one_or_none():
                        session.add(InfluencerCustomPayouts(
                            influencer_id=influencer.id,
                            offer_id=offer.id,
                            amount=influencer_info["custom_amount"]
                        ))
        
    await session.commit()
