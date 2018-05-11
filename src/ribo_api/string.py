from ribo_api.const import const


class MSG_STRING(const):
    WHATS_UP = "Can I help you?"
    NEED_RIBO = ["Tell me know if you need me", "Would you like anything else?", "May I help you?"]
    NO_REMINDER = "You have not any reminders"

    #events
    EVENT_ITEM_NOREPEAT = '\n {0}. {1} starts at {2} to {3}'
    EVENT_ITEM_DAILY = '\n {0}. {1} starts at {2} to {3} everyday'
    EVENT_ITEM_WEEKLY = '\n {0}. {1} starts at {2} to {3} every {4}'
    EVENT_ITEM_WEEKENDS = '\n {0}. {1} starts at {2} to {3} every weekends'
    EVENT_ITEM_WEEKDAYS = '\n {0}. {1} starts at {2} to {3} every weekdays'
    EVENT_ITEM_MONTHLY = '\n {0}. {1} starts at {2} to {3} every the {4} of the month'

    #reminder
    REMINDER_ITEM_NOREPEAT = '\n {0}. {1} on {2}'
    REMINDER_ITEM_DAILY = '\n {0}. {1} at {2} everyday'
    REMINDER_ITEM_WEEKLY = '\n {0}. {1} at {2} every {3}'
    REMINDER_ITEM_WEEKENDS = '\n {0}. {1} at {2} every weekends'
    REMINDER_ITEM_WEEKDAYS = '\n {0}. {1} at {2} every weekdays'
    REMINDER_ITEM_MONTHLY = '\n {0}. {1} at {2} every the {3} of the month'

    #remove reminder
    NO_REMINDER_REMOVE = 'There are nothing to delete!'
    REMOVE_ALL_REMINDER_CONFIRM = 'Do you want to delete all your reminder?'
    REMOVE_REMINDER_CONFIRM = 'Do you want to delete this reminder: \n {0} on {1}?'

