from sqlalchemy.orm import aliased
from models.mysql_models import Tickets, Groups, GroupTickets, Session, TicketUser, User
from datetime import datetime, timedelta


def tickets_expiring_in_2h_or_less():
    session = Session()

    subquery = (
        session.query(TicketUser)
        .filter(TicketUser.type == 2)
        .subquery()
    )

    gtu_alias = aliased(TicketUser, subquery)

    hours_to_expire = 2

    status_open = [1, 2, 3]
    central_groups = [198, 295]
    current_date = datetime.now()

    condicao1 = Tickets.is_deleted == 0
    condicao2 = Tickets.status.in_(status_open)
    condicao3 = GroupTickets.type == 2
    condicao4 = Groups.groups_id.in_(central_groups)

    try:
        condicao5 = (Tickets.time_to_resolve < (current_date + timedelta(hours=hours_to_expire)))

        request = (session.query(Tickets.id, Tickets.time_to_resolve, Groups.name, User.name)
                   .select_from(Tickets)
                   .join(GroupTickets, GroupTickets.tickets_id == Tickets.id)
                   .join(Groups, Groups.id == GroupTickets.groups_id)
                   .outerjoin(gtu_alias, gtu_alias.tickets_id == Tickets.id)
                   .outerjoin(User, User.id == gtu_alias.users_id)
                   .filter(condicao1, condicao2, condicao3, condicao4, condicao5))

        return request

    finally:
        session.close()
