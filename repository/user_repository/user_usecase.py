from repository.model.user import UserModel


def get_user_model(model=None) -> UserModel:
    return UserModel(
        model['id_user'],
        model['name_user'],
        model['dep_user'],
        model['label_tech'],
        model['label_creo'],
    ) if model is not None else None


def get_user_model_list(models=None) -> [UserModel]:
    model_list = []
    if models is not None:
        for model in models:
            model_list.append(get_user_model(model))

    return model_list if model_list.__len__() > 0 else None
