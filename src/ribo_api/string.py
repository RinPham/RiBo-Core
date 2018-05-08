from ribo_api.const import const


class MSG_STRING(const):
    WHATS_UP = "Can I help you?"
    NEED_RIBO = ["Tell me know if you need me", "Would you like anything else?", "May I help you?"]
    NO_REMINDER = "You have not any reminders"

    #reminder
    REMINDER_ITEM = '\n {0}. {1} on {2}?'

    #remove reminder
    NO_REMINDER_REMOVE = 'There are nothing to delete!'
    REMOVE_ALL_REMINDER_CONFIRM = 'Do you want to delete all your reminder?'
    REMOVE_REMINDER_CONFIRM = 'Do you want to delete this reminder: \n {0} on {1}?'

