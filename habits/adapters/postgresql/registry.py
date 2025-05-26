from habits import entities
from habits.adapters.postgresql import models
from habits.core.mapper import Mapper, get_context

mapper = Mapper()


def habit_to_entity(instance: models.Habit) -> entities.Habit:
    return entities.Habit(
        uuid=instance.uuid,
        user_uuid=instance.user_uuid,
        name=instance.name,
        description=instance.description,
        is_quantifiable=instance.is_quantifiable,
        target_quantity=instance.target_quantity,
        unit=instance.unit,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
    )


def habit_to_model(habit: entities.Habit) -> models.Habit:
    instance: models.Habit = get_context(habit, default_factory=models.Habit)
    instance.uuid = habit.uuid
    instance.user_uuid = habit.user_uuid
    instance.name = habit.name
    instance.description = habit.description
    instance.is_quantifiable = habit.is_quantifiable
    instance.target_quantity = habit.target_quantity
    instance.unit = habit.unit
    instance.created_at = habit.created_at
    instance.updated_at = habit.updated_at
    return instance


def habit_log_to_entity(instance: models.HabitLog) -> entities.HabitLog:
    return entities.HabitLog(
        uuid=instance.uuid,
        habit_uuid=instance.habit_uuid,
        date=instance.date,
        is_completed=instance.is_completed,
        quantity=instance.quantity,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
    )


def habit_log_to_model(habit_log: entities.HabitLog) -> models.HabitLog:
    instance: models.HabitLog = get_context(habit_log, default_factory=models.HabitLog)
    instance.uuid = habit_log.uuid
    instance.habit_uuid = habit_log.habit_uuid
    instance.date = habit_log.date
    instance.is_completed = habit_log.is_completed
    instance.quantity = habit_log.quantity
    instance.created_at = habit_log.created_at
    instance.updated_at = habit_log.updated_at
    return instance


def user_to_entity(instance: models.User) -> entities.User:
    return entities.User(
        uuid=instance.uuid,
        username=instance.username,
        email=instance.email,
        hashed_password=instance.hashed_password,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
    )


def user_to_model(user: entities.User) -> models.User:
    instance: models.User = get_context(user, default_factory=models.User)
    instance.uuid = user.uuid
    instance.username = user.username
    instance.email = user.email
    instance.hashed_password = user.hashed_password
    instance.created_at = user.created_at
    instance.updated_at = user.updated_at
    return instance


mapper.register(models.Habit, entities.Habit, habit_to_entity, save_ctx=True)
mapper.register(entities.Habit, models.Habit, habit_to_model)

mapper.register(models.HabitLog, entities.HabitLog, habit_log_to_entity, save_ctx=True)
mapper.register(entities.HabitLog, models.HabitLog, habit_log_to_model)

mapper.register(models.User, entities.User, user_to_entity, save_ctx=True)
mapper.register(entities.User, models.User, user_to_model)
