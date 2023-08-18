# states
modes = {"none", "add_user", "delete_user", "mailing_all", "add_offer", "edit_offer", "order_creative",
         "order_creative_gamble", "share_app", "pwa_app", "create_campaign", "add_comment", "set_domain",
         "setting_cloak", "prepare_vait", "media_other_task", "masons_partners"}

user_state = {"state": "none"}

# dep states
dep_states = {"admin", "gambleppc", "gambleuac", "gamblefb", "afmngr", "media", "gambleuac_gambleppc", "tech",
              "mt_partners"}


# set operations state 'none'
def set_state_none():
    user_state["state"] = "none"
