from products.adapters.mongodb import models
from products.core.mapper import Mapper, get_context
from products.domain import entities

mapper = Mapper()


def category_to_entity(instance: models.Category) -> entities.Product:
    return entities.Category(
        id=str(instance.id),
        name=instance.name,
        description=instance.description,
    )


# def category_to_model(category: entities.Product) -> models.Product:
#     instance: models.Category = get_context(
#         category, default_factory=models.Category
#     )
#     instance.uuid = product.uuid
#     instance.category_id = product.category_id
#     instance.title = product.title
#     instance.description = product.description
#     instance.price = product.price
#     instance.dim = product.dim
#
#     return instance
#

mapper.register(models.Category, entities.Category, category_to_entity, True)
# mapper.register(entities.Product, models.Product, product_to_model)
