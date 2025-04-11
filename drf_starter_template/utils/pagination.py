from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomDRFPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_page_number(self, request, paginator):
        page_number = request.query_params.get(self.page_query_param, 1)
        try:
            page_number = int(page_number)
            page_number = max(page_number, 1)
        except (TypeError, ValueError):
            page_number = 1
        return page_number

    def get_paginated_response(self, data):
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages
        page_size = self.get_page_size(self.request)
        total_items = self.page.paginator.count

        links = {
            "self": self.request.build_absolute_uri(),
            "first": self._build_page_url(1),
            "last": self._build_page_url(total_pages),
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }

        return Response(
            {
                "data": data,
                "meta": {
                    "totalItems": total_items,
                    "pageSize": page_size,
                    "currentPage": current_page,
                    "totalPages": total_pages,
                },
                "links": links,
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "data": schema,
                "meta": {
                    "type": "object",
                    "properties": {
                        "totalItems": {
                            "type": "integer",
                            "example": 123,
                        },
                        "pageSize": {
                            "type": "integer",
                            "example": 10,
                        },
                        "currentPage": {
                            "type": "integer",
                            "example": 1,
                        },
                        "totalPages": {
                            "type": "integer",
                            "example": 13,
                        },
                    },
                },
                "links": {
                    "type": "object",
                    "properties": {
                        "self": {
                            "type": "string",
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?page=1",
                        },
                        "first": {
                            "type": "string",
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?page=1",
                        },
                        "last": {
                            "type": "string",
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?page=5",
                        },
                        "next": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": "http://api.example.org/accounts/?page=2",
                        },
                        "previous": {
                            "type": "string",
                            "nullable": True,
                            "format": "uri",
                            "example": None,
                        },
                    },
                },
                "apiVersion": {
                    "type": "string",
                    "example": "1.0",
                },
            },
        }

    def _build_page_url(self, page_number):
        if not page_number:
            return None
        base_url = self.request.build_absolute_uri()
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        query_params[self.page_query_param] = [str(page_number)]
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )
