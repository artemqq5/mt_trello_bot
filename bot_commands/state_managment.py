# states
modes = {"none", "add_user", "delete_user", "mailing_all", "add_offer", "edit_offer", "order_creative_crypto",
         "order_creative_gamble", "share_app", "pwa_app", "create_campaign", "add_comment", "set_domain",
         "setting_cloak", "prepare_vait", "order_creative_media", "masons_partners"}

user_state = {"state": "none"}

# dep states
dep_states = {"admin", "gambleppc", "gambleuac", "gamblefb", "afmngr", "media", "gambleuac_gambleppc", "tech",
              "mt_partners", "designer"}

# accesses_tech_task = {
#     'mt_partners_t': ['admin', 'mt_partners'],
#     'edit_offer_t': ['admin', 'afmngr'],
#     'add_offer_t': ['admin', 'afmngr'],
#     'share_app_t': ['admin', 'gambleuac', 'gamblefb'],
#     'create_campaign_t': ['admin', 'gambleppc', 'gambleuac', 'gamblefb'],
#     'pwa_app_t': ['admin', ],
#     'other_task_t': ['admin', ],
#     'prepare_vait_t': ['admin', ],
#     'settings_cloak_t': ['admin', ],
#     'set_domain_t': ['admin', ],
# }


# set operations state 'none'
def set_state_none():
    user_state["state"] = "none"
