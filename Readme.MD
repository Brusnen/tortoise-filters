![PyPI](https://img.shields.io/pypi/v/tortoise-filters?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tortoise-filters)

# Tortoise Filters

## Async library inspired by django-filters, used with FastAPI and Tortoise ORM

```pip install tortoise-filters```

### examples

```
from tortoise_filters.filterset import FilterSet
from tortoise_filters.filter_fields import NumberFilter, CharFilter

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

class UserFilterSet(FilterSet): 
    
    model = User

    id = NumberFilter(field_name="id", lookup_expr="gt")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    
app = FastAPI()

register_tortoise(app=app,
                  config=TORTOISE_ORM)

@app.get("/")
# this dependency injection will automatically create filter fields in swagger
async def get_user(user: TortoiseFilterSet.to_dependencies() = Depends()):
    TortoiseFilterSet.to_dependencies()
    a = TortoiseFilterSet(query_params=user.dict())
    qs = await a.filter_queryset()
    a = await qs
    return 'some_text'
 ```

# RoadMap
- [x] add classes for filtering multiple values (InFilter) 
- [ ] add validation for input values
- [ ] add classes for date filtering and range filtering
- [ ] add custom methods support
- [ ] add support for outer querysets
- [ ] add integration with AutoRouter library
- [ ] tests
## Contributing
you are welcome to contribute this project!
