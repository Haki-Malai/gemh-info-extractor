import pickle
from functools import wraps
from apifairy import arguments, response
from typing import Any, Dict, Callable, List
from sqlalchemy.orm import Query
from marshmallow import Schema

from api.app import redis_client
from api.schemas import StringPaginationSchema, paginated_collection
from config import config

PaginationDict = Dict[str, Any]


def paginated_response(schema: Schema,
                       max_limit: int = config['default'].ITEMS_PER_BODY,
                       pagination_schema: Schema = StringPaginationSchema,
                       ) -> Callable[[Callable[..., Query]],
                            Callable[..., Dict[str, Any]]]:
    """Decorator for paginated responses
    :param schema: Marshmallow schema for the response
    :param max_limit: Maximum number of items per page
    :param pagination_schema: Marshmallow schema for pagination parameters
    :return: Decorator function
    """
    def inner(func: Callable[..., Query]) -> Callable[..., Dict[str, Any]]:
        """Decorator function
        :param func: Function to decorate
        :return: Decorated function
        """
        @wraps(func)
        def paginate(*args, **kwargs):
            """Paginate the response of a SQLAlchemy query
            :param args: Arguments to pass to the function
            :param kwargs: Keyword arguments to pass to the function
            :return: Paginated response
            """
            args: List = list(args)
            pagination: PaginationDict = args.pop(-1) if len(args) > 0 else {}
            query: Query = func(*args, **kwargs)

            if query is None:
                return {}

            count: int = query.count()

            limit: int = min(pagination.get('limit', max_limit), max_limit)
            query: int = query.limit(limit)

            page: int = max(pagination.get('page', 1), 1)
            if limit >= 1:
                query = query.offset((page - 1) * limit)

            # Check if the result is cached in Redis
            cache_key = (f'{func.__name__}_{pickle.dumps(args)}_'
                         f'{pickle.dumps(kwargs)}_{pickle.dumps(pagination)}')
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return pickle.loads(cached_result)

            data: List = query.all()
            result: Dict = {
                'data': data,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'count': len(data),
                    'total': count
                }
            }

            # Cache the result in Redis
            redis_client.setex(cache_key,
                               config['default'].CACHE_TIMEOUT,
                               pickle.dumps(result))

            return result

        return arguments(pagination_schema)(response(paginated_collection(
            schema, pagination_schema=pagination_schema))(paginate))

    return inner
