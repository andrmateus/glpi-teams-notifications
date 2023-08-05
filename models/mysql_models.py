from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.mysql_engine import Session

class Base(DeclarativeBase):
    pass

class Tickets(Base):
    __tablename__ = 'glpi_tickets'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    type = Column(Integer)
    time_to_resolve = Column(DateTime)
    is_deleted = Column(Boolean)

    groups_tickets = relationship('GroupTickets', back_populates='ticket')
    ticket_users = relationship('TicketUser', back_populates='ticket')

    def __repr__(self) -> str:
        return f'Ticket(id={self.id}, status={self.status}, type={self.type}, time_to_resolve={self.time_to_resolve}, is_deleted={self.is_deleted})'


class GroupTickets(Base):
    __tablename__ = 'glpi_groups_tickets'
    id = Column(Integer, primary_key=True)
    groups_id = Column(Integer, ForeignKey('glpi_groups.id'))
    tickets_id = Column(Integer, ForeignKey('glpi_tickets.id'))
    type = Column(Integer)

    ticket = relationship('Tickets', back_populates='groups_tickets')
    group = relationship('Groups', back_populates='group_tickets')

    def __repr__(self) -> str:
        return f'GroupTickets(id={self.id}, groups_id={self.groups_id}, tickets_id={self.tickets_id}, type={self.type})'


class Groups(Base):
    __tablename__ = 'glpi_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    groups_id = Column(Integer)

    group_tickets = relationship('GroupTickets', back_populates='group')

    def __repr__(self) -> str:
        return f'Groups(id={self.id}, name={self.name})'


class User(Base):
    __tablename__ = 'glpi_users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    ticket_users = relationship("TicketUser", back_populates="user")
    def __repr__(self) -> str:
        return f'User(id={self.id}, name={self.name})'


class TicketUser(Base):
    __tablename__ = 'glpi_tickets_users'
    id = Column(Integer, primary_key=True)
    tickets_id = Column(Integer, ForeignKey('glpi_tickets.id'))
    users_id = Column(Integer, ForeignKey('glpi_users.id'))
    type = Column(Integer)

    ticket = relationship("Tickets", back_populates="ticket_users")
    user = relationship("User", back_populates="ticket_users")

    def __repr__(self) -> str:
        return f'TicketUser(id={self.id}, tickets_id={self.tickets_id}, users_id={self.users_id}, type={self.type})'
