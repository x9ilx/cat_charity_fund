from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.mixins import DonationMixIn
from app.services.base import close_donation_or_project


async def donate_to_project(
    new_obj: DonationMixIn,
    session: AsyncSession,
):
    apply_object_type = (
        CharityProject if type(new_obj) == Donation else Donation
    )
    while not new_obj.fully_invested:
        apply_object = await session.execute(
            select(apply_object_type)
            .where(apply_object_type.fully_invested is False)
            .order_by(apply_object_type.create_date)
        )
        apply_object = apply_object.scalars().first()
        if apply_object is None:
            break
        if apply_object_type is CharityProject:
            charity_project, donation = apply_object, new_obj
        else:
            charity_project, donation = new_obj, apply_object
        left_to_pay = (
            charity_project.full_amount - charity_project.invested_amount
        )
        remaining_balance = donation.full_amount - donation.invested_amount
        if remaining_balance < left_to_pay:
            left_to_pay -= remaining_balance
            charity_project.invested_amount += remaining_balance
            donation = close_donation_or_project(donation)
        elif remaining_balance > left_to_pay:
            donation.invested_amount += left_to_pay
            charity_project = close_donation_or_project(charity_project)
        else:
            donation = close_donation_or_project(donation)
            charity_project = close_donation_or_project(charity_project)
    await session.commit()
    await session.refresh(new_obj)
    return new_obj
