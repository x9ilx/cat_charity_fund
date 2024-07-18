from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


class DonationMixIn(object):
    full_amount = Column(
        Integer, CheckConstraint('full_amount>0'), nullable=False
    )
    invested_amount = Column(
        Integer,
        CheckConstraint('invested_amount>=0'),
        default=0,
        nullable=False,
    )
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True)
