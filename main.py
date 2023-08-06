from queries.mysql_queries import tickets_expiring_in_2h_or_less
from webhooks.webhooks import send_notifications_by_webhook
from queries.sqlite_queries import search_ticket, \
    insert_ticket, \
    update_ticket_expired_notified, \
    update_ticket_less_than_30m_notified, \
    update_ticket_less_than_1h_notified, \
    update_ticket_less_than_2h_notified

from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    tickets_expiring = tickets_expiring_in_2h_or_less()
    for row in tickets_expiring:
        ticket = row[0]
        time_to_resolve = row[1]
        office = row[2]
        it_support = row[3]
        notification = search_ticket(ticket, office)

        if not notification:
            insert_ticket(ticket, office)
            logging.info(f'New ticket {ticket} added to the database')
            notification = search_ticket(ticket, office)

        if time_to_resolve <= datetime.now() and not notification.expired_notified:
            send_notifications_by_webhook(ticket, office, time_to_resolve, it_support, expired=True)
            update_ticket_expired_notified(ticket, office)
            logging.info(f'Ticket {ticket} expired')
            pass

        elif time_to_resolve <= datetime.now() + timedelta(
                minutes=30) and not notification.less_than_30m_notified and not notification.expired_notified:
            send_notifications_by_webhook(ticket, office, time_to_resolve, it_support)
            update_ticket_less_than_30m_notified(ticket, office)
            logging.info(f'Ticket {ticket} less than 30m to expire')

        elif time_to_resolve <= datetime.now() + timedelta(hours=1) and not notification.less_than_1h_notified and not \
                notification.expired_notified and not notification.less_than_30m_notified:
            send_notifications_by_webhook(ticket, office, time_to_resolve, it_support)
            update_ticket_less_than_1h_notified(ticket, office)
            logging.info(f'Ticket {ticket} less than 1h to expire')

        elif time_to_resolve <= datetime.now() + timedelta(hours=2) and not notification.less_than_2h_notified and not \
                notification.expired_notified and not notification.less_than_30m_notified and not \
                notification.less_than_1h_notified:
            send_notifications_by_webhook(ticket, office, time_to_resolve, it_support)
            update_ticket_less_than_2h_notified(ticket, office)
            logging.info(f'Ticket {ticket} less than 2h to expire')


if __name__ == '__main__':
    main()
