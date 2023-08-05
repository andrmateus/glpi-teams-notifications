from models.sqlite_models import Notification, Session


def insert_ticket(ticket_id, office):
    session = Session()
    try:
        notification = Notification(ticket_id=ticket_id, office=f'{office}')
        session.add(notification)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def update_ticket(ticket_id, office, field):
    session = Session()
    try:
        notification = session.query(Notification).filter_by(ticket_id=ticket_id, office=office).first()
        if notification:
            setattr(notification, field, 1)
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def update_ticket_expired_notified(ticket_id, office):
    update_ticket(ticket_id, office, 'expired_notified')


def update_ticket_less_than_30m_notified(ticket_id, office):
    update_ticket(ticket_id, office, 'less_than_30m_notified')


def update_ticket_less_than_1h_notified(ticket_id, office):
    update_ticket(ticket_id, office, 'less_than_1h_notified')


def update_ticket_less_than_2h_notified(ticket_id, office):
    update_ticket(ticket_id, office, 'less_than_2h_notified')


def search_ticket(ticket_id, office):
    session = Session()
    try:
        notification = session.query(Notification).filter_by(ticket_id=ticket_id, office=f'{office}').first()
        return notification
    except:
        session.rollback()
        raise
    finally:
        session.close()